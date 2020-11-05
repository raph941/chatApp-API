[![Status](https://img.shields.io/website-up-down-green-red/https/chatapp-be-api.herokuapp.com//health.svg)](https://chatapp-be-api.herokuapp.com/)
[![Python Version](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/django%20versions-3.0-blue.svg)](https://www.djangoproject.com/)
[![Made with React](https://img.shields.io/badge/made%20with-React-orange.svg)](https://reactjs.org/)

| **Branch** | **CircleCI** |
|:-----------|:-------------|
| [`master`](https://github.com/raph941/chatApp-API/tree/master) | [![raph941](https://circleci.com/gh/raph941/chatApp-API.svg?style=svg)](https://app.circleci.com/pipelines/github/raph941/chatApp-API)


## Getting Started
Follow these instructions, to get a copy and run on your PC

### Prerequisites
1. A Computer (😀😁)
2. Virtual Environment Installed (recommended not compulsory)
3. Pyhthon 3.8 installed globaly or within the VirtualEnv


### Environmental Variables

| Name | Required | Value |
|------|----------|---------|
| `SECRET_KEY` | :heavy_check_mark: | String, standard Django setting |
| `ALLOWED_HOSTS` | :heavy_check_mark: | `localhost` |
| `DEBUG` | :heavy_check_mark: | Boolean, standard Django setting |
| `DATABASE_URL` | :x: | standard Django setting |
| `SQL_ENGINE` | :heavy_check_mark: | standard Django setting |
| `SQL_DATABASE` | :heavy_check_mark: | standard Django setting |
| `SQL_USER` | :heavy_check_mark: | standard Django setting |
| `SQL_PASSWORD` | :heavy_check_mark: | standard Django setting |
| `SQL_HOST` | :heavy_check_mark: | standard Django setting |
| `REDIS_URL` | :heavy_check_mark: | standard Django setting |

#### Frontend

- [Node.js](https://nodejs.org/en/download/)
- [yarn](https://yarnpkg.com/)
- Repo: [Click here](https://github.com/raph941/chatApp-FE)

### Procedures

1. Clone this repository: `https://github.com/raph941/chatApp-API.git`

2. Setup `pipenv` and Python dependencies:

   ```
   pip install --user pipenv
   pipenv --python 3.6
   pipenv shell
   ```

   After successful setup, a prefix `(env_name)` should appear on the left of your terminal.

3. Install Project Dependencies
    ```
    pipenv install (if you are using pipenv)
    or
    pip install -r requirements.txt
    ```

4. Create the environment file `.env` on the root directory Use this as an example (do not copy😀):
    ```
    SECRET_KEY=choose-a-secreat-key
    DEBUG=True
    ALLOWED_HOSTS = *
    SQL_ENGINE=django.db.backends.postgresql
    SQL_DATABASE=sample-db
    SQL_USER=db-user
    SQL_PASSWORD=db-password
    SQL_HOST=your-db-host-name
    SQL_PORT=5432
    REDIS_URL = 'redis://localhost:6379'
    DATABASE_URL = 'your-database-url-here'
    ```

5. Create Migrations: this sets up your database with all the necessary tables needed for the app to run
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
6. Run the app
    ```
    python manage.py runserver
    ```