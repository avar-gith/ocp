import requests

def get_streamed_messages():
    # API hívás egy külső szolgáltatásra
    url = "https://external-api.com/stream"

    with requests.get(url, stream=True) as response:
        for line in response.iter_lines():
            if line:
                yield line.decode('utf-8')
