## Make a Todo List by Flask

Things learned:
- Run a "Hello world" application
    ```sh
    python -m venv env
    ./env/Scripts/activate
    pip install -r requirements.txt
    python app.py
    ```
- Template (jinja template), template inheritance
- Init the database
    ```sh
    python
    >>> from app import db
    >>> from app import app
    >>> with app.app_context():
    >>> ...  db.create_all()
    ```