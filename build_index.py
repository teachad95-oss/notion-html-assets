import os
from urllib.parse import quote

base_dir = r"d:\Projects\teachad_notion"
index_path = os.path.join(base_dir, "index.html")

html_files = []
for root, dirs, files in os.walk(base_dir):
    # Ignore hidden folders
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    for file in files:
        if file.endswith('.html') and file != 'index.html':
            rel_path = os.path.relpath(os.path.join(root, file), base_dir)
            html_files.append(rel_path)

html_files.sort()

# Build the HTML content
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notion HTML Assets</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            margin: 40px auto;
            max-width: 800px;
            line-height: 1.6;
            font-size: 16px;
            color: #333;
            padding: 0 20px;
        }
        h1, h2, h3 { line-height: 1.2; }
        a { color: #0077cd; text-decoration: none; word-break: break-all; }
        a:hover { text-decoration: underline; }
        .list-group {
            list-style-type: none;
            padding: 0;
        }
        .list-group li {
            margin-bottom: 10px;
            padding: 10px;
            background-color: #f9f9f9;
            border-radius: 4px;
        }
        .folder {
            margin-top: 20px;
            font-weight: bold;
            font-size: 1.2em;
            border-bottom: 1px solid #eee;
            padding-bottom: 5px;
        }
    </style>
</head>
<body>
    <h1>Notion HTML Assets Directory</h1>
    <p>This repository hosts the static HTML versions of tutorial notebooks to be embedded in Notion.</p>

    <h2>Available Files</h2>
"""

# Group files by their folder
from collections import defaultdict
grouped_files = defaultdict(list)

for f in html_files:
    dir_name = os.path.dirname(f)
    if not dir_name:
        dir_name = "Root"
    grouped_files[dir_name].append(os.path.basename(f))

# Helper to normalize directory names for sorting
for dir_name in sorted(grouped_files.keys()):
    html_content += f'    <div class="folder">{dir_name}</div>\n    <ul class="list-group">\n'
    for f_name in sorted(grouped_files[dir_name]):
        # Reconstruct path and quote it
        full_rel_path = f_name if dir_name == "Root" else f"{dir_name}/{f_name}"
        # We need to replace backslashes with forward slashes for the web href
        url_path = quote(full_rel_path.replace("\\", "/"))
        html_content += f'        <li><a href="{url_path}">{f_name}</a></li>\n'
    html_content += '    </ul>\n'

html_content += """</body>
</html>
"""

with open(index_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Updated {index_path} with {len(html_files)} files.")
