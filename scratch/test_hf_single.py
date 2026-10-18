import subprocess
import os

cwd = os.path.abspath(os.path.dirname(__file__))
root = os.path.abspath(os.path.join(cwd, ".."))

html_content = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>半导体见顶了吗？</title>
  <style>
    @page {
      size: A4;
      margin: 15mm 20mm 15mm 20mm;
    }
    body {
      font-family: sans-serif;
      margin: 0;
    }
    .page {
      page-break-after: always;
      padding: 10px;
    }
  </style>
</head>
<body>
  <div class="page">
    <h1>第一页内容</h1>
    <p>这是正文第一页。</p>
  </div>
  <div class="page">
    <h1>第二页内容</h1>
    <p>这是正文第二页。</p>
  </div>
</body>
</html>"""

test_html = os.path.join(root, "scratch", "test_hf_single.html")
test_pdf = os.path.join(root, "scratch", "test_hf_single.pdf")

with open(test_html, "w", encoding="utf-8") as f:
    f.write(html_content)

header = '<div style="font-size: 8pt; width: 100%; text-align: right; margin-right: 20mm; color: #888;">《半导体见顶了吗？》</div>'
footer = '<div style="font-size: 8pt; width: 100%; text-align: center; color: #888;">第 <span class="pageNumber"></span> 页 / 共 <span class="totalPages"></span> 页</div>'

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
cmd = [
    chrome_path,
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--virtual-time-budget=5000",
    "--display-header-footer",
    f'--header-template={header}',
    f'--footer-template={footer}',
    f'--print-to-pdf={test_pdf}',
    test_html
]

res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print("Exit code:", res.returncode)
print("PDF exists:", os.path.exists(test_pdf))
