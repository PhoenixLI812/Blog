import os
import re
import glob
import subprocess
import markdown

ROOT = os.path.abspath(r"C:\Users\Administrator\Desktop\半导体见顶了吗？")
MANUSCRIPT_DIR = os.path.join(ROOT, "manuscript")
OUTPUT_HTML = os.path.join(ROOT, "scratch", "book.html")
OUTPUT_PDF = os.path.join(ROOT, "半导体见顶了吗？.pdf")
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

chapter_files = sorted(glob.glob(os.path.join(MANUSCRIPT_DIR, "*.md")))

print(f"Loading {len(chapter_files)} chapter files...")

# Math-safe Markdown to HTML converter
def convert_markdown_with_math(md_text):
    # Step 1: Protect fenced code blocks ```...```
    code_blocks = []
    def save_code_block(match):
        code_blocks.append(match.group(0))
        return f"\n\n@@@CODE_BLOCK_{len(code_blocks)-1}@@@\n\n"
    text = re.sub(r'```[\s\S]*?```', save_code_block, md_text)
    
    # Step 2: Protect inline backticks `...`
    inline_codes = []
    def save_inline_code(match):
        inline_codes.append(match.group(0))
        return f"@@@INLINE_CODE_{len(inline_codes)-1}@@@"
    text = re.sub(r'`[^`\n]+`', save_inline_code, text)
    
    # Step 3: Protect block math $$...$$
    math_blocks = []
    def save_math_block(match):
        content = match.group(1).strip()
        math_blocks.append(content)
        return f"\n\n@@@MATH_BLOCK_{len(math_blocks)-1}@@@\n\n"
    text = re.sub(r'\$\$([\s\S]*?)\$\$', save_math_block, text)
    
    # Step 4: Protect inline math $...$
    math_inlines = []
    def save_math_inline(match):
        content = match.group(1).strip()
        math_inlines.append(content)
        return f"@@@MATH_INLINE_{len(math_inlines)-1}@@@"
    text = re.sub(r'(?<!\$)\$(?!\$)([^\$\n]+?)(?<!\$)\$(?!\$)', save_math_inline, text)
    
    # Step 5: Restore inline codes and code blocks for Markdown rendering
    for i, code in enumerate(inline_codes):
        text = text.replace(f"@@@INLINE_CODE_{i}@@@", code)
    for i, code in enumerate(code_blocks):
        text = text.replace(f"@@@CODE_BLOCK_{i}@@@", code)
        
    # Step 6: Render markdown
    html = markdown.markdown(text, extensions=['tables', 'fenced_code', 'attr_list'])
    
    # Step 7: Restore math formulas
    for i, m in enumerate(math_blocks):
        rep = f'<div class="display-math">$${m}$$</div>'
        html = html.replace(f"<p>@@@MATH_BLOCK_{i}@@@</p>", rep)
        html = html.replace(f"@@@MATH_BLOCK_{i}@@@", rep)
        
    for i, m in enumerate(math_inlines):
        rep = f'<span class="inline-math">${m}$</span>'
        html = html.replace(f"@@@MATH_INLINE_{i}@@@", rep)
        
    return html

# Parse chapters
chapters_data = []

for idx, fpath in enumerate(chapter_files):
    fname = os.path.basename(fpath)
    with open(fpath, "r", encoding="utf-8") as fp:
        raw_md = fp.read()
    
    lines = raw_md.splitlines()
    title = ""
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            break
            
    sections = []
    for line in lines:
        if line.startswith("## "):
            sec = line[3:].strip()
            sections.append(sec)
            
    chap_id = f"chap-{idx:02d}"
    body_html = convert_markdown_with_math(raw_md)
    
    chapters_data.append({
        "id": chap_id,
        "title": title,
        "sections": sections,
        "body_html": body_html
    })

# Build TOC HTML
toc_items_html = []
for idx, chap in enumerate(chapters_data):
    sec_html = ""
    if chap["sections"]:
        sec_lis = "".join([f'<li>{s}</li>' for s in chap["sections"]])
        sec_html = f'<ul class="toc-sections">{sec_lis}</ul>'
        
    item = f"""
    <div class="toc-item">
      <div class="toc-chapter-title">
        <a href="#{chap['id']}">{chap['title']}</a>
      </div>
      {sec_html}
    </div>
    """
    toc_items_html.append(item)

toc_html = "\n".join(toc_items_html)

# CSS Stylesheet
CSS = """
@page {
  size: A4;
  margin: 22mm 20mm 22mm 20mm;
  @top-right {
    content: "《半导体见顶了吗？》";
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
    font-size: 8.5pt;
    color: #94a3b8;
    border-bottom: 0.5pt solid #cbd5e1;
    padding-bottom: 4px;
  }
  @bottom-center {
    content: "第 " counter(page) " 页 / 共 " counter(pages) " 页";
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
    font-size: 8.5pt;
    color: #94a3b8;
  }
}

@page :first {
  margin: 0;
  @top-right { content: normal; }
  @bottom-center { content: normal; }
}

* {
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Noto Sans CJK SC", sans-serif;
  font-size: 10.5pt;
  line-height: 1.8;
  color: #1e293b;
  background: #ffffff;
  margin: 0;
  padding: 0;
  text-align: justify;
}

/* ================= Cover Page ================= */
.cover-page {
  page-break-before: avoid;
  page-break-after: always;
  height: 297mm;
  width: 210mm;
  padding: 45mm 25mm 30mm 25mm;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background: linear-gradient(145deg, #0f172a 0%, #1e293b 60%, #0f172a 100%);
  color: #f8fafc;
  position: relative;
  overflow: hidden;
}

.cover-accent-line {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 6px;
  background: linear-gradient(90deg, #3b82f6, #06b6d4, #10b981);
}

.cover-decor {
  position: absolute;
  right: -60px;
  top: 40px;
  width: 320px;
  height: 320px;
  border: 1px solid rgba(255, 255, 255, 0.07);
  border-radius: 50%;
  pointer-events: none;
}

.cover-decor-2 {
  position: absolute;
  right: -20px;
  top: 80px;
  width: 240px;
  height: 240px;
  border: 1px solid rgba(59, 130, 246, 0.15);
  border-radius: 50%;
  pointer-events: none;
}

.cover-badge {
  display: inline-block;
  padding: 4px 14px;
  background: rgba(59, 130, 246, 0.15);
  border: 1px solid rgba(59, 130, 246, 0.35);
  border-radius: 20px;
  font-size: 9pt;
  color: #93c5fd;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 25px;
}

.cover-title {
  font-size: 34pt;
  font-weight: 800;
  line-height: 1.25;
  color: #ffffff;
  letter-spacing: 0.04em;
  margin: 0 0 20px 0;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
  border-left: none;
  padding-left: 0;
}

.cover-divider {
  width: 80px;
  height: 4px;
  background: #3b82f6;
  border-radius: 2px;
  margin-bottom: 25px;
}

.cover-subtitle {
  font-size: 13.5pt;
  font-weight: 400;
  line-height: 1.6;
  color: #cbd5e1;
  max-width: 95%;
  margin: 0 0 30px 0;
}

.cover-core-chains {
  margin-top: 25px;
  padding: 16px 20px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  font-size: 9pt;
  line-height: 1.7;
  color: #94a3b8;
}

.cover-core-chains strong {
  color: #e2e8f0;
}

.cover-footer {
  border-top: 1px solid rgba(255, 255, 255, 0.12);
  padding-top: 20px;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  font-size: 9.5pt;
  color: #64748b;
}

.cover-footer-left {
  line-height: 1.6;
}

.cover-footer-left .author-name {
  color: #f1f5f9;
  font-weight: 600;
  font-size: 11pt;
}

.cover-footer-right {
  text-align: right;
  letter-spacing: 0.05em;
  color: #94a3b8;
}

/* ================= Table of Contents ================= */
.toc-page {
  page-break-before: always;
  page-break-after: always;
  padding-top: 10mm;
}

.toc-header {
  font-size: 22pt;
  font-weight: 700;
  color: #0f172a;
  border-bottom: 2px solid #0f172a;
  padding-bottom: 8px;
  margin-bottom: 24px;
  letter-spacing: 0.05em;
}

.toc-item {
  margin-bottom: 14px;
  page-break-inside: avoid;
}

.toc-chapter-title {
  font-size: 10.5pt;
  font-weight: 600;
}

.toc-chapter-title a {
  color: #0f172a;
  text-decoration: none;
  border-bottom: 1px dotted #94a3b8;
  padding-bottom: 1px;
}

.toc-chapter-title a:hover {
  color: #2563eb;
}

.toc-sections {
  list-style: none;
  padding-left: 18px;
  margin: 4px 0 0 0;
  font-size: 8.5pt;
  color: #64748b;
  line-height: 1.55;
}

.toc-sections li {
  position: relative;
  padding-left: 12px;
}

.toc-sections li::before {
  content: "•";
  position: absolute;
  left: 0;
  color: #94a3b8;
}

/* ================= Chapters Layout ================= */
.chapter-container {
  page-break-before: always;
  padding-top: 10mm;
}

h1 {
  font-size: 20pt;
  font-weight: 800;
  color: #0f172a;
  line-height: 1.35;
  margin: 0 0 16px 0;
  letter-spacing: 0.02em;
  border-left: 5px solid #2563eb;
  padding-left: 14px;
}

h2 {
  font-size: 14pt;
  font-weight: 700;
  color: #1e293b;
  margin: 28px 0 12px 0;
  padding-bottom: 6px;
  border-bottom: 1px solid #e2e8f0;
  page-break-after: avoid;
}

h3 {
  font-size: 12pt;
  font-weight: 600;
  color: #334155;
  margin: 20px 0 10px 0;
  page-break-after: avoid;
}

h4 {
  font-size: 11pt;
  font-weight: 600;
  color: #475569;
  margin: 16px 0 8px 0;
  page-break-after: avoid;
}

p {
  margin: 0 0 14px 0;
  text-indent: 0;
}

hr {
  border: none;
  border-top: 1px solid #e2e8f0;
  margin: 24px 0;
}

/* ================= Lists ================= */
ul, ol {
  padding-left: 24px;
  margin: 8px 0 16px 0;
}

li {
  margin-bottom: 6px;
  line-height: 1.7;
}

li strong {
  color: #0f172a;
}

/* ================= Blockquotes ================= */
blockquote {
  border-left: 3.5px solid #3b82f6;
  background: #f8fafc;
  padding: 12px 18px;
  margin: 16px 0;
  border-radius: 0 6px 6px 0;
  color: #334155;
  font-size: 10pt;
  line-height: 1.7;
  page-break-inside: avoid;
}

blockquote p:last-child {
  margin-bottom: 0;
}

/* ================= Code & ASCII Diagrams ================= */
pre {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 12px 16px;
  margin: 16px 0;
  font-family: "Consolas", "Fira Code", "Courier New", monospace;
  font-size: 8pt;
  line-height: 1.38;
  color: #0f172a;
  overflow-x: auto;
  white-space: pre;
  page-break-inside: avoid;
}

code {
  font-family: "Consolas", "Fira Code", "Courier New", monospace;
  font-size: 9pt;
  background: #f1f5f9;
  padding: 2px 5px;
  border-radius: 4px;
  color: #0f172a;
}

pre code {
  background: transparent;
  padding: 0;
  border-radius: 0;
  color: inherit;
}

/* ================= Tables ================= */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 18px 0;
  font-size: 9pt;
  line-height: 1.5;
  page-break-inside: avoid;
}

th, td {
  border: 1px solid #cbd5e1;
  padding: 7px 10px;
  text-align: left;
  vertical-align: top;
}

th {
  background-color: #f1f5f9;
  font-weight: 600;
  color: #0f172a;
}

tr:nth-child(even) td {
  background-color: #f8fafc;
}

/* ================= Images ================= */
img {
  display: block;
  max-width: 96%;
  max-height: 215mm;
  margin: 18px auto;
  border-radius: 4px;
  page-break-inside: avoid;
}

/* ================= KaTeX Math ================= */
.display-math {
  margin: 16px 0;
  text-align: center;
  page-break-inside: avoid;
  overflow-x: auto;
}

.inline-math {
  white-space: nowrap;
}

.katex {
  font-size: 1.05em;
}

.katex-display {
  margin: 12px 0 !important;
}
"""

chapters_body = "\n".join(
    f'<div class="chapter-container" id="{c["id"]}">{c["body_html"]}</div>'
    for c in chapters_data
)

FULL_HTML = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>半导体见顶了吗？</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
  <style>
{CSS}
  </style>
</head>
<body>

  <!-- Cover Page -->
  <div class="cover-page">
    <div class="cover-accent-line"></div>
    <div class="cover-decor"></div>
    <div class="cover-decor-2"></div>
    
    <div class="cover-top">
      <div class="cover-badge">THEORY &amp; PARADIGM · 全景推演</div>
      <h1 class="cover-title">半导体<br>见顶了吗？</h1>
      <div class="cover-divider"></div>
      <div class="cover-subtitle">从微观能带到宏观二阶导：一场跨越八个数量级的理性推演</div>
      
      <div class="cover-core-chains">
        <strong>推演核心因果链：</strong><br>
        宏观资本二阶导折现重力 ➔ 晶圆物理时差与 K 型撕裂 ➔ 军备竞赛纳什均衡与折旧悬崖 ➔ 瓦解的福特主义与有效需求崩塌 ➔ 去阻尼欲望与热能耗硬墙 ➔ 沉重原子与 Sim-to-Real 鸿沟 ➔ 离散时空宇宙状态机 ➔ 内生同源观察者算力死局（$C_{{\\text{{obs}}}} \\ll C_{{\\text{{sys}}}}$）➔ 粗粒化有损压缩与时间代偿 ➔ 能带工程纳秒锚定 ➔ 跨越 8 个数量级的时钟代沟 ➔ 阻抗匹配与中观缝隙（尺度重叠原理）➔ 百毫秒主观意识卷积积分 ➔ 在波澜中自洽的驻波。
      </div>
    </div>
    
    <div class="cover-footer">
      <div class="cover-footer-left">
        <div class="author-name">理性推演录</div>
        <div>宏观经济 · 固体物理 · 计算理论 · 认知科学</div>
      </div>
      <div class="cover-footer-right">
        <div>2026 年 · 完整典藏版</div>
        <div style="font-size: 8pt; opacity: 0.7; margin-top: 2px;">A Cross-Scale Philosophical Exploration</div>
      </div>
    </div>
  </div>

  <!-- Table of Contents -->
  <div class="toc-page">
    <div class="toc-header">目 录</div>
    {toc_html}
  </div>

  <!-- Chapters Content -->
  {chapters_body}

  <script>
    document.addEventListener("DOMContentLoaded", function() {{
      if (typeof renderMathInElement === "function") {{
        renderMathInElement(document.body, {{
          delimiters: [
            {{left: '$$', right: '$$', display: true}},
            {{left: '$', right: '$', display: false}}
          ],
          throwOnError: false
        }});
      }}
    }});
  </script>
</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(FULL_HTML)

print(f"HTML generated at: {OUTPUT_HTML} (Size: {os.path.getsize(OUTPUT_HTML) / 1024:.1f} KB)")

# Now invoke Chrome headless to generate the PDF
print("Invoking Chrome to render PDF...")
cmd = [
    CHROME_PATH,
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--virtual-time-budget=20000",
    "--no-pdf-header-footer",
    f"--print-to-pdf={OUTPUT_PDF}",
    OUTPUT_HTML
]

res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print("Chrome return code:", res.returncode)

if os.path.exists(OUTPUT_PDF):
    size_mb = os.path.getsize(OUTPUT_PDF) / (1024 * 1024)
    print(f"PDF successfully generated: {OUTPUT_PDF} ({size_mb:.2f} MB)")
else:
    print("PDF generation failed! Stderr:", res.stderr.decode('utf-8', errors='replace'))
