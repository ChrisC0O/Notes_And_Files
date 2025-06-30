from flask import Flask, send_from_directory, render_template_string, abort, send_file
import os
from pathlib import Path
import zipfile
import io

app = Flask(__name__)

# HTML template for the index page
INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Browser</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        tr:hover { background-color: #f5f5f5; }
        a { text-decoration: none; color: #0066cc; }
        a:hover { text-decoration: underline; }
        .folder { font-weight: bold; }
        .file-size { text-align: right; }
    </style>
</head>
<body>
    <h1>File Browser: {{ current_path }}</h1>
    <p><a href="{{ parent_path }}">.. (Parent Directory)</a></p>
    <table>
        <tr><th>Name</th><th>Size</th><th>Type</th></tr>
        {% for item in items %}
        <tr>
            <td>
                {% if item.is_dir %}
                <span class="folder">📁</span>
                <a href="{{ url_for('index', path=item.relative_path) }}">{{ item.name }}</a>
                (<a href="{{ url_for('download_file', path=item.relative_path) }}">Download as ZIP</a>)
                {% else %}
                <span>📄</span>
                <a href="{{ url_for('download_file', path=item.relative_path) }}">{{ item.name }}</a>
                {% endif %}
            </td>
            <td class="file-size">{{ item.size }}</td>
            <td>{{ 'Directory' if item.is_dir else 'File' }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

def get_file_size(path):
    """Get file or folder size in human-readable format."""
    if not path.is_file():
        if path.is_dir():
            total_size = sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
            for unit in ['B', 'KB', 'MB', 'GB']:
                if total_size < 1024:
                    return f"{total_size:.2f} {unit}"
                total_size /= 1024
            return f"{total_size:.2f} TB"
        return "-"
    size = path.stat().st_size
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"

def zip_folder(folder_path):
    """Create a ZIP archive of a folder in memory."""
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = Path(root) / file
                arcname = str(file_path.relative_to(folder_path.parent))
                zf.write(file_path, arcname)
    memory_file.seek(0)
    return memory_file

@app.route('/')
@app.route('/<path:path>')
def index(path=''):
    """Display directory listing."""
    current_dir = Path.cwd() / path
    if not current_dir.exists():
        abort(404)
    
    if current_dir.is_file():
        return send_from_directory(current_dir.parent, current_dir.name, as_attachment=True)
    
    items = []
    for item in current_dir.iterdir():
        if item.name.startswith('.'):  # Skip hidden files
            continue
        items.append({
            'name': item.name,
            'is_dir': item.is_dir(),
            'size': get_file_size(item),
            'relative_path': str(item.relative_to(Path.cwd()))
        })
    
    items.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
    
    parent_path = str(Path(path).parent) if path else ''
    
    return render_template_string(
        INDEX_TEMPLATE,
        items=items,
        current_path=str(path) or '/',
        parent_path=parent_path
    )

@app.route('/download/<path:path>')
def download_file(path):
    """Serve file or folder (as ZIP) for download."""
    target_path = Path.cwd() / path
    if not target_path.exists():
        abort(404)
    
    if target_path.is_file():
        return send_from_directory(target_path.parent, target_path.name, as_attachment=True)
    
    if target_path.is_dir():
        zip_file = zip_folder(target_path)
        return send_file(
            zip_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f"{target_path.name}.zip"
        )
    
    abort(404)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
