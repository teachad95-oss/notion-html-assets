# Python `requests` Module – Full Tutorial

> The `requests` module is the most popular HTTP library for Python. It makes sending HTTP requests simple and human-friendly. Unlike the built-in `urllib`, it handles encoding, headers, sessions, and more with minimal code.

---

## 1. Installation

```bash
pip install requests
```

```python
import requests
```

---

## 2. HTTP Methods Overview

| Method    | Purpose                        | Function               |
|-----------|--------------------------------|------------------------|
| GET       | Retrieve data                  | `requests.get()`       |
| POST      | Send / create data             | `requests.post()`      |
| PUT       | Replace / update data          | `requests.put()`       |
| PATCH     | Partially update data          | `requests.patch()`     |
| DELETE    | Delete data                    | `requests.delete()`    |
| HEAD      | Get headers only (no body)     | `requests.head()`      |
| OPTIONS   | Get supported methods          | `requests.options()`   |

---

## 3. GET Request

```python
import requests

response = requests.get('https://jsonplaceholder.typicode.com/posts/1')

print(response.status_code)   # 200
print(response.url)           # https://jsonplaceholder.typicode.com/posts/1
print(response.text)          # Response body as string
print(response.json())        # Parsed JSON as dict
print(response.content)       # Raw bytes
print(response.encoding)      # 'utf-8'
print(response.headers)       # Response headers dict
```

### With Query Parameters

```python
params = {
    'userId': 1,
    'completed': 'false'
}

response = requests.get(
    'https://jsonplaceholder.typicode.com/todos',
    params=params
)

print(response.url)
# https://jsonplaceholder.typicode.com/todos?userId=1&completed=false

data = response.json()
print(len(data))  # number of results
```

---

## 4. POST Request

```python
# Send JSON body
payload = {
    'title': 'My Post',
    'body': 'This is the body',
    'userId': 1
}

response = requests.post(
    'https://jsonplaceholder.typicode.com/posts',
    json=payload  # automatically sets Content-Type: application/json
)

print(response.status_code)  # 201 Created
print(response.json())       # {'id': 101, 'title': 'My Post', ...}
```

### Send Form Data

```python
form_data = {
    'username': 'alice',
    'password': 'secret123'
}

response = requests.post(
    'https://httpbin.org/post',
    data=form_data  # sends as application/x-www-form-urlencoded
)
```

---

## 5. PUT & PATCH Requests

```python
# PUT — replace entire resource
response = requests.put(
    'https://jsonplaceholder.typicode.com/posts/1',
    json={'title': 'Updated Title', 'body': 'New body', 'userId': 1}
)
print(response.json())

# PATCH — partial update
response = requests.patch(
    'https://jsonplaceholder.typicode.com/posts/1',
    json={'title': 'Just the title changed'}
)
print(response.json())
```

---

## 6. DELETE Request

```python
response = requests.delete('https://jsonplaceholder.typicode.com/posts/1')

print(response.status_code)  # 200
print(response.json())       # {}
```

---

## 7. Response Object

```python
response = requests.get('https://httpbin.org/get')

# Status
response.status_code       # 200
response.ok                # True if status < 400
response.reason            # 'OK'

# Content
response.text              # Body as string
response.content           # Body as bytes
response.json()            # Body parsed as JSON (raises if not JSON)

# Headers & metadata
response.headers           # CaseInsensitiveDict of response headers
response.headers['Content-Type']
response.url               # Final URL (after redirects)
response.encoding          # Detected encoding
response.elapsed           # timedelta of request duration

# Request info
response.request           # PreparedRequest object
response.request.headers   # Headers sent in the request
response.history           # List of redirects
```

---

## 8. Status Codes & Error Handling

```python
import requests

response = requests.get('https://jsonplaceholder.typicode.com/posts/1')

# Check manually
if response.status_code == 200:
    print("Success")
elif response.status_code == 404:
    print("Not found")

# Use .ok shorthand (True if < 400)
if response.ok:
    print(response.json())

# Raise exception for 4xx/5xx
response.raise_for_status()  # raises requests.HTTPError if bad status

# Full error handling pattern
try:
    response = requests.get('https://httpbin.org/status/404')
    response.raise_for_status()
except requests.HTTPError as e:
    print(f"HTTP error: {e}")
except requests.ConnectionError:
    print("Failed to connect")
except requests.Timeout:
    print("Request timed out")
except requests.RequestException as e:
    print(f"Request failed: {e}")
```

---

## 9. Custom Headers

```python
headers = {
    'Authorization': 'Bearer your_token_here',
    'Accept': 'application/json',
    'User-Agent': 'MyApp/1.0',
    'X-Custom-Header': 'value'
}

response = requests.get(
    'https://httpbin.org/headers',
    headers=headers
)

print(response.json())
```

---

## 10. Authentication

### Basic Auth

```python
from requests.auth import HTTPBasicAuth

response = requests.get(
    'https://httpbin.org/basic-auth/user/pass',
    auth=HTTPBasicAuth('user', 'pass')
)

# Shorthand tuple
response = requests.get(
    'https://httpbin.org/basic-auth/user/pass',
    auth=('user', 'pass')
)

print(response.status_code)  # 200
```

### Digest Auth

```python
from requests.auth import HTTPDigestAuth

response = requests.get(
    'https://httpbin.org/digest-auth/auth/user/pass',
    auth=HTTPDigestAuth('user', 'pass')
)
```

### Token / Bearer Auth

```python
token = "your_api_token"

response = requests.get(
    'https://api.example.com/data',
    headers={'Authorization': f'Bearer {token}'}
)
```

### API Key in Params or Header

```python
# As query parameter
requests.get('https://api.example.com/data', params={'api_key': 'your_key'})

# As header
requests.get('https://api.example.com/data', headers={'X-API-Key': 'your_key'})
```

---

## 11. Timeouts

Always set timeouts in production to avoid hanging requests.

```python
# Single timeout (connect + read)
response = requests.get('https://httpbin.org/delay/1', timeout=5)

# Separate connect and read timeouts
response = requests.get(
    'https://httpbin.org/delay/1',
    timeout=(3, 10)  # (connect_timeout, read_timeout) in seconds
)

try:
    response = requests.get('https://httpbin.org/delay/5', timeout=2)
except requests.Timeout:
    print("Request timed out!")
```

---

## 12. Sessions

A `Session` persists settings like headers, cookies, and auth across multiple requests. It also reuses the TCP connection (faster).

```python
import requests

with requests.Session() as session:
    # Set headers for all requests in this session
    session.headers.update({'Authorization': 'Bearer my_token'})

    # Make multiple requests
    r1 = session.get('https://httpbin.org/get')
    r2 = session.post('https://httpbin.org/post', json={'key': 'value'})

    print(r1.status_code)
    print(r2.status_code)
```

### Session with Base URL Pattern

```python
class APIClient:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Bearer {token}'})

    def get(self, endpoint, **kwargs):
        return self.session.get(f'{self.base_url}{endpoint}', **kwargs)

    def post(self, endpoint, **kwargs):
        return self.session.post(f'{self.base_url}{endpoint}', **kwargs)

client = APIClient('https://api.example.com', 'my_token')
response = client.get('/users')
```

---

## 13. Cookies

```python
# Send cookies in a request
cookies = {'session_id': 'abc123', 'theme': 'dark'}
response = requests.get('https://httpbin.org/cookies', cookies=cookies)
print(response.json())

# Read cookies from a response
response = requests.get('https://httpbin.org/cookies/set?name=alice')
print(response.cookies['name'])  # alice

# Persist cookies across requests using a session
with requests.Session() as session:
    session.get('https://httpbin.org/cookies/set?token=xyz')
    response = session.get('https://httpbin.org/cookies')
    print(response.json())  # {'cookies': {'token': 'xyz'}}
```

---

## 14. File Uploads

```python
# Upload a single file
with open('report.pdf', 'rb') as f:
    response = requests.post(
        'https://httpbin.org/post',
        files={'file': f}
    )

# Upload with custom filename and content type
with open('photo.jpg', 'rb') as f:
    response = requests.post(
        'https://httpbin.org/post',
        files={'image': ('avatar.jpg', f, 'image/jpeg')}
    )

# Upload multiple files
files = {
    'file1': open('a.txt', 'rb'),
    'file2': open('b.txt', 'rb'),
}
response = requests.post('https://httpbin.org/post', files=files)

# Upload file alongside form fields
with open('doc.pdf', 'rb') as f:
    response = requests.post(
        'https://httpbin.org/post',
        data={'title': 'My Document'},
        files={'file': f}
    )
```

---

## 15. Downloading Files

```python
import requests

url = 'https://example.com/largefile.zip'

# Small file — load all at once
response = requests.get(url)
with open('file.zip', 'wb') as f:
    f.write(response.content)

# Large file — stream in chunks to save memory
response = requests.get(url, stream=True)
with open('file.zip', 'wb') as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)

# With progress tracking
response = requests.get(url, stream=True)
total = int(response.headers.get('content-length', 0))
downloaded = 0

with open('file.zip', 'wb') as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)
        downloaded += len(chunk)
        print(f"Downloaded {downloaded}/{total} bytes", end='\r')
```

---

## 16. SSL & Certificates

```python
# Verify SSL (default: True — always keep True in production)
response = requests.get('https://example.com', verify=True)

# Disable SSL verification (NOT recommended in production)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
response = requests.get('https://self-signed.example.com', verify=False)

# Use a custom CA bundle
response = requests.get('https://example.com', verify='/path/to/ca-bundle.crt')

# Provide client certificate (mutual TLS)
response = requests.get(
    'https://example.com',
    cert=('/path/to/client.crt', '/path/to/client.key')
)
```

---

## 17. Proxies

```python
proxies = {
    'http': 'http://10.10.1.10:3128',
    'https': 'http://10.10.1.10:1080',
}

response = requests.get('https://httpbin.org/ip', proxies=proxies)
print(response.json())

# With authentication
proxies = {
    'http': 'http://user:password@proxy.example.com:8080'
}
```

---

## 18. Redirects

```python
# Redirects followed automatically by default
response = requests.get('http://github.com')  # redirects to https
print(response.url)          # https://github.com/
print(response.history)      # [<Response [301]>]

# Disable automatic redirects
response = requests.get('http://github.com', allow_redirects=False)
print(response.status_code)  # 301
print(response.headers['Location'])
```

---

## 19. Sending JSON, Form Data & Raw Body

```python
import requests

# JSON (sets Content-Type: application/json automatically)
requests.post(url, json={'key': 'value'})

# Form data (sets Content-Type: application/x-www-form-urlencoded)
requests.post(url, data={'key': 'value'})

# Raw string / bytes body
requests.post(url, data='raw text body')
requests.post(url, data=b'\x00\x01\x02')

# Multipart form data (with files)
requests.post(url, files={'file': open('f.txt', 'rb')})

# Custom Content-Type with raw body
requests.post(
    url,
    data='<xml><tag>value</tag></xml>',
    headers={'Content-Type': 'application/xml'}
)
```

---

## 20. Hooks

Hooks let you trigger callbacks on events like receiving a response.

```python
def print_url(response, *args, **kwargs):
    print(f"Request to: {response.url} → {response.status_code}")

response = requests.get(
    'https://httpbin.org/get',
    hooks={'response': print_url}
)

# Session-level hooks applied to every request
session = requests.Session()
session.hooks['response'].append(print_url)
```

---

## 21. Custom Retry Logic

```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests

retry_strategy = Retry(
    total=3,                          # max retries
    backoff_factor=1,                 # wait 1, 2, 4 seconds between retries
    status_forcelist=[429, 500, 502, 503, 504],  # retry on these status codes
    allowed_methods=["GET", "POST"]
)

adapter = HTTPAdapter(max_retries=retry_strategy)

session = requests.Session()
session.mount('https://', adapter)
session.mount('http://', adapter)

response = session.get('https://httpbin.org/get', timeout=5)
print(response.status_code)
```

---

## 22. Prepared Requests

```python
from requests import Request, Session

req = Request(
    method='POST',
    url='https://httpbin.org/post',
    headers={'Authorization': 'Bearer token123'},
    json={'name': 'Alice'}
)

prepared = req.prepare()

print(prepared.method)   # POST
print(prepared.url)      # https://httpbin.org/post
print(prepared.headers)
print(prepared.body)

session = Session()
response = session.send(prepared, timeout=5)
print(response.json())
```

---

## 23. Exception Hierarchy

```python
requests.RequestException        # Base class for all exceptions
├── requests.ConnectionError     # Network problem (DNS, refused, etc.)
├── requests.Timeout             # Request timed out
│   ├── requests.ConnectTimeout  # Connection timeout
│   └── requests.ReadTimeout     # Read timeout
├── requests.HTTPError           # HTTP error response (from raise_for_status)
├── requests.URLRequired         # Invalid URL
└── requests.TooManyRedirects    # Too many redirects
```

```python
try:
    response = requests.get('https://example.com', timeout=5)
    response.raise_for_status()
    data = response.json()
except requests.ConnectTimeout:
    print("Could not connect in time")
except requests.ReadTimeout:
    print("Server took too long to respond")
except requests.HTTPError as e:
    print(f"HTTP {e.response.status_code}: {e}")
except requests.ConnectionError:
    print("Network error")
except requests.RequestException as e:
    print(f"Unexpected error: {e}")
```

---

## 24. Practical Examples

### Fetch & Parse a REST API

```python
import requests

def get_user(user_id):
    url = f'https://jsonplaceholder.typicode.com/users/{user_id}'
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching user {user_id}: {e}")
        return None

user = get_user(1)
if user:
    print(f"Name: {user['name']}, Email: {user['email']}")
```

### Paginate Through an API

```python
import requests

def fetch_all_posts():
    all_posts = []
    page = 1

    while True:
        response = requests.get(
            'https://jsonplaceholder.typicode.com/posts',
            params={'_page': page, '_limit': 10},
            timeout=5
        )
        response.raise_for_status()
        posts = response.json()

        if not posts:
            break

        all_posts.extend(posts)
        page += 1

    return all_posts

posts = fetch_all_posts()
print(f"Total posts: {len(posts)}")
```

### Reusable API Wrapper

```python
import requests

class JSONPlaceholderAPI:
    BASE_URL = 'https://jsonplaceholder.typicode.com'

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})

    def _request(self, method, endpoint, **kwargs):
        url = f'{self.BASE_URL}{endpoint}'
        response = self.session.request(method, url, timeout=10, **kwargs)
        response.raise_for_status()
        return response.json()

    def get_post(self, post_id):
        return self._request('GET', f'/posts/{post_id}')

    def create_post(self, title, body, user_id):
        return self._request('POST', '/posts', json={
            'title': title, 'body': body, 'userId': user_id
        })

    def delete_post(self, post_id):
        return self._request('DELETE', f'/posts/{post_id}')

api = JSONPlaceholderAPI()
post = api.get_post(1)
print(post['title'])
```

### Download Image

```python
import requests

def download_image(url, filename):
    response = requests.get(url, stream=True, timeout=10)
    response.raise_for_status()

    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"Saved to {filename}")

download_image('https://httpbin.org/image/png', 'image.png')
```

### POST with Retry & Logging

```python
import requests
import time

def post_with_retry(url, payload, retries=3, delay=2):
    for attempt in range(1, retries + 1):
        try:
            response = requests.post(url, json=payload, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt < retries:
                time.sleep(delay)
    return None

result = post_with_retry(
    'https://jsonplaceholder.typicode.com/posts',
    {'title': 'Test', 'body': 'Hello', 'userId': 1}
)
print(result)
```

---

## 25. Quick Reference

| Task                        | Code                                                    |
|-----------------------------|---------------------------------------------------------|
| GET request                 | `requests.get(url)`                                     |
| POST JSON                   | `requests.post(url, json=data)`                         |
| POST form data              | `requests.post(url, data=data)`                         |
| Query parameters            | `requests.get(url, params={'k': 'v'})`                  |
| Custom headers              | `requests.get(url, headers={'Key': 'Val'})`             |
| Basic auth                  | `requests.get(url, auth=('user', 'pass'))`              |
| Bearer token                | `headers={'Authorization': 'Bearer token'}`             |
| Set timeout                 | `requests.get(url, timeout=5)`                          |
| Parse JSON response         | `response.json()`                                       |
| Check status                | `response.status_code`, `response.ok`                   |
| Raise on error              | `response.raise_for_status()`                           |
| Download file (stream)      | `requests.get(url, stream=True)`                        |
| Upload file                 | `requests.post(url, files={'f': open(..., 'rb')})`      |
| Use session                 | `with requests.Session() as s:`                         |
| Disable SSL verify          | `requests.get(url, verify=False)`                       |
| Disable redirects           | `requests.get(url, allow_redirects=False)`              |
| Add retries                 | `HTTPAdapter(max_retries=Retry(total=3))`               |

---

> 💡 **Tip:** For async HTTP requests, look into `httpx` or `aiohttp` — they support `async/await` and are great for high-concurrency applications.
