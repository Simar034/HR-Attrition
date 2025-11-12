import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from database import HRDatabase

# Page configuration
st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

class HRAnalytics:
    def __init__(self):
        self.db = HRDatabase()
        self.df = self.db.get_all_employees()
    
    def calculate_metrics(self):
        """Calculate key HR metrics"""
        total_employees = len(self.df)
        attrition_count = len(self.df[self.df['attrition'] == 'Yes'])
        attrition_rate = (attrition_count / total_employees) * 100 if total_employees > 0 else 0
        avg_years_at_company = self.df['years_at_company'].mean() if len(self.df) > 0 else 0
        avg_monthly_salary = self.df['monthly_income'].mean() if len(self.df) > 0 else 0
        avg_training_time = self.df['training_times_last_year'].mean() if len(self.df) > 0 else 0
        
        return {
            'total_employees': total_employees,
            'attrition_count': attrition_count,
            'attrition_rate': attrition_rate,
            'avg_years_at_company': avg_years_at_company,
            'avg_monthly_salary': avg_monthly_salary,
            'avg_training_time': avg_training_time
        }
    
    def create_overview_metrics(self):
        """Display overview metrics"""
        st.markdown('<div class="main-header">🏢 HR Attrition Analytics Dashboard</div>', 
                   unsafe_allow_html=True)
        
        metrics = self.calculate_metrics()
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            st.metric("Total Employees", f"{metrics['total_employees']:,}")
        with col2:
            st.metric("Attrition Count", metrics['attrition_count'])
        with col3:
            st.metric("Attrition Rate", f"{metrics['attrition_rate']:.1f}%")
        with col4:
            st.metric("Avg Years at Company", f"{metrics['avg_years_at_company']:.1f}")
        with col5:
            st.metric("Avg Monthly Salary", f"${metrics['avg_monthly_salary']:,.0f}")
        with col6:
            st.metric("Avg Training Time", f"{metrics['avg_training_time']:.1f}")
    
    def create_attrition_charts(self):
        """Create attrition analysis charts"""
        st.header("📊 Attrition Analysis")
        
        if len(self.df) == 0:
            st.warning("No data available for visualization")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart - Attrition vs Active
            attrition_counts = self.df['attrition'].value_counts()
            fig = px.pie(
                values=attrition_counts.values,
                names=attrition_counts.index,
                title="Attrition vs Active Employees",
                color=attrition_counts.index,
                color_discrete_map={'Yes': '#FF6B6B', 'No': '#4ECDC4'}
            )
            st.plotly_chart(fig, width='stretch')
        
        with col2:
            # Bar chart - Attrition by Department
            dept_attrition = self.df[self.df['attrition'] == 'Yes']['department'].value_counts()
            if len(dept_attrition) > 0:
                fig = px.bar(
                    x=dept_attrition.index,
                    y=dept_attrition.values,
                    title="Attrition Count by Department",
                    labels={'x': 'Department', 'y': 'Count'},
                    color=dept_attrition.values,
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig, width='stretch')
            else:
                st.info("No attrition data available")
        
        col3, col4 = st.columns(2)
        
        with col3:
            # Histogram - Years at Company distribution
            fig = px.histogram(
                self.df,
                x='years_at_company',
                title="Distribution of Years at Company",
                nbins=20,
                color_discrete_sequence=['#3366CC']
            )
            st.plotly_chart(fig, width='stretch')
        
        with col4:
            # Donut chart - Gender distribution
            gender_counts = self.df['gender'].value_counts()
            fig = px.pie(
                values=gender_counts.values,
                names=gender_counts.index,
                title="Gender Distribution",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(fig, width='stretch')
    
    def create_salary_analysis(self):
        """Create salary and department analysis"""
        st.header("💰 Salary & Department Insights")
        
        if len(self.df) == 0:
            st.warning("No data available for visualization")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Boxplot - Monthly salary by department
            fig = px.box(
                self.df,
                x='department',
                y='monthly_income',
                title="Monthly Salary by Department",
                color='department',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig, width='stretch')
        
        with col2:
            # Employee count by department and gender
            dept_gender = pd.crosstab(self.df['department'], self.df['gender'])
            fig = px.bar(
                dept_gender,
                title="Employee Count by Department and Gender",
                barmode='group',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig, width='stretch')
    
    def create_trend_analysis(self):
        """Create trend and correlation analysis"""
        st.header("📈 Trends & Correlations")
        
        if len(self.df) == 0:
            st.warning("No data available for visualization")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Line chart - Attrition trend over years
            years_trend = self.df.groupby('years_at_company')['attrition'].apply(
                lambda x: (x == 'Yes').mean() * 100
            ).reset_index()
            years_trend.columns = ['years_at_company', 'attrition_rate']
            
            fig = px.line(
                years_trend,
                x='years_at_company',
                y='attrition_rate',
                title="Attrition Rate by Years at Company",
                labels={'attrition_rate': 'Attrition Rate (%)', 'years_at_company': 'Years at Company'}
            )
            st.plotly_chart(fig, width='stretch')
        
        with col2:
            # Heatmap - Correlation matrix
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                corr_matrix = self.df[numeric_cols].corr()
                
                fig = px.imshow(
                    corr_matrix,
                    title="Correlation Heatmap",
                    aspect="auto",
                    color_continuous_scale="RdBu_r"
                )
                st.plotly_chart(fig, width='stretch')
            else:
                st.info("No numeric columns for correlation")
    
    def create_filters(self):
        """Create interactive filters"""
        st.sidebar.header("🔍 Filters")
        
        if len(self.df) == 0:
            return self.df
        
        departments = st.sidebar.multiselect(
            "Department",
            options=self.df['department'].unique().tolist(),
            default=self.df['department'].unique().tolist()
        )
        
        genders = st.sidebar.multiselect(
            "Gender",
            options=self.df['gender'].unique().tolist(),
            default=self.df['gender'].unique().tolist()
        )
        
        job_roles = st.sidebar.multiselect(
            "Job Role",
            options=self.df['job_role'].unique().tolist(),
            default=self.df['job_role'].unique().tolist()
        )
        
        # Apply filters
        filtered_df = self.df[
            (self.df['department'].isin(departments)) &
            (self.df['gender'].isin(genders)) &
            (self.df['job_role'].isin(job_roles))
        ]
        
        return filtered_df

def main():
    analytics = HRAnalytics()
    
    # Apply filters
    filtered_df = analytics.create_filters()
    analytics.df = filtered_df
    
    # Display all sections
    analytics.create_overview_metrics()
    analytics.create_attrition_charts()
    analytics.create_salary_analysis()
    analytics.create_trend_analysis()
    
    # Show raw data option
    if st.sidebar.checkbox("Show Raw Data"):
        st.header("📋 Raw Data")
        st.dataframe(analytics.df)

if __name__ == "__main__":
    main()

