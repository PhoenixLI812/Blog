import subprocess
import os

cwd = os.path.abspath(os.path.dirname(__file__))
root = os.path.abspath(os.path.join(cwd, ".."))

html_content = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>CSS Margin Box Test</title>
  <style>
    @page {
      size: A4;
      margin: 25mm 20mm 25mm 20mm;
      @top-right {
        content: "《半导体见顶了吗？》";
        font-family: sans-serif;
        font-size: 9pt;
        color: #888;
        border-bottom: 1px solid #ddd;
        padding-bottom: 4px;
      }
      @bottom-center {
        content: "第 " counter(page) " 页 / 共 " counter(pages) " 页";
        font-family: sans-serif;
        font-size: 9pt;
        color: #888;
      }
    }
    @page :first {
      @top-right { content: normal; }
      @bottom-center { content: normal; }
    }
    body {
      font-family: sans-serif;
      margin: 0;
    }
    .cover {
      page-break-after: always;
      height: 80vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
    }
    .page {
      page-break-before: always;
    }
  </style>
</head>
<body>
  <div class="cover">
    <h1>半导体见顶了吗？</h1>
    <p>全景认知框架与物理推演</p>
  </div>
  <div class="page">
    <h2>序言</h2>
    <p>这是序言内容，第一页应当有页眉和页脚，但封面没有。</p>
  </div>
  <div class="page">
    <h2>第一章</h2>
    <p>这是第一章内容，应该显示第 3 页。</p>
  </div>
</body>
</html>"""

test_html = os.path.join(root, "scratch", "test_css_page.html")
test_pdf = os.path.join(root, "scratch", "test_css_page.pdf")

with open(test_html, "w", encoding="utf-8") as f:
    f.write(html_content)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
cmd = [
    chrome_path,
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f'--print-to-pdf={test_pdf}',
    test_html
]

res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print("Exit code:", res.returncode)
print("PDF exists:", os.path.exists(test_pdf))
