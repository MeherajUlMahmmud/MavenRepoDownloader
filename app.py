import requests
import os
import logging
from flask import Flask, request, send_from_directory


# logging.basicConfig(
#     filename="record.log", level=logging.DEBUG,
#     format="%(asctime)s %(levelname)s %(name)s %(lineno)d : %(message)s",
# )

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(lineno)d : %(message)s",
)

app = Flask(__name__)


@app.route('/')
def index():
    return 'Local Maven Repository'


@app.route('/local-repo/<path:filepath>', methods=["GET"])
def serve_local_file(filepath):
    logging.info(f'IP ADDRESS: {request.remote_addr}')
    logging.info(f'FILEPATH: {filepath}')

    maven_repo_path = os.path.join(os.getcwd(), 'maven-repo')
    local_file_path = os.path.join(maven_repo_path, filepath)

    # check if the file exists locally
    if os.path.isfile(local_file_path):
        logging.info(f'Serving file from local repository: {filepath}')
        return send_from_directory(maven_repo_path, filepath)

    logging.warning(
        f'File not found locally. Attempting to download: {filepath}')

    # If the file is not found locally, try to download it from a remote repository
    # Replace with your remote repository URL
    remote_repository_url = 'https://repo1.maven.org/maven2'
    remote_file_url = f'{remote_repository_url}/{filepath}'

    response = requests.get(remote_file_url)

    if response.status_code == 200:
        # Save the downloaded file to the local repository
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
        with open(local_file_path, 'wb') as local_file:
            local_file.write(response.content)

        logging.info(f'Downloaded and served: {filepath}')
        return send_from_directory(maven_repo_path, filepath)
    else:
        logging.error(f'Error downloading file: {response.status_code}')
        return "File not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
