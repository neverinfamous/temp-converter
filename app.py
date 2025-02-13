from flask import Flask, render_template, request, jsonify
import time
import psutil
import os

app = Flask(__name__)

# Production optimizations
app.config['TEMPLATES_AUTO_RELOAD'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # 1 year
app.config['STATIC_FILE_MAX_AGE'] = 31536000  # 1 year

# Jinja2 template optimization
app.jinja_env.auto_reload = False
app.jinja_env.cache_size = 50

PERFORMANCE_METRICS = {
    'response_times': [],
    'memory_usage': [],
    'start_time': time.time()
}

def get_system_metrics():
    return {
        'memory_percent': psutil.Process(os.getpid()).memory_percent(),
        'cpu_percent': psutil.Process(os.getpid()).cpu_percent()
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    start_time = time.time()
    
    try:
        data = request.get_json()
        temp = float(data['temperature'])
        conversion_type = data['type']
        
        if conversion_type == 'ctof':
            result = (temp * 9/5) + 32
        else:
            result = (temp - 32) * 5/9
            
        # Record performance metrics
        response_time = (time.time() - start_time) * 1000  # Convert to ms
        PERFORMANCE_METRICS['response_times'].append(response_time)
        
        # Get system metrics
        metrics = get_system_metrics()
        PERFORMANCE_METRICS['memory_usage'].append(metrics['memory_percent'])
        
        return jsonify({
            'result': round(result, 2),
            'metrics': {
                'response_time_ms': response_time,
                'memory_percent': metrics['memory_percent'],
                'cpu_percent': metrics['cpu_percent']
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/metrics')
def metrics():
    total_requests = len(PERFORMANCE_METRICS['response_times'])
    avg_response_time = sum(PERFORMANCE_METRICS['response_times']) / total_requests if total_requests > 0 else 0
    avg_memory = sum(PERFORMANCE_METRICS['memory_usage']) / len(PERFORMANCE_METRICS['memory_usage']) if PERFORMANCE_METRICS['memory_usage'] else 0
    
    uptime = time.time() - PERFORMANCE_METRICS['start_time']
    
    return jsonify({
        'total_requests': total_requests,
        'avg_response_time_ms': avg_response_time,
        'avg_memory_percent': avg_memory,
        'uptime_seconds': uptime
    })

if __name__ == '__main__':
    # Production settings when running directly
    app.config['ENV'] = 'production'
    app.config['DEBUG'] = False
    app.run(host='0.0.0.0', port=3000)