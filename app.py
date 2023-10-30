import os
from flask import Flask, make_response, request, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app=app,
     origins=['http://localhost:8065/'],
     supports_credentials=True)   # , resources={r"/*": {"origins": "http://localhost:3000"}})
# CORS(app)


# Session config
# app.secret_key = os.getenv("APP_SECRET_KEY")  # Set the secret key for session management
# app.config['SESSION_COOKIE_SAMESITE'] = 'None'
# app.config['SESSION_COOKIE_SECURE'] = False

# Set the cookie settings
# app.config['COOKIE_SAMESITE'] = None
# app.config['COOKIE_HTTPONLY'] = False
# app.config['COOKIE_SECURE'] = False

@app.route('/', methods=['GET'])
def ping():
    return 'Hi'

@app.route('/set_cookie', methods=['GET', 'POST'])
def set_cookie():
    cookie_name = "my_cookie"
    cookie_value = "request.json.get('value', 'default_value')"
    
    response = make_response("Cookie set successfully: " + cookie_value)
    response.set_cookie(
        key=cookie_name,
        value=cookie_value,
        max_age=3600,  # Set a maximum age for the cookie in seconds (e.g., 1 hour)
        samesite="None",  # SameSite: None
        httponly=False,    # Http_only: False
        secure=False,      # Cookie_secure: False
    )
    
    # Additional settings to make the cookie accessible
    response.headers['Access-Control-Allow-Origin'] = '*'  # Allow cross-origin access
    
    return response

@app.route('/get_cookie', methods=['GET'])
def get_cookie():
    cookies = dict(request.cookies)
    print('hi', cookies)
    return 'Hi *** ' + str(cookies)

port_no = os.environ.get('PORT', 5005)

print(f"Server running on port {port_no}...")
if __name__ == '__main__':
    app.run(port=int(port_no), debug=True, host="0.0.0.0")

