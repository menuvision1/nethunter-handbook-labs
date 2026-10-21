import http.server, json, urllib.parse
TOKENS = {'alice':'tok-alice','admin':'tok-admin'}
ORDERS = {'1':{'id':'1','owner':'alice','item':'notebook','total':12.5},
          '2':{'id':'2','owner':'admin','item':'server','total':999.0}}
def who(tok): return next((u for u,t in TOKENS.items() if t==tok), None)
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self,*a): pass
    def j(self, code, obj):
        self.send_response(code); self.send_header('Content-Type','application/json'); self.end_headers()
        self.wfile.write(json.dumps(obj).encode())
    def do_GET(self):
        u=urllib.parse.urlparse(self.path); parts=u.path.strip('/').split('/')
        tok=self.headers.get('Authorization','').replace('Bearer ','')
        # /api/orders/<id>  VULNERABLE: returns any order to any valid token (IDOR)
        if parts[:2]==['api','orders'] and len(parts)==3:
            if not who(tok): return self.j(401,{'error':'missing or invalid token'})
            o=ORDERS.get(parts[2])
            return self.j(200,o) if o else self.j(404,{'error':'no such order'})
        # /api/safe-orders/<id>  SAFE: caller must own the order
        if parts[:2]==['api','safe-orders'] and len(parts)==3:
            caller=who(tok)
            if not caller: return self.j(401,{'error':'missing or invalid token'})
            o=ORDERS.get(parts[2])
            if not o: return self.j(404,{'error':'no such order'})
            if o['owner']!=caller: return self.j(403,{'error':'not your order'})
            return self.j(200,o)
        self.j(404,{'error':'not found'})
http.server.HTTPServer(('127.0.0.1',8001), H).serve_forever()
