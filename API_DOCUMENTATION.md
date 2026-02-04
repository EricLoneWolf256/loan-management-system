# 🏦 Loan Management System API - Complete Test Guide

## **Server URL**
```
http://127.0.0.1:8000
```

## **API Documentation**
- Swagger UI: http://127.0.0.1:8000/api/v1/docs
- ReDoc: http://127.0.0.1:8000/api/v1/redoc

---

## **1. AUTHENTICATION ENDPOINTS**

### 1.1 Register a New User
**Endpoint:** `POST /api/v1/auth/register`

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "password": "SecurePassword123"
  }'
```

**Response (201 Created):**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "phone_number": null,
  "role": "customer",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2026-02-04T19:11:45.123456",
  "updated_at": null
}
```

---

### 1.2 Login and Get Access Token
**Endpoint:** `POST /api/v1/auth/login`

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john_doe&password=SecurePassword123"
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "role": "customer"
  }
}
```

---

### 1.3 Get Current User Info
**Endpoint:** `GET /api/v1/auth/me`

```bash
curl -X GET http://127.0.0.1:8000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "role": "customer",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2026-02-04T19:11:45.123456",
  "updated_at": null
}
```

---

### 1.4 Change Password
**Endpoint:** `POST /api/v1/auth/change-password`

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/change-password \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "old_password=SecurePassword123&new_password=NewPassword456"
```

---

## **2. USER MANAGEMENT ENDPOINTS**

### 2.1 Create User (Admin Only)
**Endpoint:** `POST /api/v1/users`

```bash
curl -X POST http://127.0.0.1:8000/api/v1/users \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice_smith",
    "email": "alice@example.com",
    "full_name": "Alice Smith",
    "password": "AlicePass123"
  }'
```

---

### 2.2 Get User by ID
**Endpoint:** `GET /api/v1/users/{user_id}`

```bash
curl -X GET http://127.0.0.1:8000/api/v1/users/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

### 2.3 List All Users (With Pagination)
**Endpoint:** `GET /api/v1/users?skip=0&limit=10`

```bash
curl -X GET "http://127.0.0.1:8000/api/v1/users?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

### 2.4 Update User
**Endpoint:** `PUT /api/v1/users/{user_id}`

```bash
curl -X PUT http://127.0.0.1:8000/api/v1/users/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Updated",
    "phone_number": "1234567890"
  }'
```

---

### 2.5 Delete User (Admin Only)
**Endpoint:** `DELETE /api/v1/users/{user_id}`

```bash
curl -X DELETE http://127.0.0.1:8000/api/v1/users/1 \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

---

## **3. LOAN MANAGEMENT ENDPOINTS**

### 3.1 Create Loan Application
**Endpoint:** `POST /api/v1/loans`

```bash
curl -X POST http://127.0.0.1:8000/api/v1/loans \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": 1,
    "loan_type": "personal",
    "requested_amount": 50000,
    "loan_term_months": 24,
    "purpose": "Home renovation"
  }'
```

**Loan Types:**
- `personal` - Personal loans
- `mortgage` - Home loans
- `auto` - Car loans
- `student` - Student loans
- `business` - Business loans
- `education` - Education loans

**Response (201 Created):**
```json
{
  "id": 1,
  "applicant_id": 1,
  "loan_type": "personal",
  "requested_amount": 50000,
  "loan_term_months": 24,
  "purpose": "Home renovation",
  "interest_rate": 8.5,
  "status": "PENDING",
  "created_at": "2026-02-04T19:11:45.123456",
  "updated_at": null
}
```

---

### 3.2 Get Loan by ID
**Endpoint:** `GET /api/v1/loans/{loan_id}`

```bash
curl -X GET http://127.0.0.1:8000/api/v1/loans/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

### 3.3 Get All Loans for a User
**Endpoint:** `GET /api/v1/loans/user/{user_id}`

```bash
curl -X GET http://127.0.0.1:8000/api/v1/loans/user/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

### 3.4 List All Loans (Loan Officer/Admin Only)
**Endpoint:** `GET /api/v1/loans?skip=0&limit=10`

```bash
curl -X GET "http://127.0.0.1:8000/api/v1/loans?skip=0&limit=10" \
  -H "Authorization: Bearer LOAN_OFFICER_TOKEN"
```

---

### 3.5 Update Loan Status (Loan Officer/Admin Only)
**Endpoint:** `PUT /api/v1/loans/{loan_id}`

```bash
curl -X PUT http://127.0.0.1:8000/api/v1/loans/1 \
  -H "Authorization: Bearer LOAN_OFFICER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "UNDER_REVIEW",
    "review_comments": "Reviewing application..."
  }'
```

---

### 3.6 Approve Loan (Loan Officer/Admin Only)
**Endpoint:** `POST /api/v1/loans/{loan_id}/approve`

Approves a PENDING loan and generates a repayment schedule.

```bash
curl -X POST http://127.0.0.1:8000/api/v1/loans/1/approve \
  -H "Authorization: Bearer LOAN_OFFICER_TOKEN"
```

**Response (200 OK):**
```json
{
  "id": 1,
  "status": "APPROVED",
  "interest_rate": 8.5,
  "requested_amount": 50000,
  ...
}
```

---

### 3.7 Reject Loan (Loan Officer/Admin Only)
**Endpoint:** `POST /api/v1/loans/{loan_id}/reject`

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/loans/1/reject?reason=Insufficient%20credit%20score" \
  -H "Authorization: Bearer LOAN_OFFICER_TOKEN"
```

---

## **4. PAYMENT ENDPOINTS**

### 4.1 Get Repayment Schedule
**Endpoint:** `GET /api/v1/payments/loan/{loan_id}/schedule`

```bash
curl -X GET http://127.0.0.1:8000/api/v1/payments/loan/1/schedule \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "loan_id": 1,
    "installment_number": 1,
    "due_date": "2026-03-04T19:11:45.123456",
    "amount_due": 2291.67,
    "principal_component": 2083.33,
    "interest_component": 208.34,
    "status": "PENDING",
    "amount_paid": 0,
    "payment_date": null,
    "created_at": "2026-02-04T19:11:45.123456"
  },
  ...
]
```

---

### 4.2 Get Repayment Schedule Detail
**Endpoint:** `GET /api/v1/payments/schedule/{schedule_id}`

```bash
curl -X GET http://127.0.0.1:8000/api/v1/payments/schedule/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

### 4.3 Make a Payment
**Endpoint:** `POST /api/v1/payments/schedule/{schedule_id}/pay`

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/payments/schedule/1/pay?amount=2291.67&payment_method=bank_transfer&transaction_reference=TXN123456" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response (200 OK):**
```json
{
  "schedule_id": 1,
  "amount_paid": 2291.67,
  "total_paid": 2291.67,
  "remaining": 52708.33,
  "status": "PAID",
  "transaction_reference": "TXN123456"
}
```

---

### 4.4 Get Payment History
**Endpoint:** `GET /api/v1/payments/loan/{loan_id}/history`

```bash
curl -X GET http://127.0.0.1:8000/api/v1/payments/loan/1/history \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response (200 OK):**
```json
[
  {
    "installment": 1,
    "due_date": "2026-03-04T19:11:45.123456",
    "amount_due": 2291.67,
    "amount_paid": 2291.67,
    "status": "PAID",
    "payment_date": "2026-03-04T10:00:00"
  },
  ...
]
```

---

### 4.5 Get Loan Balance
**Endpoint:** `GET /api/v1/payments/loan/{loan_id}/balance`

```bash
curl -X GET http://127.0.0.1:8000/api/v1/payments/loan/1/balance \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response (200 OK):**
```json
{
  "loan_id": 1,
  "total_due": 55000,
  "total_paid": 2291.67,
  "outstanding_balance": 52708.33,
  "paid_percentage": 4.17
}
```

---

## **COMPLETE WORKFLOW EXAMPLE**

```bash
# 1. Register
curl -X POST http://127.0.0.1:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"sarah","email":"sarah@test.com","full_name":"Sarah","password":"Sarah123"}'

# 2. Login (returns access_token)
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=sarah&password=Sarah123" | jq -r '.access_token')

# 3. Apply for Loan
curl -X POST http://127.0.0.1:8000/api/v1/loans \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"applicant_id":1,"loan_type":"auto","requested_amount":100000,"loan_term_months":60,"purpose":"Buy a car"}'

# 4. Get Loan Details
curl -X GET http://127.0.0.1:8000/api/v1/loans/1 \
  -H "Authorization: Bearer $TOKEN"

# 5. Get Repayment Schedule (after loan is approved)
curl -X GET http://127.0.0.1:8000/api/v1/payments/loan/1/schedule \
  -H "Authorization: Bearer $TOKEN"

# 6. Make a Payment
curl -X POST "http://127.0.0.1:8000/api/v1/payments/schedule/1/pay?amount=2000&payment_method=credit_card&transaction_reference=PAY123" \
  -H "Authorization: Bearer $TOKEN"

# 7. Check Balance
curl -X GET http://127.0.0.1:8000/api/v1/payments/loan/1/balance \
  -H "Authorization: Bearer $TOKEN"
```

---

## **ERROR CODES**

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized (Invalid/Missing token) |
| 403 | Forbidden (Insufficient permissions) |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Server Error |

---

## **NOTES**

- Always include `Authorization: Bearer TOKEN` in requests (except register and login)
- Use `Content-Type: application/json` for JSON payloads
- Use `Content-Type: application/x-www-form-urlencoded` for login
- Tokens expire after 30 minutes by default
- All timestamps are in UTC
- Loan Officer role required for approving/rejecting loans
