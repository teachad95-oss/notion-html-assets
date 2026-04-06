import glob, json, os, subprocess

files = glob.glob('Machine Learning/**/*.ipynb', recursive=True)
missing = []

for f in files:
    if '.ipynb_checkpoints' in f:
        continue
    
    with open(f, 'r', encoding='utf-8') as n:
        nb = json.load(n)
        
    changed = False
    if 'widgets' in nb.get('metadata', {}):
        del nb['metadata']['widgets']
        changed = True
        
    if changed:
        with open(f, 'w', encoding='utf-8') as n:
            json.dump(nb, n)
        print(f'Fixed widget metadata in {f}')

    html_file = f[:-6] + '.html'
    if not os.path.exists(html_file):
        missing.append((f, html_file))

print(f"Missing HTML files: {len(missing)}")
for ipynb, html in missing:
    print(f"Converting {ipynb}")
    subprocess.run(['py', '-m', 'jupyter', 'nbconvert', '--to', 'html', ipynb])
