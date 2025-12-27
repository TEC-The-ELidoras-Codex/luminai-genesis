#!/usr/bin/env python3
import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_len = int(self.headers.get("content-length", 0))
        body = self.rfile.read(content_len).decode("utf-8")
        print("Received POST to", self.path)
        print(body)
        resp = {
            "id": "mock-1",
            "object": "chat.completion",
            "choices": [
                {"message": {"content": "Mock response: received your prompt."}},
            ],
        }
        resp_bytes = json.dumps(resp).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(resp_bytes)))
        self.end_headers()
        self.wfile.write(resp_bytes)


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), Handler)
    print("Mock Grok server listening on http://127.0.0.1:8000")
    server.serve_forever()
