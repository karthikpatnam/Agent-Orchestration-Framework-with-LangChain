# Smart Route Optimization Backend

A powerful routing backend built with FastAPI and LangGraph.

## Instructions to run locally

### 1. Install dependencies
Ensure you are using Python 3.9+ and run:
```bash
pip install -r requirements.txt
```

### 2. Start the server
Run the Uvicorn ASGI server as a Python module (useful if uvicorn is not in your system PATH):
```bash
python -m uvicorn main:app --reload
```

The server will start on `http://127.0.0.1:8000`.

### 3. Sample Request
Submit a POST request to `/optimize-route` to compute the optimal route between two coordinates. Replace the coordinates below with your actual source and destination points.

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/optimize-route' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "source_coords": [8.681495, 49.41461],
  "dest_coords": [8.686507, 49.41943]
}'
```

### 4. Sample Response
```json
{
  "best_route_id": "route-1a2b3c4d",
  "explanation": "This route was selected because it balances a short duration with lower weather risks, optimizing both safety and overall speed. Despite a slightly higher cost, it successfully minimizes total travel impedance.",
  "routes": [
    {
      "id": "route-1a2b3c4d",
      "geometry": "...polyline...",
      "distance_m": 1205.5,
      "duration_s": 150.2,
      "weather_risk_score": 10.0,
      "cost": 1.43,
      "total_score": 23.52
    }
  ]
}
```
