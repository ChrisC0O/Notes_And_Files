from flask import Flask, request, Response
import requests

"""
Flask Universal Proxy Script (flask_proxy.py)

Description:
This Flask application acts as a universal proxy, forwarding any incoming HTTP request 
(GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD) to a specified server defined in the 
FORWARD_ADDRESS variable. It handles various data types (HTML, JSON, images, files, etc.) 
by passing the request headers, query parameters, and body to the target server and 
returning the response to the client with the appropriate status code and headers.

Usage:
1. Set the FORWARD_ADDRESS variable to the target server's base URL (e.g., 'http://example.com').
2. Run the script using Python: `python flask_proxy.py`.
3. The app listens on the default Flask port (5000) unless otherwise configured.
4. Send HTTP requests to the Flask app, and they will be forwarded to the specified server.
5. Ensure the target server is accessible and properly configured.

Notes:
- The script excludes hop-by-hop headers (e.g., 'content-length', 'connection') to ensure compatibility.
- Error handling returns a 500 status code with the error message if the forwarded request fails.
- Set `debug=False` in the `app.run()` call for production use.
"""

# The address to forward requests to (e.g., 'http://example.com' or 'http://192.168.1.100:8080')
FORWARD_ADDRESS = 'http://100.95.131.221:5000/'  # Replace with the actual forward address

app = Flask(__name__)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD'])
def proxy(path):
    # Construct the full URL to forward to
    forward_url = f"{FORWARD_ADDRESS}/{path}"

    # Get query parameters
    query_params = request.args

    # Get headers, excluding 'Host' to avoid issues
    headers = {key: value for key, value in request.headers if key.lower() != 'host'}

    # Get body data
    data = request.get_data()

    # Forward the request
    try:
        resp = requests.request(
            method=request.method,
            url=forward_url,
            headers=headers,
            params=query_params,
            data=data,
            allow_redirects=False,  # Handle redirects manually if needed, but disable for proxy purity
            stream=False  # Load response in memory for simplicity
        )

        # Prepare the response headers, excluding hop-by-hop headers
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        response_headers = [(name, value) for name, value in resp.raw.headers.items() if
                            name.lower() not in excluded_headers]

        # Return the response
        return Response(resp.content, resp.status_code, response_headers)

    except requests.exceptions.RequestException as e:
        # Handle errors robustly
        return str(e), 500


if __name__ == '__main__':
    app.run(debug=True)  # Set debug=False in production
