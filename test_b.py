好的，下面是使用 `pytest` 重写的通用 API 接口测试代码。`pytest` 是一个非常流行且功能强大的 Python 测试框架，能够让你更方便地编写和运行测试。

### 1. 安装依赖

首先，确保安装了 `pytest` 和 `requests`：

```bash
pip install pytest requests
```

### 2. 使用 `pytest` 的通用 API 接口测试代码

```python
import pytest
import requests
import json

# 配置基础 URL 和请求头
BASE_URL = "https://api.example.com"  # 替换为你的基础URL
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer <your-token>",  # 可选，根据接口需求
}

def send_request(method, endpoint, params=None, data=None, headers=None):
    """
    发送 API 请求的通用方法
    :param method: 请求方法 (GET, POST, PUT, DELETE)
    :param endpoint: API 接口的具体路径
    :param params: URL 参数 (GET 请求常用)
    :param data: 请求体数据 (POST、PUT 请求常用)
    :param headers: 请求头
    :return: 请求响应对象
    """
    url = f"{BASE_URL}{endpoint}"
    
    if headers:
        HEADERS.update(headers)

    if method.upper() == 'GET':
        response = requests.get(url, params=params, headers=HEADERS)
    elif method.upper() == 'POST':
        response = requests.post(url, json=data, headers=HEADERS)
    elif method.upper() == 'PUT':
        response = requests.put(url, json=data, headers=HEADERS)
    elif method.upper() == 'DELETE':
        response = requests.delete(url, params=params, headers=HEADERS)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")
    
    return response

def assert_response(response, expected_status_code, expected_json=None):
    """
    通用的响应验证方法
    :param response: 请求返回的响应
    :param expected_status_code: 预期的 HTTP 状态码
    :param expected_json: 预期返回的 JSON 数据结构 (可选)
    """
    assert response.status_code == expected_status_code, \
        f"Expected status code {expected_status_code}, but got {response.status_code}"
    
    if expected_json is not None:
        try:
            response_json = response.json()  # 解析 JSON 响应
            assert response_json == expected_json, \
                f"Expected JSON response {expected_json}, but got {response_json}"
        except ValueError:
            pytest.fail(f"Response is not a valid JSON: {response.text}")

# 示例 GET 请求的测试
@pytest.mark.parametrize("endpoint,params,expected_status_code,expected_json", [
    ("/example/get_endpoint", {"key": "value"}, 200, {"key": "value"}),
])
def test_get_endpoint(endpoint, params, expected_status_code, expected_json):
    response = send_request("GET", endpoint, params=params)
    assert_response(response, expected_status_code, expected_json)

# 示例 POST 请求的测试
@pytest.mark.parametrize("endpoint,data,expected_status_code,expected_json", [
    ("/example/post_endpoint", {"name": "test", "age": 25}, 201, {"status": "success", "data": {"name": "test", "age": 25}}),
])
def test_post_endpoint(endpoint, data, expected_status_code, expected_json):
    response = send_request("POST", endpoint, data=data)
    assert_response(response, expected_status_code, expected_json)

# 示例 PUT 请求的测试
@pytest.mark.parametrize("endpoint,data,expected_status_code,expected_json", [
    ("/example/put_endpoint/1", {"name": "updated name"}, 200, {"status": "success", "data": {"name": "updated name"}}),
])
def test_put_endpoint(endpoint, data, expected_status_code, expected_json):
    response = send_request("PUT", endpoint, data=data)
    assert_response(response, expected_status_code, expected_json)

# 示例 DELETE 请求的测试
@pytest.mark.parametrize("endpoint,expected_status_code", [
    ("/example/delete_endpoint/1", 204),  # 假设删除成功返回 204 No Content
])
def test_delete_endpoint(endpoint, expected_status_code):
    response = send_request("DELETE", endpoint)
    assert_response(response, expected_status_code)

```

### 3. 代码解释

- **`send_request`**：这是一个通用的请求方法，和之前的实现类似，支持 GET、POST、PUT、DELETE 四种 HTTP 方法。
  
- **`assert_response`**：通用的响应验证方法，用于检查响应的状态码和 JSON 内容。

- **`pytest.mark.parametrize`**：这是 `pytest` 的参数化功能，它允许我们在一个测试函数中运行多个测试用例。通过传递不同的参数组合，可以减少重复代码。
  
- **测试函数**：如 `test_get_endpoint`、`test_post_endpoint` 等，分别对应 GET、POST、PUT 和 DELETE 请求的测试。每个测试都使用 `pytest.mark.parametrize` 来定义不同的输入数据和期望结果。

### 4. 运行测试

1. 将代码保存为 `test_api.py`。
2. 在终端中运行以下命令来执行测试：

```bash
pytest test_api.py
```

`pytest` 会自动发现所有以 `test_` 开头的函数，并运行它们。测试的结果会以彩色的方式输出。

### 5. 可扩展性

- **增加更多的测试用例**：你可以根据需要添加更多的 API 接口测试，只需要在现有框架中添加新的 `@pytest.mark.parametrize` 装饰器和测试函数即可。
- **Mock 测试**：你可以结合 `unittest.mock` 或 `pytest-mock` 来模拟外部 API 的调用，进行单元测试而不需要实际请求。
- **自动化集成**：你可以将这个测试框架集成到 CI/CD 管道中，每次代码变更时自动运行 API 测试。

### 6. 其他功能

- **失败时截图/日志**：如果测试失败，你可以在测试中捕获日志或响应截图，特别是对于 UI 自动化测试。
  
- **并行化测试**：`pytest` 通过插件如 `pytest-xdist` 支持并行化执行测试，提高测试效率。

通过这种方式，你可以创建一个易于维护和扩展的 API 测试框架，适用于多个模块和接口。
