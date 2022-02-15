# Pet Agenda (backend)

## Description

API for keeping track of a pet parent's pets and their a pet's needs.<br>Used for Pet Agenda (frontend).

FastAPI framework using ORM SQLAlchemy with a PostgreSQL server. Deployed to Heroku.


## Dependencies

These are some important dependencies, but all are found in requirements.txt<br>
Python version important if using Heroku for deployment.

In `requirements.txt`,
  ```bash
  black==22.1.0
  email-validator==1.1.3
  fastapi==0.73.0
  passlib==1.7.4
  psycopg2-binary==2.8.6
  pydantic==1.9.0
  python==3.8.9
  python-dotenv==0.19.2
  python-jose==3.3.0
  SQLAlchemy==1.3.24
  uvicorn==0.17.4
  ```

## Instructions
<ol>
  <li>Clone repository</li>
  <li>cd into project folder</li>
  <li>Create virtual environment in project folder</li>
  
    python -m venv venv

  <li>Create .env file in root directory and add the below lines</li>
  
    POSTGRES_USER=USER
    POSTGRES_PASSWORD=PASSWORD
    POSTGRES_SERVER=localhost
    POSTGRES_PORT=5432
    POSTGRES_DB=DATABASENAME


  <li>Install dependencies</li>
  
    pip install -r requirements.txt
</ol>


## TODOs
<ol>
  <li>Clean up user authentication code</li>
  <li>Edit pet diet endpoints to reflect keeping track of a pet's diet</li>
  <li>Include pet exercise model and schema</li>
</ol>

## Useful Tutorials & Resources

- rithmic -Youtube
- Bitfumes -Youtube

[SQLAlchemy Docs](https://www.sqlalchemy.org/)

[FastAPI SQL Relational db tutorial](https://fastapi.tiangolo.com/tutorial/)

[FastAPI Bigger Application Tutorial](https://fastapi.tiangolo.com/tutorial/bigger-applications/)


