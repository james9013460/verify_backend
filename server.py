import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    
    def get_echo_str(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        echostr = query_params.get('echostr', [None])[0]
        print("echostr = " + str(echostr))
        return echostr

    def do_GET(self):
        self.print_request_details()
        echostr = self.get_echo_str()
        if (echostr):
            print("SEND BACK")
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(echostr.encode())
            return

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, GET request received!')

    def do_POST(self):
        self.print_request_details()
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else b''
        print(f"Body:\n{body.decode('utf-8')}\n")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, POST request received!')


    def print_request_details(self):
        print(f"Incoming {self.command} request")
        print(f"Path: {self.path}")
        print("Headers:")
        for header, value in self.headers.items():
            print(f"{header}: {value}")
        print("\n")

if __name__ == '__main__':
    host = '0.0.0.0'
    port = int(os.environ.get('PORT', 80))  # Railway sets PORT env var

    server = HTTPServer((host, port), SimpleHTTPRequestHandler)
    print(f"Starting server on {host}:{port}")
    server.serve_forever()
