# 🔧 Setup Instructions

## Issue: Python 3.13 Compatibility

Python 3.13 is very new and some packages may not have full support yet. If you encounter installation errors, please follow these solutions:

## Solution 1: Fix pip and Install (Recommended First Step)

```bash
# Fix pip installation
python -m ensurepip --upgrade
python -m pip install --upgrade pip setuptools wheel

# Try installing requirements
python -m pip install -r requirements.txt
```

## Solution 2: Use Python 3.11 or 3.12 (Most Reliable)

If Solution 1 doesn't work, Python 3.11 or 3.12 have better package support:

### Option A: Create Virtual Environment with Python 3.11/3.12

1. **Download Python 3.11 or 3.12** from [python.org](https://www.python.org/downloads/)
2. **Create virtual environment:**
   ```bash
   # If you have Python 3.11/3.12 installed as py -3.11 or py -3.12
   py -3.11 -m venv hr_analytics_env
   
   # Or if installed as python3.11
   python3.11 -m venv hr_analytics_env
   ```

3. **Activate virtual environment:**
   ```bash
   # Windows
   hr_analytics_env\Scripts\activate
   
   # Mac/Linux
   source hr_analytics_env/bin/activate
   ```

4. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

### Option B: Use Conda (Alternative)

```bash
# Create conda environment with Python 3.11
conda create -n hr_analytics python=3.11
conda activate hr_analytics
pip install -r requirements.txt
```

## Solution 3: Install Packages Individually

If bulk installation fails, try installing one by one:

```bash
python -m pip install streamlit
python -m pip install pandas
python -m pip install numpy
python -m pip install matplotlib
python -m pip install seaborn
python -m pip install plotly
python -m pip install scikit-learn
```

## Solution 4: Use Latest Package Versions (No Version Pinning)

If specific versions fail, try installing without version constraints:

```bash
python -m pip install streamlit pandas numpy matplotlib seaborn plotly scikit-learn
```

## After Successful Installation

Once packages are installed, run the application:

```bash
# Option 1: Using run.py
python -m streamlit run run.py

# Option 2: Direct
python -m streamlit run main_app.py
```

## Verify Installation

Check if Streamlit is installed:

```bash
python -m streamlit --version
```

## Troubleshooting

### Error: "streamlit is not recognized"
- Make sure you're in the activated virtual environment (if using one)
- Try: `python -m streamlit run run.py` instead of `streamlit run run.py`

### Error: "No module named streamlit"
- Verify installation: `python -m pip list | findstr streamlit` (Windows) or `pip list | grep streamlit` (Mac/Linux)
- Reinstall: `python -m pip install --force-reinstall streamlit`

### Error: Package build failures
- Upgrade pip: `python -m pip install --upgrade pip`
- Install build tools: `python -m pip install --upgrade setuptools wheel`
- Consider using Python 3.11 or 3.12 instead

## Need Help?

If none of these solutions work, please share:
1. Your Python version: `python --version`
2. Your pip version: `python -m pip --version`
3. The full error message you're seeing

