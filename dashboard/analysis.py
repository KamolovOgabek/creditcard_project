import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import os
from django.conf import settings

# Global matplotlib style for professional, clean look
plt.style.use('default')
sns.set_theme(style="whitegrid", palette="muted")
matplotlib.rcParams['axes.spines.top'] = False
matplotlib.rcParams['axes.spines.right'] = False
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Inter', 'Arial']
matplotlib.rcParams['axes.labelsize'] = 11
matplotlib.rcParams['xtick.labelsize'] = 10
matplotlib.rcParams['ytick.labelsize'] = 10

def load_data(file_path=None):
    """
    To'g'ridan-to'g'ri haqiqiy BankChurners.csv faylini yuklash.
    file_path berilmasa, default yo'ldan qidiradi.
    """
    if file_path is None:
        file_path = os.path.join(settings.BASE_DIR, 'dashboard', 'data', 'BankChurners.csv')
    if not os.path.exists(file_path):
        return None
    try:
        df = pd.read_csv(file_path)
        df = df.iloc[:, :21]
        return df
    except:
        return None

def _get_image():
    """Plotni base64 rasmga aylantirish"""
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

def get_dashboard_analysis(df):
    """Bosh vizual dashboard uchun KPI va asisiy grafiklar"""
    total_customers = len(df)
    attrited_count = len(df[df['Attrition_Flag'] == 'Attrited Customer'])
    churn_rate = (attrited_count / total_customers) * 100
    avg_age = df['Customer_Age'].mean()
    
    kpi_stats = {
        'total_customers': f"{total_customers:,}",
        'churn_rate': f"{churn_rate:.1f}%",
        'active_customers': f"{total_customers - attrited_count:,}",
        'avg_age': f"{avg_age:.1f}"
    }
    
    charts = {}
    
    # Chart 1: Attrition Donut
    plt.figure(figsize=(6, 4))
    counts = df['Attrition_Flag'].value_counts()
    plt.pie(counts, labels=counts.index, autopct='%1.1f%%', colors=['#2563eb', '#ef4444'], startangle=90, wedgeprops=dict(width=0.4))
    plt.title('Mijozlar Holati', pad=10)
    charts['attrition'] = _get_image()
    
    # Chart 2: Age Distribution
    plt.figure(figsize=(8, 4))
    sns.histplot(data=df, x='Customer_Age', bins=30, hue='Attrition_Flag', multiple="stack", palette=['#2563eb', '#ef4444'])
    plt.title('Mijozlar Yoshi va Qochish (Churn) Ta\'siri')
    plt.xlabel('Yosh')
    plt.ylabel('Mijozlar Soni')
    charts['age_dist'] = _get_image()
    
    # Chart 3: Income Category
    plt.figure(figsize=(8, 4))
    inc_order = ['Less than $40K', '$40K - $60K', '$60K - $80K', '$80K - $120K', '$120K +', 'Unknown']
    sns.countplot(data=df, y='Income_Category', order=inc_order, hue='Attrition_Flag', palette=['#2563eb', '#ef4444'])
    plt.title('Daromad Toifasi Bo\'yicha Ta\'qsimot')
    plt.xlabel('Mijozlar Soni')
    plt.ylabel('Daromad Toifasi')
    charts['income'] = _get_image()
    
    return kpi_stats, charts

def get_spending_analysis(df):
    """Xarajatlar tahlili: Total_Trans_Amt va Total_Trans_Ct"""
    total_amt = df['Total_Trans_Amt'].sum()
    avg_amt = df['Total_Trans_Amt'].mean()
    avg_ct = df['Total_Trans_Ct'].mean()
    
    stats = {
        'total_amount': f"${total_amt:,.0f}",
        'avg_amount': f"${avg_amt:,.2f}",
        'avg_count': f"{avg_ct:.1f}",
        'max_amount': f"${df['Total_Trans_Amt'].max():,.0f}"
    }
    
    charts = {}
    
    # Chart 1: Transaction Amount vs Count (Scatter)
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x='Total_Trans_Ct', y='Total_Trans_Amt', hue='Attrition_Flag', palette=['#2563eb', '#ef4444'], alpha=0.6)
    plt.title('Tranzaksiyalar Soni va Summasi O\'rtasidagi Bog\'liqlik')
    plt.xlabel('Tranzaksiyalar Soni (Yil davomida)')
    plt.ylabel('Tranzaksiyalar Summasi ($)')
    charts['scatter'] = _get_image()
    
    # Chart 2: Spending by Education
    plt.figure(figsize=(8, 4))
    sns.boxplot(data=df, x='Total_Trans_Amt', y='Education_Level', palette='Blues')
    plt.title('Ta\'lim Darajasiga Ko\'ra Xarajatlar Taqsimoti')
    plt.xlabel('Tranzaksiyalar Summasi ($)')
    plt.ylabel('Ta\'lim Darajasi')
    charts['education'] = _get_image()
    
    return stats, charts

def get_balance_analysis(df):
    """Balans va Kredit Limitlari tahlili: Credit_Limit va Total_Revolving_Bal"""
    avg_limit = df['Credit_Limit'].mean()
    avg_bal = df['Total_Revolving_Bal'].mean()
    avg_util = df['Avg_Utilization_Ratio'].mean() * 100
    
    stats = {
        'avg_credit_limit': f"${avg_limit:,.0f}",
        'avg_revolving_bal': f"${avg_bal:,.0f}",
        'avg_utilization': f"{avg_util:.1f}%",
        'max_credit_limit': f"${df['Credit_Limit'].max():,.0f}"
    }
    
    charts = {}
    
    # Chart 1: Credit Limit Distribution
    plt.figure(figsize=(8, 4))
    sns.histplot(df['Credit_Limit'], bins=40, color='#0ea5e9')
    plt.title('Kredit Limitlari Taqsimoti')
    plt.xlabel('Kredit Limiti ($)')
    plt.ylabel('Mijozlar Soni')
    charts['limit_dist'] = _get_image()
    
    # Chart 2: Limit vs Revolving Balance
    plt.figure(figsize=(8, 4))
    sns.jointplot(data=df, x='Credit_Limit', y='Total_Revolving_Bal', kind="hex", color="#2563eb")
    plt.subplots_adjust(top=0.9)
    plt.suptitle('Kredit Limiti va Aylanma Balans Zichligi', fontsize=12)
    charts['joint'] = _get_image()
    
    return stats, charts
