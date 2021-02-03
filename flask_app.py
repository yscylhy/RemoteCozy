from web_app import app
import sys

if __name__ == '__main__':
    if sys.platform == 'win32':
        app.run()
    else:
        app.run(host='0.0.0.0')
