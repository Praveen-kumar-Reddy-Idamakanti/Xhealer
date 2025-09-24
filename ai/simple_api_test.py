"""
Simple API test to debug the issue
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'message': 'API is working'})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    return jsonify({
        'predicted_disease': 'Test Disease',
        'confidence': 0.85,
        'message': 'Test prediction working'
    })

if __name__ == '__main__':
    print("Starting simple test API...")
    app.run(debug=True, host='0.0.0.0', port=5001)
