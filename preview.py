import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 3000

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 允许跨域与 UTF-8 缓存优化
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 自动探测可用端口
    port = PORT
    for p in range(PORT, PORT + 20):
        try:
            httpd = socketserver.TCPServer(('127.0.0.1', p), Handler)
            port = p
            break
        except OSError:
            continue
            
    url = f"http://localhost:{port}/"
    print("=" * 60)
    print(f"📖 《半导体见顶了吗？》本地博客预览服务已启动！")
    print(f"🔗 本地访问地址: {url}")
    print(f"💡 提示: 按 Ctrl+C 可停止预览服务")
    print("=" * 60)
    
    webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已关闭。")

if __name__ == '__main__':
    main()
