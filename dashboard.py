"""
Premium HR Analytics Dashboard
"""
import streamlit as st
import pandas as pd
from database import HRDatabase
from utils import (
    load_custom_css, calculate_metrics, create_attrition_pie_chart,
    create_department_attrition_chart, create_gender_donut_chart,
    create_years_histogram, create_attrition_trend_chart,
    create_correlation_heatmap, create_salary_boxplot, apply_filters
)

def render_dashboard():
    """Render the premium HR Analytics Dashboard"""
    
    # Get dark mode state
    dark_mode = st.session_state.get('dark_mode', False)
    
    # Load custom CSS
    css = load_custom_css()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    
    # Initialize database with auto-refresh
    db = HRDatabase()
    
    # Auto-refresh button
    col_refresh1, col_refresh2 = st.columns([1, 5])
    with col_refresh1:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    # Get fresh data
    df = db.get_all_employees()
    
    # Premium Header
    st.markdown("""
    <div class="premium-header" style="margin-bottom: 1.5rem !important;">
        <h1>🏢 HR Attrition Analytics Dashboard</h1>
        <p>Comprehensive insights into employee retention and organizational health</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filters Panel
    st.markdown('<div class="filter-panel" style="margin-top: 0 !important;">', unsafe_allow_html=True)
    st.markdown('<div class="filter-title">🔍 Filters</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        departments = st.multiselect(
            "Department",
            options=df['department'].unique().tolist() if len(df) > 0 else [],
            default=df['department'].unique().tolist() if len(df) > 0 else [],
            key="filter_department"
        )
        
        genders = st.multiselect(
            "Gender",
            options=df['gender'].unique().tolist() if len(df) > 0 else [],
            default=df['gender'].unique().tolist() if len(df) > 0 else [],
            key="filter_gender"
        )
    
    with col2:
        job_roles = st.multiselect(
            "Job Role",
            options=df['job_role'].unique().tolist() if len(df) > 0 else [],
            default=df['job_role'].unique().tolist() if len(df) > 0 else [],
            key="filter_job_role"
        )
        
        education_levels = st.multiselect(
            "Education",
            options=df['education'].unique().tolist() if len(df) > 0 else [],
            default=df['education'].unique().tolist() if len(df) > 0 else [],
            key="filter_education"
        )
    
    with col3:
        if len(df) > 0:
            age_range = st.slider(
                "Age Range",
                min_value=int(df['age'].min()),
                max_value=int(df['age'].max()),
                value=(int(df['age'].min()), int(df['age'].max())),
                key="filter_age"
            )
            
            salary_range = st.slider(
                "Salary Range ($)",
                min_value=int(df['monthly_income'].min()),
                max_value=int(df['monthly_income'].max()),
                value=(int(df['monthly_income'].min()), int(df['monthly_income'].max())),
                key="filter_salary"
            )
        else:
            age_range = (18, 65)
            salary_range = (1000, 20000)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Apply filters
    filters = {
        'departments': departments,
        'genders': genders,
        'job_roles': job_roles,
        'education_levels': education_levels,
        'age_range': age_range,
        'salary_range': salary_range
    }
    
    filtered_df = apply_filters(df, filters) if len(df) > 0 else df
    
    # KPI Cards
    metrics = calculate_metrics(filtered_df)
    
    st.markdown('<h3 style="color: #1e293b !important; margin-bottom: 1rem;">📊 Key Performance Indicators</h3>', unsafe_allow_html=True)
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5, kpi_col6 = st.columns(6)
    
    with kpi_col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">👥</div>
            <div class="kpi-value">{metrics['total_employees']:,}</div>
            <div class="kpi-label">Total Employees</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">⚠️</div>
            <div class="kpi-value">{metrics['attrition_count']}</div>
            <div class="kpi-label">Attrition Count</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">📉</div>
            <div class="kpi-value">{metrics['attrition_rate']:.1f}%</div>
            <div class="kpi-label">Attrition Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">⏱️</div>
            <div class="kpi-value">{metrics['avg_years_at_company']:.1f}</div>
            <div class="kpi-label">Avg Years at Company</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col5:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">💰</div>
            <div class="kpi-value">${metrics['avg_monthly_salary']:,.0f}</div>
            <div class="kpi-label">Avg Monthly Salary</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col6:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🎓</div>
            <div class="kpi-value">{metrics['avg_training_time']:.1f}</div>
            <div class="kpi-label">Avg Training Time</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Section
    st.markdown('<h3 style="color: #1e293b !important; margin-bottom: 1rem;">📈 Analytics & Visualizations</h3>', unsafe_allow_html=True)
    
    if len(filtered_df) == 0:
        st.warning("⚠️ No data available for the selected filters. Please adjust your filter criteria.")
        return
    
    # Row 1: Attrition Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📊 Attrition Distribution</div>', unsafe_allow_html=True)
        fig_pie = create_attrition_pie_chart(filtered_df, dark_mode=dark_mode)
        st.plotly_chart(fig_pie, width='stretch', config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🏢 Attrition by Department</div>', unsafe_allow_html=True)
        fig_dept = create_department_attrition_chart(filtered_df, dark_mode=dark_mode)
        st.plotly_chart(fig_dept, width='stretch', config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 2: Demographics
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">👥 Gender Distribution</div>', unsafe_allow_html=True)
        fig_gender = create_gender_donut_chart(filtered_df, dark_mode=dark_mode)
        st.plotly_chart(fig_gender, width='stretch', config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📅 Years at Company Distribution</div>', unsafe_allow_html=True)
        fig_hist = create_years_histogram(filtered_df, dark_mode=dark_mode)
        st.plotly_chart(fig_hist, width='stretch', config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 3: Trends & Analysis
    col5, col6 = st.columns(2)
    
    with col5:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📈 Attrition Trend</div>', unsafe_allow_html=True)
        fig_trend = create_attrition_trend_chart(filtered_df, dark_mode=dark_mode)
        st.plotly_chart(fig_trend, width='stretch', config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col6:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">💰 Salary by Department</div>', unsafe_allow_html=True)
        fig_box = create_salary_boxplot(filtered_df, dark_mode=dark_mode)
        st.plotly_chart(fig_box, width='stretch', config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 4: Correlation Heatmap
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">🔥 Correlation Analysis</div>', unsafe_allow_html=True)
    fig_heatmap = create_correlation_heatmap(filtered_df, dark_mode=dark_mode)
    st.plotly_chart(fig_heatmap, width='stretch', config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Raw Data Section
    with st.expander("📋 View Raw Data", expanded=False):
        st.dataframe(
            filtered_df,
            width='stretch',
            height=400
        )
        
        # Export buttons
        st.markdown("#### 📥 Export Filtered Data")
        export_col1, export_col2, export_col3 = st.columns(3)
        
        with export_col1:
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📄 Download as CSV",
                data=csv,
                file_name="hr_analytics_data.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with export_col2:
            try:
                from utils.export_utils import export_to_excel
                excel_data = export_to_excel(filtered_df, filename="hr_analytics_data.xlsx")
                st.download_button(
                    label="📊 Download as Excel",
                    data=excel_data,
                    file_name="hr_analytics_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Excel export error: {str(e)}")
        
        with export_col3:
            try:
                from utils.export_utils import export_to_pdf
                pdf_data = export_to_pdf(filtered_df, title="HR Attrition Analytics Dashboard Report")
                st.download_button(
                    label="📑 Download as PDF",
                    data=pdf_data,
                    file_name="hr_analytics_report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"PDF export error: {str(e)}")

