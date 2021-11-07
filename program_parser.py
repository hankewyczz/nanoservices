import json
import os
import re
import shutil
from pathlib import Path
import parse as parser
from typing import Dict, List, Tuple, Set

DOCKERFILE = """
# Base Image 
FROM python:3.8
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["main.py"]
"""

BUILTIN_PY_MODULES = {'BaseHTTPServer', 'ast', 'idna', 'secretstorage', 'Bastion', 'asynchat', 'ihooks', 'select', 'CDROM', 'asyncore', 'imaplib', 'sets', 'CGIHTTPServer', 'atexit', 'imghdr', 'setuptools', 'Canvas', 'audiodev', 'imp', 'sgmllib', 'ConfigParser', 'audioop', 'importlib', 'sha', 'Cookie', 'base64', 'imputil', 'shelve', 'Crypto', 'bdb', 'inspect', 'shlex', 'DLFCN', 'binascii', 'io', 'shutil', 'Dialog', 'binhex', 'ipaddress', 'signal', 'DocXMLRPCServer', 'bisect', 'itertools', 'signatures', 'FileDialog', 'bsddb', 'json', 'site', 'FixTk', 'bz2', 'keyring', 'sitecustomize', 'HTMLParser', 'cPickle', 'keyrings', 'six', 'IN', 'cProfile', 'keyword', 'smtpd', 'MimeWriter', 'cStringIO', 'lib2to3', 'smtplib', 'Queue', 'cachecontrol', 'linecache', 'sndhdr', 'ScrolledText', 'caches', 'linuxaudiodev', 'socket', 'SimpleDialog', 'calendar', 'locale', 'spwd', 'SimpleHTTPServer', 'certifi', 'logging', 'sqlite3', 'SimpleXMLRPCServer', 'cgi', 'lsb_release', 'sre', 'SocketServer', 'cgitb', 'macpath', 'sre_compile', 'StringIO', 'chardet', 'macurl2path', 'sre_constants', 'TYPES', 'chunk', 'mailbox', 'sre_parse', 'Tix', 'cli', 'mailcap', 'ssl', 'Tkconstants', 'cmath', 'markupbase', 'stat', 'Tkdnd', 'cmd', 'marshal', 'statvfs', 'Tkinter', 'code', 'math', 'string', 'UserDict', 'codecs', 'md5', 'stringold', 'UserList', 'codeop', 'mercurial', 'stringprep', 'UserString', 'collections', 'mhlib', 'strop', '_LWPCookieJar', 'colorsys', 'mimetools', 'struct', '_MozillaCookieJar', 'command', 'mimetypes', 'subprocess', '__builtin__', 'commands', 'mimify', 'sunau', '__future__', 'compileall', 'mmap', 'sunaudio', '_abcoll', 'compiler', 'modulefinder', 'symbol', '_ast', 'contextlib', 'multifile', 'symtable', '_backport', 'contrib', 'multiprocessing', 'sys', '_bisect', 'cookielib', 'mutex', 'sysconfig', '_bsddb', 'copy', 'netifaces', 'syslog', '_cffi_backend', 'copy_reg', 'netrc', 'tabnanny', '_codecs', 'crypt', 'new', 'tarfile', '_codecs_cn', 'cryptography', 'nis', 'telnetlib', '_codecs_hk', 'csv', 'nmap', 'tempfile', '_codecs_iso2022', 'ctypes', 'nntplib', 'termios', '_codecs_jp', 'curses', 'ntpath', 'test', '_codecs_kr', 'datetime', 'nturl2path', 'textwrap', '_codecs_tw', 'dbhash', 'numbers', 'this', '_collections', 'dbm', 'opcode', 'thread', '_csv', 'dbus', 'operator', 'threading', '_ctypes', 'decimal', 'optparse', 'time', '_ctypes_test', 'difflib', 'os', 'timeit', '_curses', 'dircache', 'os2emxpath', 'tkColorChooser', '_curses_panel', 'dis', 'ossaudiodev', 'tkCommonDialog', '_dbus_bindings', 'distlib', 'packages', 'tkFileDialog', '_dbus_glib_bindings', 'distutils', 'packaging', 'tkFont', '_elementtree', 'doctest', 'parser', 'tkMessageBox', '_functools', 'dumbdbm', 'pdb', 'tkSimpleDialog', '_hashlib', 'dummy_thread', 'pickle', 'toaiff', '_heapq', 'dummy_threading', 'pickletools', 'token', '_hotshot', 'easy_install', 'pip', 'tokenize', '_io', 'email', 'pipes', 'tool', '_json', 'encodings', 'pkg_resources', 'trace', '_locale', 'ensurepip', 'pkgutil', 'traceback', '_lsprof', 'enum', 'platform', 'ttk', '_md5', 'errno', 'plistlib', 'tty', '_multibytecodec', 'exceptions', 'popen2', 'turtle', '_multiprocessing', 'extern', 'poplib', 'types', '_osx_support', 'fcntl', 'posix', 'unicodedata', '_pyio', 'filecmp', 'posixfile', 'unittest', '_random', 'fileinput', 'posixpath', 'urllib', '_sha', 'fnmatch', 'pprint', 'urllib2', '_sha256', 'formatter', 'profile', 'urllib3', '_sha512', 'fpformat', 'progress', 'urlparse', '_socket', 'fractions', 'pstats', 'user', '_sqlite3', 'ftplib', 'pty', 'util', '_sre', 'functools', 'pwd', 'uu', '_ssl', 'future_builtins', 'py_compile', 'uuid', '_strptime', 'gc', 'pyclbr', 'warnings', '_struct', 'genericpath', 'pydoc', 'wave', '_symtable', 'getopt', 'pydoc_data', 'weakref', '_sysconfigdata', 'getpass', 'pyexpat', 'webbrowser', '_sysconfigdata_nd', 'gettext', 'pygtkcompat', 'wheel', '_testcapi', 'gi', 'quopri', 'whichdb', '_threading_local', 'glob', 'random', 'wsgiref', '_vendor', 'grp', 're', 'xdg', '_warnings', 'gzip', 'readline', 'xdrlib', '_weakref', 'hashlib', 'repr', 'xml', '_weakrefset', 'heapq', 'requests', 'xmllib', 'abc', 'hgdemandimport', 'resource', 'xmlrpclib', 'aifc', 'hgext', 'rexec', 'xxsubtype', 'antigravity', 'hgext3rd', 'rfc822', 'zipfile', 'anydbm', 'hmac', 'rlcompleter', 'zipimport', 'appdirs', 'hotshot', 'robotparser', 'zlib', 'argparse', 'htmlentitydefs', 'runpy', 'array', 'htmllib', 'scapy', 'asn1crypto', 'httplib', 'sched'}

# Modules to install for all
DEFAULT_MODULES = {'flask', 'requests'}

def match_function_imports(functions, imports) -> None:
    """
    Takes functions and import objects, and matches each function with import dependencies
    :return: Nothing
    """
    for func, values in functions.items():
        # Create a set representing what modules this needs to import from pip
        values["pip"] = set()

        for import_name, import_values in imports.items():
            if import_name in values["code"]:
                # This function needs this import - add it
                values["code"] = f"    {import_values['import']}\n" + values["code"]
                values["pip"].add(import_values["module"])


# Convert the function calls to GET requests
def convert_to_GET(functions):
    for func, values in functions.items():
        # Check if any of these are dependencies
        for func2 in functions.keys():
            pattern = func2 + "\((.*)\)"
            for match in re.finditer(pattern, values["code"]):
                function_call = match.group(0)

                function_args = match.group(1)
                function_args = function_args.split(',') if function_args else []
                function_args = "}, {".join([s.strip() for s in function_args])
                function_args = f'?args=[{{{function_args}}}]'

                # Replace it with a get request
                get_request = f"requests.get(f'''http://{func2}:5000{function_args}''').json()"
                values["code"] = values["code"].replace(function_call.rstrip(), get_request)



def convert_to_server(name, function):
    intro = """import json
from flask import Flask, request, jsonify
import requests
app = Flask(__name__)
@app.route('/', methods=['GET'])
"""

    code = re.sub(f"{name}\(.*\)", f"{name}()", function["code"])

    init_args = []
    for i, arg in enumerate(function["args"]):
        init_args.append(f"    {arg} = json.loads(request.args.get('args'))[{i}]")

    code = '\n'.join(init_args) + '\n' + code

    for returns in re.finditer(r"(?:return )(.*)", code):
        code = code.replace(returns.group(0), f"return jsonify({returns.group(1)})")

    code += "\n\napp.run(host='0.0.0.0')\n"
    return intro + f"def {name}():\n" + code

def save_to_files(functions, path):
    docker_compose = """
version: "3"
services:
"""

    for name, values in functions.items():
        dirpath = path / name
        os.mkdir(dirpath)
        # Write the file
        with open(dirpath / "main.py", 'w', encoding='utf8') as f:
            f.write(convert_to_server(name, values))
        # Write the requirements
        with open(dirpath / "requirements.txt", 'w', encoding='utf8') as f:
            imports = values["pip"].difference(BUILTIN_PY_MODULES)
            imports.update(DEFAULT_MODULES)

            f.write('\n'.join(imports))
        # Write the dockerfile
        with open(dirpath / "Dockerfile", 'w', encoding='utf8') as f:
            f.write(DOCKERFILE)

        docker_compose += f"""
    {name}:
        build:
            context: ./{name}"""

        if name == "main":
            docker_compose += f"""
        ports:
            - target: 5000
              published: 8081
              protocol: tcp"""

    with open(path / "docker-compose.yml", 'w', encoding='utf8') as f:
        f.write(docker_compose)



def parse_program(input_program: str):
    functions = parser.parse_functions(input_program)
    imports = parser.parse_imports(input_program)

    match_function_imports(functions, imports)
    convert_to_GET(functions)

    # Delete the build directory
    dirpath = Path('build')
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    # Recreate it
    os.mkdir(dirpath)

    save_to_files(functions, dirpath)


def import_file(filename: str) -> str:
    # Import the file
    with open(filename, 'r', encoding='utf8') as f:
        # Standardize the input
        return parser.standardize_input(f.read())


def main():
    in_str = import_file('examples/test.py')
    parse_program(in_str)


main()
