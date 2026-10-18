import os
import glob

manuscript_dir = os.path.join(os.path.dirname(__file__), 'manuscript')
files = sorted(glob.glob(os.path.join(manuscript_dir, '*.md')))

for fpath in files:
    fname = os.path.basename(fpath)
    with open(fpath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    matches = [i for i, l in enumerate(lines) if '承上启下' in l or '衔接第' in l]
    if matches:
        print(f"=== {fname} ===")
        start = max(0, matches[0] - 8)
        for i in range(start, len(lines)):
            print(f"{i+1:3d}: {lines[i]}", end='')
        print("\n" + "="*50 + "\n")
