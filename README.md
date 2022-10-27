[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=8874483&assignment_repo_type=AssignmentRepo)
# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement
An application to help students find bathrooms across NYU's campus, with the following pages:
1. Search by building (listed buildings)
2. Search by floor once a building is selected
3. Bathroom page
4. Add a bathroom
5. Your profile
6. Sign in/sign up

## User stories

User stories can be found [here](https://github.com/software-students-fall2022/web-app-exercise-team-3-1/issues)

## Task boards

[Sprint Boards](https://github.com/software-students-fall2022/web-app-exercise-team-3-1/projects?query=is:open)

## Daily Standups
Find daily standup summaries [here](https://docs.google.com/document/d/1l_AtEtYUgvswqCIDV1XkllwdDflMdx1pdjg-QFJPSUE/edit)

## How to run the application
- install and run [docker desktop](https://www.docker.com/get-started)
- create a [dockerhub](https://hub.docker.com/signup) account
- run command, `docker run --name mongodb_dockerhub -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=secret -d mongo:latest`
- connect to the database server from the command line: `docker exec -ti mongodb_dockerhub mongosh -u admin -p secret`
- this will set up your database but it will be empty right now, and will be filled in later by the app.
- exit the database shell: `exit`
- create a `.env` file
    - contents of the file:
        - MONGO_DBNAME=example
        - MONGO_URI="mongodb://admin:secret@localhost:27017/example?authSource=admin&retryWrites=true&w=majority"
        - FLASK_APP=app.py
        - FLASK_ENV=development
        - GITHUB_SECRET=your_github_secret
        - GITHUB_REPO=https://github.com/your-repository-url
- create a new virtual environment with the name `.venv`:
    ```bash
    python3 -m venv .venv
    ```
- Activate the virtual environment:
To activate the virtual environment named `.venv`...

    - On Mac:

    ```bash
    source .venv/bin/activate
    ```

    - On Windows:

    ```bash
    .venv\Scripts\activate.bat
    ```
- Install dependencies contained in the file 'requirements.txt'
    ```bash
    pip3 install -r requirements.txt
    ```
- define two environment variables from the command line:
  - on Mac, use the commands: `export FLASK_APP=app.py` and `export FLASK_ENV=development`.
  - on Windows, use `set FLASK_APP=app.py` and `set FLASK_ENV=development`.
- start flask with `flask run` - this will output an address at which the app is running locally, e.g. https://127.0.0.1:5000. Visit that address in a web browser.
- in some cases, the command `flask` will not be found when attempting `flask run`... you can alternatively launch it with `python3 -m flask run --host=0.0.0.0 --port=10000`

