# FlaskRestDemo
A demo of a basic RESTful Flask back end

## Installation and Dependencies

To get started on the project, you will
need to install Python 3.
[You can install Python 3 here](https://www.python.org/downloads/).

This project uses [venv](https://docs.python.org/3/library/venv.html)
to manage dependencies.

Once Python 3 is installed, run the following:

```bash
python -m venv venv # Create a virtual environment
pip install -r requirements.txt # Install the dependencies in the venv
```

Once the requirements are installed, the database will have to be created from
the provided CSV file. To do this, run the `initdb.py` script:

```bash
python initdb.py
```

## Running the App

On the command line with the `venv` active, run:

```bash
python api.py
```

This launches the backend on the local host.
Go to the localhost and port specified in your
browser (e.g. `localhost:8000/`).
Then, go to the path you want to see the APIs
results. For example, try `localhost:8000/hello`.
