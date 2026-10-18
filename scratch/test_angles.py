import subprocess
import os

cwd = os.path.abspath(os.path.dirname(__file__))
root = os.path.abspath(os.path.join(cwd, ".."))

html_path = os.path.join(root, "scratch", "test_angles.html")
pdf_path = os.path.join(root, "scratch", "test_angles.pdf")

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
cmd = [
    chrome_path,
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--virtual-time-budget=5000",
    f"--print-to-pdf={pdf_path}",
    html_path
]
res = subprocess.run(cmd, capture_output=True, text=True)
print("Exit code:", res.returncode)
if os.path.exists(pdf_path):
    print("Angle test generated. Size:", os.path.getsize(pdf_path))
else:
    print("Not found! Stderr:", res.stderr)
