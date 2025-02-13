from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    temp = float(data['temp'])
    unit = data['unit']
    
    if unit == 'C':
        result = (temp * 9/5) + 32
        new_unit = 'F'
    else:
        result = (temp - 32) * 5/9
        new_unit = 'C'
        
    return jsonify({
        'result': round(result, 2),
        'unit': new_unit
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)