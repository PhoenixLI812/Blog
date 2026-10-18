import subprocess
import os

cwd = os.path.abspath(os.path.dirname(__file__))
root = os.path.abspath(os.path.join(cwd, ".."))

html_content = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    @page {
      size: A4;
      margin: 20mm 15mm 20mm 15mm;
    }
    .cover {
      page-break-after: always;
      height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      background: #111827;
      color: white;
      text-align: center;
    }
    .content {
      page-break-before: always;
      font-family: sans-serif;
    }
  </style>
</head>
<body>
  <div class="cover">
    <h1>半导体见顶了吗？</h1>
    <p>封面页测试</p>
  </div>
  <div class="content">
    <h2>第一章</h2>
    <p>正文内容第一页</p>
  </div>
</body>
</html>"""

test_html = os.path.join(root, "scratch", "test_header_footer.html")
test_pdf = os.path.join(root, "scratch", "test_header_footer.pdf")

with open(test_html, "w", encoding="utf-8") as f:
    f.write(html_content)

header_html = """
<div style="font-size: 8pt; font-family: sans-serif; width: 100%; text-align: right; padding-right: 15mm; color: #888;">
  《半导体见顶了吗？》
</div>
"""

footer_html = """
<div style="font-size: 8pt; font-family: sans-serif; width: 100%; text-align: center; color: #888;">
  第 <span class="pageNumber"></span> 页 / 共 <span class="totalPages"></span> 页
</div>
"""

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
cmd = [
    chrome_path,
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--virtual-time-budget=5000",
    "--display-header-footer",
    f"--header-template={header_html}",
    f"--footer-template={footer_html}",
    f"--print-to-pdf={test_pdf}",
    test_html
]

subprocess.run(cmd, check=True)
print("PDF created. Size:", os.path.getsize(test_pdf))
