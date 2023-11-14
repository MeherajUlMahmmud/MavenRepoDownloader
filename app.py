import requests
import os
import logging
from flask import Flask, request, send_from_directory


logging.basicConfig(
    filename="record.log", level=logging.DEBUG,
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
    print(f'maven_repo_path: {maven_repo_path}')

    try:
        # Try to serve the file
        print(os.path.join(maven_repo_path, filepath))
        return send_from_directory(maven_repo_path, filepath)
    except Exception as e:
        logging.error('ERROR SERVING FILE FROM LOCAL REPO')
        return "File not found", 404

# @app.route('/local-repo/<path:filepath>', methods=["GET"])
# def serve_file(filepath):
#     print(f'filepath: {filepath}')

#     maven_repo_path = os.path.join(os.getcwd(), 'maven-repo')
#     # check if the filepath points to a file or a directory
#     isFile = os.path.isfile(os.path.join(maven_repo_path, filepath))
#     print(f'isFile: {isFile}')

#     if isFile:
#         try:
#             # Try to serve the file
#             return send_from_directory(maven_repo_path, filepath)
#         except Exception as e:
#             print(f'Error serving file: {e}')
#             return "File not found", 404
#     else:
#         # If the filepath points to a directory, go into the directory and find the latest version
#         # of the artifact and serve it
#         try:
#             # Get the list of all the directories in the directory
#             directories = os.listdir(os.path.join(maven_repo_path, filepath))
#             print(os.path.join(maven_repo_path, filepath))
#             print(directories)
#             print(len(directories))

#             METADATA_FILE = 'maven-metadata.xml'
#             # read the maven-metadata.xml file
#             if METADATA_FILE in directories:
#                 with open(os.path.join(maven_repo_path, filepath, METADATA_FILE), 'r') as f:
#                     metadata = f.read()
#                     print(metadata)
#                     # Get the latest version from the maven-metadata.xml file
#                     latest_version = metadata.split(
#                         '<latest>')[1].split('</latest>')[0]
#                     print(f'latest_version: {latest_version}')
#                     # Get the list of files in the latest version directory
#                     latest_version_files = os.listdir(
#                         os.path.join(maven_repo_path, filepath, latest_version))
#                     print(f'latest_version_files: {latest_version_files}')
#                     # Check if the latest version of the artifact has the expected filename
#                     if latest_version_files[0] != filepath.split('/')[-1] + '-' + latest_version + '.jar':
#                         return "File not found", 404
#                     # Serve the file
#                     return send_from_directory(os.path.join(maven_repo_path, filepath, latest_version), latest_version_files[0])
#             else:
#                 return "File not found", 404

#         except Exception as e:
#             print(f'Error serving file: {e}')
#             return "File not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
