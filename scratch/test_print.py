import subprocess
import os

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
html_path = r"C:\Users\Administrator\Desktop\半导体见顶了吗？\scratch\test_math.html"
pdf_path = r"C:\Users\Administrator\Desktop\半导体见顶了吗？\scratch\test_math.pdf"

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

cmd = [
    chrome_path,
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--virtual-time-budget=5000",
    "--display-header-footer",
    f"--header-template={header_html}",
    f"--footer-template={footer_html}",
    f"--print-to-pdf={pdf_path}",
    html_path
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("Exit code:", res.returncode)
print("PDF size:", os.path.getsize(pdf_path))
