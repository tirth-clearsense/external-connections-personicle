from application import create_app
import os

app = create_app()
if __name__ == "__main__":
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run("localhost", ssl_context="adhoc", port=5000, debug=True)
    