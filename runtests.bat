@echo off
set PYTHONPATH=%PYTHONPATH%;%CD%\finite_fields
cd tests
python test_polynomial.py
python test_finite_field.py
pause
cd ..