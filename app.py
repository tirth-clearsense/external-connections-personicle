from flask import Flask

app = Flask(__name__)
# app.run()

@app.route('/testing')
def hello():
    return "Hello World!"

# handle fitbit oauth
@app.route('/fitbitConnection', methods=['GET', 'POST'])
def fitbit_data_connection():
    
    return True