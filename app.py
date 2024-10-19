from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)
socketio = SocketIO(app)

# Store population coordinates
population_coords = []

# Haversine distance function to calculate the distance between two coordinates
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to receive and store GPS coordinates from users
@app.route('/send_location', methods=['POST'])
def receive_location():
    data = request.json
    lat = data.get('latitude')
    lon = data.get('longitude')
    
    if lat is not None and lon is not None:
        population_coords.append((lat, lon))
        
        # Emit the updated data to all connected clients
        socketio.emit('update_population', population_coords)
        return jsonify({"message": "Coordinates received", "total_people": len(population_coords)})
    
    return jsonify({"error": "Invalid data"}), 400

# Flask-SocketIO function to run real-time updates
if __name__ == '__main__':
    socketio.run(app, debug=True)