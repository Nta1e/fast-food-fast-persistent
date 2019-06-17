#!usr/local/bin/python3

from flask import redirect
from app import app
from schema import main


@app.route("/")
def default():
    return redirect('/apidocs')

if __name__ == '__main__':
    main()
    app.run(debug=True)
