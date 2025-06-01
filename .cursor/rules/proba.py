import requests



url = "http://127.0.0.1:8000/mcp/"
headers = {
    "Accept": "text/event-stream"
}

with requests.get(url, headers=headers, stream=True) as response:
    print(response.status_code)
    for line in response.iter_lines():
        if line:
            print(line.decode())