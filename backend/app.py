"""
====================================================
  BOND CENTRAL — Python Flask Backend
  Tech Stack: Flask + SQLite (dev) / PostgreSQL (prod)
====================================================
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
import datetime
import os

app = Flask(__name__)
CORS(app)

# ─── CONFIG ──────────────────────────────────────────────────────────────────
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'bondcentral_dev_secret_2025')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///bondcentral.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ─── MODELS ──────────────────────────────────────────────────────────────────

class User(db.Model):
    """Retail / HNI Investor"""
    __tablename__ = 'users'
    id           = db.Column(db.Integer, primary_key=True)
    first_name   = db.Column(db.String(50), nullable=False)
    last_name    = db.Column(db.String(50), nullable=False)
    email        = db.Column(db.String(120), unique=True, nullable=False)
    mobile       = db.Column(db.String(15), unique=True, nullable=False)
    pan          = db.Column(db.String(10), unique=True, nullable=False)
    investor_type = db.Column(db.String(50), default='Retail Individual Investor')
    password_hash = db.Column(db.String(256), nullable=False)
    kyc_status   = db.Column(db.String(20), default='pending')   # pending | verified | rejected
    demat_account = db.Column(db.String(20))
    created_at   = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_active    = db.Column(db.Boolean, default=True)

    portfolio    = db.relationship('Portfolio', backref='user', lazy=True)
    watchlist    = db.relationship('Watchlist', backref='user', lazy=True)

    def to_dict(self):
        return {
            'id': self.id, 'first_name': self.first_name,
            'last_name': self.last_name, 'email': self.email,
            'mobile': self.mobile, 'pan': self.pan,
            'investor_type': self.investor_type, 'kyc_status': self.kyc_status,
            'created_at': str(self.created_at)
        }


class Company(db.Model):
    """Bond Issuer / Company"""
    __tablename__ = 'companies'
    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(150), nullable=False)
    cin          = db.Column(db.String(21), unique=True, nullable=False)
    pan          = db.Column(db.String(10), unique=True, nullable=False)
    sector       = db.Column(db.String(80))
    contact_email = db.Column(db.String(120), unique=True, nullable=False)
    mobile       = db.Column(db.String(15))
    password_hash = db.Column(db.String(256), nullable=False)
    status       = db.Column(db.String(20), default='pending')  # pending | approved | rejected
    created_at   = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    bonds        = db.relationship('Bond', backref='company', lazy=True)

    def to_dict(self):
        return {
            'id': self.id, 'name': self.name, 'cin': self.cin,
            'sector': self.sector, 'status': self.status,
            'contact_email': self.contact_email, 'created_at': str(self.created_at)
        }


class Bond(db.Model):
    """Bond Listing"""
    __tablename__ = 'bonds'
    id            = db.Column(db.Integer, primary_key=True)
    company_id    = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True)
    issuer_name   = db.Column(db.String(150), nullable=False)
    isin          = db.Column(db.String(12), unique=True, nullable=False)
    bond_type     = db.Column(db.String(30), nullable=False)   # G-Sec | Corporate | PSU | SGB | Zero Coupon | 54EC
    face_value    = db.Column(db.Float, default=1000.0)
    coupon_rate   = db.Column(db.Float, nullable=False)         # % per annum
    maturity_date = db.Column(db.Date, nullable=False)
    credit_rating = db.Column(db.String(20))
    exchange      = db.Column(db.String(20))                    # BSE | NSE | BSE/NSE
    min_investment = db.Column(db.Float, default=10000.0)
    frequency     = db.Column(db.String(20), default='Annual')  # Annual | Semi-Annual | Quarterly
    status        = db.Column(db.String(20), default='active')  # active | inactive | matured
    created_at    = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    portfolio_entries = db.relationship('Portfolio', backref='bond', lazy=True)
    watchlist_entries = db.relationship('Watchlist', backref='bond', lazy=True)

    def to_dict(self):
        return {
            'id': self.id, 'issuer_name': self.issuer_name,
            'isin': self.isin, 'bond_type': self.bond_type,
            'face_value': self.face_value, 'coupon_rate': self.coupon_rate,
            'maturity_date': str(self.maturity_date),
            'credit_rating': self.credit_rating,
            'exchange': self.exchange, 'min_investment': self.min_investment,
            'frequency': self.frequency, 'status': self.status
        }


class Portfolio(db.Model):
    """User's Bond Holdings"""
    __tablename__ = 'portfolio'
    id            = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bond_id       = db.Column(db.Integer, db.ForeignKey('bonds.id'), nullable=False)
    units         = db.Column(db.Integer, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    purchase_date  = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id, 'bond_id': self.bond_id,
            'units': self.units, 'purchase_price': self.purchase_price,
            'purchase_date': str(self.purchase_date),
            'bond': self.bond.to_dict() if self.bond else {}
        }


class Watchlist(db.Model):
    __tablename__ = 'watchlist'
    id      = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bond_id = db.Column(db.Integer, db.ForeignKey('bonds.id'), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


# ─── AUTH HELPERS ─────────────────────────────────────────────────────────────

def generate_token(user_id, role='investor'):
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'error': 'Token missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            request.user_id = data['user_id']
            request.role = data['role']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        @token_required
        def decorated(*args, **kwargs):
            if request.role not in roles:
                return jsonify({'error': 'Unauthorized role'}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator


# ─── ROUTES ───────────────────────────────────────────────────────────────────

@app.route('/')
def home():
    return jsonify({'message': 'Bond Central API v1.0', 'status': 'running'})


# --- AUTH ---

@app.route('/api/auth/register/investor', methods=['POST'])
def register_investor():
    data = request.get_json()
    required = ['first_name', 'last_name', 'email', 'mobile', 'pan', 'password', 'investor_type']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409
    if User.query.filter_by(pan=data['pan'].upper()).first():
        return jsonify({'error': 'PAN already registered'}), 409

    user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'].lower(),
        mobile=data['mobile'],
        pan=data['pan'].upper(),
        investor_type=data['investor_type'],
        password_hash=generate_password_hash(data['password'])
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Investor registered successfully', 'user': user.to_dict()}), 201


@app.route('/api/auth/register/company', methods=['POST'])
def register_company():
    data = request.get_json()
    required = ['name', 'cin', 'pan', 'contact_email', 'mobile', 'sector', 'password']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400

    if Company.query.filter_by(contact_email=data['contact_email']).first():
        return jsonify({'error': 'Email already registered'}), 409

    company = Company(
        name=data['name'],
        cin=data['cin'],
        pan=data['pan'].upper(),
        sector=data['sector'],
        contact_email=data['contact_email'].lower(),
        mobile=data['mobile'],
        password_hash=generate_password_hash(data['password'])
    )
    db.session.add(company)
    db.session.commit()
    return jsonify({'message': 'Company registered. Pending admin approval.', 'company': company.to_dict()}), 201


@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    role = data.get('role', 'investor')
    email = data.get('email', '').lower()
    password = data.get('password', '')

    if role == 'investor':
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({'error': 'Invalid credentials'}), 401
        token = generate_token(user.id, 'investor')
        return jsonify({'token': token, 'user': user.to_dict(), 'role': 'investor'})

    elif role == 'company':
        company = Company.query.filter_by(contact_email=email).first()
        if not company or not check_password_hash(company.password_hash, password):
            return jsonify({'error': 'Invalid credentials'}), 401
        if company.status != 'approved':
            return jsonify({'error': 'Company account pending approval'}), 403
        token = generate_token(company.id, 'company')
        return jsonify({'token': token, 'company': company.to_dict(), 'role': 'company'})

    elif role == 'admin':
        # Static admin for demo
        if email == 'admin@bondcentral.in' and password == 'Admin@2025':
            token = generate_token(0, 'admin')
            return jsonify({'token': token, 'role': 'admin'})
        return jsonify({'error': 'Invalid admin credentials'}), 401

    return jsonify({'error': 'Invalid role'}), 400


# --- BONDS ---

@app.route('/api/bonds', methods=['GET'])
def get_bonds():
    bond_type = request.args.get('type')
    rating    = request.args.get('rating')
    min_yield = request.args.get('min_yield', type=float)
    max_yield = request.args.get('max_yield', type=float)
    search    = request.args.get('q', '')
    sort_by   = request.args.get('sort', 'coupon_rate')
    page      = request.args.get('page', 1, type=int)
    per_page  = request.args.get('per_page', 10, type=int)

    query = Bond.query.filter_by(status='active')
    if bond_type:
        query = query.filter_by(bond_type=bond_type)
    if rating:
        query = query.filter_by(credit_rating=rating)
    if min_yield is not None:
        query = query.filter(Bond.coupon_rate >= min_yield)
    if max_yield is not None:
        query = query.filter(Bond.coupon_rate <= max_yield)
    if search:
        query = query.filter(Bond.issuer_name.ilike(f'%{search}%'))

    if sort_by == 'coupon_rate':
        query = query.order_by(Bond.coupon_rate.desc())
    elif sort_by == 'maturity':
        query = query.order_by(Bond.maturity_date.asc())
    elif sort_by == 'rating':
        query = query.order_by(Bond.credit_rating.asc())

    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'bonds': [b.to_dict() for b in paginated.items],
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': page
    })


@app.route('/api/bonds/<int:bond_id>', methods=['GET'])
def get_bond(bond_id):
    bond = Bond.query.get_or_404(bond_id)
    return jsonify(bond.to_dict())


@app.route('/api/bonds', methods=['POST'])
@role_required('company', 'admin')
def create_bond():
    data = request.get_json()
    required = ['issuer_name', 'isin', 'bond_type', 'coupon_rate', 'maturity_date']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400

    bond = Bond(
        company_id=request.user_id if request.role == 'company' else None,
        issuer_name=data['issuer_name'],
        isin=data['isin'],
        bond_type=data['bond_type'],
        face_value=data.get('face_value', 1000),
        coupon_rate=data['coupon_rate'],
        maturity_date=datetime.datetime.strptime(data['maturity_date'], '%Y-%m-%d').date(),
        credit_rating=data.get('credit_rating'),
        exchange=data.get('exchange', 'BSE/NSE'),
        min_investment=data.get('min_investment', 10000),
        frequency=data.get('frequency', 'Annual')
    )
    db.session.add(bond)
    db.session.commit()
    return jsonify({'message': 'Bond listed successfully', 'bond': bond.to_dict()}), 201


# --- PORTFOLIO ---

@app.route('/api/portfolio', methods=['GET'])
@token_required
def get_portfolio():
    if request.role != 'investor':
        return jsonify({'error': 'Investor only'}), 403
    items = Portfolio.query.filter_by(user_id=request.user_id).all()
    total_invested = sum(i.units * i.purchase_price for i in items)
    return jsonify({
        'portfolio': [i.to_dict() for i in items],
        'total_invested': total_invested,
        'count': len(items)
    })


@app.route('/api/portfolio', methods=['POST'])
@token_required
def add_to_portfolio():
    if request.role != 'investor':
        return jsonify({'error': 'Investor only'}), 403
    data = request.get_json()
    bond = Bond.query.get(data.get('bond_id'))
    if not bond:
        return jsonify({'error': 'Bond not found'}), 404
    entry = Portfolio(
        user_id=request.user_id,
        bond_id=data['bond_id'],
        units=data.get('units', 1),
        purchase_price=data.get('purchase_price', bond.face_value)
    )
    db.session.add(entry)
    db.session.commit()
    return jsonify({'message': 'Added to portfolio', 'entry': entry.to_dict()}), 201


# --- WATCHLIST ---

@app.route('/api/watchlist', methods=['GET'])
@token_required
def get_watchlist():
    items = Watchlist.query.filter_by(user_id=request.user_id).all()
    result = []
    for item in items:
        bond_data = item.bond.to_dict() if item.bond else {}
        result.append({'id': item.id, 'bond': bond_data, 'added_at': str(item.added_at)})
    return jsonify({'watchlist': result})


@app.route('/api/watchlist', methods=['POST'])
@token_required
def add_watchlist():
    data = request.get_json()
    existing = Watchlist.query.filter_by(user_id=request.user_id, bond_id=data['bond_id']).first()
    if existing:
        return jsonify({'message': 'Already in watchlist'}), 200
    wl = Watchlist(user_id=request.user_id, bond_id=data['bond_id'])
    db.session.add(wl)
    db.session.commit()
    return jsonify({'message': 'Added to watchlist'}), 201


@app.route('/api/watchlist/<int:wl_id>', methods=['DELETE'])
@token_required
def remove_watchlist(wl_id):
    wl = Watchlist.query.filter_by(id=wl_id, user_id=request.user_id).first_or_404()
    db.session.delete(wl)
    db.session.commit()
    return jsonify({'message': 'Removed from watchlist'})


# --- USER PROFILE ---

@app.route('/api/user/profile', methods=['GET'])
@token_required
def get_profile():
    if request.role != 'investor':
        return jsonify({'error': 'Investor only'}), 403
    user = User.query.get(request.user_id)
    return jsonify(user.to_dict())


@app.route('/api/user/kyc', methods=['PUT'])
@token_required
def update_kyc():
    if request.role != 'investor':
        return jsonify({'error': 'Investor only'}), 403
    data = request.get_json()
    user = User.query.get(request.user_id)
    if data.get('demat_account'):
        user.demat_account = data['demat_account']
        user.kyc_status = 'verified'
    db.session.commit()
    return jsonify({'message': 'KYC updated', 'user': user.to_dict()})


# --- ADMIN ---

@app.route('/api/admin/companies', methods=['GET'])
@role_required('admin')
def admin_get_companies():
    companies = Company.query.all()
    return jsonify({'companies': [c.to_dict() for c in companies]})


@app.route('/api/admin/companies/<int:cid>/approve', methods=['PUT'])
@role_required('admin')
def admin_approve_company(cid):
    company = Company.query.get_or_404(cid)
    company.status = 'approved'
    db.session.commit()
    return jsonify({'message': f'{company.name} approved'})


@app.route('/api/admin/companies/<int:cid>/reject', methods=['PUT'])
@role_required('admin')
def admin_reject_company(cid):
    company = Company.query.get_or_404(cid)
    company.status = 'rejected'
    db.session.commit()
    return jsonify({'message': f'{company.name} rejected'})


@app.route('/api/admin/stats', methods=['GET'])
@role_required('admin')
def admin_stats():
    return jsonify({
        'total_users': User.query.count(),
        'total_companies': Company.query.count(),
        'pending_companies': Company.query.filter_by(status='pending').count(),
        'total_bonds': Bond.query.count(),
        'active_bonds': Bond.query.filter_by(status='active').count(),
    })


# --- CALCULATOR API ---

@app.route('/api/calculator/ytm', methods=['POST'])
def calc_ytm():
    data = request.get_json()
    F = float(data.get('face_value', 10000))
    C = F * float(data.get('coupon_rate', 9.5)) / 100
    P = float(data.get('market_price', 10000))
    n = float(data.get('years', 5))
    if n == 0:
        return jsonify({'error': 'Years cannot be 0'}), 400
    ytm = ((C + (F - P) / n) / ((F + P) / 2)) * 100
    return jsonify({
        'annual_coupon': round(C, 2),
        'total_coupons': round(C * n, 2),
        'capital_gain_loss': round(F - P, 2),
        'ytm': round(ytm, 4)
    })


# ─── SEED DATA ────────────────────────────────────────────────────────────────

def seed_data():
    """Seed some sample bonds if DB is empty"""
    if Bond.query.count() == 0:
        sample_bonds = [
            Bond(issuer_name='Govt. of India 2034', isin='IN0020190104', bond_type='G-Sec',
                 coupon_rate=7.18, maturity_date=datetime.date(2034,3,15), credit_rating='Sovereign',
                 exchange='BSE/NSE', min_investment=10000),
            Bond(issuer_name='HDFC Bank Ltd.', isin='INE040A08378', bond_type='Corporate',
                 coupon_rate=9.25, maturity_date=datetime.date(2027,6,30), credit_rating='AAA',
                 exchange='BSE', min_investment=10000),
            Bond(issuer_name='NTPC Limited', isin='INE733E07379', bond_type='PSU',
                 coupon_rate=8.75, maturity_date=datetime.date(2029,1,15), credit_rating='AAA',
                 exchange='NSE', min_investment=10000),
            Bond(issuer_name='Tata Capital Financial Services', isin='INE306N07278', bond_type='Corporate',
                 coupon_rate=10.50, maturity_date=datetime.date(2026,9,20), credit_rating='AA+',
                 exchange='BSE', min_investment=10000),
            Bond(issuer_name='REC Limited', isin='INE020B08BF5', bond_type='PSU',
                 coupon_rate=7.90, maturity_date=datetime.date(2026,12,1), credit_rating='AAA',
                 exchange='NSE', min_investment=10000),
            Bond(issuer_name='NHAI Bonds (54EC)', isin='INE906B07GA6', bond_type='54EC',
                 coupon_rate=5.25, maturity_date=datetime.date(2028,3,31), credit_rating='Sovereign',
                 exchange='BSE', min_investment=10000),
            Bond(issuer_name='Sovereign Gold Bond Series III', isin='IN0020230034', bond_type='SGB',
                 coupon_rate=2.50, maturity_date=datetime.date(2033,10,30), credit_rating='Sovereign',
                 exchange='BSE/NSE', min_investment=4800),
        ]
        for b in sample_bonds:
            db.session.add(b)
        db.session.commit()
        print("✅ Sample bonds seeded.")


# ─── ENTRY POINT ─────────────────────────────────────────────────────────────


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)