import os
import json
import pandas as pd
import numpy as np
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse


def get_user_data_path(user):
    return os.path.join(settings.MEDIA_ROOT, f'user_{user.id}', 'BankChurners.csv')


def load_user_data(user):
    path = get_user_data_path(user)
    if not os.path.exists(path):
        return None
    try:
        df = pd.read_csv(path).iloc[:, :21]
        return df
    except:
        return None


# ─── AUTH VIEWS ──────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
        messages.error(request, "Login yoki parol noto'g'ri.")
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('upload_file')
    return render(request, 'auth/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# ─── DASHBOARD VIEWS ─────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    df = load_user_data(request.user)
    if df is None:
        return redirect('upload_file')

    total = len(df)
    attrited = int((df['Attrition_Flag'] == 'Attrited Customer').sum())
    active = total - attrited

    # Attrition pie
    attrition_data = {
        'labels': ['Faol Mijozlar', 'Ketgan Mijozlar'],
        'values': [active, attrited],
        'colors': ['#2563eb', '#ef4444'],
    }

    # Age histogram
    bins = list(range(20, 80, 5))
    age_counts, _ = np.histogram(df['Customer_Age'], bins=bins)
    age_labels = [f"{b}-{b+5}" for b in bins[:-1]]

    # Income bar
    inc_order = ['Less than $40K', '$40K - $60K', '$60K - $80K', '$80K - $120K', '$120K +', 'Unknown']
    inc_counts = [int(df[df['Income_Category'] == c].shape[0]) for c in inc_order]

    context = {
        'page_title': "Umumiy Vizual Ko'rsatkichlar",
        'active_page': 'dashboard',
        'user': request.user,
        # KPI
        'total_customers': f"{total:,}",
        'active_customers': f"{active:,}",
        'churn_rate': f"{attrited/total*100:.1f}%",
        'avg_age': f"{df['Customer_Age'].mean():.1f}",
        # Chart data as JSON
        'attrition_json': json.dumps(attrition_data),
        'age_labels': json.dumps(age_labels),
        'age_values': json.dumps(age_counts.tolist()),
        'income_labels': json.dumps(inc_order),
        'income_values': json.dumps(inc_counts),
    }
    return render(request, 'dashboard.html', context)


@login_required
def spending(request):
    df = load_user_data(request.user)
    if df is None:
        return redirect('upload_file')

    total_amt = float(df['Total_Trans_Amt'].sum())
    avg_amt = float(df['Total_Trans_Amt'].mean())
    avg_ct = float(df['Total_Trans_Ct'].mean())
    max_amt = float(df['Total_Trans_Amt'].max())

    # Scatter: group by total_trans_ct buckets
    df_sorted = df.sort_values('Total_Trans_Ct')
    scatter_data = {
        'existing': {
            'x': df[df['Attrition_Flag'] == 'Existing Customer']['Total_Trans_Ct'].tolist()[:300],
            'y': df[df['Attrition_Flag'] == 'Existing Customer']['Total_Trans_Amt'].tolist()[:300],
        },
        'attrited': {
            'x': df[df['Attrition_Flag'] == 'Attrited Customer']['Total_Trans_Ct'].tolist()[:200],
            'y': df[df['Attrition_Flag'] == 'Attrited Customer']['Total_Trans_Amt'].tolist()[:200],
        }
    }

    # Avg spend by education
    edu_levels = ['High School', 'Graduate', 'Uneducated', 'Unknown', 'College', 'Post-Graduate', 'Doctorate']
    edu_avgs = []
    for lvl in edu_levels:
        sub = df[df['Education_Level'] == lvl]['Total_Trans_Amt']
        edu_avgs.append(round(float(sub.mean()), 2) if len(sub) else 0)

    context = {
        'page_title': 'Mijozlar Xarajatlari Tahlili',
        'active_page': 'spending',
        'user': request.user,
        'total_amount': f"${total_amt:,.0f}",
        'avg_amount': f"${avg_amt:,.2f}",
        'avg_count': f"{avg_ct:.1f}",
        'max_amount': f"${max_amt:,.0f}",
        'scatter_json': json.dumps(scatter_data),
        'edu_labels': json.dumps(edu_levels),
        'edu_values': json.dumps(edu_avgs),
    }
    return render(request, 'spending.html', context)


@login_required
def balance(request):
    df = load_user_data(request.user)
    if df is None:
        return redirect('upload_file')

    avg_limit = float(df['Credit_Limit'].mean())
    avg_bal = float(df['Total_Revolving_Bal'].mean())
    avg_util = float(df['Avg_Utilization_Ratio'].mean() * 100)
    max_limit = float(df['Credit_Limit'].max())

    # Credit limit histogram
    bins = list(range(0, int(max_limit) + 5000, 5000))
    limit_counts, limit_edges = np.histogram(df['Credit_Limit'], bins=bins)
    limit_labels = [f"${b:,}" for b in limit_edges[:-1]]

    # Utilization by card category
    card_cats = df['Card_Category'].unique().tolist()
    card_util = [round(float(df[df['Card_Category'] == c]['Avg_Utilization_Ratio'].mean() * 100), 2)
                 for c in card_cats]

    # Revolving balance distribution
    rev_bins = list(range(0, 2600, 200))
    rev_counts, rev_edges = np.histogram(df['Total_Revolving_Bal'], bins=rev_bins)
    rev_labels = [f"${b}" for b in rev_edges[:-1]]

    context = {
        'page_title': 'Hisob Balansi Statistikasi',
        'active_page': 'balance',
        'user': request.user,
        'avg_credit_limit': f"${avg_limit:,.0f}",
        'avg_revolving_bal': f"${avg_bal:,.0f}",
        'avg_utilization': f"{avg_util:.1f}%",
        'max_credit_limit': f"${max_limit:,.0f}",
        'limit_labels': json.dumps(limit_labels),
        'limit_values': json.dumps(limit_counts.tolist()),
        'card_labels': json.dumps(card_cats),
        'card_util': json.dumps(card_util),
        'rev_labels': json.dumps(rev_labels),
        'rev_values': json.dumps(rev_counts.tolist()),
    }
    return render(request, 'balance.html', context)


@login_required
def customers(request):
    df = load_user_data(request.user)
    if df is None:
        return redirect('upload_file')

    search = request.GET.get('q', '').strip()
    page = int(request.GET.get('page', 1))
    per_page = 50

    # Display subset of columns
    cols = ['CLIENTNUM', 'Attrition_Flag', 'Customer_Age', 'Gender',
            'Education_Level', 'Income_Category', 'Card_Category',
            'Credit_Limit', 'Total_Revolving_Bal', 'Total_Trans_Amt', 'Total_Trans_Ct']
    existing_cols = [c for c in cols if c in df.columns]
    sub = df[existing_cols].copy()

    if search:
        mask = sub.apply(lambda col: col.astype(str).str.contains(search, case=False, na=False)).any(axis=1)
        sub = sub[mask]

    total_rows = len(sub)
    total_pages = max(1, (total_rows + per_page - 1) // per_page)
    page = min(max(page, 1), total_pages)
    start = (page - 1) * per_page
    page_data = sub.iloc[start:start + per_page]

    return render(request, 'customers.html', {
        'page_title': 'Barcha Mijozlar',
        'active_page': 'customers',
        'user': request.user,
        'headers': existing_cols,
        'rows': page_data.values.tolist(),
        'total_rows': total_rows,
        'page': page,
        'total_pages': total_pages,
        'search': search,
        'page_range': range(max(1, page-2), min(total_pages+1, page+3)),
    })


@login_required
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        file_obj = request.FILES['csv_file']
        user_dir = os.path.join(settings.MEDIA_ROOT, f'user_{request.user.id}')
        os.makedirs(user_dir, exist_ok=True)
        file_path = os.path.join(user_dir, 'BankChurners.csv')
        with open(file_path, 'wb+') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)
        messages.success(request, "Fayl muvaffaqiyatli yuklandi!")
        return redirect('dashboard')

    has_data = load_user_data(request.user) is not None
    return render(request, 'upload.html', {
        'page_title': "Ma'lumotlar Yuklash",
        'active_page': 'upload',
        'has_data': has_data,
        'user': request.user,
    })
