import glob
import re
import os

files = sorted(glob.glob('manuscript/*.md'))

for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    
    # Check block math
    block_matches = re.findall(r'\$\$(.*?)\$\$', content, re.DOTALL)
    
    # Remove block math and code blocks temporarily to test inline math
    temp = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    temp = re.sub(r'`.*?`', '', temp)
    temp = re.sub(r'\$\$.*?\$\$', '', temp, flags=re.DOTALL)
    
    inline_matches = re.findall(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)', temp)
    
    # Are there any remaining lone $?
    rem = re.sub(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)', '', temp)
    lone_dollars = re.findall(r'\$', rem)
    
    print(f'{os.path.basename(f)}: blocks={len(block_matches)}, inline={len(inline_matches)}, lone_dollars={len(lone_dollars)}')
