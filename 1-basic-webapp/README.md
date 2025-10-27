# Tutorial 1: Basic Web Application

A simple todo list application demonstrating fundamental web application concepts including REST APIs, client-server architecture, and frontend-backend communication.

## Learning Objectives

By completing this tutorial, you will understand:
- How web applications work (client-server architecture)
- The difference between REST and RPC
- How to build a REST API with Flask (Python)
- How to create a frontend that communicates with a backend
- HTTP methods and their purposes
- JSON data format
- CORS (Cross-Origin Resource Sharing)

---

## Fundamental Concepts

### 1. Client-Server Architecture

A web application typically consists of two parts:

```
┌─────────────┐         HTTP/HTTPS          ┌─────────────┐
│             │    ──────────────────►      │             │
│  Client     │         Request             │   Server    │
│ (Browser)   │                             │  (Backend)  │
│             │    ◄──────────────────      │             │
└─────────────┘         Response            └─────────────┘
```

- **Client (Frontend)**: The user interface running in the browser (HTML, CSS, JavaScript)
- **Server (Backend)**: Processes requests, handles business logic, manages data (Python, Node.js, Java, etc.)
- **Communication**: They talk via HTTP protocol using structured messages

### 2. RPC vs REST

There are different ways for clients and servers to communicate:

#### RPC (Remote Procedure Call)
- **Concept**: Call functions/procedures on a remote server as if they were local
- **Style**: Action-oriented (verbs)
- **Example endpoints**:
  - `POST /createTodo`
  - `POST /deleteTodo`
  - `POST /getTodos`

**Characteristics:**
- All operations typically use POST
- Function names in the URL
- Think: "What action should the server perform?"

#### REST (Representational State Transfer)
- **Concept**: Treat everything as a "resource" that you can manipulate
- **Style**: Resource-oriented (nouns)
- **Example endpoints**:
  - `GET /todos` - Retrieve todos
  - `POST /todos` - Create a new todo
  - `DELETE /todos/1` - Delete todo with id 1
  - `PUT /todos/1` - Update todo with id 1

**Characteristics:**
- Uses HTTP methods (GET, POST, PUT, DELETE) meaningfully
- URLs represent resources (nouns)
- Stateless - each request contains all needed information
- Think: "What resource am I working with?"

**This tutorial uses REST** because it's the most common pattern for modern web APIs.

### 3. HTTP Methods

REST APIs use different HTTP methods to indicate the type of operation:

| Method   | Purpose                | Example                    | Idempotent* |
|----------|------------------------|----------------------------|-------------|
| `GET`    | Retrieve data          | Get list of todos          | Yes         |
| `POST`   | Create new resource    | Create a new todo          | No          |
| `PUT`    | Update/replace resource| Update an existing todo    | Yes         |
| `DELETE` | Remove resource        | Delete a todo              | Yes         |

*Idempotent: Calling it multiple times has the same effect as calling it once

### 4. JSON Data Format

Web APIs typically exchange data in JSON (JavaScript Object Notation):

```json
{
  "id": 1,
  "text": "Learn Flask",
  "completed": false
}
```

**Why JSON?**
- Human-readable
- Easy to parse in any programming language
- Native support in JavaScript
- Lightweight compared to XML

### 5. CORS (Cross-Origin Resource Sharing)

When your frontend (e.g., `http://localhost:8080`) tries to call your backend (e.g., `http://localhost:5000`), browsers block this by default for security.

**CORS** allows the server to specify who can access it:
- Server adds special headers: `Access-Control-Allow-Origin: *`
- This tells the browser: "It's okay to allow requests from other origins"

---

## Application Architecture

Our simple todo list application:

```
┌───────────────────────────────────┐
│         Frontend (Browser)         │
│  ┌─────────────────────────────┐  │
│  │  index.html                 │  │
│  │  - HTML structure           │  │
│  │  - CSS styling              │  │
│  │  - JavaScript logic         │  │
│  │    * Fetch todos            │  │
│  │    * Add new todo           │  │
│  │    * Delete todo            │  │
│  └─────────────────────────────┘  │
└───────────────┬───────────────────┘
                │
                │ HTTP Requests (Fetch API)
                │
┌───────────────┴───────────────────┐
│        Backend (Flask Server)      │
│  ┌─────────────────────────────┐  │
│  │  app.py                     │  │
│  │  REST API Endpoints:        │  │
│  │  - GET    /api/todos        │  │
│  │  - POST   /api/todos        │  │
│  │  - DELETE /api/todos/<id>   │  │
│  │                             │  │
│  │  Data Storage:              │  │
│  │  - In-memory list           │  │
│  │    (resets on restart)      │  │
│  └─────────────────────────────┘  │
└───────────────────────────────────┘
```

**Data Flow Example - Adding a Todo:**

1. User types "Learn Flask" and clicks "Add"
2. JavaScript captures the event
3. JavaScript sends: `POST /api/todos` with body `{"text": "Learn Flask"}`
4. Flask receives request, creates todo with unique ID
5. Flask responds: `{"id": 1, "text": "Learn Flask"}`
6. JavaScript receives response, updates the page

---

## Project Structure

```
1-basic-webapp/
├── README.md              # This file
├── backend/
│   ├── app.py            # Flask server (REST API)
│   └── requirements.txt  # Python dependencies
└── frontend/
    └── index.html        # Complete frontend (HTML + CSS + JS)
```

---

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- A web browser
- A text editor

---

## Step 1: Set Up the Backend

### 1.1 Navigate to the backend directory

```bash
cd backend
```

### 1.2 Create a virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 1.3 Install dependencies

```bash
pip install -r requirements.txt
```

This will install:
- **Flask**: Web framework for building the API
- **Flask-CORS**: Extension to handle CORS

### 1.4 Run the Flask server

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

The backend is now running! Keep this terminal open.

---

## Step 2: Run the Frontend

### 2.1 Open a new terminal

### 2.2 Navigate to the frontend directory

```bash
cd frontend
```

### 2.3 Start a simple HTTP server

**Python 3:**
```bash
python3 -m http.server 8080
```

**Python 2:**
```bash
python -m SimpleHTTPServer 8080
```

**Node.js (if you have it):**
```bash
npx http-server -p 8080
```

### 2.4 Open your browser

Navigate to: `http://localhost:8080`

You should see the todo list application!

---

## Step 3: Test the Application

1. **Add a todo**: Type something in the input box and click "Add Todo"
2. **View todos**: Your todos appear in a list below
3. **Delete a todo**: Click the "Delete" button next to any todo
4. **Check the API**: Open `http://localhost:5000/api/todos` in your browser to see the raw JSON data

---

## How It Works

### Backend (Flask) - `backend/app.py`

The Flask server provides three endpoints:

**1. GET /api/todos - Retrieve all todos**
```python
@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)
```
- Returns the entire list of todos as JSON

**2. POST /api/todos - Create a new todo**
```python
@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.json
    new_todo = {
        'id': len(todos) + 1,
        'text': data['text']
    }
    todos.append(new_todo)
    return jsonify(new_todo), 201
```
- Receives JSON data from the client
- Creates a new todo with a unique ID
- Adds it to the list
- Returns the created todo with status code 201 (Created)

**3. DELETE /api/todos/<id> - Delete a todo**
```python
@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todos = [t for t in todos if t['id'] != todo_id]
    return '', 204
```
- Filters out the todo with the specified ID
- Returns empty response with status code 204 (No Content)

### Frontend (JavaScript) - `frontend/index.html`

The JavaScript code uses the **Fetch API** to communicate with the backend:

**Fetching todos:**
```javascript
fetch('http://localhost:5000/api/todos')
    .then(response => response.json())
    .then(data => {
        // Update the UI with the todos
    });
```

**Creating a todo:**
```javascript
fetch('http://localhost:5000/api/todos', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ text: todoText })
})
```

**Deleting a todo:**
```javascript
fetch(`http://localhost:5000/api/todos/${todoId}`, {
    method: 'DELETE'
})
```

---

## Understanding the Code

### Key Concepts in `app.py`:

1. **Flask initialization**:
   ```python
   app = Flask(__name__)
   CORS(app)  # Enable CORS for all routes
   ```

2. **Route decorators**: `@app.route('/path', methods=['GET', 'POST'])`
   - Define URL endpoints
   - Specify which HTTP methods are allowed

3. **Request handling**: `request.json`
   - Access data sent by the client

4. **Response formatting**: `jsonify(data)`
   - Convert Python dictionaries/lists to JSON

5. **In-memory storage**: `todos = []`
   - Simple list to store data
   - Data is lost when server restarts
   - In real apps, you'd use a database

### Key Concepts in `index.html`:

1. **DOM manipulation**:
   ```javascript
   document.getElementById('todoInput')
   ```

2. **Event listeners**:
   ```javascript
   form.addEventListener('submit', handleSubmit)
   ```

3. **Fetch API** - Modern way to make HTTP requests:
   ```javascript
   fetch(url, options)
       .then(response => response.json())
       .then(data => { /* use data */ })
   ```

4. **Async operations** - Web requests are asynchronous:
   - Promises (`.then()` chains)
   - Request is sent, code continues
   - When response arrives, callback is executed

---

## Common Issues and Solutions

### Issue 1: CORS Error
**Error**: "Access to fetch has been blocked by CORS policy"

**Solution**: Make sure Flask-CORS is installed and enabled:
```python
from flask_cors import CORS
CORS(app)
```

### Issue 2: Connection Refused
**Error**: "Failed to fetch" or "Connection refused"

**Solution**:
- Ensure Flask server is running on port 5000
- Check that you're using the correct URL in frontend

### Issue 3: Port Already in Use
**Error**: "Address already in use"

**Solution**:
```bash
# Find process using port 5000
lsof -i :5000
# Kill the process
kill -9 <PID>
```

Or use a different port:
```python
app.run(debug=True, port=5001)
```

---

## Exercises

Try these to deepen your understanding:

### Exercise 1: Add Todo Completion
Add a "completed" status to todos:
- Backend: Add `completed` field (boolean) to todos
- Frontend: Add checkbox to toggle completion
- API: Add `PUT /api/todos/<id>` to update completion status

### Exercise 2: Add Timestamps
Add creation timestamp to each todo:
- Use `datetime.now()` in Python
- Display the date in the frontend

### Exercise 3: Add Validation
Prevent empty todos:
- Backend: Check if text is empty, return error (400 Bad Request)
- Frontend: Disable button if input is empty

### Exercise 4: Add Todo Editing
Allow editing todo text:
- Frontend: Add "Edit" button that shows input field
- Backend: Implement `PUT /api/todos/<id>` endpoint
- Update the todo text

---

## Next Steps

After completing this tutorial:

1. **Add a database**: Replace in-memory list with PostgreSQL (see Tutorial 4)
2. **Deploy to Kubernetes**: Learn containerization and orchestration (Tutorials 2-3)
3. **Add authentication**: Protect your API with user login
4. **Build a more complex app**: User accounts, multiple resources, relationships

---

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [MDN Web Docs - Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [REST API Tutorial](https://restfulapi.net/)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

---

## Summary

You've learned:
- ✅ Client-server architecture
- ✅ Difference between RPC and REST
- ✅ How to build a REST API with Flask
- ✅ How to make HTTP requests from JavaScript
- ✅ HTTP methods (GET, POST, DELETE)
- ✅ JSON data format
- ✅ CORS and why it's needed

**Key Takeaway**: Web applications are just programs running on different machines talking to each other using HTTP protocol and structured data formats like JSON.
