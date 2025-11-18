import os
from flask import Flask

app = Flask(__name__)

# GCSマウントディレクトリのパス（Cloud Runの設定で指定したパス）
GCS_MOUNT_PATH = os.environ.get('GCS_MOUNT_PATH', '/gcs')


@app.route('/')
def index():
    return '''
    <h1>Cloud Run GCS Mount Test</h1>
    <ul>
        <li><a href="/list">List files in GCS</a></li>
        <li><a href="/read/sample.txt">Read sample.txt</a></li>
        <li><a href="/write">Write test file</a></li>
    </ul>
    '''



@app.route('/list')
def list_files():
    """マウントされたGCSバケット内のファイル一覧を表示"""
    try:
        if not os.path.exists(GCS_MOUNT_PATH):
            return f"Error: Mount path {GCS_MOUNT_PATH} does not exist", 404

        files = []
        for root, dirs, filenames in os.walk(GCS_MOUNT_PATH):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                relative_path = os.path.relpath(filepath, GCS_MOUNT_PATH)
                size = os.path.getsize(filepath)
                files.append(f"{relative_path} ({size} bytes)")

        if not files:
            return f"No files found in {GCS_MOUNT_PATH}"

        return "<br>".join(files)
    except Exception as e:
        return f"Error listing files: {str(e)}", 500


@app.route('/read/<path:filename>')
def read_file(filename):
    """指定されたファイルの内容を読み取る"""
    try:
        filepath = os.path.join(GCS_MOUNT_PATH, filename)

        if not os.path.exists(filepath):
            return f"File {filename} not found", 404

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        return f"<h2>Content of {filename}:</h2><pre>{content}</pre>"
    except Exception as e:
        return f"Error reading file: {str(e)}", 500


@app.route('/write')
def write_file():
    """テストファイルを書き込む"""
    try:
        test_file = os.path.join(GCS_MOUNT_PATH, 'test_write.txt')

        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('This is a test file written from Cloud Run\n')
            f.write(f'Timestamp: {os.popen("date").read()}')

        return f"Successfully wrote to {test_file}"
    except Exception as e:
        return f"Error writing file: {str(e)}", 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
