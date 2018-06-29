# encoding: utf-8
import os
from views import app
from flask_debugtoolbar import DebugToolbarExtension



def main():
    app.debug = True
    #toolbar = DebugToolbarExtension(app)
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()


