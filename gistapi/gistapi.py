import requests
from flask import Flask, jsonify, request
app = Flask(__name__)


@app.route("/ping")
def ping():
    return "pong"


def gists_for_user(username):
    gists_url = 'https://api.github.com/users/{username}/gist'.format(
            username=username)
    response = requests.get(gists_url)
    # TODO: What failures could happen?
    # TODO: Paging? How does this work for users with tons of gists?
    return response.json()


@app.route("/api/v1/search", methods=['POST'])
def search():
    post_data = request.get_json()

    # TODO: Validate the arguments?
    username = post_data['username']
    pattern = post_data['pattern']

    result = {}
    gists = gists_for_user(username)
    # TODO: Handle invalid users?

    for gist in gists:
        # TODO: Fetch each gist and check for the pattern
        # TODO: What about huge gists?
        # TODO: Can we cache results in a datastore/db?
        pass

    result['status'] = 'success'
    result['username'] = username
    result['pattern'] = pattern
    result['matches'] = []

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
