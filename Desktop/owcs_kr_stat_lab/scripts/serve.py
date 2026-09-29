#!/usr/bin/env python3
import os
import sys
import threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB_DIR = os.path.join(BASE_DIR, "owcs-stat-lab 2")

class CustomHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def run_port(port):
    try:
        server = ThreadingHTTPServer(("0.0.0.0", port), CustomHandler)
        print(f"Serving {WEB_DIR} on http://localhost:{port}")
        server.serve_forever()
    except Exception as e:
        print(f"Port {port} error: {e}")

if __name__ == "__main__":
    ports = [8008, 8000]
    threads = []
    for p in ports[:-1]:
        t = threading.Thread(target=run_port, args=(p,), daemon=True)
        t.start()
        threads.append(t)
    run_port(ports[-1])
