# Quick Start - Testing and CI

Run the included examples and set up a CI pipeline. Start commands from the repository root unless stated otherwise.

## Prerequisites

- Python 3.10+
- Node.js 22.12+
- PostgreSQL (local or from Tutorial 8)
- GitHub account

---

## Option A: Backend Testing (Python/Flask)

### Step 1: Install Dependencies

```bash
cd 10-testing-ci/backend-tests
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

### Step 2: Run Unit Tests (No Database Needed)

```bash
# Unit tests use mocks - they run instantly!
pytest test_unit.py -v
```

**Expected result:** All 7 unit tests pass. They cover creating todos, retrieving them, and marking them complete, including validation and not-found cases.

### Step 3: Run with Coverage

```bash
pytest test_unit.py --cov=../examples --cov-report=term-missing
```

**Output:**
```
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
examples/todo_service.py   85      5    94%   142, 156, 201
-----------------------------------------------------
TOTAL                      85      5    94%
```

### Step 4: Run Integration Tests (Requires PostgreSQL)

```bash
# Use a disposable PostgreSQL instance. The fixture creates and drops
# test_tododb automatically; it must not contain data you want to keep.
# Export DB_HOST, DB_PORT, DB_USER, DB_PASSWORD if using non-default values.

# Run integration tests
pytest test_integration.py -v
```

**Done!** You've run both unit and integration tests.

---

## Option B: Frontend Testing (React/Jest)

### Step 1: Install Dependencies

```bash
cd 10-testing-ci/frontend-tests
npm ci
```

### Step 2: Run Tests

```bash
npm test -- --watchAll=false
```

**Expected result:** The TodoList suite passes all 10 tests, covering loading, errors, retrieval, creation, completion, and form controls.

### Step 3: Run with Coverage

```bash
npm test -- --coverage --watchAll=false
```

**Output:**
```
File           | % Stmts | % Branch | % Funcs | % Lines
-----------|---------|----------|---------|--------
TodoList.jsx  |   95.45 |    90.91 |     100 |   95.00
```

**Done!** Frontend tests passing!

---

## Option C: GitHub Actions CI (Automated Testing)

### Step 1: Create Workflow File

Create `.github/workflows/ci.yml` in your repository:

```yaml
name: CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          cd 10-testing-ci/backend-tests
          pip install -r requirements.txt

      - name: Run tests
        run: |
          cd 10-testing-ci/backend-tests
          pytest test_unit.py -v --cov=../examples
```

### Step 2: Commit and Push

```bash
git add .github/workflows/ci.yml
git commit -m "ci: Add automated testing workflow"
git push
```

### Step 3: Check GitHub Actions Tab

1. Go to your repository on GitHub
2. Click "Actions" tab
3. See your workflow running!

**Result:**
- ✅ Every push triggers tests automatically
- ✅ Pull requests show test status
- ✅ Tests can block merging after required status checks are enabled in branch protection

**Done!** Automated CI is set up!

---

## Quick Testing Workflow

### 1. Write a New Function

```python
def delete_todo(todo_id, user_id):
    """Delete a todo"""
    # Implementation here
    pass
```

### 2. Write Tests First (TDD)

```python
def test_delete_todo_success():
    # Test the happy path
    result = delete_todo(1, 1)
    assert result == True

def test_delete_todo_not_found():
    # Test error case
    with pytest.raises(ValueError):
        delete_todo(999, 1)
```

### 3. Run Tests (They Fail)

```bash
pytest test_unit.py::test_delete_todo_success -v
# ❌ FAILED - function not implemented
```

### 4. Implement Function

```python
def delete_todo(todo_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM todos WHERE todo_id = %s AND user_id = %s RETURNING todo_id",
        (todo_id, user_id)
    )
    result = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    if not result:
        raise ValueError("Todo not found")

    return True
```

### 5. Run Tests (They Pass)

```bash
pytest test_unit.py::test_delete_todo_success -v
# Passes after you add a database mock (unit test), or a test DB fixture
# (integration test). The abbreviated TDD example above omits that setup.
```

This is **Test-Driven Development (TDD)**!

---

## Common Commands

### Backend (pytest)

```bash
# Run all tests
pytest

# Run specific file
pytest test_unit.py

# Run specific test
pytest test_unit.py::TestCreateTodo::test_create_todo_success

# Run with coverage
pytest --cov=../examples --cov-report=html

# Run tests matching pattern
pytest -k "create_todo"

# Verbose output
pytest -v

# Show print statements
pytest -s
```

### Frontend (Jest)

```bash
# Run all tests
npm test -- --watchAll=false

# Run in watch mode (re-runs on file changes)
npm test -- --watch

# Run with coverage
npm test -- --coverage --watchAll=false

# Run specific file
npm test -- TodoList.test.jsx

# Update snapshots
npm test -- -u
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'pytest'"

```bash
pip install pytest pytest-cov pytest-mock
```

### "Database connection failed"

```bash
# Check PostgreSQL is running
psql -U postgres -c "SELECT 1"

# Use a disposable PostgreSQL instance. The fixture creates and drops
# test_tododb automatically; it must not contain data you want to keep.
# Export DB_HOST, DB_PORT, DB_USER, DB_PASSWORD if using non-default values.

# Or use port-forwarding from Kubernetes (Tutorial 8)
kubectl port-forward -n db svc/postgres-service 5432:5432
```

### "Tests pass locally but fail in CI"

Common reasons:
- Different Python/Node versions
- Missing environment variables
- Database not available in CI

**Fix:** Check GitHub Actions logs for errors

### "Coverage is below 80%"

```bash
# See which lines are not covered
pytest --cov=../examples --cov-report=term-missing

# Output shows missing lines:
# examples/todo_service.py   85      10    88%   142, 156, 201-205
```

Review uncovered behavior and add meaningful tests for the cases that matter.

---

## Testing Tips

### 1. Test One Thing at a Time

```python
# ✅ Good
def test_create_todo_validates_title():
    with pytest.raises(ValueError):
        create_todo('', 'Description', 1)

# ❌ Bad - testing multiple things
def test_create_todo():
    with pytest.raises(ValueError):
        create_todo('', 'Description', 1)
    todo_id = create_todo('Valid', 'Description', 1)
    assert todo_id > 0
```

### 2. Use Descriptive Test Names

```python
# ✅ Good - name explains what's being tested
def test_create_todo_with_empty_title_raises_value_error():
    pass

# ❌ Bad - vague name
def test_create_todo_error():
    pass
```

### 3. Follow AAA Pattern

```python
def test_example():
    # Arrange - set up test data
    title = "Test todo"
    user_id = 1

    # Act - call the function
    result = create_todo(title, "Description", user_id)

    # Assert - verify result
    assert result is not None
```

### 4. Mock External Dependencies

```python
# ✅ Good - mock database
@patch('todo_service.get_db_connection')
def test_create_todo(mock_db):
    mock_conn = Mock()
    mock_conn.cursor.return_value.fetchone.return_value = [123]
    mock_db.return_value = mock_conn
    result = create_todo('Test', 'Desc', 1)

# ❌ Bad - actually hits database in unit test
def test_create_todo():
    result = create_todo('Test', 'Desc', 1)  # Real DB call!
```

---

## Next Steps

1. ✅ **Write tests for all new code** - Don't skip testing!
2. **Set up branch protection** - Require tests to pass before merging
3. **Add more test types** - API tests, E2E tests
4. **Monitor coverage** - Keep it above 80%
5. **Tutorial 11 (ArgoCD)** - Deploy automatically when tests pass!

---

## Success Indicators

✅ Tests run and pass
✅ Coverage is above 80%
✅ GitHub Actions workflow runs on push
✅ Can't merge PR if tests fail
✅ Tests run in < 1 minute

You're ready for continuous integration! 🚀
