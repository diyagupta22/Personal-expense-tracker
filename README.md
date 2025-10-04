# Student Budget Tracker 💰

A simple web-based expense tracking application designed specifically for students to manage their daily expenses and build better spending habits.

## How to Run

### Prerequisites
- Python 3.7 or higher
- Web browser (Chrome, Firefox, Safari, etc.)

### Installation Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd student-budget-tracker
   ```

2. Install required dependencies:
   ```bash
   pip install flask
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Features

### Core Functionality
- **Add Expenses**: Record expenses with amount, category, date, and optional notes
- **View Expenses**: Display all expenses in a clean, organized list
- **Edit Expenses**: Modify existing expense entries
- **Delete Expenses**: Remove unwanted expense records
- **Filter & Search**: Filter expenses by category and date range
- **Summary Dashboard**: View total spending and category-wise breakdowns

### Student-Specific Categories
- 🍕 Food & Snacks
- 🚌 Transport
- 📚 Books & Stationery
- 🎮 Entertainment
- 👕 Clothes & Shopping
- 💊 Health & Medicine
- 🎓 College Fees
- 📦 Other

## Documentation

### Assumptions
- Users are primarily students with limited income
- Expenses are recorded in Indian Rupees (₹)
- Categories are pre-defined to match common student expenses
- Data persistence is handled through backend API calls
- Users have basic web browser functionality available

### Design Architecture
```
Frontend (HTML/CSS/JS) → Backend API (Flask) → Data Storage
```

- **Frontend**: Responsive web interface using Bootstrap framework
- **Backend**: RESTful API endpoints for CRUD operations
- **Styling**: Clean black and white theme for better focus and performance
- **Data Flow**: Asynchronous JavaScript calls to backend API

### API Endpoints
- `POST /api/expenses` - Add new expense
- `GET /api/expenses` - Retrieve expenses (with optional filters)
- `PUT /api/expenses/{id}` - Update existing expense
- `DELETE /api/expenses/{id}` - Delete expense
- `GET /api/summary` - Get spending summary and analytics

## Sample Input/Output

### Sample Input - Adding an Expense
```json
{
  "amount": 150.00,
  "category": "Food",
  "date": "2024-10-04",
  "note": "Lunch at college canteen"
}
```

### Sample Output - Expense List
json
[
  {
    "id": 1,
    "amount": 150.00,
    "category": "Food",
    "date": "2024-10-04",
    "note": "Lunch at college canteen"
  },
  {
    "id": 2,
    "amount": 50.00,
    "category": "Transport",
    "date": "2024-10-04",
    "note": "Bus fare to college"
  }
]


### Sample Output - Summary
json
{
  "total": 1250.00,
  "count": 8,
  "by_category": {
    "Food": 600.00,
    "Transport": 300.00,
    "Books": 350.00
  },
  "by_month": {
    "2024-10": 1250.00
  }
}


### User Interface Examples

Adding Expense:
- Amount: ₹150
- Category: Food & Snacks
- Date: 2024-10-04
- Note: Lunch at college canteen

*Filter Options:*
- Category Filter: All Categories / Food & Snacks / Transport etc.
- Date Range: From: 2024-10-01 To: 2024-10-31

*Summary Display:*
- Total Spent: ₹1,250
- Total Expenses: 8 transactions
- Top Category: Food & Snacks (₹600)

# File Structure
student-budget-tracker/
├── app.py              # Flask backend server
├── templates/
│   └── index.html      # Frontend interface
├── static/             # CSS/JS assets (if any)
└── README.md          # This file



*Built for students, by students. Simple expense tracking without the complexity.*
