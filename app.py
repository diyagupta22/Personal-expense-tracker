from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False, default='Other')
    note = db.Column(db.String(200))
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category,
            'note': self.note,
            'date': self.date.strftime('%Y-%m-%d'),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# Create database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    category = request.args.get('category')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Expense.query
    
    if category and category != 'all':
        query = query.filter_by(category=category)
    if start_date:
        query = query.filter(Expense.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(Expense.date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    expenses = query.order_by(Expense.date.desc()).all()
    return jsonify([expense.to_dict() for expense in expenses])

@app.route('/api/expenses', methods=['POST'])
def add_expense():
    try:
        data = request.json
        
        # Validation
        if not data.get('amount') or float(data['amount']) <= 0:
            return jsonify({'error': 'Valid amount is required'}), 400
        
        if not data.get('date'):
            return jsonify({'error': 'Date is required'}), 400
        
        expense = Expense(
            amount=float(data['amount']),
            category=data.get('category', 'Other'),
            note=data.get('note', ''),
            date=datetime.strptime(data['date'], '%Y-%m-%d').date()
        )
        
        db.session.add(expense)
        db.session.commit()
        
        return jsonify(expense.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/expenses/<int:id>', methods=['PUT'])
def update_expense(id):
    try:
        expense = Expense.query.get_or_404(id)
        data = request.json
        
        if data.get('amount'):
            if float(data['amount']) <= 0:
                return jsonify({'error': 'Amount must be positive'}), 400
            expense.amount = float(data['amount'])
        
        if data.get('category'):
            expense.category = data['category']
        
        if data.get('note') is not None:
            expense.note = data['note']
        
        if data.get('date'):
            expense.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        
        db.session.commit()
        return jsonify(expense.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/expenses/<int:id>', methods=['DELETE'])
def delete_expense(id):
    try:
        expense = Expense.query.get_or_404(id)
        db.session.delete(expense)
        db.session.commit()
        return jsonify({'message': 'Expense deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/summary', methods=['GET'])
def get_summary():
    category = request.args.get('category')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Expense.query
    
    if category and category != 'all':
        query = query.filter_by(category=category)
    if start_date:
        query = query.filter(Expense.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(Expense.date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    expenses = query.all()
    
    # Calculate totals
    total = sum(exp.amount for exp in expenses)
    
    # Group by category
    by_category = {}
    for exp in expenses:
        by_category[exp.category] = by_category.get(exp.category, 0) + exp.amount
    
    # Group by month
    by_month = {}
    for exp in expenses:
        month_key = exp.date.strftime('%Y-%m')
        by_month[month_key] = by_month.get(month_key, 0) + exp.amount
    
    return jsonify({
        'total': round(total, 2),
        'by_category': {k: round(v, 2) for k, v in by_category.items()},
        'by_month': {k: round(v, 2) for k, v in by_month.items()},
        'count': len(expenses)
    })

if __name__ == '__main__':
    app.run(debug=True)