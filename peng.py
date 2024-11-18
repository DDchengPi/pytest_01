import requests
import json
import pytest

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, params=params)
        return self._process_response(response)

    def post(self, endpoint, data=None, json=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, data=data, json=json)
        return self._process_response(response)

    def put(self, endpoint, data=None, json=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.put(url, data=data, json=json)
        return self._process_response(response)

    def delete(self, endpoint, data=None, json=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.delete(url, data=data, json=json)
        return self._process_response(response)

    def _process_response(self, response):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
            return None
        return response.json()

def test_api(api_client):
    # 示例测试用例，可以在不同模块中重用
    response = api_client.get("example-endpoint")
    assert response is not None, "GET request failed"
    assert response["status"] == "success", "Expected status to be 'success'"

@pytest.fixture
def api_client():
    return APIClient(base_url="http://example.com")

if __name__ == "__main__":
    pytest.main()
