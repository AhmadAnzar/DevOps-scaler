from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"<h1>Hello World from Python + Docker!</h1>"
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


server = ThreadingHTTPServer(("0.0.0.0", 8000), HelloHandler)
print("Python app listening on port 8000", flush=True)
server.serve_forever()
