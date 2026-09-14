from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8001


class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"<html>Hello, World! Jurek</html>"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    HTTPServer(("127.0.0.1", PORT), HelloHandler).serve_forever()
