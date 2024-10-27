import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
from werkzeug.utils import secure_filename
from app.models import db, Document, Covenant
from app.documents.processor import process_document
import openai

documents_bp = Blueprint('documents', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@documents_bp.route('/documents')
def list_documents():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    documents = Document.query.filter_by(user_id=session['user']['username']).all()
    return render_template('documents/list.html', documents=documents)

@documents_bp.route('/documents/upload', methods=['GET', 'POST'])
def upload_document():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        if 'document' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['document']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Create uploads directory if it doesn't exist
            os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
            
            # Save file
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Create document record
            document = Document(
                filename=filename,
                original_filename=file.filename,
                user_id=session['user']['username'],
                metadata={
                    'description': request.form.get('description', ''),
                    'document_type': request.form.get('document_type', 'other')
                }
            )
            db.session.add(document)
            db.session.commit()
            
            # Process document in background (in production, use Celery)
            try:
                covenants = process_document(file_path, document.id)
                document.status = 'completed'
                db.session.commit()
                flash('Document uploaded and processed successfully', 'success')
            except Exception as e:
                document.status = 'error'
                db.session.commit()
                flash(f'Error processing document: {str(e)}', 'error')
            
            return redirect(url_for('documents.list_documents'))
        
        flash('Invalid file type', 'error')
        return redirect(request.url)
    
    return render_template('documents/upload.html')

@documents_bp.route('/documents/<int:document_id>')
def view_document(document_id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    document = Document.query.get_or_404(document_id)
    if document.user_id != session['user']['username']:
        flash('Access denied', 'error')
        return redirect(url_for('documents.list_documents'))
    
    covenants = Covenant.query.filter_by(document_id=document_id).all()
    return render_template('documents/view.html', document=document, covenants=covenants)

@documents_bp.route('/documents/<int:document_id>/covenant/<int:covenant_id>', methods=['POST'])
def update_covenant(document_id, covenant_id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    covenant = Covenant.query.get_or_404(covenant_id)
    if covenant.document.user_id != session['user']['username']:
        flash('Access denied', 'error')
        return redirect(url_for('documents.list_documents'))
    
    covenant.confirmed = True
    covenant.user_notes = request.form.get('notes', '')
    covenant.compliance_status = request.form.get('status', 'pending')
    db.session.commit()
    
    flash('Covenant updated successfully', 'success')
    return redirect(url_for('documents.view_document', document_id=document_id))
