import http.server, urllib.parse, sqlite3, html
db = sqlite3.connect(':memory:', check_same_thread=False)
db.execute("CREATE TABLE users(user TEXT, pass TEXT, role TEXT)")
db.executemany("INSERT INTO users VALUES(?,?,?)",
               [('alice','wonderland','user'),('admin','s3cret-demo','admin')])
db.commit()
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def reply(self, code, body, cookie=None):
        self.send_response(code)
        self.send_header('Content-Type','text/html')
        if cookie: self.send_header('Set-Cookie', cookie)
        self.end_headers(); self.wfile.write(body.encode())
    def do_GET(self):
        u = urllib.parse.urlparse(self.path); q = urllib.parse.parse_qs(u.query)
        user = q.get('user',[''])[0]; pw = q.get('pass',[''])[0]
        if u.path == '/login':   # VULNERABLE: string-built SQL
            sql = "SELECT user,role FROM users WHERE user='%s' AND pass='%s'" % (user, pw)
            try: row = db.execute(sql).fetchone()
            except Exception as e: return self.reply(500, 'SQL error: %s' % e)
            if row: return self.reply(200, 'Welcome %s (role=%s)' % (row[0], row[1]),
                                      cookie='session=demo-'+row[0])
            return self.reply(401, 'Invalid credentials')
        if u.path == '/safelogin':  # SAFE: parameterized
            row = db.execute("SELECT user,role FROM users WHERE user=? AND pass=?",(user,pw)).fetchone()
            if row: return self.reply(200, 'Welcome %s (role=%s)' % (row[0], row[1]))
            return self.reply(401, 'Invalid credentials')
        if u.path == '/search':  # reflects input (demonstrates reflection)
            term = q.get('q',[''])[0]
            return self.reply(200, '<p>Results for: %s</p>' % term)
        self.reply(404, 'not found')
http.server.HTTPServer(('127.0.0.1',8000), H).serve_forever()
