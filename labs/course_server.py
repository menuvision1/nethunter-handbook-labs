#!/usr/bin/env python3
"""Local, deliberately flawed teaching API. Synthetic records only."""
import argparse,json
from http.server import BaseHTTPRequestHandler,HTTPServer
from urllib.parse import urlsplit

ORDERS={"1":{"id":1,"owner":"alice","item":"training notebook"},
        "2":{"id":2,"owner":"admin","item":"training cable"}}
TOKENS={"Bearer tok-alice":"alice","Bearer tok-admin":"admin"}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path=urlsplit(self.path).path
        if path=="/health":
            return self.reply(200,{"status":"ok","mode":self.server.mode})
        if not path.startswith("/api/orders/"):
            return self.reply(404,{"error":"route not found"})
        user=TOKENS.get(self.headers.get("Authorization"))
        if not user:return self.reply(401,{"error":"authentication required"})
        order=ORDERS.get(path.removeprefix("/api/orders/"))
        if order is None:return self.reply(404,{"error":"order not found"})
        # Vulnerable mode deliberately omits object ownership enforcement.
        if self.server.mode=="fixed" and order["owner"]!=user:
            return self.reply(403,{"error":"forbidden"})
        self.reply(200,order)
    def reply(self,status,data):
        body=(json.dumps(data,sort_keys=True)+"\n").encode()
        self.send_response(status)
        self.send_header("Content-Type","application/json")
        self.send_header("Content-Length",str(len(body)))
        self.end_headers();self.wfile.write(body)

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode",choices=["vulnerable","fixed"],required=True)
    args=parser.parse_args()
    server=HTTPServer(("127.0.0.1",8765),Handler)
    server.mode=args.mode
    print(f"Local course API: http://127.0.0.1:8765 ({args.mode})",flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()
