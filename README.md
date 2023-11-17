# mongofitness-backend

Simple FastAPI backend for the mongofitness app.

## Pre-requisites

This is a backend for the mongofitness app. It requires a MongoDB database to be running. The database is populated with data using the [`mongofitness-sync`](https://github.com/officialankan/mongofitness-sync) package. 

## Installation

Follow these steps to install the package using Poetry:

1. Clone the repository
2. Install Poetry
3. Run `poetry install` in the root directory of the repository

## Usage

To run the server, run `poetry run uvicorn mongofitness_backend.main:app` in the root directory of the repository.