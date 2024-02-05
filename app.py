"""
@Project: Local Maven Repository Server for Java
@Description: This server will serve the maven repository locally. If the file is not found locally, it will download the file from remote repository and serve it.

@Author:  Meharaj - Ul- Mahmmud
@Date: 15-Nov-2023

"""

import requests
import os
from flask import Flask, render_template, request, send_from_directory

from logger import setup_logger

app = Flask(__name__)

# Set up logger
logger = setup_logger()

remote_repository_urls = [
    'https://repo1.maven.org/maven2',
    'https://repo.maven.apache.org/maven2',
]


@app.route('/')
def index():
    maven_repo_path = os.path.join(os.getcwd(), 'maven-repo')
    folders = os.listdir(maven_repo_path)
    return render_template('index.html', folders=folders, parent_content=[], url_path='/')


@app.route('/<path:folderpath>')
def folder(folderpath):
    # folderpath = junit/junit/4.12/junit-4.12.pom

    maven_repo_path = os.path.join(os.getcwd(), 'maven-repo')
    # maven_repo_path = current working directory + maven-repo

    folder_path = os.path.join(maven_repo_path, folderpath)
    # folderpath = https://repo1.maven.org/maven2 + junit/junit/4.12/junit-4.12.pom

    url_path = os.path.join('/', folderpath)
    # url_path = / + junit/junit/4.12/junit-4.12.pom

    # if folder_path is a file, serve the file
    if os.path.isfile(folder_path):
        """
        Folder path is a file, serve the file
        """
        return send_from_directory(maven_repo_path, folderpath)

    # if folder_path is a folder, list the content of the folder
    parent_folder = os.path.dirname(folderpath)
    parent_folder_path = os.path.join(maven_repo_path, parent_folder)
    parent_content = os.listdir(parent_folder_path)

    # Get the list of folders and files in the folder_path
    try:
        item_list = os.listdir(folder_path)
        folders = []
        files = []
        for item in item_list:
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                folders.append(item)
            else:
                files.append(item)
        return render_template('index.html', folders=folders, files=files, parent_content=parent_content, url_path=url_path)
    except FileNotFoundError:
        return "Folder not found", 404


@app.route('/local-repo/<path:filepath>', methods=["GET"])
def serve_local_file(filepath):
    logger.info(f'IP ADDRESS: {request.remote_addr}')
    logger.info(f'FILEPATH: {filepath}')

    maven_repo_path = os.path.join(os.getcwd(), 'maven-repo')
    # maven_repo_path = current working directory + maven-repo

    local_file_path = os.path.join(maven_repo_path, filepath)
    # local_file_path = maven_repo_path + junit/junit/4.12/junit-4.12.pom

    if os.path.isfile(local_file_path):
        logger.info('FILE FOUND IN LOCAL REPOSITORY')
        logger.info(f'SERVING FILE FROM LOCAL REPOSITORY: {filepath}')
        return send_from_directory(maven_repo_path, filepath)

    logger.warning(
        f'FILE NOT FORUND LOCALLY. ATTEMPTING TO DOWNLOAD: {filepath}')

    for remote_repository_url in remote_repository_urls:
        logger.info(
            f'ATTEMPTING TO DOWNLOAD FROM REMOTE REPOSITORY: {remote_repository_url}')
        remote_file_url = f'{remote_repository_url}/{filepath}'
        response = requests.get(remote_file_url)

        if response.status_code == 200:
            logger.info(
                f'FILE DOWNLOADED FROM REMOTE REPOSITORY: {remote_file_url}')
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
            with open(local_file_path, 'wb') as local_file:
                local_file.write(response.content)

            logger.info(f'FILE DOWNLOADED AND SERVING: {filepath}')
            return send_from_directory(maven_repo_path, filepath)
        else:
            logger.error(
                f'ERROR DOWNLOADING FILE FROM REMOTE REPOSITORY: {remote_file_url}')
            logger.error(f'ERROR DOWNLOADING FILE: {response.status_code}')
            continue


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
