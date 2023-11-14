# Maven Repository Downloader

The Maven Repository Downloader is a Flask REST API to automate retrieval of artifacts from Maven repositories.

## Features

-   Dynamic handling of Maven repository URLs.
-   Automatic creation of a Maven-like folder structure.
-   Efficient downloading of artifacts from provided URLs or via API calls.

## Installation

-   Create a virtual environement with the `requirements.txt` file

```bash
  python -m venv venv
```

```bash
  pip install -r requirements.txt
```

-   Run the application

```bash
python app.py
```

## API Reference

#### Get a artifact from local repository (will not download from Maven if not found in local repository)

```http
  GET /local-repo/${filepath}
```

| Parameter  | Type     | Description                                                |
| :--------- | :------- | :--------------------------------------------------------- |
| `filepath` | `string` | **Required**. Path to the artifact in the Maven repository |

#### Get a artifact from local repository (will download from Maven if not found in local repository)

```http
  GET /remote-repo/${filepath}
```

| Parameter  | Type     | Description                                                |
| :--------- | :------- | :--------------------------------------------------------- |
| `filepath` | `string` | **Required**. Path to the artifact in the Maven repository |

## Authors

-   [@MeherajUlMahmmud](https://github.com/MeherajUlMahmmud)
