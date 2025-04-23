from flask import Flask, request, render_template
from datetime import datetime
import json
import os

app = Flask(__name__)

# Log file path
LOG_FILE = 'logs.json'

# Helper function to load logs from the file
def load_logs():
    if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
        with open(LOG_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []  # Return an empty list if there's an error decoding the JSON
    return []

# Helper function to save logs to the file
def save_log(log_entry):
    logs = load_logs()  # Load existing logs
    logs.append(log_entry)
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=4)

@app.route('/')
def home():
    logs = load_logs()  # Load logs for the homepage
    return render_template('index.html', logs=logs)

@app.route('/log')
def log():
    logs = load_logs()  # Load logs for the /log page
    return render_template('log.html', logs=logs)

@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    if path == 'favicon.ico':  
        return '', 204  # No content response
    
    # Log the valid path request
    log_entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'ip': request.remote_addr,
        'method': request.method,
        'request_path': request.path,
        'user_agent': request.headers.get('User-Agent'),
        'referrer': request.headers.get('Referer', 'N/A'),
        'status_code': 200,
        'content_length': len(request.data) if request.data else 'N/A'
    }
    # Save the log to the file
    save_log(log_entry)
    
    return render_template('index.html', logs=load_logs())

if __name__ == '__main__':
    app.run(debug=True)
