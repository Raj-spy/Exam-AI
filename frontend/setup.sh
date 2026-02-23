#!/bin/bash

# ================================
# Exam AI Frontend Setup Script
# ================================

echo ""
echo "===================================="
echo " Exam AI Frontend Setup"
echo "===================================="
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "[ERROR] Node.js is not installed!"
    echo "Please download and install Node.js from https://nodejs.org/"
    exit 1
fi

echo "[OK] Node.js is installed"
node --version
npm --version

echo ""
echo "[INFO] Installing dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies!"
    exit 1
fi

echo ""
echo "[SUCCESS] Dependencies installed!"
echo ""
echo "Next steps:"
echo "  npm run dev     - Start development server"
echo "  npm run build   - Build for production"
echo ""
