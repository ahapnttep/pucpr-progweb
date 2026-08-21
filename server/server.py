from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote, urlsplit
import os

HOST = "0.0.0.0"
# 49152 starts the dynamic/private range, so it is handy for a local cybersec lab and stays away from common service ports.
PORT = 49152

# publish projeto/ even when this runs from server/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ROUTES_PAGE = PROJECT_ROOT / "pages" / "routes.html"
os.chdir(PROJECT_ROOT)


class ProjetoHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # no cache while I keep changing the pages
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def translate_path(self, path):
        clean_path = unquote(urlsplit(path).path)

        # fake pages only change which window looks focused
        # assets/_views/notepad-focus.html -> /__notepad__.html
        # assets/_views/server-vim-focus.html -> /server/__vim__.html
        if clean_path == "/__notepad__.html":
            return str(PROJECT_ROOT / "assets" / "_views" / "notepad-focus.html")
        if clean_path == "/server/__vim__.html":
            return str(PROJECT_ROOT / "assets" / "_views" / "server-vim-focus.html")

        # localhost opens pages/routes.html on purpose: the routes exercise looks better as the desktop/landing page than the website itself.
        if clean_path in {"/", "/pages/routes.html", "/__explorer__.html"}:
            return str(ROUTES_PAGE)

        # strip this if an old absolute project path shows up
        marker = "/prog_web/projeto/"
        if marker in clean_path:
            clean_path = "/" + clean_path.split(marker, 1)[1]

        return super().translate_path(clean_path)


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), ProjetoHandler)

    print(f"Rotas e Links: http://localhost:{PORT}/")
    print(f"Website: http://localhost:{PORT}/index.html")
    print(f"Animais: http://localhost:{PORT}/animais/index.html")
    print(f"Cadastrar: http://localhost:{PORT}/animais/cadastrar/cadastrar.html")
    print(f"Sobre: http://localhost:{PORT}/empresa/sobre.html")
    print(f"MS-DOS: http://localhost:{PORT}/server/server-terminal.html")
    print(f"Notepad focus: http://localhost:{PORT}/__notepad__.html")
    print(f"VIM focus: http://localhost:{PORT}/server/__vim__.html")
    print(f"Diretório publicado: {PROJECT_ROOT}")
    print("CTRL+C para encerrar.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        server.server_close()
