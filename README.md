# mongofitness-backend

Simple FastAPI backend for the mongofitness app.

## Pre-requisites

This is a backend for the mongofitness app. It requires a MongoDB database to be running. The database is populated with data using the [`mongofitness-sync`](https://github.com/officialankan/mongofitness-sync) package. 

## Installation

Follow these steps to install the package using Poetry:

1. Clone the repository
2. Run `poetry install` in the root directory of the repository


Environment variables are handled using `pydantic` settings and `.env` files. The following files are required:
- `.env`: Contains a `environment` variable set to either `dev` or `dev`. This is used to determine which `.env` file to use. Set to `dev` to be able to run the tests.
- `.env.dev`: Contains `db_dsn`, the mongodb dsn, `db_name`, the name of the database to use and `db_collection`, the name of the collection to use.
- `.env.prod`: Contains `db_dsn`, the mongodb dsn, `db_name`, the name of the database to use and `db_collection`, the name of the collection to use.

## Usage

To run the server, run `poetry run uvicorn app.main:app` in the root directory of the repository.