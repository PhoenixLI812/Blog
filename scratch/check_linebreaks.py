import glob
import os

files = sorted(glob.glob('manuscript/*.md'))

for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    
    # Check if there are consecutive non-empty lines that are not lists, headers, or code blocks
    in_code = False
    consec_text = 0
    for i in range(len(lines) - 1):
        l1 = lines[i].strip()
        l2 = lines[i+1].strip()
        if l1.startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        if l1 and l2 and not l1.startswith('#') and not l2.startswith('#') and not l1.startswith('-') and not l2.startswith('-') and not l1.startswith('*') and not l2.startswith('*') and not l1.startswith('|') and not l2.startswith('|') and not l1.startswith('>'):
            consec_text += 1
            
    print(f'{os.path.basename(f)}: consecutive prose lines = {consec_text}')
