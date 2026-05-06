# 🏦 Bond Central — College Project

> India's Central Bond Market Hub | SEBI Regulated | OBPP Association

---

## 📌 Project Overview

**Bond Central** is a full-stack web application that replicates the official [bondcentral.in](https://bondcentral.in) platform. It serves as a centralized database and investment portal for corporate bonds, government securities, and other fixed-income instruments in India.

---

## 🛠️ Technology Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Frontend   | HTML5, CSS3, JavaScript (Vanilla) |
| Backend    | Python 3.11 + Flask               |
| Database   | SQLite (Dev) / PostgreSQL (Prod)  |
| Auth       | JWT (JSON Web Tokens)             |
| ORM        | SQLAlchemy + Flask-SQLAlchemy     |

---

## 📁 Project Structure

```
bondcentral/
├── frontend/
│   ├── index.html          ← Home Page
│   ├── bonds.html          ← Bond Listing & Search
│   ├── login.html          ← Login (Investor / Company / Admin)
│   ├── register.html       ← Registration
│   ├── dashboard.html      ← Investor Dashboard
│   ├── calculator.html     ← Bond Calculator (YTM, Price, Returns, Tax)
│   ├── company.html        ← Company / Issuer Info Page
│   ├── style.css           ← Main Stylesheet
│   ├── main.js             ← Shared JS + Bond Data
│   └── bonds.js            ← Bonds Page Logic
│
├── backend/
│   ├── app.py              ← Flask Application (All API Routes)
│   └── requirements.txt    ← Python Dependencies
│
└── database/
    └── schema.sql          ← PostgreSQL Schema + Sample Data
```

---

## 👥 User Roles

### 1. 👤 Investor (Retail / HNI / NRI)
- Register with PAN, mobile, email
- Browse and filter bonds
- Add bonds to portfolio and watchlist
- Use bond calculator
- Complete KYC
- Track returns

### 2. 🏢 Company / Issuer
- Register as a bond issuer
- List new bonds (after admin approval)
- Upload bond documents
- Monitor investor interest

### 3. 🛡️ Admin
- Approve/reject company registrations
- Manage all bond listings
- View platform statistics

---

## 📋 Types of Bonds Supported

| Bond Type         | Description                                    | Typical Yield |
|-------------------|------------------------------------------------|---------------|
| G-Sec             | Central & State Government Securities          | 7.0 – 7.5%   |
| Corporate Bonds   | Issued by private companies                    | 8.0 – 12%    |
| PSU Bonds         | Public Sector Undertakings                     | 7.5 – 9%     |
| Zero Coupon       | Issued at discount, redeemed at face value     | Deep discount |
| 54EC Bonds        | Capital gains tax saving bonds (NHAI/REC)      | 5.0 – 5.75%  |
| SGB               | Sovereign Gold Bonds (RBI)                     | Gold + 2.5%  |

---

## 🚀 How to Run

### Frontend (Open directly in browser)
```bash
# No server needed - just open index.html
open frontend/index.html
```

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
# Server runs at http://localhost:5000
```

### Database Setup (PostgreSQL)
```bash
psql -U postgres -d bondcentral -f database/schema.sql
```

---

## 🔌 API Endpoints

| Method | Endpoint                          | Description              | Auth    |
|--------|-----------------------------------|--------------------------|---------|
| POST   | /api/auth/register/investor       | Register investor        | None    |
| POST   | /api/auth/register/company        | Register company         | None    |
| POST   | /api/auth/login                   | Login (all roles)        | None    |
| GET    | /api/bonds                        | List bonds (with filters)| None    |
| GET    | /api/bonds/:id                    | Bond detail              | None    |
| POST   | /api/bonds                        | Create bond              | Company |
| GET    | /api/portfolio                    | User portfolio           | Investor|
| POST   | /api/portfolio                    | Add to portfolio         | Investor|
| GET    | /api/watchlist                    | User watchlist           | Investor|
| POST   | /api/watchlist                    | Add to watchlist         | Investor|
| GET    | /api/user/profile                 | Get user profile         | Investor|
| PUT    | /api/user/kyc                     | Update KYC               | Investor|
| GET    | /api/admin/companies              | All companies            | Admin   |
| PUT    | /api/admin/companies/:id/approve  | Approve company          | Admin   |
| GET    | /api/admin/stats                  | Platform stats           | Admin   |
| POST   | /api/calculator/ytm               | Calculate YTM            | None    |

---

## 🧮 Bond Calculator Features

1. **YTM Calculator** — Yield to Maturity using approximate formula
2. **Bond Price Calculator** — Fair value via discounted cash flows
3. **Total Returns** — Coupon income + principal across tenure
4. **Post-Tax Returns** — Net returns after TDS and income tax

---

## 🎓 Developed by

**Dipti Mathur** — College Final Year Project  
**Platform Reference:** [bondcentral.in](https://bondcentral.in) (SEBI / OBPP Association of India)

---

> ⚠️ **Disclaimer:** This project is built purely for educational purposes. It is not a real investment platform. Bond Central (bondcentral.in) is an initiative by SEBI and OBPP Association of India.
