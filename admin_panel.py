"""
Premium Admin Panel for HR Analytics
"""
import streamlit as st
import pandas as pd
import sqlite3
import os
from database import HRDatabase
from utils import load_custom_css
from utils.export_utils import export_to_excel, export_to_pdf

def admin_panel():
    """Render premium admin panel"""
    
    # Load premium CSS
    css = load_custom_css()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    
    # Check authentication
    if not st.session_state.get('admin_authenticated', False):
        st.markdown("""
        <div class="unlock-container">
            <div class="unlock-card">
                <h2 style="text-align: center; color: #1e293b; margin-bottom: 1rem;">🔒 Access Denied</h2>
                <p style="text-align: center; color: #64748b;">
                    Please login to access the Admin Panel.<br>
                    Type "open" in the sidebar to access the login page.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Premium Header
    st.markdown("""
    <div class="premium-header">
        <h1>🏢 HR Analytics - Admin Panel</h1>
        <p>Manage employee data, perform CRUD operations, and bulk uploads</p>
    </div>
    """, unsafe_allow_html=True)
    
    db = HRDatabase()
    
    # Sidebar navigation
    st.sidebar.markdown("### 📋 Navigation")
    menu = st.sidebar.radio(
        "Select Action",
        ["View Employees", "Add Employee", "Edit Employee", "Delete Employee", "Bulk Upload"],
        label_visibility="visible"
    )
    
    if menu == "View Employees":
        st.markdown("### 👥 Employee Database")
        
        df = db.get_all_employees()
        
        if len(df) == 0:
            st.warning("⚠️ No employees found in database. Add employees to get started.")
        else:
            # Display metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-icon">👥</div>
                    <div class="kpi-value">{len(df):,}</div>
                    <div class="kpi-label">Total Employees</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                attrition_count = df['attrition'].value_counts().get('Yes', 0)
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-icon">⚠️</div>
                    <div class="kpi-value">{attrition_count}</div>
                    <div class="kpi-label">Attrition Count</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                attrition_rate = (attrition_count / len(df) * 100) if len(df) > 0 else 0
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-icon">📉</div>
                    <div class="kpi-value">{attrition_rate:.1f}%</div>
                    <div class="kpi-label">Attrition Rate</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Search and Filter Section
            st.markdown('<div class="filter-panel">', unsafe_allow_html=True)
            st.markdown("#### 🔍 Search & Filter")
            
            col_search1, col_search2, col_search3 = st.columns(3)
            
            with col_search1:
                search_text = st.text_input(
                    "🔎 Search (Name, Department, Job Role, etc.)",
                    key="search_employees",
                    placeholder="Type to search..."
                )
            
            with col_search2:
                filter_department = st.multiselect(
                    "Department",
                    options=df['department'].unique().tolist() if 'department' in df.columns else [],
                    default=[],
                    key="filter_dept_view"
                )
            
            with col_search3:
                filter_attrition = st.multiselect(
                    "Attrition Status",
                    options=['Yes', 'No'],
                    default=[],
                    key="filter_attrition_view"
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Apply filters
            filtered_df = df.copy()
            
            if search_text:
                # Search across multiple columns
                mask = pd.Series([False] * len(filtered_df))
                searchable_cols = ['department', 'job_role', 'gender', 'education', 'education_field', 'marital_status']
                for col in searchable_cols:
                    if col in filtered_df.columns:
                        mask |= filtered_df[col].astype(str).str.contains(search_text, case=False, na=False)
                filtered_df = filtered_df[mask]
            
            if filter_department:
                filtered_df = filtered_df[filtered_df['department'].isin(filter_department)]
            
            if filter_attrition:
                filtered_df = filtered_df[filtered_df['attrition'].isin(filter_attrition)]
            
            st.markdown(f"**Showing {len(filtered_df)} of {len(df)} employees**")
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Data table with premium styling
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.dataframe(
                filtered_df,
                use_container_width=True,
                height=400
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Export buttons
            st.markdown("#### 📥 Export Data")
            export_col1, export_col2, export_col3 = st.columns(3)
            
            with export_col1:
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="📄 Download as CSV",
                    data=csv,
                    file_name="employees_data.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with export_col2:
                try:
                    excel_data = export_to_excel(filtered_df)
                    st.download_button(
                        label="📊 Download as Excel",
                        data=excel_data,
                        file_name="employees_data.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Excel export error: {str(e)}")
            
            with export_col3:
                try:
                    pdf_data = export_to_pdf(filtered_df, title="HR Employee Database Report")
                    st.download_button(
                        label="📑 Download as PDF",
                        data=pdf_data,
                        file_name="employees_report.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"PDF export error: {str(e)}")
    
    elif menu == "Add Employee":
        st.markdown("### ➕ Add New Employee")
        
        with st.form("add_employee_form", clear_on_submit=True):
            st.markdown('<div class="filter-panel">', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Personal Information")
                age = st.number_input("Age", min_value=18, max_value=65, value=30, key="add_age")
                gender = st.selectbox("Gender", ["Male", "Female"], key="add_gender")
                marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced"], key="add_marital")
                education = st.selectbox("Education", 
                                       ["Below College", "College", "Bachelor", "Master", "Doctor"], key="add_education")
                education_field = st.selectbox("Education Field", 
                                            ["Life Sciences", "Medical", "Marketing", "Technical Degree", "Other"], key="add_edu_field")
            
            with col2:
                st.markdown("#### Work Information")
                department = st.selectbox("Department", 
                                        ["Sales", "Research & Development", "Human Resources"], key="add_dept")
                job_role = st.selectbox("Job Role", 
                                      ["Sales Executive", "Research Scientist", "Laboratory Technician", 
                                       "Manufacturing Director", "Healthcare Representative"], key="add_role")
                monthly_income = st.number_input("Monthly Income", min_value=1000, max_value=20000, value=5000, key="add_income")
                num_companies_worked = st.number_input("Companies Worked", min_value=0, max_value=15, value=2, key="add_companies")
                total_working_years = st.number_input("Total Working Years", min_value=0, max_value=40, value=5, key="add_total_years")
            
            col3, col4 = st.columns(2)
            with col3:
                st.markdown("#### Company Details")
                training_times_last_year = st.number_input("Training Times Last Year", min_value=0, max_value=6, value=2, key="add_training")
                years_at_company = st.number_input("Years at Company", min_value=0, max_value=30, value=3, key="add_years_company")
                years_since_last_promotion = st.number_input("Years Since Last Promotion", min_value=0, max_value=15, value=1, key="add_promotion")
            
            with col4:
                st.markdown("#### Status")
                years_with_curr_manager = st.number_input("Years with Current Manager", min_value=0, max_value=15, value=2, key="add_manager_years")
                overtime = st.selectbox("Overtime", ["Yes", "No"], key="add_overtime")
                attrition = st.selectbox("Attrition", ["Yes", "No"], key="add_attrition")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            submitted = st.form_submit_button("➕ Add Employee", use_container_width=True, type="primary")
            
            if submitted:
                try:
                    employee_data = {
                        'age': age,
                        'department': department,
                        'education': education,
                        'education_field': education_field,
                        'gender': gender,
                        'job_role': job_role,
                        'marital_status': marital_status,
                        'monthly_income': monthly_income,
                        'num_companies_worked': num_companies_worked,
                        'total_working_years': total_working_years,
                        'training_times_last_year': training_times_last_year,
                        'years_at_company': years_at_company,
                        'years_since_last_promotion': years_since_last_promotion,
                        'years_with_curr_manager': years_with_curr_manager,
                        'overtime': overtime,
                        'attrition': attrition
                    }
                    
                    employee_id = db.add_employee(employee_data)
                    st.success(f"✅ Employee added successfully! ID: {employee_id}")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Error adding employee: {str(e)}")
    
    elif menu == "Edit Employee":
        st.markdown("### ✏️ Edit Employee")
        
        df = db.get_all_employees()
        if len(df) == 0:
            st.warning("⚠️ No employees found in database")
            return
        
        employee_ids = df['id'].tolist()
        selected_id = st.selectbox("Select Employee ID", employee_ids, key="edit_select")
        
        if selected_id:
            employee_data = df[df['id'] == selected_id].iloc[0]
            
            with st.form("edit_employee_form"):
                st.markdown('<div class="filter-panel">', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    age = st.number_input("Age", value=int(employee_data['age']), key="edit_age")
                    department = st.selectbox("Department", 
                                            ["Sales", "Research & Development", "Human Resources"],
                                            index=["Sales", "Research & Development", "Human Resources"].index(employee_data['department']) 
                                            if employee_data['department'] in ["Sales", "Research & Development", "Human Resources"] else 0,
                                            key="edit_dept")
                    monthly_income = st.number_input("Monthly Income", value=float(employee_data['monthly_income']), key="edit_income")
                    attrition = st.selectbox("Attrition", ["Yes", "No"], 
                                           index=0 if employee_data['attrition'] == 'Yes' else 1, key="edit_attrition")
                
                with col2:
                    years_at_company = st.number_input("Years at Company", value=int(employee_data['years_at_company']), key="edit_years")
                    training_times_last_year = st.number_input("Training Times", value=int(employee_data['training_times_last_year']), key="edit_training")
                    overtime = st.selectbox("Overtime", ["Yes", "No"],
                                          index=0 if employee_data['overtime'] == 'Yes' else 1, key="edit_overtime")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                submitted = st.form_submit_button("💾 Update Employee", use_container_width=True, type="primary")
                
                if submitted:
                    try:
                        update_data = {
                            'age': age,
                            'department': department,
                            'monthly_income': monthly_income,
                            'attrition': attrition,
                            'years_at_company': years_at_company,
                            'training_times_last_year': training_times_last_year,
                            'overtime': overtime
                        }
                        
                        db.update_employee(selected_id, update_data)
                        st.success("✅ Employee updated successfully!")
                        st.balloons()
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error updating employee: {str(e)}")
    
    elif menu == "Delete Employee":
        st.markdown("### 🗑️ Delete Employee")
        
        df = db.get_all_employees()
        if len(df) == 0:
            st.warning("⚠️ No employees found in database")
            return
        
        employee_options = [f"ID: {row['id']} - {row['job_role']} ({row['department']})" for _, row in df.iterrows()]
        
        selected_employee = st.selectbox("Select Employee to Delete", employee_options, key="delete_select")
        
        if selected_employee:
            st.warning("⚠️ This action cannot be undone!")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("🗑️ Confirm Delete", use_container_width=True, type="primary"):
                    try:
                        selected_id = int(selected_employee.split(" - ")[0].replace("ID: ", ""))
                        db.delete_employee(selected_id)
                        st.success("✅ Employee deleted successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error deleting employee: {str(e)}")
            
            with col2:
                if st.button("❌ Cancel", use_container_width=True):
                    st.rerun()
    
    elif menu == "Bulk Upload":
        st.markdown("### 📤 Bulk Upload CSV/Excel")
        
        st.info("💡 Upload a CSV or Excel file with employee data. The file should contain columns matching the employee schema.")
        
        # File uploader with multiple formats
        uploaded_file = st.file_uploader(
            "Choose CSV or Excel file", 
            type=['csv', 'xlsx', 'xls'], 
            key="bulk_upload",
            help="Supported formats: CSV, Excel (.xlsx, .xls)"
        )
        
        if uploaded_file is not None:
            try:
                # Read file based on extension
                file_extension = uploaded_file.name.split('.')[-1].lower()
                
                if file_extension == 'csv':
                    preview_df = pd.read_csv(uploaded_file)
                elif file_extension in ['xlsx', 'xls']:
                    preview_df = pd.read_excel(uploaded_file)
                else:
                    st.error("❌ Unsupported file format. Please upload CSV or Excel file.")
                    return
                
                st.markdown("#### 📋 Data Preview")
                st.markdown(f"**Total rows in file:** {len(preview_df)}")
                st.dataframe(preview_df.head(10), use_container_width=True)
                
                # Column mapping check
                required_columns = ['age', 'department', 'gender', 'job_role', 'monthly_income', 'attrition']
                missing_columns = [col for col in required_columns if col not in preview_df.columns]
                
                if missing_columns:
                    st.warning(f"⚠️ Missing recommended columns: {', '.join(missing_columns)}")
                    st.info("💡 The upload will proceed, but missing columns will be set to default values.")
                else:
                    st.success("✅ All recommended columns found!")
                
                # Upload options
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col1:
                    if st.button("📥 Upload Data", use_container_width=True, type="primary"):
                        try:
                            # Save uploaded file temporarily
                            import tempfile
                            
                            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as tmp_file:
                                tmp_file.write(uploaded_file.getvalue())
                                tmp_path = tmp_file.name
                            
                            # Upload to database
                            if file_extension == 'csv':
                                records_added = db.bulk_upload(tmp_path)
                            else:
                                # For Excel, read and convert to CSV format
                                excel_df = pd.read_excel(tmp_path)
                                records_added = len(excel_df)
                                conn = db.db_path
                                excel_df.to_sql('employees', sqlite3.connect(conn), if_exists='append', index=False)
                            
                            # Clean up temp file
                            os.unlink(tmp_path)
                            
                            st.success(f"✅ Successfully uploaded {records_added} records!")
                            st.balloons()
                            st.rerun()
                        except Exception as upload_error:
                            st.error(f"❌ Error uploading file: {str(upload_error)}")
                            if os.path.exists(tmp_path):
                                os.unlink(tmp_path)
                
                with col2:
                    if st.button("🔄 Preview Again", use_container_width=True):
                        st.rerun()
                
                with col3:
                    if st.button("❌ Cancel", use_container_width=True):
                        st.rerun()
                        
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
                st.info("💡 Please ensure your file has the correct format. For CSV, use comma-separated values. For Excel, ensure the first sheet contains the data.")
                st.code("""
Expected columns (recommended):
- age, department, gender, job_role, monthly_income, attrition
- education, education_field, marital_status
- years_at_company, training_times_last_year
- overtime, num_companies_worked, total_working_years
                """)
