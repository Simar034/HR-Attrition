import sqlite3
import pandas as pd
import os

class HRDatabase:
    def __init__(self, db_path="data/database.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with employee table"""
        os.makedirs("data", exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                age INTEGER,
                department TEXT,
                education TEXT,
                education_field TEXT,
                gender TEXT,
                job_role TEXT,
                marital_status TEXT,
                monthly_income REAL,
                num_companies_worked INTEGER,
                total_working_years INTEGER,
                training_times_last_year INTEGER,
                years_at_company INTEGER,
                years_since_last_promotion INTEGER,
                years_with_curr_manager INTEGER,
                overtime TEXT,
                attrition TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Insert sample data if empty
        self.insert_sample_data()
    
    def insert_sample_data(self):
        """Insert sample data if table is empty"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM employees")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Generate sample data if CSV doesn't exist
            if not os.path.exists("data/sample_hr_data.csv"):
                try:
                    from utils.data_loader import generate_sample_data
                    generate_sample_data()
                except Exception as e:
                    print(f"Could not generate sample data: {e}")
            
            # Load sample data if it exists
            if os.path.exists("data/sample_hr_data.csv"):
                sample_df = pd.read_csv("data/sample_hr_data.csv")
                sample_df.to_sql('employees', conn, if_exists='append', index=False)
                print(f"Inserted {len(sample_df)} sample records")
        
        conn.close()
    
    def add_employee(self, employee_data):
        """Add single employee record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        columns = ', '.join(employee_data.keys())
        placeholders = ', '.join(['?' for _ in employee_data])
        
        cursor.execute(f'''
            INSERT INTO employees ({columns})
            VALUES ({placeholders})
        ''', list(employee_data.values()))
        
        conn.commit()
        employee_id = cursor.lastrowid
        conn.close()
        return employee_id
    
    def get_all_employees(self):
        """Get all employee records"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM employees", conn)
        conn.close()
        return df
    
    def update_employee(self, employee_id, update_data):
        """Update employee record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        set_clause = ', '.join([f"{key} = ?" for key in update_data.keys()])
        
        cursor.execute(f'''
            UPDATE employees 
            SET {set_clause}
            WHERE id = ?
        ''', list(update_data.values()) + [employee_id])
        
        conn.commit()
        conn.close()
    
    def delete_employee(self, employee_id):
        """Delete employee record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM employees WHERE id = ?', (employee_id,))
        conn.commit()
        conn.close()
    
    def bulk_upload(self, csv_file):
        """Bulk upload from CSV"""
        df = pd.read_csv(csv_file)
        conn = sqlite3.connect(self.db_path)
        df.to_sql('employees', conn, if_exists='append', index=False)
        conn.close()
        return len(df)

