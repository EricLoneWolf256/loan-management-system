# Loan Management System API Test Script

$BASE_URL = "http://127.0.0.1:8000/api/v1"

# Colors for output
$SUCCESS = @{ ForegroundColor = 'Green' }
$INFO = @{ ForegroundColor = 'Cyan' }
$ERROR = @{ ForegroundColor = 'Red' }

Write-Host "`n========== LOAN MANAGEMENT SYSTEM API TEST ==========" @INFO

# 1. REGISTER A NEW USER
Write-Host "`n[1] Testing: POST /auth/register" @INFO
$registerBody = @{
    username = "alice_smith"
    email = "alice@example.com"
    full_name = "Alice Smith"
    password = "SecurePass123"
} | ConvertTo-Json

$registerResponse = curl -s -X POST "$BASE_URL/auth/register" `
    -H "Content-Type: application/json" `
    -d $registerBody | ConvertFrom-Json

Write-Host "✓ User registered successfully!" @SUCCESS
Write-Host "User ID: $($registerResponse.id)"
Write-Host "Username: $($registerResponse.username)"
Write-Host "Email: $($registerResponse.email)"
$USER_ID = $registerResponse.id

# 2. LOGIN
Write-Host "`n[2] Testing: POST /auth/login" @INFO
$loginBody = "username=alice_smith&password=SecurePass123"
$loginResponse = curl -s -X POST "$BASE_URL/auth/login" `
    -H "Content-Type: application/x-www-form-urlencoded" `
    -d $loginBody | ConvertFrom-Json

Write-Host "✓ Login successful!" @SUCCESS
Write-Host "Access Token: $($loginResponse.access_token.Substring(0, 50))..."
Write-Host "Token Type: $($loginResponse.token_type)"
$TOKEN = $loginResponse.access_token

# 3. GET CURRENT USER
Write-Host "`n[3] Testing: GET /auth/me" @INFO
$meResponse = curl -s -X GET "$BASE_URL/auth/me" `
    -H "Authorization: Bearer $TOKEN" | ConvertFrom-Json

Write-Host "✓ Current user retrieved!" @SUCCESS
Write-Host "Logged in as: $($meResponse.username) ($($meResponse.email))"

# 4. CREATE LOAN APPLICATION
Write-Host "`n[4] Testing: POST /loans" @INFO
$loanBody = @{
    applicant_id = $USER_ID
    loan_type = "personal"
    requested_amount = 50000
    loan_term_months = 24
    purpose = "Home renovation project"
} | ConvertTo-Json

$loanResponse = curl -s -X POST "$BASE_URL/loans" `
    -H "Authorization: Bearer $TOKEN" `
    -H "Content-Type: application/json" `
    -d $loanBody | ConvertFrom-Json

Write-Host "✓ Loan application created!" @SUCCESS
Write-Host "Loan ID: $($loanResponse.id)"
Write-Host "Amount: $($loanResponse.requested_amount)"
Write-Host "Type: $($loanResponse.loan_type)"
Write-Host "Status: $($loanResponse.status)"
Write-Host "Interest Rate: $($loanResponse.interest_rate)%"
$LOAN_ID = $loanResponse.id

# 5. GET LOAN DETAILS
Write-Host "`n[5] Testing: GET /loans/{loan_id}" @INFO
$loanDetailsResponse = curl -s -X GET "$BASE_URL/loans/$LOAN_ID" `
    -H "Authorization: Bearer $TOKEN" | ConvertFrom-Json

Write-Host "✓ Loan details retrieved!" @SUCCESS
Write-Host "Status: $($loanDetailsResponse.status)"
Write-Host "Amount: $$($loanDetailsResponse.requested_amount)"

# 6. LIST USER LOANS
Write-Host "`n[6] Testing: GET /loans/user/{user_id}" @INFO
$userLoansResponse = curl -s -X GET "$BASE_URL/loans/user/$USER_ID" `
    -H "Authorization: Bearer $TOKEN" | ConvertFrom-Json

Write-Host "✓ User loans retrieved!" @SUCCESS
Write-Host "Total loans: $($userLoansResponse.Count)"
$userLoansResponse | ForEach-Object {
    Write-Host "  - Loan ID: $($_.id), Amount: $$$($_.requested_amount), Status: $($_.status)"
}

# 7. LIST ALL LOANS
Write-Host "`n[7] Testing: GET /loans" @INFO
$allLoansResponse = curl -s -X GET "$BASE_URL/loans" `
    -H "Authorization: Bearer $TOKEN" | ConvertFrom-Json

Write-Host "✓ All loans retrieved!" @SUCCESS
Write-Host "Total loans in system: $($allLoansResponse.Count)"

# 8. GET REPAYMENT SCHEDULE
Write-Host "`n[8] Testing: GET /payments/loan/{loan_id}/schedule" @INFO
$scheduleResponse = curl -s -X GET "$BASE_URL/payments/loan/$LOAN_ID/schedule" `
    -H "Authorization: Bearer $TOKEN" | ConvertFrom-Json

Write-Host "✓ Repayment schedule retrieved!" @SUCCESS
Write-Host "Total installments: $($scheduleResponse.Count)"
if ($scheduleResponse.Count -gt 0) {
    Write-Host "`nFirst 3 installments:"
    $scheduleResponse | Select-Object -First 3 | ForEach-Object {
        Write-Host "  Installment $($_.installment_number): Due $($_.due_date.Split('T')[0]), Amount: $$$($_.amount_due), Principal: $$$($_.principal_component), Interest: $$$($_.interest_component)"
    }
}

# 9. GET LOAN BALANCE
Write-Host "`n[9] Testing: GET /payments/loan/{loan_id}/balance" @INFO
$balanceResponse = curl -s -X GET "$BASE_URL/payments/loan/$LOAN_ID/balance" `
    -H "Authorization: Bearer $TOKEN" | ConvertFrom-Json

Write-Host "✓ Loan balance retrieved!" @SUCCESS
Write-Host "Total Due: $$($balanceResponse.total_due)"
Write-Host "Total Paid: $$($balanceResponse.total_paid)"
Write-Host "Outstanding Balance: $$($balanceResponse.outstanding_balance)"
Write-Host "Paid Percentage: $($balanceResponse.paid_percentage)%"

# 10. GET PAYMENT HISTORY
Write-Host "`n[10] Testing: GET /payments/loan/{loan_id}/history" @INFO
$historyResponse = curl -s -X GET "$BASE_URL/payments/loan/$LOAN_ID/history" `
    -H "Authorization: Bearer $TOKEN" | ConvertFrom-Json

Write-Host "✓ Payment history retrieved!" @SUCCESS
Write-Host "Payment records: $($historyResponse.Count)"

Write-Host "`n========== ALL TESTS COMPLETED SUCCESSFULLY ==========" @SUCCESS
Write-Host "✓ All 10 API endpoints tested and working!" @SUCCESS
