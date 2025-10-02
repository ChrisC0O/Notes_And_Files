from flask import Flask, send_file, request, render_template_string, abort
import os
import zipfile
import io

app = Flask(__name__)
UPLOAD_FOLDER = os.getcwd()

# HTML template for the file browser
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Browser</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        a { text-decoration: none; color: #0066cc; }
        a:hover { text-decoration: underline; }
        .upload-form { margin-bottom: 20px; }
        .error { color: red; }
    </style>
</head>
<body>
    <h1>File Browser</h1>
    <h2>Current Directory: {{ current_dir }}</h2>

    {% if error %}
    <p class="error">{{ error }}</p>
    {% endif %}

    <div class="upload-form">
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" multiple>
            <input type="submit" value="Upload File(s)">
        </form>
    </div>

    <table>
        <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Action</th>
        </tr>
        {% for item in items %}
        <tr>
            <td>{{ item.name }}</td>
            <td>{{ 'Directory' if item.is_dir else 'File' }}</td>
            <td>
                {% if item.is_dir %}
                <a href="/download?path={{ item.path }}&zip=true">Download as ZIP</a>
                {% else %}
                <a href="/download?path={{ item.path }}">Download</a>
                {% endif %}
            </td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""


@app.route('/')
def index():
    files = []
    for item in os.listdir(UPLOAD_FOLDER):
        item_path = os.path.join(UPLOAD_FOLDER, item)
        files.append({
            'name': item,
            'path': item,
            'is_dir': os.path.isdir(item_path)
        })
    files.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
    return render_template_string(HTML_TEMPLATE, items=files, current_dir=UPLOAD_FOLDER, error=None)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template_string(HTML_TEMPLATE, items=[], current_dir=UPLOAD_FOLDER,
                                      error="No file part in the request")

    files = request.files.getlist('file')
    for file in files:
        if file and file.filename:
            # Extract only the filename, discarding client-side path
            filename = os.path.basename(file.filename)
            # Ensure filename is not empty and is safe
            if filename:
                try:
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                except Exception as e:
                    return render_template_string(HTML_TEMPLATE, items=[], current_dir=UPLOAD_FOLDER,
                                                  error=f"Error saving file {filename}: {str(e)}")
            else:
                return render_template_string(HTML_TEMPLATE, items=[], current_dir=UPLOAD_FOLDER,
                                              error="Invalid filename")

    return index()


@app.route('/download')
def download_file():
    path = request.args.get('path')
    as_zip = request.args.get('zip') == 'true'
    full_path = os.path.join(UPLOAD_FOLDER, path)

    if not os.path.exists(full_path):
        abort(404)

    if os.path.isdir(full_path) and as_zip:
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(full_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, UPLOAD_FOLDER)
                    zf.write(arcname, file_path)
        memory_file.seek(0)
        return send_file(
            memory_file,
            download_name=f"{path}.zip",
            as_attachment=True
        )
    elif os.path.isfile(full_path):
        return send_file(full_path, as_attachment=True)
    else:
        abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
