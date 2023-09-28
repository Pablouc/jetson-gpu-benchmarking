from flask import Flask, jsonify
from flask_cors import CORS #allow the server and front-end to run on different domains( different ports are considered different domains)

# Create a Flask web application
app = Flask('evaluatorServer')
CORS(app)

# Sample array of app names
appsNames= {
    "itemNames" : ['gaussian', 'particlefilter', 'pathfinder', 'hotspot', 'bfs']
}

workloadsNames= {
    "itemNames" : ['gaussian66989.txt', 'particlefilter.txt', 'pathfinder.txt', 'hotspot.txt', 'bfs.txt']
}

# Define a route to return the app names as JSON
@app.route('/appsNames', methods=['GET'])
def get_app_names():
    # Convert the array to JSON and return it
    return jsonify(appsNames)

# Define a route to return the workloads names as JSON
@app.route('/workloadsNames', methods=['GET'])
def get_workloads_names():
    # Convert the array to JSON and return it
    return jsonify(workloadsNames)

# Run the Flask application on a local development server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)