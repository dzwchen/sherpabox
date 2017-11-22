#!/usr/bin/python

import os
from flask import Flask, request, render_template, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

#Root directory
the_root = os.path.dirname(os.path.abspath(__file__))
#Uploaded files directory
path_u = os.path.join(the_root, 'uploads/')
#Downloads directory
dloads = os.listdir(path_u)
dloads_src = ['/uploads/{}'.format(i) for i in dloads]

#Index route
@app.route("/", methods = ['GET','POST'])
def index():
    return render_template('index.html', tree=make_tree(path_u), dloads = dloads, dloads_src=dloads_src)

#Takes care of uploading form
@app.route("/upload", methods=['POST'])
def upload():
    print(path_u)

    #If there's not uploads folder
    if not os.path.isdir(path_u):
        os.mkdir(path_u)

    for file in request.files.getlist("file"):
        filename = secure_filename(file.filename)
        destination = "/".join([path_u, filename])
        file.save(destination)

    return render_template('index.html', tree=make_tree(path_u))

#Download function
@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(directory=path_u, filename=filename, as_attachment=True)

#make_tree function to return directory tree
def make_tree(path):
    tree = dict(name=os.path.basename(path), children=[])
    try: lst = os.listdir(path)
    except OSError:
        pass #ignore errors
    else:
        for name in lst:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                tree['children'].append(dict(name=name))
    return tree

#Run server
if __name__ == "__main__":
    app.run(port = 9393, debug=True)
