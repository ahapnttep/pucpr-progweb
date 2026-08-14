from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class Handler(SimpleHTTPRequestHandler):

    def do_GET(self):
        # Serve filmes.html when the user accesses the root path.
        if self.path == "/":
            self.path = "/filmes.html"

        super().do_GET()

    def list_directory(self, path):
        # Disable directory listing completely.
        self.send_error(403, "Directory listing disabled")
        return None


HOST = "0.0.0.0"
PORT = 49152

server = ThreadingHTTPServer((HOST, PORT), Handler)

print(f"Serving on http://{HOST}:{PORT}")
server.serve_forever()

