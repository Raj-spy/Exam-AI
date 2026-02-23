@echo off
REM ================================
REM Exam AI Frontend Setup Script
REM ================================

echo.
echo ====================================
echo  Exam AI Frontend Setup
echo ====================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed!
    echo Please download and install Node.js from https://nodejs.org/
    echo Make sure to add Node.js to your PATH during installation.
    pause
    exit /b 1
)

echo [OK] Node.js is installed
node --version
npm --version

echo.
echo [INFO] Installing dependencies...
npm install

if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies!
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Dependencies installed!
echo.
echo Next steps:
echo   npm run dev     - Start development server
echo   npm run build   - Build for production
echo.
pause
