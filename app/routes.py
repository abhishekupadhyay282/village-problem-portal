"""Flask routes for the village portal."""

from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app import db
from app.models import Problem

main_bp = Blueprint('main', __name__)

# Problem categories
CATEGORIES = ['Infrastructure', 'Health', 'Water', 'Education', 'Other']


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
    
    # Create new problem record
    problem = Problem(
        name=data.get('name').strip(),
        category=data.get('category'),
        description=data.get('description').strip(),
        contact=data.get('contact').strip()
    )
    
    try:
        db.session.add(problem)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Problem submitted successfully!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Error submitting problem'}), 500


@main_bp.route('/admin')
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
    
    return jsonify({'success': True, 'message': 'Status updated successfully'})


@main_bp.route('/api/problems/<int:problem_id>', methods=['DELETE'])
def delete_problem(problem_id):
    """Delete a problem."""
    problem = Problem.query.get_or_404(problem_id)
    db.session.delete(problem)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Probhhlem deleted successfully'})
