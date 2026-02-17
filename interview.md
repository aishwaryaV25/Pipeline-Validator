# Frontend Assignment — Preparation Notes

## Overview
This repository contains a React frontend (React Flow) and a FastAPI backend. I implemented:

- A `BaseNode` abstraction to unify node rendering and handle management.
- Refactored existing nodes (`Input`, `Text`, `LLM`, `Output`) to use `BaseNode`.
- Added five demo nodes: `Uppercase`, `Lowercase`, `Concat`, `Split`, and `No-op`.
- Improved styling with a dark professional theme, variables and CSS tokens in `frontend/src/index.css`.
- Enhanced `Text` node to dynamically resize with text and auto-create left-side Handles when variables are used (syntax `{{varName}}`).
- Wired frontend `Submit` button to send pipeline (nodes + edges) to backend `/pipelines/parse` and display an alert with node/edge counts and DAG status.
- Backend endpoint implemented in `backend/main.py` with CORS, JSON parsing, counts, and DAG detection (Kahn's algorithm).


## File Highlights
- `frontend/src/nodes/baseNode.js`: shared node layout, accepts `leftHandles`, `rightHandles`, `title`, `children`, and `style`.
- `frontend/src/nodes/textNode.js`: uses `BaseNode`, parses `{{var}}`, creates left handles, and auto-resizes.
- `frontend/src/submit.js`: posts pipeline to `http://localhost:8000/pipelines/parse` and alerts results.
- `backend/main.py`: new POST `/pipelines/parse` returning `{ num_nodes, num_edges, is_dag }`.


## How I approached the task
1. Start with a small, well-scoped abstraction (`BaseNode`) focused on consistent layout and handle rendering.
2. Refactor existing nodes to use the abstraction (smaller, easier to read files).
3. Demonstrate the abstraction with several small demo nodes.
4. Improve UX on the `Text` node (dynamic sizing + variable handles) because it has the most behavior.
5. Integrate frontend and backend with a small, robust API and DAG check.
6. Style the app with CSS variables and clean component-level styles for a professional look.


## Running locally (quick steps)
1. Frontend

```bash
cd frontend
npm install
npm start
```

2. Backend

```bash
cd backend
# create virtualenv and install fastapi + uvicorn
pip install fastapi uvicorn
uvicorn main:app --reload
```

Open `http://localhost:3000` for frontend and ensure backend runs on `http://localhost:8000`.


## What to test
- Drag nodes from the toolbar into the canvas and connect handles.
- Add a `Text` node and type `Hello {{name}}` — you should see a left handle for `name`.
- Increase text length and observe the node width/height adjust.
- Click `Submit` — you should receive an alert showing `Nodes`, `Edges`, and `Is DAG`.


## Design decisions and tradeoffs
- I kept `BaseNode` intentionally minimal: it handles handle placement and styling. More features (label positions, ports layout engine) can be added later.
- `TextNode` uses a simple regex to detect variables. This keeps runtime cheap and predictable.
- For DAG detection I used Kahn's algorithm on node ids referenced by edges; edges that reference missing nodes are ignored.
- CORS is permissive for `http://localhost:3000` to allow local dev.


## Possible improvements
- Persist pipelines to a backend store and provide validation errors for disconnected graphs.
- Add visual badges on nodes for missing inputs or cycles.
- Add animations and improved asset imagery for a richer branding.
- Add unit tests for DAG detection and variable parsing.


## Interview talking points
- Explain why a `BaseNode` abstraction improves developer velocity and reduces duplication.
- Describe the `TextNode` UX improvements: dynamic sizing and variable handles, and how regex was used to detect variables.
- Walk through the backend integration: POST body shape, counts computation, Kahn's algorithm for DAG detection.
- Point out how CSS variables make theming straightforward and simple to change in one place.


## Notes for the reviewer
- I focused on code clarity and small, safe changes; each node is now concise and easy to extend.
- If you'd like, I can add unit tests for the backend DAG detection and a small Cypress/E2E test for submit flow.


---

Good luck with testing — tell me if you want a different color palette, more nodes, or additional validation/UX details.
