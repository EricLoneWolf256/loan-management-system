# Loan calculation utilities - EMI, interest, repayment schedule
from typing import List
from datetime import date, datetime, timedelta  
from dateutil.relativedelta import relativedelta
from app.models.payment import RepaymentSchedule


def calculate_emi(principal: float, annual_interest_rate: float, loan_term_months: int) -> float:
    """Calculate the Equated Monthly Installment (EMI) for a loan
    
    Formula: EMI = P * r * (1 + r)^n / ((1 + r)^n - 1)
    where P = principal, r = monthly interest rate, n = Number of monthly installments
    
    Args:
        principal: The principal loan amount
        annual_interest_rate: The annual interest rate (in percentage)
        loan_term_months: Loan duration in months
    
    Returns:
        Monthly payment amount
    """
    monthly_rate = annual_interest_rate / 12 / 100  # Convert annual rate percentage to monthly decimal
    
    if monthly_rate == 0:  # Zero interest loan
        return principal / loan_term_months
    
    emi = principal * monthly_rate * (1 + monthly_rate) ** loan_term_months / ((1 + monthly_rate) ** loan_term_months - 1)
    return emi


def calculate_monthly_payment(principal: float, annual_interest_rate: float, loan_term_months: int) -> float:
    """Alias for calculate_emi - calculate monthly payment amount"""
    return calculate_emi(principal, annual_interest_rate, loan_term_months)


def generate_repayment_schedule(loan_amount: float, interest_rate: float, term_months: int, loan_id: int, start_date: date = None) -> List[RepaymentSchedule]:
    """Generate the repayment schedule for a loan
    
    Creates a list of RepaymentSchedule objects showing:
    - When each payment is due
    - How much is principal vs interest
    - Outstanding balance after each payment
    
    Args:
        loan_amount: The principal loan amount
        interest_rate: The annual interest rate (in percentage)
        term_months: Loan duration in months
        loan_id: The ID of the loan
        start_date: The start date of the loan (default is today)
    
    Returns:
        List of RepaymentSchedule objects
    """
    if start_date is None:
        start_date = datetime.utcnow()
    
    monthly_rate = interest_rate / 12 / 100  # Convert annual rate to monthly decimal
    emi = calculate_emi(loan_amount, interest_rate, term_months)
    schedule = []
    remaining_balance = loan_amount
    
    for month in range(1, term_months + 1):
        # Calculate interest for the month on the remaining balance
        interest_component = remaining_balance * monthly_rate
        
        # Rest goes to reducing the principal
        principal_component = emi - interest_component
        
        # Update remaining balance
        remaining_balance -= principal_component
        
        # Handle final payment rounding issues
        if month == term_months:
            principal_component += remaining_balance
            remaining_balance = 0.0
        
        # Calculate due date for this installment
        due_date = start_date + relativedelta(months=month)
        
        # Create RepaymentSchedule object
        repayment = RepaymentSchedule(
            loan_id=loan_id,
            installment_number=month,
            due_date=due_date,
            amount_due=round(emi, 2),
            principal_component=round(principal_component, 2),
            interest_component=round(interest_component, 2),
            status="PENDING"
        )
        schedule.append(repayment)
    
    return schedule


def calculate_total_interest(principal: float, annual_interest_rate: float, loan_term_months: int) -> float:
    """Calculate the total interest payable over the loan lifetime
    
    Args:
        principal: The principal loan amount
        annual_interest_rate: The annual interest rate (in percentage)
        loan_term_months: Loan duration in months
    
    Returns:
        Total interest payable
    """
    emi = calculate_emi(principal, annual_interest_rate, loan_term_months)
    total_payment = emi * loan_term_months
    total_interest = total_payment - principal
    return round(total_interest, 2)


def determine_interest_rate(credit_score: int) -> float:
    """Determine interest rate based on credit score
    
    Simple tiered model for demonstration
    
    Args:
        credit_score: Borrower's credit score
    
    Returns:
        Annual interest rate percentage
    """
    if credit_score >= 750:
        return 5.0  # Excellent credit
    elif credit_score >= 700:
        return 7.0  # Good credit
    elif credit_score >= 650:
        return 10.0  # Fair credit
    else:
        return 15.0  # Poor credit


def calculate_prepayment_details(
    remaining_balance: float,
    prepayment_amount: float,
    monthly_emi: float,
    remaining_months: int,
    annual_interest_rate: float
) -> dict:
    """Calculate the impact of an extra payment on loan tenure and interest savings
    
    Args:
        remaining_balance: Current remaining loan balance
        prepayment_amount: Amount being prepaid
        monthly_emi: Current monthly EMI
        remaining_months: Months remaining in the loan
        annual_interest_rate: Annual interest rate
    
    Returns:
        Dictionary with new balance, months saved, and interest saved
    """
    # Calculate new balance after prepayment
    new_balance = remaining_balance - prepayment_amount
    
    # If prepayment exceeds remaining balance, set new balance to 0
    if new_balance <= 0:
        return {
            "new_balance": 0.0,
            "months_saved": remaining_months,
            "interest_saved": calculate_total_interest(remaining_balance, annual_interest_rate, remaining_months)
        }
    
    new_months = 0
    temp_balance = new_balance
    monthly_rate = annual_interest_rate / 12 / 100
    
    while temp_balance > 0 and new_months < remaining_months:
        interest = temp_balance * monthly_rate
        principal = monthly_emi - interest
        temp_balance -= principal
        new_months += 1
    
    months_saved = remaining_months - new_months
    # Calculate interest saved by prepayment
    old_interest = calculate_total_interest(remaining_balance, annual_interest_rate, remaining_months)
    new_interest = calculate_total_interest(new_balance, annual_interest_rate, new_months) if new_months > 0 else 0
    interest_saved = old_interest - new_interest
    
    return {
        "new_balance": round(new_balance, 2),
        "months_saved": months_saved,
        "interest_saved": round(interest_saved, 2),
        "new_monthly_payment": round(calculate_emi(new_balance, annual_interest_rate, new_months), 2) if new_months > 0 else 0
    }