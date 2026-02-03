# loan calculation utilities, EMI , interest etc.the mathematical brain of the loan system

from email.mime import base
import re
from typing import Tuple, List
from datetime import date, datetime, timedelta  
from dateutil.relativedelta import relativedelta

from app.models import loan

def calculate_emi(principal: float, annual_interest_rate: float, loan_term_months: int) -> float:
    """Calculate the Equated Monthly Installment (EMI) for a loan
    formula: EMI = P * r * (1 + r)^n / ((1 + r)^n - 1)
    where P = principal, r = monthly interest rate, n = Number of monthly installments

    args:
        principal (float): The principal loan amount
        annual_interest_rate (float): The annual interest rate (in percentage)
        loan_term_months (int): Loan duration in months
    returns:
        monthly payment amount
    """
    monthly_rate = annual_interest_rate/12/100  # convert annual rate percentage to monthly decimal
    
    if monthly_rate == 0:  # zero interest loan
        return principal / loan_term_months
    
        emi = principal * monthly_rate * (1 + monthly_rate) ** loan_term_months / ((1 + monthly_rate) ** loan_term_months - 1)
        
        return emi
    
    def amortization_schedule(
              principal: float, annual_interest_rate: float, loan_term_months: int, start_date: date = date.today()
            ) -> List[Tuple[int, date, float, float, float]]:       
        """Generate the amortization schedule for a loan
    shows breakdown of each payment into principal and interest components
    when each payment is due
    how much goes to the actual loan(principal)
    how much is interest(bank's profit)
    args:
        principal (float): The principal loan amount
        annual_interest_rate (float): The annual interest rate (in percentage)
        loan_term_months (int): Loan duration in months
        start_date (date): The start date of the loan (default is today's date)     
    returns:
        List of tuples containing (installment number, due date, total_payment, principal_component, interest_component, remaining_balance)
    """
    monthly_rate = annual_interest_rate/12/100  # convert annual rate percentage to monthly decimal
    emi = calculate_emi(principal, annual_interest_rate, loan_term_months)
    schedule = []
    remaining_balance = principal
    for month in range(1, loan_term_months + 1):
        # calculate interest for the month
        # the interest is charged on the remaining balance
        interest_component = remaining_balance * monthly_rate
        
        # rest goes to reducing the principal
        principal_component = emi - interest_component
        # update remaining balance
        remaining_balance -= principal_component
        
        # handle final payment rounding issues
        if month == loan_term_months:
            principal_component += remaining_balance
            remaining_balance = 0.0
            
        # calculate due date for this installment
        due_date = start_date + relativedelta(months=month)
        schedule.append((
            month, 
            due_date,
            emi, 
            principal_component, interest_component, 
            
            max(0,remaining_balance)))  # what's left to pay
    return schedule
    
def calculate_total_interest(principal: float, annual_interest_rate: float, loan_term_months: int) -> float:
    """Calculate the total interest payable over the loan lifetime.
    args:
        principal (float): The principal loan amount
        annual_interest_rate (float): The annual interest rate (in percentage)
        loan_term_months (int): Loan duration in months
    returns:
        total interest payable
    """
    emi = calculate_emi(principal, annual_interest_rate, loan_term_months)
    total_payment = emi * loan_term_months
    total_interest = total_payment - principal
    return total_interest
    
def determine_interest_rate(credit_score: int) -> float:
    """Determine interest rate based on credit score
    simple tiered model for demonstration
    args:
        credit_score (int): borrower's credit score
    returns:
        annual interest rate percentage
    """
    # based on hypothetical credit score tiers
    base_rates = {
        'excellent': 5.0,
        'good': 7.0,
        'fair': 10.0,
        'poor': 15.0
    }
    
    if credit_score >= 750:
        return 5.0  # excellent credit
    elif credit_score >= 700:
        return 7.0  # good credit
    elif credit_score >= 650:
        return 10.0  # fair credit
    else:
        return 15.0  # poor credit
        
    return round(base_rate, 2)
    
def calculate_prepayment_details(
    remaining_balance: float,
    prepayment_amount: float,
    monthly_emi: float,
    remaining_months: int,
    annual_interest_rate: float
    ) -> dict:
    """Calculate the impact of a extra payment
    on loan tenure and interest savings
    like seeing the benefeits of paying off your loan early
    args:
        new balance (float): remaining loan balance
        months saved (int): how many months will be cut off the loan
        interest_saved (float): total interest saved by prepaying
    """
    # calculate new balance after prepayment
    new_balance = remaining_balance - prepayment_amount
    
    # if prepayment exceeds remaining balance, set new balance to 0
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
    # calculate interest saved by prepayment
    old_interest = calculate_total_interest(remaining_balance, annual_interest_rate, remaining_months)
    new_interest = calculate_total_interest(new_balance, annual_interest_rate, new_months)
    interest_saved = old_interest - new_interest
    
    return {
        "new_balance": round(new_balance, 2),
        "months_saved": months_saved,
        "interest_saved": round(interest_saved, 2),
        "new_monthly_payment": round(calculate_emi(new_balance, annual_interest_rate, new_months), 2)
    }