# 🚀 Quick Fix for Installation Issues

## The Problem
Python 3.13 is very new and some packages may not have full support yet, causing installation failures.

## ✅ Best Solution: Use Python 3.11 or 3.12

### Step 1: Install Python 3.11 or 3.12
1. Download from: https://www.python.org/downloads/
2. Choose Python 3.11.9 or Python 3.12.x (stable versions)
3. During installation, check "Add Python to PATH"

### Step 2: Create Virtual Environment
Open PowerShell in the project folder and run:

```powershell
# For Python 3.11 (if installed as py -3.11)
py -3.11 -m venv hr_env

# Or if you have python3.11 command
python3.11 -m venv hr_env
```

### Step 3: Activate Virtual Environment
```powershell
hr_env\Scripts\activate
```

### Step 4: Install Requirements
```powershell
pip install -r requirements.txt
```

### Step 5: Run the App
```powershell
python -m streamlit run run.py
```

---

## Alternative: Try Fixing Current Python 3.13 Setup

### Option A: Run the Batch Script
Double-click `install_packages.bat` or run:
```powershell
.\install_packages.bat
```

### Option B: Manual Installation
```powershell
# Fix pip first
python -m ensurepip --upgrade
python -m pip install --upgrade pip setuptools wheel

# Install without version constraints
python -m pip install streamlit pandas numpy matplotlib seaborn plotly scikit-learn
```

### Option C: Use pipx (if available)
```powershell
pipx install streamlit
```

---

## Verify Installation

After installation, verify:
```powershell
python -c "import streamlit; print('Success!')"
```

If successful, run:
```powershell
python -m streamlit run run.py
```

---

## Still Having Issues?

1. **Check Python version**: `python --version`
2. **Check pip version**: `python -m pip --version`
3. **Try Python 3.11/3.12** - This is the most reliable solution

