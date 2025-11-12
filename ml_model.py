import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from database import HRDatabase
from utils import load_custom_css
import streamlit as st

class AttritionPredictor:
    def __init__(self):
        self.db = HRDatabase()
        self.df = self.db.get_all_employees()
        self.model = None
        self.feature_importance = None
    
    def preprocess_data(self):
        """Preprocess data for machine learning"""
        if len(self.df) == 0:
            return None
            
        df_ml = self.df.copy()
        
        # Convert categorical variables
        categorical_cols = ['department', 'education', 'education_field', 'gender', 
                          'job_role', 'marital_status', 'overtime']
        
        # Only process columns that exist
        categorical_cols = [col for col in categorical_cols if col in df_ml.columns]
        
        df_ml = pd.get_dummies(df_ml, columns=categorical_cols, drop_first=True)
        
        # Convert target variable
        if 'attrition' in df_ml.columns:
            df_ml['attrition'] = df_ml['attrition'].map({'Yes': 1, 'No': 0})
        
        # Drop non-feature columns
        drop_cols = ['id', 'created_at']
        df_ml = df_ml.drop([col for col in drop_cols if col in df_ml.columns], axis=1)
        
        return df_ml
    
    def train_model(self):
        """Train the attrition prediction model"""
        df_ml = self.preprocess_data()
        
        if df_ml is None or len(df_ml) == 0:
            return None
        
        if 'attrition' not in df_ml.columns:
            return None
        
        # Separate features and target
        X = df_ml.drop('attrition', axis=1)
        y = df_ml['attrition']
        
        # Check if we have enough data
        if len(X) < 10:
            return None
        
        # Handle missing values
        X = X.fillna(X.mean())
        
        # Check if we have any features
        if X.shape[1] == 0:
            return None
        
        # Split data
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.3, random_state=42, stratify=y
            )
        except ValueError:
            # If stratification fails, use regular split
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.3, random_state=42
            )
        
        # Train Random Forest
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        auc_score = roc_auc_score(y_test, y_pred_proba)
        
        # Feature importance
        self.feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return {
            'accuracy': accuracy,
            'auc_score': auc_score,
            'y_test': y_test,
            'y_pred': y_pred,
            'y_pred_proba': y_pred_proba,
            'feature_names': X.columns
        }
    
    def plot_feature_importance(self, top_n=15):
        """Plot feature importance"""
        if self.feature_importance is not None and len(self.feature_importance) > 0:
            top_features = self.feature_importance.head(top_n)
            
            fig = px.bar(
                top_features,
                x='importance',
                y='feature',
                orientation='h',
                title=f"Top {top_n} Features Influencing Attrition",
                labels={'importance': 'Feature Importance', 'feature': ''},
                color='importance',
                color_continuous_scale='Viridis'
            )
            return fig
        return None
    
    def plot_confusion_matrix(self, y_test, y_pred):
        """Plot confusion matrix"""
        cm = confusion_matrix(y_test, y_pred)
        
        fig = px.imshow(
            cm,
            text_auto=True,
            color_continuous_scale='Blues',
            labels=dict(x="Predicted", y="Actual", color="Count"),
            x=['No Attrition', 'Attrition'],
            y=['No Attrition', 'Attrition'],
            title="Confusion Matrix"
        )
        return fig
    
    def plot_roc_curve(self, y_test, y_pred_proba):
        """Plot ROC curve"""
        fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
        auc_score = roc_auc_score(y_test, y_pred_proba)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=fpr, y=tpr, mode='lines', 
                               name=f'ROC Curve (AUC = {auc_score:.3f})'))
        fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', 
                               name='Random Classifier', line=dict(dash='dash')))
        
        fig.update_layout(
            title='ROC Curve',
            xaxis_title='False Positive Rate',
            yaxis_title='True Positive Rate',
            showlegend=True
        )
        return fig

def ml_dashboard():
    # Load premium CSS
    css = load_custom_css()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="premium-header">
        <h1>🤖 Attrition Prediction Model</h1>
        <p>Machine learning-powered attrition prediction using Random Forest</p>
    </div>
    """, unsafe_allow_html=True)
    
    predictor = AttritionPredictor()
    
    if len(predictor.df) == 0:
        st.warning("⚠️ No data available. Please add employee data first.")
        return
    
    if st.button("Train Model"):
        with st.spinner("Training model..."):
            results = predictor.train_model()
        
        if results is None:
            st.error("❌ Unable to train model. Please ensure you have sufficient data with attrition information.")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Model Accuracy", f"{results['accuracy']:.3f}")
        with col2:
            st.metric("AUC Score", f"{results['auc_score']:.3f}")
        
        # Feature Importance
        st.subheader("Feature Importance")
        fig_importance = predictor.plot_feature_importance()
        if fig_importance:
            st.plotly_chart(fig_importance, width='stretch')
        else:
            st.info("Feature importance data not available")
        
        # Confusion Matrix
        st.subheader("Model Performance")
        col3, col4 = st.columns(2)
        
        with col3:
            fig_cm = predictor.plot_confusion_matrix(results['y_test'], results['y_pred'])
            st.plotly_chart(fig_cm, width='stretch')
        
        with col4:
            fig_roc = predictor.plot_roc_curve(results['y_test'], results['y_pred_proba'])
            st.plotly_chart(fig_roc, width='stretch')
        
        # Classification Report
        st.subheader("Classification Report")
        report = classification_report(results['y_test'], results['y_pred'], output_dict=True)
        report_df = pd.DataFrame(report).transpose()
        st.dataframe(report_df)

if __name__ == "__main__":
    ml_dashboard()

