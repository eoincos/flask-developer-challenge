# gistapi
Gistapi is a simple HTTP API server implimented in Flask for searching a user's public Github Gists. The gistapi code in this repository has 
been left incompete for you to finish.

## Contents
This project contains a [tox](https://testrun.org/tox/latest/) definition for testing against both Python 2.7 and Python 3.4.
There is a `requirements.txt` file for installing the required Python modules via pip.  There is a `Dockerfile` and `docker-compose.yml` file 
if you'd like to run the project as a docker container.  The `tests/` directory contains two very simple tests to get started.  The `gistapi/`
directory contains the code you'll want to modify to implement the desired features.

## Challenge
The existing code already impliments most of the Flask boilerplate for you. The main functionality is left for you to implement.  The goal is to 
impliment an endpoint that searches a user's Gists with a regular expression.  For example, I'd like to know all Gists for user `justdionysus` that 
contain the pattern `import requests`. There is also a failing test that should pass once you've successfully implemented the search 
process (and should illustrate the expected format of the response).  The code in `gistapi.py` contains some comments to help you find your way.

To complete the challenge, you'll have to write some HTTP queries from `Gistapi` to the Github API to pull down each Gist for the target user.  
Please don't use a github API client (i.e. using an HTTP request library like requests or aiohttp or urllib3 is fine but not PyGithub or similar).

There are also a number of places in the code marked `# BONUS` where additional code would yield a more robust or performant service.  If you 
finish the above quickly, feel free to investigate these added features or anything else you think might make for an interesting demo.  Please 
don't work on the additional optional features before the main task is complete.

## Development
The code will be checked while running in a [Docker](https://www.docker.com/) container but there is no requirement to develop/test inside 
docker.  The simplest way is to use a virtualenv for development:

```bash
    ~/Projects/coding_challenge% virtualenv ./env
    New python executable in /home/dion/Projects/coding_challenge/env/bin/python
    Installing setuptools, pip, wheel...done.
    ~/Projects/coding_challenge% source env/bin/activate
    (env) ~/Projects/coding_challenge% pip install -r requirements.txt
    Collecting Flask==0.10.1 (from -r requirements.txt (line 7))
    ...
    Successfully installed Flask-0.10.1 Jinja2-2.8 MarkupSafe-0.23 Werkzeug-0.11.4 gunicorn-19.4.5 itsdangerous-0.24 requests-2.9.1 six-1.10.0
    (env) ~/Projects/coding_challenge% python -m gistapi.gistapi
     * Running on http://0.0.0.0:8000/ (Press CTRL+C to quit)
     * Restarting with stat
     * Debugger is active!
     * Debugger pin code: 111-111-111
	
    # In another terminal:
    ~/Projects/coding_challenge% curl -H "Content-Type: application/json" \
           -X POST \
           -d '{"username": "justdionysus", "pattern": "LOL[ab]*"}' \
           http://127.0.0.1:8000/api/v1/search
    {
      "matches": [],
      "pattern": "LOL[ab]*",
      "status": "success",
      "username": "justdionysus"
    }

    # When done, Ctrl-C in the server window
    # When done working on the code, deactivate the virtualenv:
    (env) ~/Projects/coding_challenge% deactivate
    ~/Projects/coding_challenge%
```

Testing your code can be done via tox.  No virtualenv is necessary; tox takes care of setting up a test enviornment with Python 2.7 and Python 
3.4.  Running the test is as simple as:

```bash
    ~/Projects/coding_challenge% tox
    GLOB sdist-make: /home/dion/Projects/coding_challenge/setup.py
    py27 inst-nodeps: /home/dion/Projects/coding_challenge/.tox/dist/gistapi-0.1.0.zip    
    ...
    _______________________________________________________________________ summary ________________________________________________________________________
      py27: commands succeeded
      py34: commands succeeded
      congratulations :)
    ~/Projects/coding_challenge%
```
