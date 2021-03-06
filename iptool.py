import json
import urllib.request
from os import environ
from flask import Flask, Response, render_template, request

app = Flask(__name__)

LOCAL = ["127.0.0.1","localhost"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lookup/')
def lookup():
    # Get target from querystring.
    target = request.args.get("target")
    if not target:
        # Use request ip if target arg not set.
        target = "google.com"
        if len(request.access_route) > 0 and request.access_route[0] not in LOCAL:
            target = request.access_route[0]
    # Remove scheme/path from target if exists
    if "//" in target:
        target = target.split("//")[1]
        if "/" in target:
            target = target.split("/")[0]
    
    # Make request to ip-api.com json api.
    try:
        requestURL = "http://ip-api.com/json/{}".format(target)
        rsp = urllib.request.urlopen(requestURL)
        data = rsp.read().decode(rsp.info().get_param('charset') or 'utf-8')
        return Response(data, mimetype='application/json')
    except Exception as err:
        # Return error in json response.
        return Response(json.dumps({"message": str(err), "status": "fail"}), mimetype='application/json')


if __name__ == '__main__':
    DEBUG = True
    HOST = "0.0.0.0"
    PORT = 5555

    app.run(HOST, PORT, debug=DEBUG)