import glob
import re

files = sorted(glob.glob('manuscript/*.md'))

for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    
    # remove code blocks
    c = re.sub(r'```[\s\S]*?```', '', c)
    c = re.sub(r'`[^`]+`', '', c)
    
    blocks = re.findall(r'\$\$([\s\S]*?)\$\$', c)
    inlines = re.findall(r'(?<!\$)\$(?!\$)([^\$\n]+?)(?<!\$)\$(?!\$)', c)
    
    for b in blocks:
        if '<' in b or '>' in b or '&' in b:
            print(f'Block with special chars in {f}: {b}')
    for inl in inlines:
        if '<' in inl or '>' in inl or '&' in inl:
            print(f'Inline with special chars in {f}: {inl}')
