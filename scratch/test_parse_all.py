import os
import re
import glob
import markdown

ROOT = os.path.abspath(r"C:\Users\Administrator\Desktop\半导体见顶了吗？")
MANUSCRIPT_DIR = os.path.join(ROOT, "manuscript")
OUTPUT_HTML = os.path.join(ROOT, "scratch", "book.html")
OUTPUT_PDF = os.path.join(ROOT, "半导体见顶了吗？.pdf")

chapter_files = sorted(glob.glob(os.path.join(MANUSCRIPT_DIR, "*.md")))

print(f"Found {len(chapter_files)} chapters.")

# Helper to protect code blocks and math formulas
def convert_markdown_with_math(md_text):
    # Step 1: Protect fenced code blocks
    code_blocks = []
    def save_code_block(match):
        code_blocks.append(match.group(0))
        return f"@@@CODE_BLOCK_{len(code_blocks)-1}@@@"
    
    # Matches ```...```
    text = re.sub(r'```[\s\S]*?```', save_code_block, md_text)
    
    # Step 2: Protect inline backtick code `...`
    inline_codes = []
    def save_inline_code(match):
        inline_codes.append(match.group(0))
        return f"@@@INLINE_CODE_{len(inline_codes)-1}@@@"
    
    text = re.sub(r'`[^`\n]+`', save_inline_code, text)
    
    # Step 3: Protect block math $$...$$
    math_blocks = []
    def save_math_block(match):
        math_content = match.group(1).strip()
        math_blocks.append(math_content)
        return f"@@@MATH_BLOCK_{len(math_blocks)-1}@@@"
    
    text = re.sub(r'\$\$([\s\S]*?)\$\$', save_math_block, text)
    
    # Step 4: Protect inline math $...$
    math_inlines = []
    def save_math_inline(match):
        math_content = match.group(1).strip()
        math_inlines.append(math_content)
        return f"@@@MATH_INLINE_{len(math_inlines)-1}@@@"
    
    text = re.sub(r'(?<!\$)\$(?!\$)([^\$\n]+?)(?<!\$)\$(?!\$)', save_math_inline, text)
    
    # Step 5: Restore inline code and fenced code blocks so markdown parser can style them
    for i, code in enumerate(inline_codes):
        text = text.replace(f"@@@INLINE_CODE_{i}@@@", code)
    for i, code in enumerate(code_blocks):
        text = text.replace(f"@@@CODE_BLOCK_{i}@@@", code)
        
    # Step 6: Convert Markdown to HTML
    html = markdown.markdown(text, extensions=['tables', 'fenced_code', 'nl2br'])
    
    # Step 7: Restore math formulas with delimiters for KaTeX
    for i, m in enumerate(math_blocks):
        # Using KaTeX display delimiter
        # Escape HTML sensitive chars inside math if needed, but in KaTeX string $$...$$ is fine
        rep = f'<div class="display-math">$${m}$$</div>'
        html = html.replace(f"@@@MATH_BLOCK_{i}@@@", rep)
        # also handle case where markdown parser wrapped it in <p>
        html = html.replace(f"<p>{rep}</p>", rep)
        
    for i, m in enumerate(math_inlines):
        rep = f'<span class="inline-math">${m}$</span>'
        html = html.replace(f"@@@MATH_INLINE_{i}@@@", rep)
        
    return html

# Parse each chapter
toc_entries = []
chapter_htmls = []

for idx, fpath in enumerate(chapter_files):
    fname = os.path.basename(fpath)
    with open(fpath, "r", encoding="utf-8") as fp:
        raw_md = fp.read()
    
    # Extract title from first line (# ...)
    lines = raw_md.splitlines()
    first_heading = ""
    for line in lines:
        if line.startswith("# "):
            first_heading = line[2:].strip()
            break
            
    if not first_heading:
        first_heading = f"第 {idx} 章"
        
    # Extract sections (## ...)
    sections = []
    for line in lines:
        if line.startswith("## "):
            sec_title = line[3:].strip()
            sections.append(sec_title)
            
    chapter_id = f"chapter-{idx:02d}"
    toc_entries.append({
        "id": chapter_id,
        "title": first_heading,
        "sections": sections
    })
    
    chapter_body_html = convert_markdown_with_math(raw_md)
    chapter_htmls.append(f"""
    <div class="chapter-container" id="{chapter_id}">
      {chapter_body_html}
    </div>
    """)

print(f"Processed {len(chapter_htmls)} chapters.")
