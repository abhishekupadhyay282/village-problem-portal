"""Flask routes for the village portal."""

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from functools import wraps
from app import db
from app.models import Problem

main_bp = Blueprint('main', __name__)

# Problem categories
CATEGORIES = ['Infrastructure', 'Health', 'Water', 'Education', 'Other']

# Admin password (change this in production!)
ADMIN_PASSWORD = 'admin123'

# Decorator to check admin access
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session or not session['admin']:
            return redirect(url_for('main.admin_login'))
        return f(*args, **kwargs)
    return decorated_function


@main_bp.route('/')
def index():
    """Display the problem submission form."""
    return render_template('submit.html', categories=CATEGORIES)


@main_bp.route('/submit', methods=['POST'])
def submit_problem():
    """Handle problem submission from villagers."""
    data = request.form
    
    # Validate form data
    if not all([data.get('name'), data.get('category'), data.get('description'), data.get('contact')]):
        return jsonify({'success': False, 'message': 'All fields are required'}), 400
    
    # Check if user wants to submit to Jansunwai
    submit_to_jansunwai = data.get('submit_to_jansunwai') == 'yes'
    
    # Create new problem record
    problem = Problem(
        name=data.get('name').strip(),
        category=data.get('category'),
        description=data.get('description').strip(),
        contact=data.get('contact').strip(),
        submitted_to_jansunwai=submit_to_jansunwai,
        jansunwai_link='https://jansunwai.up.nic.in/' if submit_to_jansunwai else None
    )
    
    try:
        db.session.add(problem)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Problem submitted successfully!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Error submitting problem'}), 500


@main_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page."""
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('main.admin_dashboard'))
        else:
            return render_template('admin_login.html', error='Invalid password'), 401
    return render_template('admin_login.html')


@main_bp.route('/admin/logout')
def admin_logout():
    """Logout admin."""
    session.pop('admin', None)
    return redirect(url_for('main.index'))


@main_bp.route('/admin')
@admin_required
def admin_dashboard():
    """Display admin dashboard with all submitted problems."""
    page = request.args.get('page', 1, type=int)
    category_filter = request.args.get('category', '', type=str)
    status_filter = request.args.get('status', '', type=str)
    
    # Build query
    query = Problem.query
    
    if category_filter and category_filter in CATEGORIES:
        query = query.filter_by(category=category_filter)
    
    if status_filter and status_filter in ['New', 'In Progress', 'Resolved']:
        query = query.filter_by(status=status_filter)
    
    # Paginate results (10 per page)
    problems = query.order_by(Problem.created_at.desc()).paginate(page=page, per_page=10)
    
    return render_template(
        'admin.html',
        problems=problems.items,
        total=problems.total,
        pages=problems.pages,
        current_page=page,
        categories=CATEGORIES,
        selected_category=category_filter,
        selected_status=status_filter
    )


@main_bp.route('/api/problems')
@admin_required
def get_problems():
    """API endpoint to get all problems as JSON."""
    page = request.args.get('page', 1, type=int)
    category_filter = request.args.get('category', '', type=str)
    status_filter = request.args.get('status', '', type=str)
    
    # Build query
    query = Problem.query
    
    if category_filter and category_filter in CATEGORIES:
        query = query.filter_by(category=category_filter)
    
    if status_filter and status_filter in ['New', 'In Progress', 'Resolved']:
        query = query.filter_by(status=status_filter)
    
    # Paginate results
    problems = query.order_by(Problem.created_at.desc()).paginate(page=page, per_page=10)
    
    return jsonify({
        'problems': [p.to_dict() for p in problems.items],
        'total': problems.total,
        'pages': problems.pages,
        'current_page': page
    })


@main_bp.route('/api/problems/<int:problem_id>/status', methods=['PUT'])
def update_problem_status(problem_id):
    """Update problem status."""
    problem = Problem.query.get_or_404(problem_id)
    data = request.get_json()
    
    if 'status' not in data or data['status'] not in ['New', 'In Progress', 'Resolved']:
        return jsonify({'success': False, 'message': 'Invalid status'}), 400
    
    problem.status = data['status']
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Status  successfully'})


@main_bp.route('/api/problems/<int:problem_id>', methods=['DELETE'])
def delete_problem(problem_id):
    """Delete a problem."""
    problem = Problem.query.get_or_404(problem_id)
    db.session.delete(problem)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Probhhlem deleted successfully'})
