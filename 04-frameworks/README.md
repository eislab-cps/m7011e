# Tutorial 4: Frontend and Backend Frameworks

A comprehensive guide to choosing the right frameworks for building modern microservices architectures.

## Learning Objectives

By the end of this tutorial, you will understand:
- The landscape of microservices-friendly frameworks
- Key criteria for selecting frameworks for microservices
- Trade-offs between different framework choices
- When to use React, Vue, Svelte, Angular, and Rust/WebAssembly for frontend development
- When to use Flask, FastAPI, Express.js, NestJS, Go, Rust, and Java frameworks for microservices
- How to choose different frameworks for different services (polyglot architecture)
- How framework features and service boundaries affect microservice design

## Why Frameworks Exist, and Why There Is More Than One

The todo page from Tutorial 1 works with ordinary JavaScript, and its API could be written using lower-level HTTP tools. As an application grows, developers repeat work: selecting handlers, parsing input, updating views, keeping state consistent, handling errors, and testing integrations. Frameworks and libraries provide reusable machinery and conventions for some of that work.

They make different tradeoffs. A small library leaves more choices to the application; a larger framework supplies an integrated structure but asks the team to learn its conventions. Browser rendering, server routing, database access, and compilation are different jobs, so tools for them can coexist. Language ecosystems and existing integrations also affect the choice.

For this course, compare tools by tracing the same operation through them. Which code is application policy, and which is repeated infrastructure? Which dependency or convention would be worth adopting, and what additional maintenance would it introduce? A short hello-world example or a popularity count cannot answer those questions on its own.

## Read One Request Through a Framework

This is a comparison guide, not an installation script. Use the [HTTP exchange from Tutorial 1](../01-basic-webapp/README.md#2-follow-one-http-request) to interpret each framework's code. First find the entry point, then the handler, then the response:

| Code or command you encounter | What it means |
| --- | --- |
| A Flask route decorator or an Express `app.get(...)` registration | Associates an HTTP method and path with a handler. Registering a handler does not send a request. |
| Reading a request body | Parses data supplied by a client. Validation and authorization remain separate application responsibilities. |
| Returning JSON | Builds the response representation; the status code communicates the outcome. |
| A browser `fetch(...)` | Starts an HTTP request. Awaiting `response.json()` then parses the response body; it does not send another request. |
| React state update | Schedules rendering from the updated state. It does not by itself write data to the backend. |
| A server-rendered page | The server generates HTML that the browser can display. Interactive client code may make later requests. |
| `npm run NAME` in later tutorials | Runs `scripts.NAME` from that project's `package.json`. The meaning comes from the project configuration, not from npm guessing a framework. |

**Compare, then explain:** Take one todo-creation handler. Identify where input is parsed, where invalid input is rejected, where data is saved, and where the response is formed. Which parts are framework facilities, and which rules would still be your responsibility in another framework? Avoid choosing a framework only because its shortest sample has fewer lines.

![One configured request path runs shared middleware, routing and route policies, application logic, then response handling. A middleware step may return an error before the handler runs.](./images/framework-request-pipeline.svg)

Middleware order depends on the framework and configuration. For example, [Express middleware](https://expressjs.com/en/guide/using-middleware/) can continue to the next step or end a response early. Authentication identifies a caller; the operation still needs authorization, including checks on the particular todo. CORS controls browser access to responses and is not authentication.

## Introduction

A framework provides implementation tools and conventions. A modular application can combine frontend and backend frameworks, and separate services can use either the same stack or different stacks. Different languages also create maintenance and operational work, so choose them for requirements you can explain.

### Key Considerations for Microservices

- **Performance**: Can it handle high throughput and low latency?
- **Deployment**: How easy is it to containerize and deploy?
- **Scalability**: Can individual services scale independently?
- **Developer Experience**: How quickly can teams build and iterate?
- **Ecosystem**: What microservices patterns does it support?
- **Resource Footprint**: Memory and CPU usage matter in cloud environments
- **Async Support**: Critical for I/O-bound microservices
- **Type Safety**: Reduces bugs in distributed systems

### Microservices vs Monolithic Frameworks

This tutorial focuses on a selection of frameworks often used for services. Django and Ruby on Rails can also implement independently deployed APIs and microservices. A framework does not determine whether an application is a monolith; service boundaries, data ownership, and deployment practices do.

![The same Flask framework can run one modular application or separately deployed services. Network and release boundaries come from the design.](./images/framework-versus-architecture.svg)

Continue with [Tutorial 4B: Software Architectures](../04b-architectures/README.md) to compare those boundaries.

The snippets illustrate framework syntax and are not complete projects. Add the dependencies, imports, components, and startup configuration required by the framework version you choose. Relative `/api` URLs assume a same-origin backend or a development proxy. In-memory stores are temporary and need concurrency controls when shared between request handlers.

## Understanding Frontend and Backend

Before diving into specific frameworks, it's important to understand the fundamental architecture of web applications.

### What is Frontend?

The **frontend** (also called client-side) is everything the user sees and interacts with in their web browser. It's responsible for:
- **User Interface (UI)**: Buttons, forms, navigation, layout
- **User Experience (UX)**: Interactions, animations, responsiveness
- **Data Display**: Rendering data received from the backend
- **Client-side Logic**: Form validation, UI state management, routing

**Technologies:**
- HTML: Structure and content
- CSS: Styling and layout
- JavaScript: Interactivity and dynamic behavior
- Frontend Frameworks: React, Vue, Svelte, Angular (organize and simplify development)

**Example:** When you type in a search box and see suggestions appear, or when you click a button and see a modal pop up - that's frontend code running in your browser.

### What is Backend?

The **backend** (also called server-side) runs on servers and handles:
- **Business Logic**: Processing rules, calculations, workflows
- **Data Storage**: Database operations (create, read, update, delete)
- **Authentication**: User login, permissions, security
- **API Endpoints**: Providing data to the frontend
- **External Integrations**: Connecting to other services (payment processors, email services)

**Technologies:**
- Server Languages: Python, JavaScript/TypeScript, Go, Rust, Java
- Backend Frameworks: Flask, FastAPI, Express, NestJS, Spring Boot
- Databases: PostgreSQL, MongoDB, Redis
- APIs: REST, GraphQL, gRPC

**Example:** When you submit a login form, the backend verifies your credentials against the database, creates a session, and sends back an authentication token.

### Frontend ↔ Backend Communication

![Browser and server code have different authority. Arrows follow a request toward its data; the response travels back to the browser.](./images/browser-api-data-boundary.svg)

Frontend code is delivered to the user, so hiding a button cannot enforce a data-access rule. The backend must decide whether the caller may perform each operation before accessing data. UI libraries and server frameworks exist to organize different work on opposite sides of this boundary; choosing the same programming language does not remove the boundary.

**Check your reasoning:** If a user bypasses the UI and sends the HTTP request directly, where must an ownership check still run?


**Example Flow:**
1. User clicks "Load Todos" button (Frontend)
2. Frontend sends HTTP GET request to `/api/todos` (Frontend → Backend)
3. Backend queries database for todos (Backend)
4. Backend sends JSON response with todo data (Backend → Frontend)
5. Frontend receives data and updates UI to display todos (Frontend)

### The DOM (Document Object Model)

The **DOM** is the browser's object model of a document. Elements, text, and other nodes form a tree that JavaScript can inspect and change. HTML is input used to build that tree; the DOM can change after the original HTML has arrived.

```html
<html>
  <body>
    <div id="app">
      <h1>My Todos</h1>
      <ul id="todo-list">
        <li>Todo 1</li>
        <li>Todo 2</li>
      </ul>
    </div>
  </body>
</html>
```

![The selected DOM subtree contains element nodes and text nodes. Arrows mean parent-child relationships inside the browser, not network requests.](./images/dom-element-tree.svg)

The figure starts at `div#app` and omits the surrounding document nodes. `getElementById('todo-list')` finds the list element; appending a child changes this browser's page. It does not save a todo in the backend. Saving needs an explicit operation such as the `POST` request in Tutorial 1.

DOM changes can lead to style calculation, layout, and painting, depending on what changed. Browsers batch some work. Repeatedly alternating layout reads and writes can be expensive, while a carefully targeted direct update can be efficient.

**Explain:** If you append a list item with JavaScript and refresh the page, what would make that item reappear? Which part of the system must have kept its data?

### Virtual DOM

Some UI libraries represent the desired UI using JavaScript objects and reconcile that representation with an earlier one before updating the real DOM. This is often called a **virtual DOM**. It helps express the page as a result of state, but it is not a second browser DOM and does not guarantee the fastest possible update.

In React, distinguish the steps described in [Render and Commit](https://react.dev/learn/render-and-commit):

1. **Trigger:** Initial loading or a state update schedules rendering.
2. **Render:** React calls component functions to calculate the desired UI.
3. **Commit:** React applies necessary DOM changes. Rendering can also produce no DOM change.
4. **Browser work:** The browser displays the result through its own rendering pipeline.

![A state update triggers component rendering; React then commits required DOM changes, and the browser handles display. No step automatically writes to an API.](./images/state-render-commit.svg)

```javascript
// A state update changes this component's state, not the backend database.
setTodos(current => [...current, newTodo]);
```

Here is one simplified list update with stable keys. It illustrates matching items, not a performance guarantee for every component:

![For this list update, keys match existing items and the new item is inserted. The drawing illustrates one reconciliation result.](./images/virtual-dom-diff-and-patch.svg)

Direct DOM code does not have to rebuild an entire list either:

```javascript
// Targeted direct DOM update: add one item without clearing the others.
const ul = document.getElementById('todo-list');
const li = document.createElement('li');
li.textContent = newTodo.text;
ul.appendChild(li);
```

The application must decide when that update is appropriate and keep its state consistent with the page. A declarative component instead describes the list for the current state:

```jsx
function TodoList({ todos }) {
  return (
    <ul>
      {todos.map(todo => (
        <li key={todo.id}>{todo.text}</li>
      ))}
    </ul>
  );
}
```

`key` identifies an item among siblings across updates; use a stable ID rather than a new random value on each render. The component still needs application code to load and save data.

### DOM vs Virtual DOM Comparison

| Concern | Direct DOM updates | UI reconciliation |
| --- | --- | --- |
| Description | Application code selects and changes nodes. | Components describe the desired UI from state. |
| Coordination | Application code coordinates state and node updates. | The UI library coordinates rendering and commits. |
| Work | Can make targeted updates; broad rebuilding can be costly. | Adds rendering and reconciliation work; can preserve matching nodes. |
| Choosing | Useful for small interfaces or precise browser integration. | Useful when reusable stateful components simplify the application. |

### Alternatives to Virtual DOM

[Svelte](https://svelte.dev/docs/svelte/overview) compiles components into code that updates the interface and works with its runtime; compilation does not mean that no JavaScript executes in the browser. [Solid's fine-grained reactivity](https://docs.solidjs.com/advanced-concepts/fine-grained-reactivity) tracks dependencies so updates can target affected computations and nodes. Angular checks bindings and updates affected DOM nodes; see its [runtime performance guide](https://angular.dev/best-practices/runtime-performance).

These are different ways to coordinate changes. Bundle size, update cost, accessibility, loading behavior, team knowledge, and ecosystem support all matter. Measure your actual page before claiming one mechanism is universally faster. WebAssembly can help some computation-heavy workloads; it does not remove browser DOM and layout costs.

---

## SPA vs SSR: Application Architecture Patterns

Two questions often get mixed together: **where is the initial HTML content produced**, and **how does later navigation happen**? A **single-page application (SPA)** commonly handles navigation in the browser. **Client-side rendering (CSR)**, **server-side rendering (SSR)**, and **static site generation (SSG)** describe when and where content is rendered. A server-rendered initial page can later behave as an SPA. These choices also work with either a monolith or services, as [Tutorial 4B](../04b-architectures/README.md) explains.

### SPA (Single Page Application)

A common client-rendered SPA starts with an HTML shell. JavaScript loads, obtains application data, and constructs the interface. Afterward a client router can update the URL and view without replacing the whole document. Navigation can still request data or additional code from a server.

![On a first uncached visit, the browser loads an HTML shell and application assets, runs JavaScript, fetches todo JSON, and builds the view. Arrows are separate HTTP exchanges.](./images/spa-first-request.svg)

Read the diagram from top to bottom. Receiving `index.html` is not the same as receiving the todo data. A script download, script error, or API failure can therefore produce different loading failures. Real applications can cache assets, prefetch resources, or overlap work; the figure shows one possible sequence.

This suits interaction-heavy screens such as the course todo dashboard. The initial content may depend on JavaScript and an API round trip, so design loading, empty, and error states deliberately. Public content that only exists after client rendering asks crawlers and preview tools to run that code; do not assume every consumer does. Offline behavior needs explicit caching and synchronization work, often with a service worker.

**Inspect:** In the browser's Network panel, distinguish the document, script, and `/api/todos` requests. Which successful responses would you still see if the API stopped working?

### SSR (Server-Side Rendering)

With request-time SSR, application code generates HTML for a request using the data available on the server. The browser can receive meaningful content without waiting for client JavaScript to construct it. Fetching data, rendering, transfer, parsing, and display still take time; SSR does not make content arrive instantly.

![The application server obtains data and generates HTML before sending it to the browser. A JavaScript UI can hydrate that HTML afterward, while plain server templates need no hydration step.](./images/ssr-and-hydration.svg)

SSR can use Python/Jinja, Java templates, JavaScript frameworks, or other server technologies. **Hydration** is the additional step some UI frameworks use to attach their client behavior to existing server-generated HTML. React's [`hydrateRoot`](https://react.dev/reference/react-dom/client/hydrateRoot) expects the initial client output to match that HTML. A plain HTML form rendered by Flask does not require React hydration.

SSR can help deliver public or request-specific content in the first document. It adds request-time rendering work and requires careful caching: a personalized response must not become a public cache entry. Later interactions can use ordinary form submissions, full-page navigation, or client-side requests. The rendering choice does not decide those interactions for you.

**Explain:** If the page displays a todo before its interactive controls work, which work might still be pending? How would this differ from a server-rendered form with no client framework?

### SSG (Static Site Generation) - Bonus

SSG renders content **before** a visitor requests it, commonly during a build. Deploy the generated files to a static server or CDN. The serving system still handles HTTP requests, but it does not need to run the application renderer for each page view.

![The build reads content and produces HTML assets. Later the host serves those files to the browser without per-request page generation. Client code can still call an API.](./images/ssg-build-and-request.svg)

Documentation and public course pages are useful examples. The generated HTML reflects the inputs used for generation; publishing changed content needs another generation or a configured regeneration mechanism. Build duration and cache invalidation become design concerns as the site grows.

A static page can include interactive JavaScript, hydrate pre-rendered components, and fetch current or personalized data afterward. That does not make its prebuilt HTML personalized. Never generate a shared static file containing a particular user's private todos.

### Comparison Table

![The timelines compare client-rendered initial content, request-time server rendering, and HTML generated before the request. Hydration applies only when the chosen UI needs it.](./images/spa-ssr-ssg-timelines.svg)

| Concern | Client-rendered initial page | Request-time SSR | SSG |
| --- | --- | --- | --- |
| Initial content built | In the browser after the required code and data arrive. | By application code handling the page request. | Before the visitor's request. |
| Page-serving work | Serve shell/assets; APIs still perform application work. | Run the renderer unless a suitable cached response is used. | Serve generated files; any APIs still run separately. |
| Freshness | Depends on API responses and client caches. | Depends on the data read and response caching. | HTML reflects generation inputs until regenerated. |
| JavaScript | Required to construct this client-rendered content. | Optional for plain HTML; hydration or richer UI requires it. | Optional for plain HTML; dynamic additions require client code. |
| Personalization | Fetch authorized user data at runtime. | Generate an authorized response with appropriate cache policy. | Keep shared HTML public; load private data separately. |
| Later navigation | Can use a client router. | Can use full-page or client navigation. | Can use full-page or client navigation. |

None of these guarantees a particular price, load time, search ranking, or accessibility result. The size of assets, server work, cache behavior, network, and page implementation determine the result.

### Hybrid Approaches (Modern Frameworks)

An application can choose different rendering strategies for different routes or parts of a page. For example, build public help pages ahead of time, render a request-specific page on the server, and use client rendering for an interactive dashboard. This is a design example, not a framework's automatic route configuration:

![One application routes public help to prebuilt HTML, a request-specific page to server rendering, and a dashboard to client rendering. Data access and cache policies still apply to each route.](./images/hybrid-rendering-routes.svg)

Frameworks can also stream HTML as portions become available or regenerate cached content. Those features have their own data-loading and caching rules. For example, Next.js distinguishes [server and client components](https://nextjs.org/docs/app/getting-started/server-and-client-components), and Angular documents [hybrid rendering](https://angular.dev/guide/ssr). Learn the selected framework's configuration rather than inferring it from a file name.

### Decision Guide

Start with the screen's requirements:

- **Interactive authenticated workspace:** A client-rendered UI can be useful. Specify startup, API-error, and expired-session behavior.
- **Public page that needs request-specific content:** Consider SSR and decide which responses may be cached.
- **Content publishable ahead of requests:** Consider SSG and decide how updates become visible.
- **Different requirements across the site:** Combine strategies and record the choice for each route.

An API must enforce authorization regardless of where the HTML was rendered. SSR, client routing, and a static host do not establish ownership of a todo.

### Framework Support Summary

| UI ecosystem | Application tooling to explore | Important distinction |
| --- | --- | --- |
| React | Next.js and other React application frameworks | React is a UI library; project setup determines routing and rendering. |
| Vue | Nuxt and Vue's server-rendering APIs | A Vue component does not prescribe a deployment architecture. |
| Svelte | SvelteKit | Rendering and prerendering depend on application configuration. |
| Angular | Angular's `@angular/ssr` integration | Supports client, server, and prerendered routes in hybrid applications. |

**For this course:** Tutorial 9 uses a client-rendered React application. Trace its document, assets, API calls, and state changes before adding another rendering mode.

---

## Framework Landscape

![Framework choices organize different kinds of work. Cards group examples by execution role and language; they do not prescribe one stack.](./images/framework-roles-and-ecosystems.svg)

These are roles and ecosystems rather than a speed or popularity ranking. React supplies UI primitives, while a complete application also needs decisions about routing, data loading, and deployment. Server frameworks similarly differ in how much structure they supply. Existing libraries, team knowledge, integration needs, and maintenance cost can outweigh the size of a short example.

**Check your reasoning:** Which facilities would your project still need after selecting a UI library or a small HTTP framework?


**Note:** GitHub star counts as of January 2025. This landscape shows only microservices-friendly frameworks.

## Frontend Frameworks

### React

**Official Website:** https://react.dev/
**GitHub:** https://github.com/facebook/react

**What it is:** A JavaScript library for building user interfaces, created by Meta (Facebook).

**Key Features:**
- Component-based architecture
- Virtual DOM for efficient updates
- Unidirectional data flow
- Huge ecosystem (React Router, Redux, Next.js)
- JSX syntax (JavaScript + HTML)

**When to Use:**
- ✅ Large, complex applications with many interactive components
- ✅ When you need a vast ecosystem of libraries and tools
- ✅ Teams already familiar with JavaScript
- ✅ When you want flexibility in choosing libraries
- ✅ Mobile development with React Native

**When NOT to Use:**
- ❌ Very simple websites (might be overkill)
- ❌ When you need the smallest possible bundle size
- ❌ When you want an opinionated, all-in-one solution

**Example:**
```javascript
import React, { useState, useEffect } from 'react';

function TodoApp() {
  const [todos, setTodos] = useState([]);

  useEffect(() => {
    fetch('/api/todos')
      .then(res => res.json())
      .then(data => setTodos(data));
  }, []);

  const addTodo = (text) => {
    const newTodo = { id: Date.now(), text, completed: false };
    setTodos([...todos, newTodo]);
  };

  return (
    <div className="todo-app">
      <h1>My Todos</h1>
      <TodoList todos={todos} />
      <AddTodo onAdd={addTodo} />
    </div>
  );
}
```


---

### Vue.js

**Official Website:** https://vuejs.org/
**GitHub:** https://github.com/vuejs/vue

**What it is:** A progressive JavaScript framework for building user interfaces.

**Key Features:**
- Progressive framework (use as little or as much as you need)
- Template syntax (HTML-like)
- Reactive data binding
- Single-file components (.vue files)
- Excellent documentation

**When to Use:**
- ✅ When you want an easy learning curve
- ✅ Progressive enhancement of existing applications
- ✅ Smaller to medium-sized projects
- ✅ When you prefer template syntax over JSX
- ✅ Teams with both beginners and experienced developers

**When NOT to Use:**
- ❌ When you need the absolute largest ecosystem (React has more)
- ❌ When corporate backing is a requirement (React/Angular have Meta/Google)

**Example:**
```vue
<template>
  <div class="todo-app">
    <h1>My Todos</h1>
    <ul>
      <li v-for="todo in todos" :key="todo.id">
        {{ todo.text }}
      </li>
    </ul>
    <input v-model="newTodo" @keyup.enter="addTodo">
  </div>
</template>

<script>
export default {
  data() {
    return {
      todos: [],
      newTodo: ''
    }
  },
  mounted() {
    fetch('/api/todos')
      .then(res => res.json())
      .then(data => this.todos = data);
  },
  methods: {
    addTodo() {
      this.todos.push({ id: Date.now(), text: this.newTodo });
      this.newTodo = '';
    }
  }
}
</script>
```


---

### Svelte

**Official Website:** https://svelte.dev/
**GitHub:** https://github.com/sveltejs/svelte

**What it is:** A compile-time framework that shifts work from the browser to build time.

**Key Features:**
- No virtual DOM (compiles to efficient vanilla JavaScript)
- Reactive by default
- Smaller bundle sizes
- Simple, intuitive syntax
- Built-in animations and transitions

**When to Use:**
- ✅ When performance and bundle size are critical
- ✅ Smaller projects or components
- ✅ When you want simpler, more readable code
- ✅ Interactive data visualizations
- ✅ Embedded widgets

**When NOT to Use:**
- ❌ When you need a massive ecosystem (still growing)
- ❌ Large enterprise applications (less mature tooling)
- ❌ When team is already invested in React/Vue

**Example:**
```svelte
<script>
  import { onMount } from 'svelte';

  let todos = [];
  let newTodo = '';

  onMount(async () => {
    const res = await fetch('/api/todos');
    todos = await res.json();
  });

  function addTodo() {
    todos = [...todos, { id: Date.now(), text: newTodo }];
    newTodo = '';
  }
</script>

<div class="todo-app">
  <h1>My Todos</h1>
  <ul>
    {#each todos as todo (todo.id)}
      <li>{todo.text}</li>
    {/each}
  </ul>
  <input bind:value={newTodo} on:keyup={(event) => { if (event.key === "Enter") addTodo(); }}>
</div>
```


---

### Angular

**Official Website:** https://angular.io/
**GitHub:** https://github.com/angular/angular

**What it is:** A full-featured TypeScript framework by Google for building web applications.

**Key Features:**
- Complete solution (routing, forms, HTTP client built-in)
- TypeScript first
- Dependency injection
- RxJS for reactive programming
- Strong opinions and structure

**When to Use:**
- ✅ Large enterprise applications
- ✅ Teams that prefer TypeScript
- ✅ When you want everything included out-of-the-box
- ✅ Long-term, large-scale projects
- ✅ When you need strong typing and structure

**When NOT to Use:**
- ❌ Small projects (might be overkill)
- ❌ When you need quick prototyping
- ❌ Teams unfamiliar with TypeScript/RxJS

**Example:**
```typescript
import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-todo',
  template: `
    <div class="todo-app">
      <h1>My Todos</h1>
      <ul>
        <li *ngFor="let todo of todos">{{ todo.text }}</li>
      </ul>
      <input [(ngModel)]="newTodo" (keyup.enter)="addTodo()">
    </div>
  `
})
export class TodoComponent implements OnInit {
  todos: any[] = [];
  newTodo: string = '';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.http.get<any[]>('/api/todos')
      .subscribe(data => this.todos = data);
  }

  addTodo() {
    this.todos.push({ id: Date.now(), text: this.newTodo });
    this.newTodo = '';
  }
}
```


---

### Rust + WebAssembly (Yew, Leptos, Dioxus)

**What it is:** High-performance frontend frameworks using Rust compiled to WebAssembly.

**Popular Options:**
- **Yew**: React-like component framework
  - **GitHub:** https://github.com/yewstack/yew
  - **Website:** https://yew.rs/
- **Leptos**: Fine-grained reactivity, similar to SolidJS
  - **GitHub:** https://github.com/leptos-rs/leptos
  - **Website:** https://leptos.dev/
- **Dioxus**: Cross-platform, React-like API
  - **GitHub:** https://github.com/DioxusLabs/dioxus
  - **Website:** https://dioxuslabs.com/

**Key Features:**
- WebAssembly can speed up CPU-heavy work; results depend on the workload and browser
- Strong type safety with Rust's type system
- Zero-cost abstractions
- Small bundle sizes (after wasm-opt)
- Memory safety without garbage collection
- Can interop with JavaScript

**When to Use:**
- ✅ Performance-critical applications (gaming, data visualization, image/video processing)
- ✅ Computational heavy tasks in the browser
- ✅ When you need strong type safety
- ✅ Teams already using Rust
- ✅ WebAssembly modules for existing JavaScript apps
- ✅ Real-time data processing in browser

**When NOT to Use:**
- ❌ Simple CRUD applications (overkill)
- ❌ When you need rapid prototyping
- ❌ SEO-critical content sites (limited SSR support)
- ❌ Teams unfamiliar with Rust

**Example (Yew Framework):**
```rust
use yew::prelude::*;

#[derive(Clone, PartialEq)]
struct Todo {
    id: usize,
    text: String,
    completed: bool,
}

#[function_component]
fn App() -> Html {
    let todos = use_state(|| vec![]);
    let new_todo = use_state(|| String::new());

    let on_add = {
        let todos = todos.clone();
        let new_todo = new_todo.clone();
        Callback::from(move |_| {
            let mut current_todos = (*todos).clone();
            current_todos.push(Todo {
                id: current_todos.len(),
                text: (*new_todo).clone(),
                completed: false,
            });
            todos.set(current_todos);
            new_todo.set(String::new());
        })
    };

    let on_input = {
        let new_todo = new_todo.clone();
        Callback::from(move |e: InputEvent| {
            let input: web_sys::HtmlInputElement = e.target_unchecked_into();
            new_todo.set(input.value());
        })
    };

    html! {
        <div class="todo-app">
            <h1>{"My Todos"}</h1>
            <ul>
                { for todos.iter().map(|todo| html! {
                    <li key={todo.id}>{&todo.text}</li>
                })}
            </ul>
            <input
                type="text"
                value={(*new_todo).clone()}
                oninput={on_input}
            />
            <button onclick={on_add}>{"Add"}</button>
        </div>
    }
}
```

**Example (Leptos Framework - Modern Reactivity):**
```rust
use leptos::*;

#[component]
fn App() -> impl IntoView {
    let (todos, set_todos) = create_signal(Vec::<String>::new());
    let (new_todo, set_new_todo) = create_signal(String::new());

    let add_todo = move |_| {
        set_todos.update(|todos| {
            todos.push(new_todo.get());
        });
        set_new_todo.set(String::new());
    };

    view! {
        <div class="todo-app">
            <h1>"My Todos"</h1>
            <ul>
                <For
                    each=move || todos.get().into_iter().enumerate()
                    key=|(index, _)| *index
                    children=|(_, todo)| view! { <li>{todo}</li> }
                />
            </ul>
            <input
                type="text"
                prop:value=new_todo
                on:input=move |ev| set_new_todo.set(event_target_value(&ev))
            />
            <button on:click=add_todo>"Add"</button>
        </div>
    }
}
```


**Why Rust/WebAssembly?**

1. **Performance**:
   - WebAssembly runs at near-native speed
   - No garbage collection pauses
   - Predictable performance

2. **Type Safety**:
   - Catch errors at compile time
   - Strong type system prevents many runtime bugs
   - No `undefined` or `null` pointer exceptions

3. **Security**:
   - Memory safe by design
   - No buffer overflows
   - Safe concurrency

4. **Use Cases**:
   - **Figma**: Uses WebAssembly for high-performance rendering
   - **Google Earth**: Performance-critical 3D rendering
   - **AutoCAD**: CAD rendering in the browser
   - **Game engines**: Unity, Unreal support WebAssembly

---

### Frontend Framework Comparison

![Choose frontend facilities from the interaction you need. These questions identify required capabilities instead of mapping every requirement to one brand.](./images/frontend-selection-questions.svg)

Different frontend tools exist because applications range from a mostly static page to a large interactive system. A compiler, a runtime UI library, and an application framework make different choices about when work happens and which conventions are included. None guarantees that a page loads quickly: bundle contents, data access, rendering work, and network conditions also matter.

**Check your reasoning:** For this todo app, identify the state changes before choosing a framework. What concrete requirement would justify a larger toolchain?


## Backend Frameworks

### Flask (Python)

**Official Website:** https://flask.palletsprojects.com/
**GitHub:** https://github.com/pallets/flask

**What it is:** A lightweight, flexible Python web framework.

**Key Features:**
- Minimalist core with extensions
- Easy to learn and get started
- Flexible - you choose your tools
- Great for APIs and small to medium applications
- Excellent documentation

**When to Use:**
- ✅ RESTful APIs
- ✅ Small to medium applications
- ✅ Microservices
- ✅ When you need flexibility
- ✅ Rapid prototyping
- ✅ Teams already using Python (data science, ML)

**When NOT to Use:**
- ❌ Very large monolithic applications
- ❌ When you need built-in admin panel and ORM
- ❌ When you want opinionated structure

**Example:**
```python
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

todos = []

@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/api/todos', methods=['POST'])
def add_todo():
    todo = request.json
    todos.append(todo)
    return jsonify(todo), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
```


---

### FastAPI (Python)

**Official Website:** https://fastapi.tiangolo.com/
**GitHub:** https://github.com/tiangolo/fastapi

**What it is:** A modern, fast Python web framework for building APIs with automatic documentation.

**Key Features:**
- Async/await support (high performance)
- Automatic API documentation (Swagger/OpenAPI)
- Type hints and validation (Pydantic)
- Fast development
- Production-ready

**When to Use:**
- ✅ RESTful APIs
- ✅ When performance is critical
- ✅ Microservices
- ✅ When you need automatic API docs
- ✅ ML model serving
- ✅ Real-time applications

**When NOT to Use:**
- ❌ Traditional server-rendered websites
- ❌ When you need built-in admin panel
- ❌ Very simple scripts (overkill)

**Example:**
```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Todo(BaseModel):
    id: int
    text: str
    completed: bool = False

todos: List[Todo] = []

@app.get("/api/todos", response_model=List[Todo])
async def get_todos():
    return todos

@app.post("/api/todos", response_model=Todo)
async def add_todo(todo: Todo):
    todos.append(todo)
    return todo

# Automatic API docs at /docs
```


---

### Express.js (Node.js)

**Official Website:** https://expressjs.com/
**GitHub:** https://github.com/expressjs/express

**What it is:** A minimal and flexible Node.js web application framework.

**Key Features:**
- Minimalist design
- Middleware-based architecture
- Large ecosystem (npm)
- Full-stack JavaScript
- Unopinionated

**When to Use:**
- ✅ RESTful APIs
- ✅ When you want full-stack JavaScript
- ✅ Real-time applications (with Socket.io)
- ✅ Microservices
- ✅ When you need maximum flexibility

**When NOT to Use:**
- ❌ CPU-intensive tasks (Node.js is single-threaded)
- ❌ When you want opinionated structure

**Example:**
```javascript
const express = require('express');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

let todos = [];

app.get('/api/todos', (req, res) => {
  res.json(todos);
});

app.post('/api/todos', (req, res) => {
  const todo = req.body;
  todos.push(todo);
  res.status(201).json(todo);
});

app.listen(8000, () => {
  console.log('Server running on port 8000');
});
```


---

### NestJS (Node.js/TypeScript)

**Official Website:** https://nestjs.com/
**GitHub:** https://github.com/nestjs/nest

**What it is:** A progressive TypeScript framework for building efficient, scalable server-side applications and microservices.

**Key Features:**
- TypeScript-first with full type safety
- Modular architecture (modules, controllers, services)
- Dependency injection
- Built-in support for microservices (gRPC, Message queues)
- Decorators and extensive documentation
- Supports both Express and Fastify under the hood

**When to Use:**
- ✅ Enterprise-grade microservices
- ✅ When you need structure and scalability
- ✅ Teams that prefer TypeScript
- ✅ Complex domain logic requiring strong architecture
- ✅ GraphQL APIs
- ✅ Monorepo with multiple services

**When NOT to Use:**
- ❌ Simple, quick prototypes
- ❌ When team prefers minimal frameworks
- ❌ Very small projects (overhead might be unnecessary)

**Example:**
```typescript
// todo.controller.ts
import { Controller, Get, Post, Body } from '@nestjs/common';
import { TodoService } from './todo.service';
import { CreateTodoDto } from './dto/create-todo.dto';

@Controller('api/todos')
export class TodoController {
  constructor(private readonly todoService: TodoService) {}

  @Get()
  findAll() {
    return this.todoService.findAll();
  }

  @Post()
  create(@Body() createTodoDto: CreateTodoDto) {
    return this.todoService.create(createTodoDto);
  }
}

// todo.service.ts
import { Injectable } from '@nestjs/common';
import { CreateTodoDto } from './dto/create-todo.dto';

interface Todo {
  id: number;
  text: string;
  completed: boolean;
}

@Injectable()
export class TodoService {
  private todos: Todo[] = [];

  findAll(): Todo[] {
    return this.todos;
  }

  create(createTodoDto: CreateTodoDto): Todo {
    const todo: Todo = {
      id: Date.now(),
      ...createTodoDto,
      completed: false
    };
    this.todos.push(todo);
    return todo;
  }
}

// main.ts
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.enableCors();
  await app.listen(8000);
}
bootstrap();
```

**Microservices Support:**
```typescript
// With microservices transport (e.g., gRPC, Redis, NATS)
import { Transport, MicroserviceOptions } from '@nestjs/microservices';

const app = await NestFactory.createMicroservice<MicroserviceOptions>(
  AppModule,
  {
    transport: Transport.REDIS,
    options: {
      host: 'localhost',
      port: 6379,
    },
  },
);
```


---

### Go Frameworks (Gin, Echo, Fiber)

**What it is:** High-performance web frameworks written in Go (Golang), designed for building fast, scalable APIs and microservices.

**Popular Options:**
- **Gin**: Most popular, HTTP router with middleware support
  - **GitHub:** https://github.com/gin-gonic/gin
  - **Website:** https://gin-gonic.com/
- **Echo**: High-performance, minimalist framework
  - **GitHub:** https://github.com/labstack/echo
  - **Website:** https://echo.labstack.com/
- **Fiber**: Express-inspired, extremely fast
  - **GitHub:** https://github.com/gofiber/fiber
  - **Website:** https://gofiber.io/

**Key Features:**
- Compiled language (single binary deployment)
- Excellent performance and low memory footprint
- Built-in concurrency (goroutines)
- Strong typing
- Fast compilation
- Small Docker images

**When to Use:**
- ✅ High-performance APIs and microservices
- ✅ When you need low latency and high throughput
- ✅ Cloud-native applications
- ✅ Real-time systems
- ✅ When you want simple deployment (single binary)
- ✅ CPU-intensive tasks
- ✅ Systems programming background

**When NOT to Use:**
- ❌ Rapid prototyping (slower development than Python/Ruby)
- ❌ When team is unfamiliar with Go
- ❌ Applications requiring rich ecosystem of libraries (Python/Node.js have more)
- ❌ Complex web applications with server-side rendering

**Example (Gin Framework):**
```go
package main

import (
    "net/http"
    "github.com/gin-gonic/gin"
    "github.com/gin-contrib/cors"
)

type Todo struct {
    ID        int    `json:"id"`
    Text      string `json:"text"`
    Completed bool   `json:"completed"`
}

var todos = []Todo{}

func main() {
    router := gin.Default()

    // Development CORS, including JSON preflight requests
    router.Use(cors.Default())

    // Get all todos
    router.GET("/api/todos", func(c *gin.Context) {
        c.JSON(http.StatusOK, todos)
    })

    // Create todo
    router.POST("/api/todos", func(c *gin.Context) {
        var todo Todo
        if err := c.ShouldBindJSON(&todo); err != nil {
            c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
            return
        }
        todos = append(todos, todo)
        c.JSON(http.StatusCreated, todo)
    })

    router.Run(":8000")
}
```

**Example (Echo Framework):**
```go
package main

import (
    "net/http"
    "github.com/labstack/echo/v4"
    "github.com/labstack/echo/v4/middleware"
)

type Todo struct {
    ID        int    `json:"id"`
    Text      string `json:"text"`
    Completed bool   `json:"completed"`
}

var todos = []Todo{}

func main() {
    e := echo.New()

    // Middleware
    e.Use(middleware.CORS())
    e.Use(middleware.Logger())

    // Routes
    e.GET("/api/todos", getTodos)
    e.POST("/api/todos", createTodo)

    e.Start(":8000")
}

func getTodos(c echo.Context) error {
    return c.JSON(http.StatusOK, todos)
}

func createTodo(c echo.Context) error {
    todo := new(Todo)
    if err := c.Bind(todo); err != nil {
        return err
    }
    todos = append(todos, *todo)
    return c.JSON(http.StatusCreated, todo)
}
```

**Example (Fiber Framework):**
```go
package main

import (
    "github.com/gofiber/fiber/v2"
    "github.com/gofiber/fiber/v2/middleware/cors"
)

type Todo struct {
    ID        int    `json:"id"`
    Text      string `json:"text"`
    Completed bool   `json:"completed"`
}

var todos = []Todo{}

func main() {
    app := fiber.New()

    // Middleware
    app.Use(cors.New())

    // Routes
    app.Get("/api/todos", func(c *fiber.Ctx) error {
        return c.JSON(todos)
    })

    app.Post("/api/todos", func(c *fiber.Ctx) error {
        todo := new(Todo)
        if err := c.BodyParser(todo); err != nil {
            return err
        }
        todos = append(todos, *todo)
        return c.Status(201).JSON(todo)
    })

    app.Listen(":8000")
}
```


**Framework Comparison:**

| Feature | Gin | Echo | Fiber |
|---------|-----|------|-------|
| **Middleware** | Excellent | Excellent | Excellent |
| **Documentation** | Good | Excellent | Good |
| **Inspiration** | Martini | - | Express.js |
| **HTTP Router** | httprouter | Custom | fasthttp |

**Why Go for Backend?**

1. **Performance**:
   - Compiled to native code
   - Efficient memory usage
   - Built-in concurrency with goroutines
   - Can handle 10,000+ concurrent connections easily

2. **Deployment**:
   - Single binary (no dependencies)
   - Cross-platform compilation
   - Tiny Docker images (~10MB with Alpine)
   - Easy to containerize

3. **Cloud-Native**:
   - Kubernetes is written in Go
   - Many cloud-native tools use Go (Docker, Prometheus, Terraform)
   - Great for microservices

4. **Developer Experience**:
   - Fast compilation
   - Built-in testing
   - Great tooling (gofmt, go vet)
   - Strong standard library

**Real-World Use Cases:**

- **Docker**: Container platform
- **Kubernetes**: Container orchestration
- **Prometheus**: Monitoring system
- **Terraform**: Infrastructure as code
- **Uber**: Microservices platform
- **Dropbox**: Migration from Python to Go
- **Twitch**: Real-time messaging

---

### Rust Backend Frameworks

**What is Rust?** Rust is a systems programming language focused on safety, speed, and concurrency. It offers memory safety without garbage collection, making it ideal for high-performance backend services.

**Why Rust for Backend?**

1. **Performance**:
   - Compiled to native code like C/C++
   - Zero-cost abstractions
   - No garbage collection pauses
   - Performance comparable to or exceeding Go and C++

2. **Safety**:
   - Memory safety guaranteed at compile time
   - No null pointer exceptions
   - No data races in concurrent code
   - Catches bugs before runtime

3. **Concurrency**:
   - Fearless concurrency model
   - Async/await support
   - Multi-threaded without data races
   - Efficient task scheduling with Tokio runtime

4. **Deployment**:
   - Single static binary
   - Extremely small Docker images (~5MB)
   - Low memory footprint
   - Fast startup times

---

#### Actix-web

**Official Website:** https://actix.rs/
**GitHub:** https://github.com/actix/actix-web

**What it is:** An asynchronous web framework for Rust. Current Actix-web does not require the Actix actor framework.

**Key Features:**
- High-performance asynchronous request handling; benchmark your own workload
- Type-safe request/response handling
- Built-in WebSocket support
- Middleware support
- Async/await with Tokio
- HTTP/2 and HTTP/1.x support
- Excellent for microservices

**When to Use:**
- ✅ Need absolute maximum performance
- APIs where profiling establishes a need to reduce handler and runtime overhead
- ✅ Real-time services
- ✅ Microservices requiring minimal latency
- ✅ CPU-intensive operations
- ✅ When resource efficiency is critical

**When NOT to Use:**
- ❌ Team not familiar with Rust
- ❌ Rapid prototyping (compile times)
- ❌ Simple CRUD apps (might be overkill)

**Example:**
```rust
use actix_web::{web, App, HttpResponse, HttpServer, Responder};
use serde::{Deserialize, Serialize};
use std::sync::Mutex;

#[derive(Serialize, Deserialize, Clone)]
struct Todo {
    id: u32,
    text: String,
    completed: bool,
}

struct AppState {
    todos: Mutex<Vec<Todo>>,
}

#[actix_web::get("/api/todos")]
async fn get_todos(data: web::Data<AppState>) -> impl Responder {
    let todos = data.todos.lock().unwrap();
    HttpResponse::Ok().json(&*todos)
}

#[actix_web::post("/api/todos")]
async fn create_todo(
    todo: web::Json<Todo>,
    data: web::Data<AppState>,
) -> impl Responder {
    let mut todos = data.todos.lock().unwrap();
    todos.push(todo.into_inner());
    HttpResponse::Created().json(&todos.last())
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let app_state = web::Data::new(AppState {
        todos: Mutex::new(vec![]),
    });

    HttpServer::new(move || {
        App::new()
            .app_data(app_state.clone())
            .service(get_todos)
            .service(create_todo)
    })
    .bind(("0.0.0.0", 8000))?
    .run()
    .await
}
```


---

#### Rocket

**Official Website:** https://rocket.rs/
**GitHub:** https://github.com/rwf2/Rocket

**What it is:** A web framework for Rust that makes it simple to write fast, type-safe, secure web applications with minimal boilerplate.

**Key Features:**
- Type-safe routing with procedural macros
- Compile-time correctness guarantees
- Built-in form validation
- Templating support
- Testing library included
- Most ergonomic Rust framework
- JSON/Data serialization built-in

**When to Use:**
- ✅ Need type safety and compile-time guarantees
- ✅ Building APIs with validation
- ✅ Developer experience matters
- ✅ Want easier Rust web framework
- ✅ Microservices with complex routing
- ✅ When correctness is critical

**When NOT to Use:**
- ❌ Need absolute maximum performance (use Actix)
- ❌ Team new to Rust (still steep learning curve)
- ❌ Very simple services

**Example:**
```rust
#[macro_use] extern crate rocket;

use rocket::State;
use rocket::serde::{json::Json, Deserialize, Serialize};
use std::sync::Mutex;

#[derive(Serialize, Deserialize, Clone)]
#[serde(crate = "rocket::serde")]
struct Todo {
    id: u32,
    text: String,
    completed: bool,
}

struct AppState {
    todos: Mutex<Vec<Todo>>,
}

#[get("/api/todos")]
fn get_todos(state: &State<AppState>) -> Json<Vec<Todo>> {
    let todos = state.todos.lock().unwrap();
    Json(todos.clone())
}

#[post("/api/todos", data = "<todo>")]
fn create_todo(todo: Json<Todo>, state: &State<AppState>) -> Json<Todo> {
    let mut todos = state.todos.lock().unwrap();
    let new_todo = todo.into_inner();
    todos.push(new_todo.clone());
    Json(new_todo)
}

#[launch]
fn rocket() -> _ {
    rocket::build()
        .manage(AppState {
            todos: Mutex::new(vec![]),
        })
        .mount("/", routes![get_todos, create_todo])
}
```


---

#### Axum

**Official Website:** https://github.com/tokio-rs/axum (Docs via crates.io)
**GitHub:** https://github.com/tokio-rs/axum

**What it is:** A modern, ergonomic web framework built on Tokio, Tower, and Hyper, designed for the async Rust ecosystem.

**Key Features:**
- Built on Tokio async runtime
- Leverages Tower middleware ecosystem
- Type-safe extractors
- Minimal macros (more explicit)
- Excellent error handling
- WebSocket support
- Compile-time request/response validation
- Modular and composable

**When to Use:**
- ✅ Building on existing Tokio/Tower ecosystem
- ✅ Need flexible middleware composition
- ✅ Want modern async Rust patterns
- ✅ Microservices with complex middleware
- ✅ Integration with other async Rust libraries
- ✅ Prefer explicitness over macros

**When NOT to Use:**
- ❌ Need maximum ergonomics (use Rocket)
- ❌ Need proven stability (newer framework)
- ❌ Team prefers macro-based routing

**Example:**
```rust
use axum::{
    extract::State,
    http::StatusCode,
    routing::{get, post},
    Json, Router,
};
use serde::{Deserialize, Serialize};
use std::sync::{Arc, Mutex};

#[derive(Clone, Serialize, Deserialize)]
struct Todo {
    id: u32,
    text: String,
    completed: bool,
}

type SharedState = Arc<Mutex<Vec<Todo>>>;

async fn get_todos(State(todos): State<SharedState>) -> Json<Vec<Todo>> {
    let todos = todos.lock().unwrap();
    Json(todos.clone())
}

async fn create_todo(
    State(todos): State<SharedState>,
    Json(todo): Json<Todo>,
) -> (StatusCode, Json<Todo>) {
    let mut todos = todos.lock().unwrap();
    todos.push(todo.clone());
    (StatusCode::CREATED, Json(todo))
}

#[tokio::main]
async fn main() {
    let shared_state = Arc::new(Mutex::new(vec![]));

    let app = Router::new()
        .route("/api/todos", get(get_todos))
        .route("/api/todos", post(create_todo))
        .with_state(shared_state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:8000")
        .await
        .unwrap();

    axum::serve(listener, app).await.unwrap();
}
```


---

**Rust Framework Comparison:**

| Feature | Actix-web | Rocket | Axum |
|---------|-----------|--------|------|
| **Async Support** | Yes (Tokio) | Yes (Tokio) | Yes (Tokio) |
| **Type Safety** | Strong | Strongest | Strong |
| **Macros** | Moderate | Heavy | Minimal |
| **Middleware** | Built-in | Built-in | Tower ecosystem |
| **Maturity** | Very Mature | Mature | Newer |

**When to Choose Rust for Backend:**

1. **Performance-Critical Services**: Payment processing, trading systems, game servers
2. **Resource-Constrained Environments**: IoT gateways, edge computing
3. **High-Concurrency Services**: WebSocket servers, real-time data processing
4. **Safety-Critical Systems**: Healthcare, finance, automotive
5. **Microservices Platform**: When 10x performance improvement justifies learning curve

**Real-World Rust Backend Examples:**
- **Discord**: Handles millions of concurrent connections
- **Cloudflare**: Workers platform, ultra-low latency
- **AWS**: Firecracker (serverless), Bottlerocket (container OS)
- **Dropbox**: File sync engine rewrite
- **npm**: Package registry performance improvements
- **Microsoft**: Azure IoT Edge runtime

---

### Java Frameworks

**What is Java?** Java is a mature, statically-typed, object-oriented programming language with a massive ecosystem. It's widely used in enterprise environments and offers excellent performance, reliability, and extensive tooling.

**Why Java for Backend?**

1. **Maturity & Stability**:
   - 25+ years of production use
   - Battle-tested in enterprise environments
   - Extensive libraries and frameworks
   - Long-term support (LTS) versions

2. **Performance**:
   - JVM (Java Virtual Machine) optimizations
   - Just-In-Time (JIT) compilation
   - Excellent garbage collection
   - Comparable to Go in many benchmarks

3. **Enterprise Features**:
   - Strong typing and compile-time checks
   - Excellent IDE support (IntelliJ, Eclipse)
   - Built-in security features
   - Comprehensive monitoring and profiling tools

4. **Ecosystem**:
   - Vast library ecosystem (Maven Central)
   - Enterprise integration patterns
   - Database drivers for all major databases
   - Cloud-native tooling

---

#### Spring Boot

**Official Website:** https://spring.io/projects/spring-boot
**GitHub:** https://github.com/spring-projects/spring-boot

**What it is:** The most popular Java framework for building production-ready microservices and enterprise applications. Part of the Spring ecosystem.

**Key Features:**
- Auto-configuration and convention over configuration
- Embedded server (Tomcat, Jetty, Undertow)
- Production-ready features (health checks, metrics)
- Extensive Spring ecosystem integration
- Dependency injection and IoC container
- Comprehensive testing support

**When to Use:**
- ✅ Enterprise microservices
- ✅ Large-scale systems with complex business logic
- ✅ When you need extensive enterprise integrations
- ✅ RESTful and reactive APIs
- ✅ Teams with Java expertise
- ✅ Long-term maintainability is critical

**When NOT to Use:**
- ❌ Startup time is critical (<1s required)
- ❌ Very memory-constrained environments
- ❌ Simple scripts or CLI tools
- ❌ Team has no Java experience

**Example:**
```java
// TodoController.java
package com.example.todoapi.controller;

import org.springframework.web.bind.annotation.*;
import org.springframework.http.HttpStatus;
import com.example.todoapi.model.Todo;
import java.util.*;

@RestController
@RequestMapping("/api/todos")
@CrossOrigin(origins = "*")
public class TodoController {

    private List<Todo> todos = new ArrayList<>();

    @GetMapping
    public List<Todo> getTodos() {
        return todos;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Todo createTodo(@RequestBody Todo todo) {
        todos.add(todo);
        return todo;
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteTodo(@PathVariable Long id) {
        todos.removeIf(t -> t.getId().equals(id));
    }
}

// Todo.java
package com.example.todoapi.model;

public class Todo {
    private Long id;
    private String text;
    private boolean completed;

    // Constructors, getters, setters
    public Todo() {}

    public Todo(Long id, String text, boolean completed) {
        this.id = id;
        this.text = text;
        this.completed = completed;
    }

    // Getters and setters...
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getText() { return text; }
    public void setText(String text) { this.text = text; }
    public boolean isCompleted() { return completed; }
    public void setCompleted(boolean completed) { this.completed = completed; }
}

// TodoApiApplication.java
package com.example.todoapi;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class TodoApiApplication {
    public static void main(String[] args) {
        SpringApplication.run(TodoApiApplication.class, args);
    }
}
```

---

#### Micronaut

**Official Website:** https://micronaut.io/
**GitHub:** https://github.com/micronaut-projects/micronaut-core

**What it is:** A modern JVM framework designed specifically for microservices and serverless applications with minimal memory footprint and fast startup.

**Key Features:**
- Compile-time dependency injection (no reflection)
- Fast startup time compared to traditional Spring Boot
- Low memory footprint with native images
- Native image support with GraalVM
- Reactive and non-blocking
- Built-in service discovery and distributed tracing

**When to Use:**
- ✅ Cloud-native microservices
- ✅ Serverless functions (AWS Lambda, Google Cloud Functions)
- ✅ When startup time matters
- ✅ Memory-constrained environments
- ✅ Need better performance than Spring Boot
- ✅ Modern reactive applications

**When NOT to Use:**
- ❌ Heavy enterprise integration requirements
- ❌ Team expects Spring-like conventions
- ❌ Need the massive Spring ecosystem

**Example:**
```java
// TodoController.java
package com.example.controller;

import io.micronaut.http.annotation.*;
import io.micronaut.http.HttpStatus;
import com.example.model.Todo;
import java.util.*;

@Controller("/api/todos")
public class TodoController {

    private List<Todo> todos = new ArrayList<>();

    @Get
    public List<Todo> getTodos() {
        return todos;
    }

    @Post
    @Status(HttpStatus.CREATED)
    public Todo createTodo(@Body Todo todo) {
        todos.add(todo);
        return todo;
    }

    @Delete("/{id}")
    @Status(HttpStatus.NO_CONTENT)
    public void deleteTodo(@PathVariable Long id) {
        todos.removeIf(t -> t.getId().equals(id));
    }
}

// Todo.java
package com.example.model;

import io.micronaut.serde.annotation.Serdeable;

@Serdeable
public class Todo {
    private Long id;
    private String text;
    private boolean completed;

    // Constructors, getters, setters
    public Todo() {}

    public Todo(Long id, String text, boolean completed) {
        this.id = id;
        this.text = text;
        this.completed = completed;
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getText() { return text; }
    public void setText(String text) { this.text = text; }
    public boolean isCompleted() { return completed; }
    public void setCompleted(boolean completed) { this.completed = completed; }
}

// Application.java
package com.example;

import io.micronaut.runtime.Micronaut;

public class Application {
    public static void main(String[] args) {
        Micronaut.run(Application.class, args);
    }
}
```

---

#### Quarkus

**Official Website:** https://quarkus.io/
**GitHub:** https://github.com/quarkusio/quarkus

**What it is:** A Kubernetes-native Java framework designed for GraalVM and OpenJDK HotSpot, optimized for containers and cloud deployments.

**Key Features:**
- Supersonic startup time with GraalVM native images
- Very low memory footprint with native compilation
- Live coding (hot reload in development)
- Developer joy focus
- Reactive and imperative programming models
- Extension ecosystem

**When to Use:**
- ✅ Kubernetes-native microservices
- ✅ Serverless/FaaS with extreme startup requirements
- ✅ Container-optimized deployments
- ✅ When memory and startup time are critical
- ✅ Modern cloud-native Java applications
- ✅ Teams wanting modern Java development experience

**When NOT to Use:**
- ❌ Cannot use GraalVM native images (some libraries incompatible)
- ❌ Traditional Java EE applications
- ❌ Team prefers Spring conventions

**Example:**
```java
// TodoResource.java
package com.example.resource;

import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import jakarta.enterprise.context.ApplicationScoped;
import com.example.model.Todo;
import java.util.*;

@ApplicationScoped
@Path("/api/todos")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class TodoResource {

    private List<Todo> todos = new ArrayList<>();

    @GET
    public List<Todo> getTodos() {
        return todos;
    }

    @POST
    public Response createTodo(Todo todo) {
        todos.add(todo);
        return Response.status(Response.Status.CREATED)
                      .entity(todo)
                      .build();
    }

    @DELETE
    @Path("/{id}")
    public Response deleteTodo(@PathParam("id") Long id) {
        todos.removeIf(t -> t.id.equals(id));
        return Response.noContent().build();
    }
}

// Todo.java
package com.example.model;

public class Todo {
    public Long id;
    public String text;
    public boolean completed;

    public Todo() {}

    public Todo(Long id, String text, boolean completed) {
        this.id = id;
        this.text = text;
        this.completed = completed;
    }
}

// Build native image:
// ./mvnw package -Pnative
// Result: native executable optimized for fast startup and low memory usage
```

---

**Java Framework Comparison:**

| Feature | Spring Boot | Micronaut | Quarkus |
|---------|-------------|-----------|---------|
| **DI/IoC** | Runtime (reflection) | Compile-time | Compile-time |
| **Reactive Support** | Spring WebFlux | Built-in | Built-in |
| **Native Image** | GraalVM support | GraalVM | GraalVM (optimized) |
| **Ecosystem** | Massive (Spring ecosystem) | Growing | Growing |
| **Maturity** | Very Mature (15+ years) | Mature | Mature |
| **Primary Focus** | Enterprise apps | Cloud microservices | Cloud-native + serverless |

**When to Choose Java for Backend:**

1. **Enterprise Requirements**: Large organizations with existing Java infrastructure
2. **Complex Business Logic**: Domain-driven design, complex transactions
3. **Team Expertise**: Team already knows Java and wants modern frameworks
4. **Long-term Stability**: Projects that will run for 5-10+ years
5. **Integration Heavy**: Need to integrate with many enterprise systems
6. **Regulated Industries**: Banking, healthcare, insurance (mature, well-tested frameworks)

**Real-World Java Backend Examples:**
- **Netflix**: Microservices platform (Spring Boot)
- **Uber**: Marketplace services (Java + Spring)
- **LinkedIn**: Backend services (Play Framework, Spring)
- **Twitter**: Some services use JVM-based frameworks
- **Amazon**: Many internal services use Java
- **Banks & Financial Services**: Most use Java extensively (JPMorgan, Goldman Sachs)

**Cloud-Native Java Performance:**

Modern frameworks like Quarkus and Micronaut have significantly improved Java's cloud-native characteristics:
- **Faster Startup**: GraalVM native images can start in milliseconds instead of seconds
- **Lower Memory**: Native compilation reduces memory footprint dramatically compared to traditional JVM
- **Container-Optimized**: Designed specifically for containerized and serverless deployments

---

### Backend Framework Comparison (Microservices Focus)

![Backend choices start with constraints, not a leaderboard. The examples describe ecosystems and evaluation questions, not guaranteed throughput.](./images/backend-selection-questions.svg)

A framework can remove repetitive routing, serialization, and integration work, but its abstractions also have a learning and maintenance cost. A database-bound endpoint can remain slow after changing languages because its dominant cost is elsewhere. Start with the team's constraints and a representative operation, then measure the complete request path before assigning a performance problem to the framework.

**Check your reasoning:** If 90% of a request's time is spent waiting for a query, what improvement could replacing only the HTTP handler possibly deliver?


**Note:** This is a selection of frameworks, not an exhaustive compatibility list. Django and Rails can also be used to build microservices.


## Decision Framework

### Frontend Selection Criteria

| Criterion | React | Vue | Svelte | Angular | Rust/WASM (Yew) |
|-----------|-------|-----|--------|---------|-----------------|
| **TypeScript Support** | Excellent | Excellent | Excellent | Native | N/A (Rust) |
| **Mobile Development** | React Native | NativeScript | Svelte Native | Ionic | Tauri (native) |
| **Corporate Backing** | Meta | Independent | Independent | Google | Independent |
| **Common Use Cases** | Most web apps | Incremental adoption | Small bundles | Large teams | Games, CAD, ML inference |

### Backend Selection Criteria (Microservices)

| Criterion | Flask | FastAPI | Express | NestJS | Go (Gin) | Rust (Actix) | Java (Spring Boot) |
|-----------|-------|---------|---------|--------|----------|--------------|-------------------|
| **Async Support** | Basic | Excellent | Excellent | Excellent | Excellent (goroutines) | Excellent (Tokio) | Good (WebFlux) |
| **Type Safety** | Optional | Good (Pydantic) | Optional (TS) | Excellent (TypeScript) | Excellent (Go) | Strongest (Rust) | Excellent (Java) |
| **API Docs** | Manual/Swagger | Automatic (Swagger) | Manual/Swagger | Automatic (Swagger) | Manual/Swagger | Manual/utoipa | SpringDoc/Swagger |
| **Deployment** | Standard | Standard | Standard | Standard | Single Binary (~20MB) | Single Binary (~5MB) | JAR/Container (~50MB) |
| **Ecosystem** | Large | Growing | Huge | Large | Large | Growing | Massive (Maven Central) |
| **Common Use Cases** | Simple APIs | ML/Data services | Real-time apps | Enterprise services | Cloud-native | Performance-critical | Enterprise/Banking |

## AI-Assisted Development Friendliness

The ratings below are qualitative teaching opinions, not measured benchmarks or evidence about an assistant's training data. Results depend on the model, framework version, task, and available project context. Verify generated code against current documentation, compiler checks, and tests.

### Frontend Frameworks

| Framework | AI Friendliness | Rating | Why |
|-----------|-----------------|--------|-----|
| **React** | ⭐⭐⭐⭐⭐ Excellent | 5/5 | Widely documented examples, clear functional patterns, hooks are straightforward, consistent conventions. AI excels at React code generation. |
| **Vue** | ⭐⭐⭐⭐ Very Good | 4/5 | Good documentation coverage, clear template syntax, options/composition API well understood. Check generated code against your Vue version. |
| **Svelte** | ⭐⭐⭐ Good | 3/5 | Simpler syntax helps, but version-specific syntax. Special reactive syntax (`$:`) can be tricky. AI handles basic patterns well. |
| **Angular** | ⭐⭐ Fair | 2/5 | Complex architecture, heavy decorators, RxJS patterns challenging for AI. More boilerplate means more room for errors. Better for experienced teams. |
| **Rust/WASM** | ⭐⭐ Fair | 2/5 | Ownership/borrowing/lifetimes are difficult for AI to reason about correctly. Type system complexity. Better with human Rust expertise. |

**Recommendation**: React and Vue are the most AI-friendly choices for rapid development with AI assistance.

### Backend Frameworks

| Framework | AI Friendliness | Rating | Why |
|-----------|-----------------|--------|-----|
| **Flask** | ⭐⭐⭐⭐⭐ Excellent | 5/5 | Simple, minimal, explicit patterns. AI generates clean Flask code easily. Extensive public documentation. Perfect for rapid prototyping with AI. |
| **FastAPI** | ⭐⭐⭐⭐⭐ Excellent | 5/5 | Type hints provide clear intent, modern Python syntax. AI leverages types for accurate code generation. Automatic validation helps catch errors. |
| **Express** | ⭐⭐⭐⭐⭐ Excellent | 5/5 | Minimal, widely used, widely documented examples. Simple middleware patterns. AI handles Express naturally. |
| **NestJS** | ⭐⭐⭐ Good | 3/5 | TypeScript helps AI understand intent. Decorators and DI add complexity. Works well once patterns established. |
| **Go (Gin/Echo/Fiber)** | ⭐⭐⭐⭐ Very Good | 4/5 | Explicit, typed, simple syntax. Go's simplicity helps AI generate correct code. Error handling can be verbose but clear. |
| **Rust (Actix/Rocket/Axum)** | ⭐⭐ Fair | 2/5 | Ownership/borrowing/lifetimes challenge AI. Complex type inference. AI can help with patterns but needs human review for correctness. |
| **Spring Boot** | ⭐⭐ Fair | 2/5 | Heavy annotations, lots of boilerplate, complex configuration. AI struggles with dependency injection wiring and Spring magic. |
| **Micronaut/Quarkus** | ⭐⭐⭐ Good | 3/5 | Less boilerplate than Spring Boot. Cleaner patterns. Still Java verbosity. AI handles better than traditional Spring. |

**Recommendation**: Flask, FastAPI, and Express are the most AI-friendly backend choices. Go frameworks also work very well with AI assistance.

### Key Factors for AI Friendliness

**What Makes a Framework AI-Friendly:**

1. **Type Information**: TypeScript, Python type hints, Go, Java help AI understand intent
   - ✅ Best: TypeScript (NestJS), FastAPI (Pydantic), Go
   - ⚠️ Okay: JavaScript (can add JSDoc), Python (optional types)
   - ❌ Challenging: Rust (complex type system)

2. **Explicit Over Implicit**: Clear, readable code beats "magic"
   - ✅ Best: Flask, Express, Go frameworks
   - ⚠️ Okay: FastAPI (Pydantic magic is well-defined)
   - ❌ Challenging: Spring Boot (heavy dependency injection, annotations)

3. **Training Data Coverage**: Available documentation and examples can help an assistant follow established patterns
   - ✅ Best: React, Express, Flask (massive representation)
   - ⚠️ Okay: Vue, FastAPI, NestJS (good coverage)
   - ❌ Less: Svelte, Rust/WASM (smaller communities)

4. **Error Messages**: Clear errors help AI fix mistakes
   - ✅ Best: TypeScript, Rust (excellent compiler errors)
   - ⚠️ Okay: Go, Python
   - ❌ Challenging: JavaScript runtime errors

5. **Pattern Consistency**: Predictable patterns = reliable generation
   - ✅ Best: Go (one obvious way), React hooks (clear patterns)
   - ⚠️ Okay: Vue (options vs composition), Python (many ways to do things)
   - ❌ Challenging: Spring Boot (many configuration styles)

### Practical AI-Assisted Development Scenarios

**Best Combinations for AI Pair Programming:**

| Scenario | Frontend | Backend | Why |
|----------|----------|---------|-----|
| **Rapid Prototyping** | React | Flask or Express | AI generates clean, working code fast. Minimal boilerplate. |
| **Production MVP** | React or Vue | FastAPI | Type safety catches AI mistakes. Great developer experience. |
| **Type-Safe Stack** | React + TypeScript | NestJS | End-to-end types help AI maintain consistency. |
| **High Performance** | React | Go (Gin) | Go's simplicity + React's popularity = good AI support. |
| **Learning Project** | React | Flask or FastAPI | AI can explain and generate educational code easily. |

**Avoid for AI-Heavy Development:**
- Angular + Spring Boot: Too much complexity, boilerplate, and "magic" for optimal AI assistance
- Rust full-stack: Ownership model challenging for AI to reason about correctly
- Complex NestJS microservices: DI and decorators add cognitive load for AI

### Tips for Working with AI on Any Framework

1. **Be Explicit**: Add type annotations even when optional (TypeScript, Python type hints)
2. **Use Comments**: Describe intent, AI uses this to generate better code
3. **Prefer Simple Patterns**: Avoid clever abstractions until needed
4. **Validate AI Output**: Always review generated code, especially for:
   - Security (authentication, input validation)
   - Error handling
   - Edge cases
   - Performance implications
5. **Iterative Refinement**: Ask AI to fix/improve generated code in small steps

## Real-World Use Cases (Microservices Architecture)

These are illustrative combinations for comparing responsibilities and tradeoffs, not applications included in this repository or a requirement to assign a different language to each service. For every example, identify the operation and its constraints before judging the suggested tools. Framework choice alone does not establish correctness, latency, or throughput.

### E-Commerce Microservices Platform

**Frontend:** Next.js (React with SSR)
- SEO-optimized product pages
- Complex state management
- Server-side rendering

**Backend:** Microservices with multiple frameworks
- **Product Service**: FastAPI (Python) - High-performance product catalog
- **User Service**: Go (Gin) - Authentication and user management
- **Order Service**: NestJS (TypeScript) - Complex order processing logic
- **Payment Service**: Go (Echo) - High-security payment processing

![An e-commerce design separates business responsibilities. Branches show request routing to responsibilities, not a prescribed framework for each one.](./images/ecommerce-service-responsibilities.svg)

This is one possible division of an application, not a requirement to use four languages or databases. Each boundary should justify independent change, ownership, or scale. An order can cross several boundaries, so the design must say what happens when payment or notification processing fails. A gateway reduces the number of public entry points without making those distributed operations atomic.

**Check your reasoning:** Which service owns the decision that an order is paid, and how would another service learn that fact without editing its private tables?


**Why this architecture:**
- Each service uses the best framework for its specific needs
- FastAPI for data-heavy product catalog
- Go for high-performance auth and payments
- NestJS for complex business logic in orders

---

### Real-Time Chat Application

**Frontend:** React or Vue
- Real-time updates
- Component-based for chat rooms/messages

**Backend:** Express.js with Socket.io
- WebSocket support
- Non-blocking I/O
- Full-stack JavaScript

![Chat combines live events with durable history. Live communication and stored history solve different requirements.](./images/chat-events-and-storage.svg)

Repeated HTTP polling is one way to discover new messages; a persistent event connection can reduce repeated request overhead and deliver updates promptly. That connection is not message durability. If a client disconnects, the application still needs rules for stored history, missed events, and duplicate handling. Socket.IO is an additional protocol and library ecosystem, not simply another name for raw WebSocket.

**Check your reasoning:** If a message is sent while a recipient is offline, which component must retain it and how does the recipient catch up?


---

### Machine Learning Dashboard

**Frontend:** Svelte
- Data visualization
- Small bundle size
- Fast updates for real-time metrics

**Backend:** FastAPI
- Serve ML models
- High performance
- Automatic API documentation
- Type validation

![A model dashboard separates display, inference, and results. Arrows show responsibility boundaries, not a claim that one framework accelerates the model.](./images/model-dashboard-request-path.svg)

A charting library solves display work; an API framework solves request handling; a model runtime performs inference. They are different technologies because their responsibilities differ. Making the HTTP handler asynchronous does not automatically make CPU-heavy inference faster. If work exceeds a useful request duration, a queued job with a status endpoint may be more suitable than holding one request open.

**Check your reasoning:** For an inference job that takes several minutes, what should the browser display and how could it retrieve progress without repeating the computation?


---

### Enterprise Internal Tool (Microservices)

**Frontend:** Angular
- TypeScript for type safety
- Large team needs structure
- Component-based architecture

**Backend:** NestJS Microservices
- TypeScript across the stack
- Modular architecture
- Built-in microservices support (gRPC, message queues)
- Dependency injection for testability

![An internal tool still needs explicit trust and data boundaries. Branches are business APIs; identity and authorization remain explicit responsibilities.](./images/internal-tool-service-boundaries.svg)

Shared framework conventions can help teams implement these APIs consistently, while a central identity provider avoids inventing separate login systems. Neither choice removes authorization inside each business operation. A reporting view also needs a data-sharing contract: directly reading another service's private tables can make independent schema changes impossible.

**Check your reasoning:** Does a user who can open the internal dashboard automatically have permission to read every employee or finance record? Where is that decided?


**Why NestJS:**
- TypeScript across frontend and backend
- Built-in microservices patterns
- Easy to scale and maintain
- Strong typing reduces bugs in large codebases

---

### Microservices Platform

**Frontend:** React
- Modern UI
- API gateway communication
- Service-agnostic

**Backend:** Go (Gin/Echo)
- High-performance microservices
- Low resource footprint
- Single binary deployment
- Built-in concurrency

![A platform uses contracts to connect independently changing parts. The branches represent independently managed contracts and their privately owned data.](./images/platform-api-and-data-ownership.svg)

Using different Go HTTP libraries is possible, but that diversity is not what makes the system a microservice architecture. Independent deployment depends on compatible interfaces, explicit ownership, and operational support. Each extra framework adds maintenance work, so a shared choice can be preferable unless a service has a concrete reason to differ.

**Check your reasoning:** What would break if the Product API renamed a field used by Orders? How could a compatible transition avoid a coordinated release?


**Why Go for Microservices?**
- Fast startup time (critical for scaling)
- Small memory footprint (cost-effective)
- Easy deployment (single binary)
- Excellent concurrency (goroutines)
- Strong typing (fewer runtime errors)

---

### High-Performance Trading Platform (Rust for Performance-Critical Services)

**Frontend:** React with WASM modules for charting
- Real-time data visualization
- WebAssembly for intensive chart calculations
- Sub-millisecond UI updates

**Backend:** Polyglot microservices emphasizing performance
- **Market Data Service**: Rust (Actix-web) - Ultra-low latency market data processing
- **Order Matching Engine**: A separate responsibility with explicit consistency, recovery, and measured latency requirements; the framework alone does not establish its throughput
- **Risk Management**: Go (Gin) - Real-time risk calculations
- **User Service**: NestJS (TypeScript) - Account management and auth
- **Analytics Service**: FastAPI (Python) - ML-based trading signals

![A trading example starts with correctness and latency budgets. Cards identify constraints that must be measured and designed; no throughput guarantee is implied.](./images/trading-system-design-questions.svg)

This is an illustrative workload decomposition, not a production trading specification or a framework benchmark. Different paths have different correctness and latency needs. A lower-overhead runtime can be relevant on a measured hot path, but a language name cannot guarantee a request rate, market-data freshness, or end-to-end deadline. Network, storage, queueing, and recovery behavior all belong in the evaluation.

**Check your reasoning:** If a risk check times out after an order was accepted, which component records the outcome and prevents a duplicate retry from creating another order?


**Why Rust for Critical Services:**
- **Sub-millisecond latency**: Rust's zero-cost abstractions and lack of garbage collection enable predictable low latency
- **Memory safety**: Prevents many memory errors in safe Rust; panics, resource exhaustion, and logic bugs can still cause failures
- **Predictable performance**: No garbage collection pauses that could delay critical operations
- **Resource efficiency**: Compiled native code with minimal runtime overhead
- **Zero-downtime**: Reliability for 24/7 trading operations

**Real-World Examples:**
- **Coinbase**: Exchange matching engine uses Rust
- **Discord**: Rust for message routing (handles millions of concurrent connections)
- **Figma**: Multiplayer engine uses Rust + WebAssembly

---

### Real-Time Gaming Backend (Rust for Low-Latency Services)

**Frontend:** React or Rust/WASM (Yew) for game client
- Real-time game state rendering
- WebAssembly for game physics (if using browser)
- Low-latency input handling

**Backend:** Rust-focused microservices
- **Game Server**: Rust (Axum) - Real-time game loop, 60+ ticks/s
- **Matchmaking**: Go (Fiber) - Fast player matching
- **User Service**: NestJS - Authentication, profiles
- **Leaderboards**: Redis + Go (Gin) - Real-time rankings

![A game backend has several kinds of state and timing. Responsibilities are illustrative; tick rates and latency targets require a specified workload.](./images/game-backend-responsibilities.svg)

A game simulation loop, an account API, and a leaderboard are different workloads, so one deployment or technology does not have to serve all of them. A fast simulation implementation cannot eliminate internet delay, and a WebAssembly client does not imply a particular network latency. Start with a measured update budget and distinguish temporary session state from progress that must survive a restart.

**Check your reasoning:** Which data should survive a game-server crash, and which must be reconstructed when a player reconnects?


**Why Rust for Game Servers:**
- **Consistent frame times**: No GC pauses during gameplay
- **High tick rate**: Maintain 60+ game updates/second
- **Concurrent connections**: Handle thousands of players per server
- **Memory efficiency**: Run more game instances per machine
- **Safety**: Reduce memory errors; error handling and testing remain necessary

---

## Full-Stack Frameworks

Some frameworks handle both frontend and backend:

![Full-stack frameworks still split server and browser code. Arrows show what crosses the network; the dashed arrow is a later request from the browser.](./images/fullstack-server-browser-split.svg)

### Next.js (React)

**Official Website:** https://nextjs.org/
**GitHub:** https://github.com/vercel/next.js

- React framework with server-side rendering
- API routes built-in
- Automatic code splitting
- Best for: SEO-critical React apps

```javascript
// pages/api/todos.js - API route
export default function handler(req, res) {
  const todos = getTodos(); // Your logic
  res.json(todos);
}

// pages/index.js - React component with SSR
export async function getServerSideProps() {
  const todos = await fetch('http://localhost:3000/api/todos').then(r => r.json());
  return { props: { todos } };
}

export default function Home({ todos }) {
  return <TodoList todos={todos} />;
}
```

### SvelteKit (Svelte)

**Official Website:** https://kit.svelte.dev/

**GitHub:** https://github.com/sveltejs/kit

- Full-stack Svelte framework
- Server-side rendering and static site generation
- File-based routing with API endpoints
- Best for: Performance-focused Svelte apps with SSR

```javascript
// src/routes/api/todos/+server.js - API endpoint
export async function GET() {
  const todos = getTodos(); // Your logic
  return new Response(JSON.stringify(todos), {
    headers: { 'content-type': 'application/json' }
  });
}

export async function POST({ request }) {
  const todo = await request.json();
  // Add todo logic
  return new Response(JSON.stringify(todo), { status: 201 });
}
```

```svelte
<!-- src/routes/+page.svelte - Page component (legacy Svelte syntax) -->
<script>
  export let data;
</script>

<h1>Todos</h1>
<ul>
  {#each data.todos as todo (todo.id)}
    <li>{todo.text}</li>
  {/each}
</ul>
```

Create a separate `src/routes/+page.js` file for the [SvelteKit load function](https://svelte.dev/docs/kit/load):

```javascript
export async function load({ fetch }) {
  const res = await fetch('/api/todos');
  const todos = await res.json();
  return { todos };
}
```

### Nuxt.js (Vue)

**Official Website:** https://nuxt.com/
**GitHub:** https://github.com/nuxt/nuxt

- Vue framework with SSR
- File-based routing with server middleware
- Similar to Next.js but for Vue

```vue
<!-- pages/index.vue - Vue component with SSR -->
<template>
  <div>
    <h1>Todos</h1>
    <TodoList :todos="todos" />
  </div>
</template>

<script setup>
const { data: todos } = await useFetch('/api/todos')
</script>

```

Create the API endpoint in a separate `server/api/todos.js` file:

```javascript
export default defineEventHandler(async (event) => {
  const todos = getTodos(); // Implement your storage logic
  return todos;
});
```

## Common Mistakes

### 1. Choosing Based on Hype

**Mistake:** "Everyone is using React, so we must too!"

**Better:** Evaluate based on your specific needs, team skills, and project requirements.

### 2. Using Enterprise Framework for Simple Project

**Mistake:** Using Angular for a simple landing page

**Better:** Match complexity of framework to complexity of project

### 3. Ignoring Team Experience

**Mistake:** Choosing Svelte when team knows React well

**Better:** Consider learning curve and team productivity

### 4. Not Considering Ecosystem

**Mistake:** Choosing framework without checking if libraries you need exist

**Better:** Research ecosystem for your specific needs (auth, forms, charts, etc.)

### 5. Premature Optimization

**Mistake:** "We need to use Go because it's fastest!"

**Better:** Developer productivity often more important than raw performance. Optimize when you have actual performance problems.

## Recommendations by Project Type (Microservices Focus)

| Project Type | Frontend | Backend | Why |
|--------------|----------|---------|-----|
| **Simple API** | None or minimal | Flask/FastAPI | Quick, lightweight, async support |
| **Todo App (Tutorial)** | Vanilla JS or React | Flask | Learning fundamentals |
| **E-commerce Platform** | Next.js (React) | FastAPI + Go + NestJS | Multiple services for different needs |
| **Real-Time Chat** | React/Vue | Express/NestJS + Socket.io | WebSockets, event-driven |
| **ML/Data Dashboard** | Svelte/React | FastAPI | Performance, async, ML model serving |
| **Enterprise Services** | Angular | NestJS | TypeScript end-to-end, strong architecture |
| **Payment Processing** | Any | Go (Gin/Echo) | Security, performance critical |
| **User Authentication** | Any | Go/NestJS | High security, scalable |
| **Mobile + Web** | React | FastAPI/Go | React Native reuse, fast APIs |
| **Microservices Platform** | React/Vue | Go (Gin/Echo/Fiber) | Cloud-native, low resources |
| **High-Traffic API** | Any | Go/FastAPI | Low latency, high throughput |
| **IoT/Real-Time System** | React/Svelte | Go (Fiber) | Concurrency, real-time performance |
| **Data Analytics Service** | React | FastAPI | Python data libs, async processing |
| **Content API** | Any | Express/FastAPI | Fast development, flexible |

**Key Principle:** Choose based on service requirements, not monolithic thinking. Different services can use different frameworks!

## What We're Using in This Course

In this tutorial series, we use:

- **Frontend:**
  - Tutorial 1: Vanilla JavaScript (fundamentals)
  - Tutorial 9: React (modern framework)

- **Backend:**
  - Flask (simple, Python-based, easy to learn)

- **Why these choices:**
  - Flask: Lightweight, great for learning APIs
  - Vanilla JS first: Understand fundamentals before frameworks
  - React: Most popular, excellent job market, large ecosystem

## Next Steps

1. **Tutorial 1**: Build with vanilla JavaScript and Flask (fundamentals)
2. **Tutorial 2**: Containerize with Docker
3. **Tutorial 3**: Understand databases
4. **[Tutorial 4b](../04b-architectures/README.md)**: Compare software architectures and their tradeoffs
5. **Tutorial 5**: Understand microservices and Kubernetes
6. **Tutorials 6-7**: Set up cluster access and deploy an application
7. **Tutorial 9**: Rebuild with React (see framework benefits)

## Further Reading

**Frontend:**
- [React Documentation](https://react.dev/)
- [Vue.js Guide](https://vuejs.org/guide/)
- [Svelte Tutorial](https://svelte.dev/tutorial)
- [Angular Docs](https://angular.io/docs)

**Backend (Microservices-Friendly):**
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Express.js Guide](https://expressjs.com/en/guide/routing.html)
- [NestJS Documentation](https://docs.nestjs.com/)
- [NestJS Microservices](https://docs.nestjs.com/microservices/basics)
- [Gin Web Framework](https://gin-gonic.com/docs/)
- [Echo Framework](https://echo.labstack.com/guide/)
- [Fiber Documentation](https://docs.gofiber.io/)
- [Go by Example](https://gobyexample.com/)

**Microservices Architecture:**
- [Microservices.io](https://microservices.io/)
- [Building Microservices Book](https://samnewman.io/books/building_microservices_2nd_edition/)

Remember: **In microservices, choose the best framework for EACH service's specific needs, not one framework for everything!**
