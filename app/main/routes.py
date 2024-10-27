from flask import Blueprint, render_template, session, redirect, url_for
from functools import wraps
from app.models import Document, Covenant

main_bp = Blueprint('main', __name__)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dashboard')
@requires_auth
def dashboard():
    # Get user's documents
    documents = Document.query.filter_by(user_id=session['user']['username']).all()
    
    # Get recent documents (last 5)
    recent_documents = Document.query.filter_by(user_id=session['user']['username'])\
        .order_by(Document.upload_date.desc())\
        .limit(5)\
        .all()
    
    # Get covenant statistics
    covenants = Covenant.query.join(Document)\
        .filter(Document.user_id == session['user']['username'])\
        .all()
    
    compliant_count = sum(1 for c in covenants if c.compliance_status == 'compliant')
    at_risk_count = sum(1 for c in covenants if c.compliance_status == 'at_risk')
    breached_count = sum(1 for c in covenants if c.compliance_status == 'breached')
    
    return render_template('dashboard.html',
                         documents=documents,
                         recent_documents=recent_documents,
                         compliant_count=compliant_count,
                         at_risk_count=at_risk_count,
                         breached_count=breached_count)
