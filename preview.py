import http.server
import socketserver
import webbrowser
import os
import sys

# 适配 Windows 控制台编码
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PORT = 3000

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    port = PORT
    httpd = None
    for p in range(PORT, PORT + 20):
        try:
            httpd = socketserver.TCPServer(('127.0.0.1', p), Handler)
            port = p
            break
        except OSError:
            continue
            
    if not httpd:
        print("[ERROR] Cannot bind to ports 3000-3020.")
        return

    url = f"http://localhost:{port}/"
    print("=" * 60)
    print(" [LOCAL PREVIEW] Blog preview server started!")
    print(f" [URL] Visit: {url}")
    print(" [TIPS] Press Ctrl+C in terminal to stop preview")
    print("=" * 60)
    
    webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == '__main__':
    main()
