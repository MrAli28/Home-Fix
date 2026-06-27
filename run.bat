@echo off
echo ======================================
echo   HomeFix - Starting Development Server
echo ======================================

cd homeservices

echo [1/3] Running migrations...
..\venv\Scripts\python.exe manage.py migrate --noinput 2>nul || ..\.venv\Scripts\python.exe manage.py migrate --noinput

echo [2/3] Seeding database...
..\venv\Scripts\python.exe seed_db.py 2>nul || ..\.venv\Scripts\python.exe seed_db.py

echo [3/3] Starting server...
echo.
echo  Open: http://localhost:8000
echo  Admin: http://localhost:8000/login/
echo  Username: admin  Password: KazimAli31
echo.
..\venv\Scripts\python.exe manage.py runserver 2>nul || ..\.venv\Scripts\python.exe manage.py runserver
