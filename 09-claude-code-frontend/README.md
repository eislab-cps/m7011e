# Tutorial 8: Building React Frontends with Claude Code

Learn how to use Claude Code to rebuild the Todo List from Tutorial 1 using React, demonstrating effective prompting techniques and iterative development.

Example of a generated React Todo List app below:
![React Todo List Example](./example.png)

## Prerequisites

- Completed Tutorial 1 (basic web app with Flask backend)
- Node.js and npm installed
- Claude Code CLI installed
- Basic React knowledge helpful but not required

---

## Getting Started with Claude Code

### Directory Structure

Before starting, understand where to run Claude Code:

```
m7011e/                           ← START CLAUDE CODE HERE (main directory)
├── 1-basic-webapp/
├── 2-docker/
├── 3-databases/
├── 4-frameworks/
├── 5-k8s-getting-started/
├── 6-k8s-helloworld/
├── 7-postgresql/
├── 8-claude-code-frontend/
└── todo-react/                   ← Claude Code will create this
```

### Starting Claude Code

**Step 1: Navigate to the main project directory**

```bash
# Replace /path/to/m7011e with your actual path
cd /path/to/m7011e
```

**Step 2: Verify you're in the right place**

```bash
ls
```

You should see output like:
```
1-basic-webapp  2-docker  3-databases  4-frameworks  5-k8s-getting-started  6-k8s-helloworld  7-postgresql  8-claude-code-frontend  ...
```

**Step 3: Start Claude Code**

```bash
claude
```

You'll see the Claude Code prompt:
```
Claude Code is ready. How can I help you today?
```

### Your First Command

Once Claude Code starts, you'll see a prompt. Try this:

```
Create a new React application in a folder called "todo-react" using Vite.
Use JavaScript (not TypeScript).
Install Tailwind CSS for styling.
Create this folder structure:
- src/components (for React components)
- src/api (for API calls)
Set up Tailwind with a basic configuration.
Create the app in the new directory `todo-react/` 
```

**What happens:**
- Claude Code creates a new folder `todo-react/` in your current directory
- Initializes a Vite + React project
- Installs and configures Tailwind CSS
- Sets up the folder structure

**Important Notes:**
- Claude Code can see and modify files in the current directory and subdirectories
- It can run terminal commands (npm, git, etc.)
- Each session maintains context - it remembers what you've asked in the current conversation
- To exit, type `/exit` or press Ctrl+C

---

## What is Claude Code?

Claude Code is an AI-powered development assistant that can:
- Generate React components and complete applications
- Set up projects with proper configuration
- Execute terminal commands (npm, git, etc.)
- Write tests and documentation
- Debug issues and explain code

**Key principle:** Clear, specific prompts get better results.

---

## The Golden Rules of Prompting

### 1. Be Specific
❌ `make a react app`
✅ `Create a React todo list app with Vite, using functional components and Tailwind CSS`

### 2. Provide Context
❌ `add styling`
✅ `Style the TodoList component with Tailwind CSS to match the design from tutorial 1: purple gradient background, white card, rounded corners`

### 3. Break Down Complex Tasks
Instead of asking for everything at once, work step-by-step:
1. Set up project
2. Create basic UI
3. Add functionality
4. Connect to backend
5. Add polish

---

## Building the Todo List: Step-by-Step Prompts

### Before You Start

**1. Start the Flask Backend (from Tutorial 1)**

Open a **separate terminal** and run:

```bash
# Navigate to Tutorial 1 backend
cd 1-basic-webapp/backend

# Start the Flask server
python3 app.py
```

Keep this running! You should see:
```
Starting Flask server...
API will be available at: http://127.0.0.1:8000
```

**2. Start Claude Code (in another terminal)**

Make sure you've started Claude Code from the main `m7011e/` directory (see "Getting Started" section above).

### Step 1: Project Setup

**Copy and paste this into Claude Code:**
```
Create a new React application in a folder called "todo-react" using Vite.
Use JavaScript (not TypeScript).
Install Tailwind CSS for styling.
Create this folder structure:
- src/components (for React components)
- src/api (for API calls)
Set up Tailwind with a basic configuration.
Create the app in the new directory `todo-react/` 
```

**What Claude Code will do:**
- Create a new `todo-react/` folder in your current directory
- Initialize Vite + React project
- Install and configure Tailwind CSS
- Create the folder structure
- Run npm install

**Wait for:** Claude Code to finish before moving to the next step. You'll see a message indicating completion.

---

### Step 2: Create Basic Todo List UI

**Copy and paste this into Claude Code:**
```
Create a TodoList component that displays:
- An input field with placeholder "What needs to be done?"
- An "Add Todo" button
- A list area for todos (can be empty for now)

Style it to match Tutorial 1's design:
- Purple gradient background (from #667eea to #764ba2)
- White card with rounded corners and shadow
- Center the card on the page
- Input and button in a flex row
- Use the same styling as the original: padding, borders, hover effects

Put this in src/components/TodoList.jsx
Update src/App.jsx to render the TodoList component.
```

**What Claude Code will do:**
- Create `src/components/TodoList.jsx` with matching UI
- Update `src/App.jsx` to import and render TodoList
- Apply proper Tailwind classes for styling

---

### Step 3: Add Local State Management

**Prompt:**
```
Update the TodoList component to manage todos locally with useState:
- Add state for: todos array and input text
- Implement addTodo function that:
  - Creates todo with id and text
  - Adds to the todos array
  - Clears the input
- Implement deleteTodo function that removes a todo by id
- Display todos in a list with:
  - Todo ID number
  - Todo text
  - Delete button for each item
- Use the same styling as Tutorial 1 for todo items

Don't connect to the backend yet - just use local state.
```

**What you'll get:**
- Working todo list with add/delete functionality
- Proper React hooks (useState)
- Event handlers
- Matching UI from Tutorial 1

---

### Step 4: Connect to Flask Backend

**Prompt:**
```
Create an API service file at src/api/todos.js with functions to:
- getTodos() - GET request to http://localhost:8000/api/todos
- createTodo(text) - POST request
- deleteTodo(id) - DELETE request

Then update TodoList component to:
- Fetch todos on component mount using useEffect
- Call API functions instead of using local state
- Show loading state while fetching
- Display error message if API call fails
- Match error handling from Tutorial 1

Make sure to handle CORS properly (the Flask backend already has CORS configured).
```

**What you'll get:**
- Separate API service layer
- Integration with Flask backend from Tutorial 1
- Loading and error states
- useEffect for data fetching
- Clean separation of concerns

---

### Step 5: Add Polish and Error Handling

**Prompt:**
```
Improve the TodoList component with:

1. Better error handling:
   - Show error message in a red banner at the top
   - Display specific error messages
   - Auto-hide errors after 5 seconds

2. Empty state:
   - When no todos, show "📝 No todos yet. Add one above!"
   - Match the styling from Tutorial 1

3. Input validation:
   - Don't allow empty todos
   - Trim whitespace
   - Show error if empty

4. Animation:
   - Fade in new todos when added
   - Use Tailwind's animation classes

5. Make the Add button disabled while loading
```

**What you'll get:**
- Professional error handling
- Empty state UI
- Input validation
- Smooth animations
- Better UX

---

## Complete Example Workflow

Here's how a conversation with Claude Code might flow:

**You:** "Create a new React app for a todo list with Vite and Tailwind"

**Claude Code:** [Creates project, installs dependencies, sets up Tailwind]

**You:** "Create a TodoList component with the same purple gradient design from tutorial 1"

**Claude Code:** [Creates component with matching UI]

**You:** "Add local state to manage todos with add and delete functionality"

**Claude Code:** [Implements useState and functions]

**You:** "Now connect it to the Flask backend at localhost:8000/api/todos"

**Claude Code:** [Creates API service and updates component]

**You:** "The error messages aren't showing up. Can you add better error handling?"

**Claude Code:** [Adds error banner with auto-dismiss]

**You:** "Looks great! Can you add an animation when new todos appear?"

**Claude Code:** [Adds fade-in animation with Tailwind]

## Tips for Success

### Do's ✅

1. **Reference existing work**
   ```
   "Style this like the todo list in tutorial 1"
   ```

2. **Be specific about technologies**
   ```
   "Use Tailwind CSS for styling, not plain CSS"
   ```

3. **Ask for explanations**
   ```
   "Explain why we need useEffect here"
   ```

4. **Request step-by-step**
   ```
   "First create the UI, then we'll add functionality"
   ```

5. **Iterate on solutions**
   ```
   "This works but can you add loading states?"
   ```

### Don'ts ❌

1. **Don't be vague**
   ```
   ❌ "make it better"
   ✅ "add error handling for failed API calls"
   ```

2. **Don't skip setup**
   ```
   ❌ "use Tailwind" (without installing it first)
   ✅ "install and configure Tailwind CSS"
   ```

3. **Don't ask for everything at once**
   ```
   ❌ "build a complete todo app with auth, teams, sharing, and mobile app"
   ✅ Build incrementally, feature by feature
   ```

---

## Common Issues and Solutions

### Issue: "Failed to fetch" errors

**Ask Claude Code:**
```
I'm getting "Failed to fetch" when calling the API.
The Flask backend is running on port 8000.
Check the API URL and help me debug the CORS issue.
```

### Issue: Component not re-rendering

**Ask Claude Code:**
```
My todo list doesn't update after adding a new todo.
Here's my code: [paste code]
What's wrong with my state management?
```

### Issue: Styling doesn't match

**Ask Claude Code:**
```
The purple gradient isn't showing up.
I want it to match tutorial 1's design exactly.
Can you check the Tailwind classes?
```

---

## Next Steps

After building the React todo list, try these enhancements:

**Prompt for Additional Features:**
```
Add these features to the todo list:
1. Mark todos as complete (strike-through text)
2. Filter buttons: All, Active, Completed
3. Show count of remaining todos
4. "Clear completed" button
5. Edit todo text inline
```

**Prompt for Testing:**
```
Add Vitest tests for the TodoList component:
- Test adding a todo
- Test deleting a todo
- Test error handling
- Test loading state
```

**Prompt for Deployment:**
```
Help me deploy this React app:
1. Build for production
2. Create a Dockerfile
3. Configure nginx to serve the app
4. Set up environment variables for the API URL
```

---

## Key Takeaways

1. **Start simple, iterate**: Don't try to build everything at once
2. **Be specific**: Mention design details, technologies, and requirements
3. **Reference examples**: Point to Tutorial 1's design and functionality
4. **Ask for explanations**: Understand what code does, don't just copy it
5. **Test as you go**: Make sure each step works before moving to the next

Claude Code is most effective when you treat it as a collaborative partner:
- You provide clear direction
- It generates code
- You review and refine
- Together you build great applications

---

## Quick Reference: All Prompts in Order

Copy and paste these prompts into Claude Code one at a time:

### 1. Project Setup
```
Create a new React application in a folder called "todo-react" using Vite.
Use JavaScript (not TypeScript).
Install Tailwind CSS for styling.
Create this folder structure:
- src/components (for React components)
- src/api (for API calls)
Set up Tailwind with a basic configuration.
```

### 2. Create UI
```
Create a TodoList component that displays:
- An input field with placeholder "What needs to be done?"
- An "Add Todo" button
- A list area for todos (can be empty for now)

Style it to match Tutorial 1's design:
- Purple gradient background (from #667eea to #764ba2)
- White card with rounded corners and shadow
- Center the card on the page
- Input and button in a flex row
- Use the same styling as the original: padding, borders, hover effects

Put this in src/components/TodoList.jsx
Update src/App.jsx to render the TodoList component.
```

### 3. Add State Management
```
Update the TodoList component to manage todos locally with useState:
- Add state for: todos array and input text
- Implement addTodo function that creates todo with id and text, adds to array, clears input
- Implement deleteTodo function that removes a todo by id
- Display todos in a list with: Todo ID number, todo text, and delete button
- Use the same styling as Tutorial 1 for todo items
Don't connect to the backend yet - just use local state.
```

### 4. Connect to Backend
```
Create an API service file at src/api/todos.js with functions to:
- getTodos() - GET request to http://localhost:8000/api/todos
- createTodo(text) - POST request
- deleteTodo(id) - DELETE request

Then update TodoList component to:
- Fetch todos on component mount using useEffect
- Call API functions instead of using local state
- Show loading state while fetching
- Display error message if API call fails
```

### 5. Add Polish
```
Improve the TodoList component with:
1. Error handling: Show error in red banner, auto-hide after 5 seconds
2. Empty state: When no todos, show "No todos yet. Add one above!"
3. Input validation: Don't allow empty todos, trim whitespace
4. Animation: Fade in new todos when added using Tailwind
5. Disable Add button while loading
```

### 6. Run the Application

After all prompts are complete, run these commands:

```bash
# Navigate to the React app
cd todo-react

# Start the development server
npm run dev
```

Then open your browser to the URL shown (usually `http://localhost:5173`)

**Don't forget:** Make sure the Flask backend from Tutorial 1 is running on port 8000!

---

## Additional Resources

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- Tutorial 1: Basic Web App (for the Flask backend)
