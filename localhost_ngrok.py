from flask import Flask, request, Response
from flask_cors import CORS
from pyngrok import ngrok
import requests, os

app = Flask(__name__)
CORS(app)
port_no = 5005

ngrok_auth_token = '2XrQnhGcfOBYHoiyaXKfDN6LqHj_7Wf1N35BvnMBaxi4Syjcy'
ngrok.set_auth_token( ngrok_auth_token )
public_url =  ngrok.connect(port_no).public_url

# Define the base URL of the target API
target_api_base_url = 'http://localhost:8065/api/v4'  # Replace with your target API's base URL

@app.route('/', methods=['GET'])
def root():
    return 'Hi'

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_request(path):
    # Build the target API URL by appending the path to the base URL
    target_url = f'{target_api_base_url}/{path}'

    # Forward the incoming request to the target API
    headers = dict(request.headers)
    headers.pop('Host', None)  # Remove the Host header to avoid conflicts
    response = requests.request(
        method=request.method,
        url=target_url,
        data=request.data,
        headers=headers,
        params=request.args,
    )

    # Relay the target API's response to the client
    return Response(response.content, response.status_code, content_type=response.headers['content-type'])

print(f"Public url for the API... {public_url}")

# if __name__ == '__main__':
app.run(
    port=port_no
)