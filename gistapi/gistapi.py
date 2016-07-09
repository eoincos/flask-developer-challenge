# coding=utf-8
"""
Exposes a simple HTTP API to search a users Gists via a regular expression.

Github provides the Gist service as a pastebin analog for sharing code and
other develpment artifacts.  See http://gist.github.com for details.  This
module implements a Flask server exposing two endpoints: a simple ping
endpoint to verify the server is up and responding and a search endpoint
providing a search across all public Gists for a given Github account.
"""

import requests
import json
import jsonschema
import re
import urllib2
from jsonschema import validate
from flask import Flask, jsonify, request


# *The* app object
app = Flask(__name__)


@app.route("/ping")
def ping():
    """Provide a static response to a simple GET request."""
    return "pong"


def gists_for_user(username):
    """Provides the list of gist metadata for a given user.

    This abstracts the /users/:username/gist endpoint from the Github API.
    See https://developer.github.com/v3/gists/#list-a-users-gists for
    more information.

    Args:
        username (string): the user to query gists for

    Returns:
        The dict parsed from the json response from the Github API.  See
        the above URL for details of the expected structure.
    """
    gists_url = 'https://api.github.com/users/{username}/gists'.format(
            username=username)
    
    response = None
    
    try:
        response = requests.get(gists_url)
    except requests.exceptions.RequestException as e:
        pass
    # BONUS: What failures could happen?
    # RequestException will handle these issue
    # we could also handle other exceptions such as Timeout to retry the request
    # BONUS: Paging? How does this work for users with tons of gists?
    # tons of gists will nmean the truncated attribute will be set to True

    return response.json()


@app.route("/api/v1/search", methods=['POST'])
def search():
    """Provides matches for a single pattern across a single users gists.

    Pulls down a list of all gists for a given user and then searches
    each gist for a given regular expression.

    Returns:
        A Flask Response object of type application/json.  The result
        object contains the list of matches along with a 'status' key
        indicating any failure conditions.
    """
    requestSchema = {
        "type" : "object",
        "properties" : {
            "username" : {"type" : "string"},
            "pattern" : {"type" : "string"},
         }
    }
    
    status = 'success'
    
    matches = []
    warnings = []
    
    post_data = request.get_json()
    # BONUS: Validate the arguments?
    # using jsonschema to validate the json is correct
    # in this case make the status code fail
    
    try:
        validate(post_data, requestSchema)
    except jsonschema.exceptions.ValidationError as e:
        status = 'fail_requestJSON'
    
    if status == 'success':
        username = post_data['username']
        pattern = post_data['pattern']
        regex_pattern = re.compile(pattern)
    
        result = {}
        gists = gists_for_user(username)
        # BONUS: Handle invalid users?
        # invalid users will lead to invalid requests    
        # in this case make the status code fail
        
        if gists is None:
            status = 'fail_requestGIST'
        
        if status == 'success':
            for gist in gists:
                # REQUIRED: Fetch each gist and check for the pattern
                # opens up each file in a gist and checks the pattern against the content
                # BONUS: What about huge gists?
                # truncated attribute will be true
                # in this case we can return warnings
                # this tells the user we can't go through all the files
                # BONUS: Can we cache results in a datastore/db?
                
                #print json.dumps(gist, indent=4, sort_keys=True)
                
                if gist['truncated'] == True:
                    warnings.append('more than 300 files in gist ' + gist['id'])
            
                matchFound = False
                
                for currentFile in gist['files']:
                    for line in urllib2.urlopen(gist['files'][currentFile]['raw_url']):
                        if re.search(regex_pattern, line) is not None:
                            matchFound = True
                
                if matchFound:
                    matches.append('https://gist.github.com/' + username + "/" + gist['id'])
    
    if status == 'success':
        result['status'] = status
        result['username'] = username
        result['pattern'] = pattern
        result['matches'] = matches
        if len(warnings) > 0:
            result['warnings'] = warnings
    else:
        result['status'] = status

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
