-- ================================================
--  BOND CENTRAL — Database Schema (PostgreSQL)
-- ================================================

-- Users (Investors)
CREATE TABLE IF NOT EXISTS users (
    id              SERIAL PRIMARY KEY,
    first_name      VARCHAR(50) NOT NULL,
    last_name       VARCHAR(50) NOT NULL,
    email           VARCHAR(120) UNIQUE NOT NULL,
    mobile          VARCHAR(15) UNIQUE NOT NULL,
    pan             VARCHAR(10) UNIQUE NOT NULL,
    investor_type   VARCHAR(60) DEFAULT 'Retail Individual Investor',
    password_hash   VARCHAR(256) NOT NULL,
    kyc_status      VARCHAR(20) DEFAULT 'pending',
    demat_account   VARCHAR(20),
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Companies (Issuers)
CREATE TABLE IF NOT EXISTS companies (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(150) NOT NULL,
    cin             VARCHAR(21) UNIQUE NOT NULL,
    pan             VARCHAR(10) UNIQUE NOT NULL,
    sector          VARCHAR(80),
    contact_email   VARCHAR(120) UNIQUE NOT NULL,
    mobile          VARCHAR(15),
    password_hash   VARCHAR(256) NOT NULL,
    status          VARCHAR(20) DEFAULT 'pending',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bonds
CREATE TABLE IF NOT EXISTS bonds (
    id              SERIAL PRIMARY KEY,
    company_id      INTEGER REFERENCES companies(id),
    issuer_name     VARCHAR(150) NOT NULL,
    isin            VARCHAR(12) UNIQUE NOT NULL,
    bond_type       VARCHAR(30) NOT NULL,
    face_value      NUMERIC(15,2) DEFAULT 1000.00,
    coupon_rate     NUMERIC(5,2) NOT NULL,
    maturity_date   DATE NOT NULL,
    credit_rating   VARCHAR(20),
    exchange        VARCHAR(20),
    min_investment  NUMERIC(15,2) DEFAULT 10000.00,
    frequency       VARCHAR(20) DEFAULT 'Annual',
    status          VARCHAR(20) DEFAULT 'active',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Portfolio (User Holdings)
CREATE TABLE IF NOT EXISTS portfolio (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    bond_id         INTEGER NOT NULL REFERENCES bonds(id) ON DELETE CASCADE,
    units           INTEGER NOT NULL,
    purchase_price  NUMERIC(15,2) NOT NULL,
    purchase_date   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, bond_id)
);

-- Watchlist
CREATE TABLE IF NOT EXISTS watchlist (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    bond_id         INTEGER NOT NULL REFERENCES bonds(id) ON DELETE CASCADE,
    added_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, bond_id)
);

-- KYC Documents
CREATE TABLE IF NOT EXISTS kyc_documents (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    doc_type        VARCHAR(30) NOT NULL,   -- PAN | Aadhaar | Bank | Demat
    doc_number      VARCHAR(50),
    verified        BOOLEAN DEFAULT FALSE,
    uploaded_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bond Documents (for Companies)
CREATE TABLE IF NOT EXISTS bond_documents (
    id              SERIAL PRIMARY KEY,
    bond_id         INTEGER NOT NULL REFERENCES bonds(id) ON DELETE CASCADE,
    doc_type        VARCHAR(50) NOT NULL,   -- Prospectus | Rating | Financials
    file_path       VARCHAR(300),
    uploaded_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_bonds_type ON bonds(bond_type);
CREATE INDEX IF NOT EXISTS idx_bonds_rating ON bonds(credit_rating);
CREATE INDEX IF NOT EXISTS idx_bonds_coupon ON bonds(coupon_rate);
CREATE INDEX IF NOT EXISTS idx_portfolio_user ON portfolio(user_id);
CREATE INDEX IF NOT EXISTS idx_watchlist_user ON watchlist(user_id);

-- ── SAMPLE DATA ────────────────────────────────
INSERT INTO bonds (issuer_name, isin, bond_type, coupon_rate, maturity_date, credit_rating, exchange, min_investment)
VALUES
  ('Govt. of India 2034',         'IN0020190104', 'G-Sec',     7.18, '2034-03-15', 'Sovereign', 'BSE/NSE', 10000),
  ('HDFC Bank Ltd.',               'INE040A08378', 'Corporate', 9.25, '2027-06-30', 'AAA',       'BSE',     10000),
  ('NTPC Limited',                 'INE733E07379', 'PSU',       8.75, '2029-01-15', 'AAA',       'NSE',     10000),
  ('Tata Capital Financial Svc',   'INE306N07278', 'Corporate',10.50, '2026-09-20', 'AA+',       'BSE',     10000),
  ('REC Limited',                  'INE020B08BF5', 'PSU',       7.90, '2026-12-01', 'AAA',       'NSE',     10000),
  ('Bajaj Finance Ltd.',           'INE296A07PS5', 'Corporate',10.10, '2027-08-15', 'AA+',       'BSE',     10000),
  ('NHAI Bonds (54EC)',            'INE906B07GA6', '54EC',      5.25, '2028-03-31', 'Sovereign', 'BSE',     10000),
  ('Sovereign Gold Bond SII-III',  'IN0020230034', 'SGB',       2.50, '2033-10-30', 'Sovereign', 'BSE/NSE',  4800),
  ('Indian Railway Finance Corp',  'INE053F07AZ3', 'PSU',       7.68, '2031-07-20', 'AAA',       'NSE',     10000),
  ('Muthoot Finance Ltd.',         'INE414G07HK2', 'Corporate',11.50, '2026-03-10', 'AA',        'BSE',     10000)
ON CONFLICT (isin) DO NOTHING;
