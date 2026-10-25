"""Localhost-only, GET-only JSON + static monitor. No order routes, no API keys."""
from __future__ import annotations
import argparse
from functools import partial
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from urllib.parse import urlsplit
from .snapshot import DashboardSources, read_snapshot

STATIC=Path(__file__).resolve().parent/'static'
ASSETS={'/':('index.html','text/html; charset=utf-8'),
        '/app.js':('app.js','text/javascript; charset=utf-8'),
        '/style.css':('style.css','text/css; charset=utf-8')}


class DashboardHandler(BaseHTTPRequestHandler):
    sources=DashboardSources()

    def do_GET(self):
        host=(self.headers.get('Host') or '').lower().strip()
        if host not in ('127.0.0.1', 'localhost', '[::1]') and not any(
            host.startswith(prefix) and host[len(prefix):].isdigit() for prefix in
            ('127.0.0.1:', 'localhost:', '[::1]:')):
            self._send(403,b'Local access only','text/plain; charset=utf-8')
            return
        uri=urlsplit(self.path)
        if uri.query or uri.fragment:
            self._send(400,b'Unexpected query','text/plain; charset=utf-8')
            return
        if uri.path=='/api/status':
            try:
                data=json.dumps(read_snapshot(self.sources),allow_nan=False,separators=(',',':')).encode('utf-8')
            except Exception:
                # Do not leak DB paths or tracebacks through the web server.
                self._send(503,b'{"error":"Snapshot unavailable"}','application/json; charset=utf-8')
                return
            self._send(200,data,'application/json; charset=utf-8')
        elif uri.path in ASSETS:
            file,kind=ASSETS[uri.path]
            self._send(200,(STATIC/file).read_bytes(),kind)
        else:
            self._send(404,b'Not found','text/plain; charset=utf-8')

    def do_POST(self):
        self._send(405,b'Read-only dashboard','text/plain; charset=utf-8')

    do_PUT=do_POST
    do_DELETE=do_POST
    do_PATCH=do_POST

    def _send(self,status,body,content_type):
        self.send_response(status)
        self.send_header('Content-Type',content_type)
        self.send_header('Content-Length',str(len(body)))
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Referrer-Policy','no-referrer')
        self.send_header('X-Frame-Options','DENY')
        self.send_header('Content-Security-Policy',"default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self' data:; frame-ancestors 'none'; base-uri 'none'; form-action 'none'")
        self.end_headers()
        self.wfile.write(body)


def handler_for(sources):
    return type('ReadOnlyDashboardHandler',(DashboardHandler,),{'sources':sources})


def main(argv=None):
    p=argparse.ArgumentParser(description='LOCAL READ-ONLY BTC/AUD PAPER BOT dashboard')
    p.add_argument('--market-db',default='data/market.sqlite')
    p.add_argument('--wallet-db',default='data/loop_wallet.sqlite')
    p.add_argument('--news-db',default='data/news.sqlite')
    p.add_argument('--journal-db',default='data/loop_journal.sqlite')
    p.add_argument('--port',type=int,default=8787)
    p.add_argument('--host',default='127.0.0.1')
    args=p.parse_args(argv)
    if args.host not in ('127.0.0.1','::1'):
        p.error('Public binds forbidden. Bind loopback only and tunnel through an authenticated channel.')
    if not 1024 <= args.port <= 65535:
        p.error('Port must be between 1024 and 65535')
    sources=DashboardSources(Path(args.market_db),Path(args.wallet_db),Path(args.news_db),Path(args.journal_db))
    with ThreadingHTTPServer((args.host,args.port),handler_for(sources)) as server:
        print(f'LOCAL PAPER dashboard: http://{args.host}:{args.port} (Ctrl+C to stop)',flush=True)
        server.serve_forever(poll_interval=.5)


if __name__=='__main__': main()
