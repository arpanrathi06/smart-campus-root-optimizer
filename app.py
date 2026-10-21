from flask import Flask, jsonify, request, send_from_directory
import heapq

app = Flask(__name__, static_folder="static", static_url_path="/static")
BUILDINGS = [
    "Main Gate", "Ganga Building", "Saraswati Building", "Shriraj Canteen",
    "Agastya KRC", "Dnyaneshwara Block", "Vivekanand Auditorium",
    "Encave Cafeteria-1", "Vashistha Block", "East Gate", "Sports Complex",
    "Aaryabhata Block", "Encave Cafeteria-2", "Chanakya Block",
    "Admission Center", "Mullik Gate"
]
EDGES = [
    (0,1,90), (0,2,110), (1,2,70), (2,3,100), (3,4,130), (1,5,280),
    (4,5,150), (5,6,110), (5,7,140), (6,7,80), (7,8,200), (8,9,150),
    (9,10,110), (10,11,200), (8,11,160), (7,12,180), (11,12,80),
    (11,13,100), (12,13,80), (13,14,200), (9,14,250), (14,15,100)
]
ADJ = [[] for _ in BUILDINGS]
for u, v, w in EDGES:
    ADJ[u].append((v, w))
    ADJ[v].append((u, w))

def shortest_path(source, destination):
    dist = [float("inf")] * len(BUILDINGS)
    parent = [-1] * len(BUILDINGS)
    dist[source] = 0
    queue = [(0, source)]
    while queue:
        current_dist, u = heapq.heappop(queue)
        if current_dist != dist[u]:
            continue
        for v, weight in ADJ[u]:
            candidate = current_dist + weight
            if candidate < dist[v]:
                dist[v] = candidate
                parent[v] = u
                heapq.heappush(queue, (candidate, v))
    if dist[destination] == float("inf"):
        return None
    path = []
    node = destination
    while node != -1:
        path.append(node)
        node = parent[node]
    path.reverse()
    return {"source": source, "destination": destination, "distance": int(dist[destination]),
            "path_indices": path, "path": [BUILDINGS[i] for i in path]}

def prim_mst():
    n = len(BUILDINGS)
    used = [False] * n
    best = [float("inf")] * n
    parent = [-1] * n
    best[0] = 0
    queue = [(0, 0)]
    edges = []
    total = 0
    while queue:
        weight, u = heapq.heappop(queue)
        if used[u]:
            continue
        used[u] = True
        if parent[u] != -1:
            edges.append({"from": parent[u], "to": u, "from_name": BUILDINGS[parent[u]],
                          "to_name": BUILDINGS[u], "distance": weight})
            total += weight
        for v, w in ADJ[u]:
            if not used[v] and w < best[v]:
                best[v] = w
                parent[v] = u
                heapq.heappush(queue, (w, v))
    return {"edges": edges, "total_distance": total, "connected": all(used)}

@app.get("/")
def home():
    return send_from_directory("static", "index.html")

@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "Smart Campus Route Optimizer"})

@app.get("/api/buildings")
def buildings():
    return jsonify([{"index": i, "name": name} for i, name in enumerate(BUILDINGS)])

@app.get("/api/adjacency")
def adjacency():
    return jsonify([{"index": i, "name": BUILDINGS[i],
                     "neighbors": [{"index": v, "name": BUILDINGS[v], "distance": w}
                                   for v, w in ADJ[i]]}
                    for i in range(len(BUILDINGS))])

@app.get("/api/matrix")
def matrix():
    n = len(BUILDINGS)
    data = [[0 if i == j else None for j in range(n)] for i in range(n)]
    for u, v, w in EDGES:
        data[u][v] = data[v][u] = w
    return jsonify({"buildings": BUILDINGS, "matrix": data})

@app.get("/api/shortest-path")
def shortest_path_api():
    try:
        source = int(request.args.get("source", "0"))
        destination = int(request.args.get("destination", "1"))
    except ValueError:
        return jsonify({"error": "Source and destination must be building indexes."}), 400
    if not (0 <= source < len(BUILDINGS) and 0 <= destination < len(BUILDINGS)):
        return jsonify({"error": f"Indexes must be between 0 and {len(BUILDINGS)-1}."}), 400
    result = shortest_path(source, destination)
    if result is None:
        return jsonify({"error": "No path exists."}), 404
    return jsonify(result)

@app.get("/api/mst")
def mst():
    return jsonify(prim_mst())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
