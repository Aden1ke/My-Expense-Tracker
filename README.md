# Expense Tracker

Expense Tracker is a web application designed to help users manage their personal finances effectively. Users can input their expenses manually or upload files (e.g., receipts, bank statements) to track and categorize their monthly spending. The app provides a summary of expenses, helping users stay organized and achieve their financial goals.

## Features

- **Manual Expense Input:** Enter expenses manually with details such as date, description, amount, and category.
- **File Upload Support:** Upload files (Excel, CSV, or PDF) to automatically parse and extract transactions for analysis.
- **Expense Categorization:** Categorize expenses into predefined or custom categories for better organization.
- **Monthly Budget Tracking:** Set a monthly allowance and track your expenses against it.
- **Summary Display:** View a summary of your financial activity, including total spending and category breakdowns.

## Technologies Used

- **Frontend:** HTML5, CSS3, JavaScript
- **Backend:** Python (e.g., Django)
- **Database:** MongoDB or MySQL
- **File Parsing:** Libraries for handling Excel, CSV, and PDF files (e.g., pandas, PyPDF2)

## Installation

### Prerequisites

Ensure you have the following installed on your system:

- Python
- Git
- A database management system (MongoDB or MySQL)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/expense-tracker.git
   cd expense-tracker

   For Python (if applicable):
        pip install -r requirements.txt

   Configure environment variables: Create a .env file with the following details:
            DATABASE_URL=your_database_url
            SECRET_KEY=your_secret_key

    Run the application:

        For Python (if applicable):
            python manage.py runserver

        Open your browser and visit:
                http://localhost:3000
   ```
## How to Use

### Set Up Your Budget:
- **Enter your monthly allowance on the home page.

### Input Expenses:
- **Choose **"Manual Input"** to enter details like date, description, amount, and category.
- **Select **"Upload File"** to upload an Excel, CSV, or PDF file for automatic expense parsing.

### View Summary:
- **Navigate to the summary page to see a breakdown of your expenses by category.
- **Compare your spending against your budget to monitor your financial health.

## Contributing

We welcome contributions! Follow these steps to contribute:

1. **Fork the repository.**
2. **Create a new branch:**
   ```bash
   git checkout -b feature-name
   Make your changes and commit them:
   git commit -m "Added feature X"
   Push to your branch:
   git push origin feature-name
   Open a pull request.
   ```

## Contact

For any questions or suggestions, feel free to reach out:

- **Email:** sarahogunlalu@gmai.com
- **GitHub:** Aden1ke

Start tracking your expenses and take control of your finances today with Expense Tracker!

