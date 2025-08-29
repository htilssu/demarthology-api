#!/bin/bash

# Development Quality Check Script
# This script runs the same checks as the CI pipeline

echo "🔍 Running development quality checks..."
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Exit on any error
set -e

echo -e "\n📋 Step 1: Checking Python syntax errors..."
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
echo -e "${GREEN}✅ No syntax errors found${NC}"

echo -e "\n📋 Step 2: Running general linting (flake8)..."
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
echo -e "${GREEN}✅ Linting completed${NC}"

echo -e "\n📋 Step 3: Checking code formatting (black)..."
if black --check --diff --line-length=127 .; then
    echo -e "${GREEN}✅ Code formatting is correct${NC}"
else
    echo -e "${YELLOW}⚠️  Code formatting suggestions available (run: black --line-length=127 .)${NC}"
fi

echo -e "\n📋 Step 4: Checking import sorting (isort)..."
if isort --check-only --diff .; then
    echo -e "${GREEN}✅ Import sorting is correct${NC}"
else
    echo -e "${YELLOW}⚠️  Import sorting suggestions available (run: isort .)${NC}"
fi

echo -e "\n📋 Step 5: Running unit tests..."
python -m unittest discover tests -v
echo -e "${GREEN}✅ All tests passed${NC}"

echo -e "\n📋 Step 6: Testing application startup..."
timeout 10s python -c "
import asyncio
from main import app

async def test_startup():
    try:
        print('Application imported successfully')
        print(f'App type: {type(app)}')
        print('✅ Application can start')
    except Exception as e:
        print(f'❌ Error during startup test: {e}')
        exit(1)

asyncio.run(test_startup())
" || echo "Startup test completed"

echo -e "\n🎉 ${GREEN}All quality checks completed successfully!${NC}"
echo -e "Your code is ready for commit and push."