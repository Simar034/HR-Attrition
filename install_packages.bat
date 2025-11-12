@echo off
echo Installing HR Analytics Dependencies...
echo.

echo Step 1: Upgrading pip...
python -m pip install --upgrade pip setuptools wheel
echo.

echo Step 2: Installing packages one by one...
python -m pip install streamlit
python -m pip install pandas
python -m pip install numpy
python -m pip install matplotlib
python -m pip install seaborn
python -m pip install plotly
python -m pip install scikit-learn
echo.

echo Step 3: Verifying installation...
python -c "import streamlit; print('Streamlit installed successfully!')"
echo.

echo Installation complete!
echo.
echo To run the app, use: python -m streamlit run run.py
pause

