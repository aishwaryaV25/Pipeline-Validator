from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow local frontend dev server to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def read_root():
    return {'Ping': 'Pong'}


def _is_dag(nodes, edges):
    # nodes: list of node objects with 'id'
    # edges: list of edge objects with 'source' and 'target'
    if not nodes:
        return True
    
    node_ids = {n.get('id') for n in nodes}
    adj = {nid: [] for nid in node_ids}
    adj_reverse = {nid: [] for nid in node_ids}
    indeg = {nid: 0 for nid in node_ids}

    for e in edges:
        src = e.get('source')
        tgt = e.get('target')
        if src in node_ids and tgt in node_ids:
            adj[src].append(tgt)
            adj_reverse[tgt].append(src)
            indeg[tgt] += 1

    # Check for cycles using Kahn's algorithm
    indeg_copy = indeg.copy()
    q = [n for n, d in indeg_copy.items() if d == 0]
    visited_cycle_check = 0
    from collections import deque
    dq = deque(q)
    while dq:
        u = dq.popleft()
        visited_cycle_check += 1
        for v in adj.get(u, []):
            indeg_copy[v] -= 1
            if indeg_copy[v] == 0:
                dq.append(v)

    # If not all nodes visited, there's a cycle
    if visited_cycle_check != len(node_ids):
        return False
    
    # If no edges at all and multiple nodes, it's disconnected
    if len(edges) == 0 and len(node_ids) > 1:
        return False
    
    # If no edges and single node, it's valid
    if len(edges) == 0:
        return True
    
    # Find connected components using union-find or BFS
    visited_global = set()
    components = 0
    
    for start_node in node_ids:
        if start_node not in visited_global:
            # BFS to find all connected nodes (ignoring edge direction)
            component = set()
            dq = deque([start_node])
            component.add(start_node)
            while dq:
                u = dq.popleft()
                for v in adj.get(u, []):
                    if v not in component:
                        component.add(v)
                        dq.append(v)
                for v in adj_reverse.get(u, []):
                    if v not in component:
                        component.add(v)
                        dq.append(v)
            
            visited_global.update(component)
            components += 1
    
    # For a valid pipeline DAG, all nodes must be in one connected component
    return components == 1


@app.post('/pipelines/parse')
def parse_pipeline(payload: dict = Body(...)):
    nodes = payload.get('nodes', []) or []
    edges = payload.get('edges', []) or []

    num_nodes = len(nodes)
    num_edges = len(edges)
    is_dag = _is_dag(nodes, edges)

    return { 'num_nodes': num_nodes, 'num_edges': num_edges, 'is_dag': is_dag }
