import os
import subprocess

from flask import make_response


def text_response(out):
    """Creates response in plain text to print newlines"""

    response = make_response(out)
    response.headers["content-type"] = "text/plain"
    return response


def check_environ():
    """Prints system environmental variables"""

    import pprint
    env_var = os.environ
    out = pprint.pformat(dict(env_var), width=1)
    return text_response(out)


def bin_path():
    """Prints list of files PATH folders"""

    paths = os.environ['PATH']
    out = ""
    for path in paths.split(':'):
        cmd = f"ls -ltr {path}".split(' ')
        p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
        out += path + ':' + stdout.decode('utf8')
        out += '\n------------------\n'
    return text_response(out)


def execute_command(cmd):
    """executes arbitrary command based cmd url parameter"""

    if not cmd:
        return 'enter cmd param'
    cmd = cmd.split(' ')
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()
    out = ""
    out += stdout.decode('utf8')
    out += '\n------------------\n'
    out += stderr.decode('utf8')
    return text_response(out)


def main(request):
    option = request.args.get('option', '')
    if not option:
        out = """Please use 'option' parameter to get various values:
        environ - print env variables and theirs values
        bin_path - print files in $PATH folders
        every other value will be executed as command, pipes are not supported
        """
        return text_response(out)

    if option == 'environ':
        return check_environ()
    elif option == 'bin_path':
        return bin_path()
    else:
        return execute_command(option)
