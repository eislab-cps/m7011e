#!/bin/bash
# Verification script for Tutorial 15 - AI Personalization
# This script checks if your environment is ready to run the tutorial

set -e

echo "=========================================="
echo "Tutorial 15 Setup Verification"
echo "=========================================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check counter
CHECKS_PASSED=0
CHECKS_TOTAL=0

check_command() {
    CHECKS_TOTAL=$((CHECKS_TOTAL + 1))
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✅${NC} $1 is installed"
        CHECKS_PASSED=$((CHECKS_PASSED + 1))
        return 0
    else
        echo -e "${RED}❌${NC} $1 is NOT installed"
        return 1
    fi
}

check_file() {
    CHECKS_TOTAL=$((CHECKS_TOTAL + 1))
    if [ -f "$1" ]; then
        echo -e "${GREEN}✅${NC} $1 exists"
        CHECKS_PASSED=$((CHECKS_PASSED + 1))
        return 0
    else
        echo -e "${RED}❌${NC} $1 is missing"
        return 1
    fi
}

check_python_package() {
    CHECKS_TOTAL=$((CHECKS_TOTAL + 1))
    if python3 -c "import $1" &> /dev/null; then
        echo -e "${GREEN}✅${NC} Python package '$1' is installed"
        CHECKS_PASSED=$((CHECKS_PASSED + 1))
        return 0
    else
        echo -e "${YELLOW}⚠️${NC}  Python package '$1' is NOT installed"
        return 1
    fi
}

echo "1. Checking required commands..."
echo "--------------------------------"
check_command python3
check_command kubectl
check_command docker
echo ""

echo "2. Checking Python version..."
echo "--------------------------------"
CHECKS_TOTAL=$((CHECKS_TOTAL + 1))
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 8 ]; then
    echo -e "${GREEN}✅${NC} Python $PYTHON_VERSION (requires 3.8+)"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
    echo -e "${RED}❌${NC} Python $PYTHON_VERSION (requires 3.8+)"
fi
echo ""

echo "3. Checking tutorial files..."
echo "--------------------------------"
check_file "training/sample_data.csv"
check_file "training/train_model.py"
check_file "training/requirements.txt"
check_file "service/recommendation_service.py"
check_file "service/requirements.txt"
check_file "service/Dockerfile"
check_file "redis-deployment.yaml"
check_file "recommendation-service.yaml"
check_file "README.md"
check_file "QUICKSTART.md"
echo ""

echo "4. Checking Python dependencies (training)..."
echo "--------------------------------"
if [ -f "training/requirements.txt" ]; then
    check_python_package "pandas"
    check_python_package "sklearn"
    check_python_package "joblib"
else
    echo -e "${YELLOW}⚠️${NC}  Skipping (requirements.txt missing)"
fi
echo ""

echo "5. Checking Python dependencies (service)..."
echo "--------------------------------"
if [ -f "service/requirements.txt" ]; then
    check_python_package "flask"
    check_python_package "sklearn"
    check_python_package "redis"
    check_python_package "prometheus_client"
else
    echo -e "${YELLOW}⚠️${NC}  Skipping (requirements.txt missing)"
fi
echo ""

echo "6. Checking Kubernetes cluster access..."
echo "--------------------------------"
CHECKS_TOTAL=$((CHECKS_TOTAL + 1))
if kubectl cluster-info &> /dev/null; then
    echo -e "${GREEN}✅${NC} Connected to Kubernetes cluster"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))

    # Show current context
    CONTEXT=$(kubectl config current-context 2>/dev/null || echo "unknown")
    NAMESPACE=$(kubectl config view --minify -o jsonpath='{..namespace}' 2>/dev/null || echo "default")
    echo "   Context: $CONTEXT"
    echo "   Namespace: $NAMESPACE"
else
    echo -e "${YELLOW}⚠️${NC}  Not connected to Kubernetes cluster (optional for local testing)"
fi
echo ""

echo "7. Checking Docker daemon..."
echo "--------------------------------"
CHECKS_TOTAL=$((CHECKS_TOTAL + 1))
if docker info &> /dev/null; then
    echo -e "${GREEN}✅${NC} Docker daemon is running"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
    echo -e "${YELLOW}⚠️${NC}  Docker daemon is not running (needed for building images)"
fi
echo ""

# Summary
echo "=========================================="
echo "Summary"
echo "=========================================="
echo ""
echo "Checks passed: $CHECKS_PASSED / $CHECKS_TOTAL"
echo ""

if [ $CHECKS_PASSED -eq $CHECKS_TOTAL ]; then
    echo -e "${GREEN}🎉 All checks passed! You're ready to start Tutorial 15.${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. cd training"
    echo "  2. pip install -r requirements.txt"
    echo "  3. python train_model.py"
    echo ""
    exit 0
elif [ $CHECKS_PASSED -ge $((CHECKS_TOTAL * 3 / 4)) ]; then
    echo -e "${YELLOW}⚠️  Most checks passed. You can proceed but may need to install missing dependencies.${NC}"
    echo ""
    echo "To install Python dependencies:"
    echo "  cd training"
    echo "  pip install -r requirements.txt"
    echo ""
    exit 0
else
    echo -e "${RED}❌ Several checks failed. Please review the output above.${NC}"
    echo ""
    echo "Common fixes:"
    echo "  - Install Python 3.8+: https://www.python.org/downloads/"
    echo "  - Install kubectl: https://kubernetes.io/docs/tasks/tools/"
    echo "  - Install Docker: https://docs.docker.com/get-docker/"
    echo "  - Install Python packages: pip install -r training/requirements.txt"
    echo ""
    exit 1
fi
