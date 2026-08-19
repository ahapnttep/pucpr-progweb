from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


# Directory where server.py is located.
SERVER_DIR = Path(__file__).resolve().parent

# Project root directory.
PROJECT_ROOT = SERVER_DIR.parent


class Handler(SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        # Serve files from the project root directory.
        super().__init__(*args, directory=str(PROJECT_ROOT), **kwargs)

    def list_directory(self, path):
        # Disable directory listing completely.
        self.send_error(403, "Directory listing disabled")
        return None


HOST = "0.0.0.0"
PORT = 49152

server = ThreadingHTTPServer((HOST, PORT), Handler)

print(f"Serving files from: {PROJECT_ROOT}")
print(f"Serving on http://localhost:{PORT}")

server.serve_forever()