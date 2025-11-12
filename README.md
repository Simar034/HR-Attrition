# 🏢 HR Attrition Analytics Suite

A comprehensive HR analytics application built with Streamlit for analyzing employee attrition, managing HR data, and predicting attrition using machine learning.

## 📋 Features

- **📊 Interactive Dashboard**: Real-time HR metrics with interactive charts and filters
- **👥 Admin Panel**: Complete CRUD operations for employee data management
- **🤖 ML Predictor**: Random Forest model for attrition prediction
- **🔐 Secure Admin Access**: Login system with unlock functionality
- **📈 Multiple Visualizations**: Pie charts, bar charts, heatmaps, correlation matrices
- **💾 SQLite Database**: Persistent data storage with automatic schema creation

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate Sample Data (Optional)

```bash
python generate_sample_data.py
```

This will create `data/sample_hr_data.csv` with 500 sample employee records.

### 3. Run the Application

```bash
streamlit run run.py
```

Or directly:

```bash
streamlit run main_app.py
```

The application will automatically:
- Create the database if it doesn't exist
- Load sample data if the database is empty
- Start the Streamlit server

## 🔐 Admin Access

To access the Admin Panel:

1. **Type 'unlock'** in the sidebar input field (under "🔓 Admin Access")
2. The login page will appear
3. Use the **Autofill** button to auto-populate credentials, or enter manually:
   - **Username**: `simar@gmail.com`
   - **Password**: `12345678`
4. Click **Login** to access the Admin Panel

## 📁 Project Structure

```
hr_attrition_analysis/
│
├── app.py                 # Main analytics dashboard
├── admin_panel.py         # Admin panel with CRUD operations
├── main_app.py           # Main application with navigation
├── ml_model.py           # Machine learning predictor
├── database.py           # Database operations
├── run.py                # Application entry point
├── generate_sample_data.py  # Sample data generator
├── requirements.txt      # Python dependencies
│
├── data/
│   ├── sample_hr_data.csv  # Sample HR data (auto-generated)
│   └── database.db        # SQLite database (auto-created)
│
├── utils/
│   ├── __init__.py
│   └── data_loader.py    # Data loading utilities
│
└── static/
    └── styles.css        # Custom CSS styles
```

## 🎯 Application Modes

### 1. Dashboard
- View key HR metrics (attrition rate, average salary, etc.)
- Interactive charts and visualizations
- Filter by department, gender, job role
- View raw data

### 2. Admin Panel
- **View Employees**: Browse all employee records
- **Add Employee**: Create new employee entries
- **Edit Employee**: Update existing employee data
- **Delete Employee**: Remove employee records
- **Bulk Upload**: Import data from CSV files

### 3. ML Predictor
- Train Random Forest model for attrition prediction
- View feature importance
- Analyze model performance (accuracy, AUC score)
- View confusion matrix and ROC curve

## 📊 Sample Metrics

The dashboard displays:
- Total Employees
- Attrition Count & Rate
- Average Years at Company
- Average Monthly Salary
- Average Training Time

## 🛠️ Technologies Used

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation
- **NumPy**: Numerical computing
- **Plotly**: Interactive visualizations
- **Scikit-learn**: Machine learning
- **SQLite**: Database

## 📝 Notes

- The database is automatically created on first run
- Sample data is loaded automatically if the database is empty
- All employee data is stored in SQLite database
- The ML model requires sufficient data (minimum 10 records recommended)

## 🔧 Troubleshooting

**Issue**: No data showing in dashboard
- **Solution**: Run `python generate_sample_data.py` to create sample data

**Issue**: Cannot access Admin Panel
- **Solution**: Type 'unlock' in the sidebar input field first

**Issue**: ML model training fails
- **Solution**: Ensure you have at least 10 employee records with attrition data

## 📄 License

This project is for educational and demonstration purposes.

