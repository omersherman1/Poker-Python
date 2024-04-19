import subprocess
from bottle import run, post, request, response, get, route

@route('/return',method = 'POST')
def process(path):
    print ({'4': 5, '6': 7})

run(host='localhost', port=8000, debug=True)