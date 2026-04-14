from fastapi import FastAPI
from fastapi.responses import HTMLResponse

def get_map_ui():
    """Return the HTML UI with map interface"""
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Smart Route Optimizer</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css" />
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                flex-direction: column;
            }
            .header {
                background: rgba(0,0,0,0.3);
                color: white;
                padding: 20px;
                text-align: center;
                box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            }
            .header h1 {
                font-size: 28px;
                margin-bottom: 5px;
            }
            .header p {
                font-size: 14px;
                opacity: 0.9;
            }
            .container {
                display: flex;
                flex: 1;
                gap: 20px;
                padding: 20px;
                max-width: 1400px;
                margin: 0 auto;
                width: 100%;
            }
            .map-section {
                flex: 2;
                background: white;
                border-radius: 12px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.2);
                overflow: hidden;
            }
            #map {
                width: 100%;
                height: 100%;
                min-height: 600px;
            }
            .control-panel {
                flex: 1;
                background: white;
                border-radius: 12px;
                padding: 25px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.2);
                display: flex;
                flex-direction: column;
                gap: 20px;
                overflow-y: auto;
                max-height: 600px;
            }
            .control-panel h2 {
                color: #667eea;
                font-size: 20px;
                margin-bottom: 5px;
            }
            .form-group {
                display: flex;
                flex-direction: column;
                gap: 8px;
            }
            .form-group label {
                font-weight: 600;
                color: #333;
                font-size: 14px;
            }
            .form-group input {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 14px;
                transition: border-color 0.3s;
            }
            .form-group input:focus {
                outline: none;
                border-color: #667eea;
            }
            .coord-pair {
                display: flex;
                gap: 10px;
            }
            .coord-pair input {
                flex: 1;
            }
            .button-group {
                display: flex;
                gap: 10px;
            }
            button {
                flex: 1;
                padding: 12px;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s;
                font-size: 14px;
            }
            .btn-optimize {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .btn-optimize:hover:not(:disabled) {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            }
            .btn-optimize:disabled {
                opacity: 0.6;
                cursor: not-allowed;
            }
            .btn-clear {
                background: #f5f5f5;
                color: #333;
                border: 2px solid #e0e0e0;
            }
            .btn-clear:hover:not(:disabled) {
                background: #eeeeee;
            }
            .loading {
                display: none;
                text-align: center;
                padding: 15px;
                background: #f5f5f5;
                border-radius: 8px;
                color: #667eea;
            }
            .loading.active {
                display: block;
            }
            .spinner {
                display: inline-block;
                width: 20px;
                height: 20px;
                border: 3px solid #f3f3f3;
                border-top: 3px solid #667eea;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin-right: 10px;
                vertical-align: middle;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .results {
                display: none;
                padding: 15px;
                background: #f0f8ff;
                border-radius: 8px;
                border-left: 4px solid #667eea;
            }
            .results.active {
                display: block;
            }
            .results h3 {
                color: #667eea;
                margin-bottom: 10px;
            }
            .route-item {
                background: white;
                padding: 10px;
                border-radius: 6px;
                margin: 8px 0;
                font-size: 13px;
                border: 1px solid #e0e0e0;
            }
            .route-score {
                color: #764ba2;
                font-weight: 600;
            }
            .best-badge {
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 2px 8px;
                border-radius: 4px;
                font-size: 11px;
                margin-left: 5px;
            }
            .explanation {
                background: #fff9e6;
                padding: 12px;
                border-radius: 8px;
                border-left: 4px solid #ffc107;
                margin: 12px 0;
                font-size: 13px;
                line-height: 1.5;
                color: #333;
            }
            .error {
                background: #ffebee;
                color: #c62828;
                padding: 12px;
                border-radius: 8px;
                border-left: 4px solid #c62828;
                display: none;
            }
            .error.active {
                display: block;
            }
            @media (max-width: 1024px) {
                .container {
                    flex-direction: column;
                }
                .map-section {
                    min-height: 400px;
                }
                .control-panel {
                    max-height: none;
                }
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🗺️ Smart Route Optimizer</h1>
            <p>AI-powered route optimization considering weather, traffic, and geopolitical factors</p>
        </div>

        <div class="container">
            <div class="map-section">
                <div id="map"></div>
            </div>

            <div class="control-panel">
                <div>
                    <h2>Route Planner</h2>
                    <p style="color: #666; font-size: 13px; margin-top: 5px;">Enter coordinates or click on map</p>
                </div>

                <div class="form-group">
                    <label>Source (Click on map or enter coordinates)</label>
                    <div class="coord-pair">
                        <input type="number" id="sourceLon" placeholder="Longitude" step="any">
                        <input type="number" id="sourceLat" placeholder="Latitude" step="any">
                    </div>
                    <small style="color: #999;">Format: [Longitude, Latitude]</small>
                </div>

                <div class="form-group">
                    <label>Destination (Click on map or enter coordinates)</label>
                    <div class="coord-pair">
                        <input type="number" id="destLon" placeholder="Longitude" step="any">
                        <input type="number" id="destLat" placeholder="Latitude" step="any">
                    </div>
                    <small style="color: #999;">Format: [Longitude, Latitude]</small>
                </div>

                <div class="button-group">
                    <button class="btn-optimize" id="optimizeBtn">Find Optimal Route</button>
                    <button class="btn-clear" id="clearBtn">Clear</button>
                </div>

                <div class="loading" id="loading">
                    <span class="spinner"></span>Analyzing routes...
                </div>

                <div class="error" id="error"></div>

                <div class="results" id="results">
                    <h3>Results</h3>
                    <div class="explanation" id="explanation"></div>
                    <div id="routesList"></div>
                </div>
            </div>
        </div>

        <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
        <script>
            // Initialize map
            const map = L.map('map').setView([49.41, 8.68], 14);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors',
                maxZoom: 19
            }).addTo(map);

            let sourceMarker = null;
            let destMarker = null;
            let routePolylines = {}; // Store polylines by route ID
            let clickMode = 'source'; // 'source' or 'dest'

            // Polyline decoding function (Google's polyline algorithm)
            function decodePolyline(encoded) {
                const poly = [];
                let index = 0, lat = 0, lng = 0;
                while (index < encoded.length) {
                    let result = 0, shift = 0, b;
                    do {
                        b = encoded.charCodeAt(index++) - 63;
                        result |= (b & 0x1f) << shift;
                        shift += 5;
                    } while (b >= 0x20);
                    lat += ((result & 1) ? ~(result >> 1) : (result >> 1));
                    result = 0;
                    shift = 0;
                    do {
                        b = encoded.charCodeAt(index++) - 63;
                        result |= (b & 0x1f) << shift;
                        shift += 5;
                    } while (b >= 0x20);
                    lng += ((result & 1) ? ~(result >> 1) : (result >> 1));
                    poly.push([lat / 1e5, lng / 1e5]);
                }
                return poly;
            }

            // DOM elements
            const sourceLonInput = document.getElementById('sourceLon');
            const sourceLatInput = document.getElementById('sourceLat');
            const destLonInput = document.getElementById('destLon');
            const destLatInput = document.getElementById('destLat');
            const optimizeBtn = document.getElementById('optimizeBtn');
            const clearBtn = document.getElementById('clearBtn');
            const loading = document.getElementById('loading');
            const error = document.getElementById('error');
            const results = document.getElementById('results');
            const explanation = document.getElementById('explanation');
            const routesList = document.getElementById('routesList');

            // Map click handler
            map.on('click', function(e) {
                const lat = e.latlng.lat;
                const lng = e.latlng.lng;

                if (clickMode === 'source') {
                    sourceLonInput.value = lng.toFixed(6);
                    sourceLatInput.value = lat.toFixed(6);
                    updateSourceMarker(lng, lat);
                    clickMode = 'dest';
                } else {
                    destLonInput.value = lng.toFixed(6);
                    destLatInput.value = lat.toFixed(6);
                    updateDestMarker(lng, lat);
                    clickMode = 'source';
                }
            });

            function updateSourceMarker(lng, lat) {
                if (sourceMarker) map.removeLayer(sourceMarker);
                sourceMarker = L.circleMarker([lat, lng], {
                    radius: 8,
                    fillColor: '#667eea',
                    color: '#fff',
                    weight: 2,
                    opacity: 1,
                    fillOpacity: 0.8
                }).addTo(map).bindPopup('Source');
            }

            function updateDestMarker(lng, lat) {
                if (destMarker) map.removeLayer(destMarker);
                destMarker = L.circleMarker([lat, lng], {
                    radius: 8,
                    fillColor: '#764ba2',
                    color: '#fff',
                    weight: 2,
                    opacity: 1,
                    fillOpacity: 0.8
                }).addTo(map).bindPopup('Destination');
            }

            optimizeBtn.addEventListener('click', async function() {
                const sourceLon = parseFloat(sourceLonInput.value);
                const sourceLat = parseFloat(sourceLatInput.value);
                const destLon = parseFloat(destLonInput.value);
                const destLat = parseFloat(destLatInput.value);

                if (!sourceLon || !sourceLat || !destLon || !destLat) {
                    showError('Please enter or select both source and destination coordinates');
                    return;
                }

                loading.classList.add('active');
                error.classList.remove('active');
                results.classList.remove('active');

                try {
                    const response = await fetch('/optimize-route', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            source_coords: [sourceLon, sourceLat],
                            dest_coords: [destLon, destLat]
                        })
                    });

                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(errorData.detail || 'Failed to optimize route');
                    }

                    const data = await response.json();
                    displayResults(data);
                } catch (err) {
                    showError(err.message);
                } finally {
                    loading.classList.remove('active');
                }
            });

            function displayResults(data) {
                explanation.textContent = data.explanation;
                
                // Clear previous polylines
                Object.values(routePolylines).forEach(polyline => {
                    if (polyline) map.removeLayer(polyline);
                });
                routePolylines = {};

                // Colors for different routes
                const colors = ['#667eea', '#764ba2', '#ff6b6b', '#ffa726', '#26a69a', '#5c6bc0'];
                
                let routesHTML = '';
                data.routes.forEach((route, index) => {
                    const isBest = route.id === data.recommended_route_id;
                    const distance = (route.distance_m / 1000).toFixed(2);
                    const duration = (route.duration_s / 60).toFixed(0);
                    const color = colors[index % colors.length];
                    
                    // Decode and display polyline on map
                    if (route.geometry) {
                        try {
                            const coordinates = decodePolyline(route.geometry);
                            const polylineOptions = {
                                color: color,
                                weight: isBest ? 4 : 2,
                                opacity: isBest ? 1 : 0.6,
                                dashArray: isBest ? null : '5, 5'
                            };
                            const polyline = L.polyline(coordinates, polylineOptions).addTo(map);
                            routePolylines[route.id] = polyline;
                        } catch (err) {
                            console.error('Error decoding polyline:', err);
                        }
                    }
                    
                    routesHTML += `
                        <div class="route-item" style="border-left: 4px solid ${color}; cursor: pointer;" onmouseover="this.style.background='#f9f9f9'" onmouseout="this.style.background='white'">
                            <strong style="color: ${color}">Route ${route.id}</strong>
                            ${isBest ? '<span class="best-badge">RECOMMENDED</span>' : ''}
                            <br/>
                            📍 Distance: <strong>${distance} km</strong> | ⏱️ Duration: <strong>${duration} min</strong>
                            ${route.total_score ? `<br/><span class="route-score">🎯 Score: ${route.total_score.toFixed(2)}</span>` : ''}
                            ${route.weather_risk_score ? `<br/>🌤️ Weather Risk: ${route.weather_risk_score.toFixed(1)}` : ''}
                            ${route.traffic_risk_score ? `<br/>🚗 Traffic Risk: ${route.traffic_risk_score.toFixed(1)}` : ''}
                        </div>
                    `;
                });
                
                routesList.innerHTML = routesHTML;
                results.classList.add('active');

                // Fit map to all routes
                setTimeout(() => {
                    const bounds = L.latLngBounds();
                    Object.values(routePolylines).forEach(polyline => {
                        polyline.getLatLngs().forEach(latLng => {
                            bounds.extend(latLng);
                        });
                    });
                    if (bounds.isValid()) {
                        map.fitBounds(bounds, { padding: [50, 50] });
                    }
                }, 100);
            }

            function showError(message) {
                error.textContent = '❌ ' + message;
                error.classList.add('active');
            }

            clearBtn.addEventListener('click', function() {
                sourceLonInput.value = '';
                sourceLatInput.value = '';
                destLonInput.value = '';
                destLatInput.value = '';
                if (sourceMarker) map.removeLayer(sourceMarker);
                if (destMarker) map.removeLayer(destMarker);
                Object.values(routePolylines).forEach(polyline => {
                    if (polyline) map.removeLayer(polyline);
                });
                routePolylines = {};
                results.classList.remove('active');
                error.classList.remove('active');
                clickMode = 'source';
            });
        </script>
    </body>
    </html>
    """)
