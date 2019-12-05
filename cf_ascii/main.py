import os
import subprocess
import logging

from flask import make_response


def main(request):
    text = request.args.get('text', '')
    if not text:
        return 'missing text parameter', 404
    logging.info(f'received url: {text}')

    cmd = f"./figlet -d fonts {text}".split(' ')
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()
    error = stderr.decode('utf8')
    if error:
        return error, 403
    out = stdout.decode('utf8')
    response = make_response(out)
    response.headers["content-type"] = "text/plain"
    return response
