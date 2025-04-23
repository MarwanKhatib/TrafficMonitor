import time
from collections import deque

class TrafficLogger:
    def __init__(self, max_logs=100):
        """
        Initialize the logger with an in-memory storage (deque) to store logs.
        """
        self.logs = deque(maxlen=max_logs)  # Keeps only the latest `max_logs` logs

    def log_request(self, request, status_code=200):
        """
        Log the incoming HTTP request details, excluding paths like '/favicon.ico'.
        """
        if request.path == "/favicon.ico":
            return
        
        ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
        
        log_entry = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()),
            'ip': ip,
            'method': request.method,
            'user_agent': request.headers.get('User-Agent'),
            'referrer': request.headers.get('Referer', 'N/A'),
            'request_path': request.path,
            'status_code': status_code,
            'content_length': request.headers.get('Content-Length', 'N/A')
        }
        self.logs.appendleft(log_entry)

    def get_logs(self):
        """
        Return all logged requests.
        """
        return list(self.logs)
