from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='pending')  # pending, processing, completed, error
    metadata = db.Column(db.JSON)
    user_id = db.Column(db.String(100))  # From session
    covenants = db.relationship('Covenant', backref='document', lazy=True)

class Covenant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    extracted_on = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, default=False)
    user_notes = db.Column(db.Text)
    covenant_type = db.Column(db.String(100))
    threshold_value = db.Column(db.String(100))
    compliance_status = db.Column(db.String(50), default='pending')  # compliant, at_risk, breached, pending
