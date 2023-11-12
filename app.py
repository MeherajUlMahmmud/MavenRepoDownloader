import os
from flask import Flask, send_from_directory

app = Flask(__name__)


@app.route('/local-repo/<path:filename>', methods=["GET"])
def serve_file(filename):
    print(f'filename: {filename}')

    maven_repo_path = os.path.join(os.getcwd(), 'maven-repo')

    try:
        # Try to serve the file
        return send_from_directory(maven_repo_path, filename)
    except Exception as e:
        print(f'Error serving file: {e}')
        return "File not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
