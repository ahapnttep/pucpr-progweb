# Local HTTP server for the movie backlog/catalog
# Opens index.html by default and blocks directory listing

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

class Handler(SimpleHTTPRequestHandler):

    def do_GET(self):
        # Open index.html when someone accesses the root URL
        if self.path == "/":
            self.path = "/filmes.html"

        super().do_GET()

    def list_directory(self, path):
        # Doesn't show the files/dir structure
        self.send_error(403, "Directory listing disabled")
        return None

# Listens on all net interfaces, so other devices on the LAN can connect
HOST = "0.0.0.0"
PORT = 49152 # Using a high n non-default port instead of 8000/default

server = ThreadingHTTPServer((HOST, PORT), Handler)

# Show where the server is running :)
print(f"I'm Serving on http://{HOST}:{PORT}")

server.serve_forever()
