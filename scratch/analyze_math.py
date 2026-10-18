import glob
import re
import os

files = sorted(glob.glob('manuscript/*.md'))
dollar_lines = []
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        for idx, line in enumerate(fp):
            if '$' in line:
                dollar_lines.append((os.path.basename(f), idx+1, line.strip()))

print(f'Total lines with $: {len(dollar_lines)}')

# Check lines where $ might not be LaTeX math
single_dollar_odd = []
for fname, lnum, line in dollar_lines:
    # count non-escaped dollars
    # check if odd number of $ in line (unless block math)
    cnt = line.count('$')
    if cnt % 2 != 0:
        single_dollar_odd.append((fname, lnum, line))

print(f'Lines with odd number of $: {len(single_dollar_odd)}')
for item in single_dollar_odd[:20]:
    print(f'{item[0]}:{item[1]}: {item[2]}')
