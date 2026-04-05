# Python `json` Module – Full Tutorial

> The `json` module provides tools to encode Python objects into JSON format and decode JSON back into Python objects. It's part of the standard library — no installation needed.

---

## 1. Importing

```python
import json
```

---

## 2. Core Concepts: Serialization vs Deserialization

| Term             | Direction                  | Functions           |
|------------------|----------------------------|---------------------|
| Serialization    | Python → JSON (encoding)   | `dump()`, `dumps()` |
| Deserialization  | JSON → Python (decoding)   | `load()`, `loads()` |

---

## 3. Python ↔ JSON Type Mapping

| Python Type     | JSON Type  |
|-----------------|------------|
| `dict`          | `object`   |
| `list`, `tuple` | `array`    |
| `str`           | `string`   |
| `int`, `float`  | `number`   |
| `True`          | `true`     |
| `False`         | `false`    |
| `None`          | `null`     |

---

## 4. `dumps()` – Python to JSON String

```python
import json

data = {
    "name": "Alice",
    "age": 30,
    "active": True,
    "score": 98.5,
    "tags": ["python", "dev"],
    "address": None
}

json_string = json.dumps(data)
print(json_string)
# {"name": "Alice", "age": 30, "active": true, "score": 98.5, "tags": ["python", "dev"], "address": null}
```

### Pretty Printing with `indent`

```python
print(json.dumps(data, indent=4))
# {
#     "name": "Alice",
#     "age": 30,
#     ...
# }
```

### Sorting Keys

```python
json.dumps(data, sort_keys=True)
```

### Custom Separator (compact output)

```python
json.dumps(data, separators=(',', ':'))
# {"name":"Alice","age":30,...}
```

---

## 5. `loads()` – JSON String to Python

```python
json_string = '{"name": "Alice", "age": 30, "active": true, "address": null}'

data = json.loads(json_string)

print(data["name"])    # Alice
print(data["active"])  # True  (JSON true → Python True)
print(data["address"]) # None  (JSON null → Python None)
print(type(data))      # <class 'dict'>
```

---

## 6. `dump()` – Write JSON to a File

```python
data = {"name": "Alice", "age": 30}

with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)
```

> 💡 Always open files in text mode (`'w'`) not binary mode (`'wb'`) when using `json.dump()`.

---

## 7. `load()` – Read JSON from a File

```python
with open('data.json', 'r') as f:
    data = json.load(f)

print(data)         # {'name': 'Alice', 'age': 30}
print(type(data))   # <class 'dict'>
```

---

## 8. Handling Nested JSON

```python
nested = {
    "user": {
        "id": 1,
        "profile": {
            "name": "Alice",
            "skills": ["Python", "SQL", "Docker"]
        }
    }
}

json_str = json.dumps(nested, indent=2)
parsed = json.loads(json_str)

# Access nested values
print(parsed["user"]["profile"]["name"])       # Alice
print(parsed["user"]["profile"]["skills"][0])  # Python
```

---

## 9. Error Handling

### `json.JSONDecodeError`

Raised when parsing invalid JSON.

```python
import json

bad_json = "{'name': 'Alice'}"  # single quotes are invalid in JSON

try:
    data = json.loads(bad_json)
except json.JSONDecodeError as e:
    print(f"Error: {e}")
    print(f"Line:  {e.lineno}, Column: {e.colno}")
    print(f"Position: {e.pos}")
```

### `TypeError` on Serialization

Raised when trying to serialize a non-JSON-serializable type.

```python
import datetime

data = {"created": datetime.datetime.now()}

try:
    json.dumps(data)
except TypeError as e:
    print(f"Serialization error: {e}")
    # Object of type datetime is not JSON serializable
```

---

## 10. Custom Serialization

### Using `default` Parameter

Pass a function to handle non-serializable types.

```python
import json
import datetime

def custom_serializer(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    if isinstance(obj, set):
        return list(obj)
    raise TypeError(f"Type {type(obj)} not serializable")

data = {
    "created": datetime.datetime(2024, 1, 15, 10, 30),
    "tags": {"python", "json"}
}

print(json.dumps(data, default=custom_serializer, indent=2))
```

### Subclassing `json.JSONEncoder`

```python
import json
import datetime

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)

data = {"created": datetime.datetime.now(), "tags": {"a", "b"}}

print(json.dumps(data, cls=CustomEncoder, indent=2))
```

---

## 11. Custom Deserialization

### Using `object_hook`

Called with every decoded JSON object (dict). Use it to transform data during parsing.

```python
import json
import datetime

def custom_decoder(obj):
    if "created" in obj:
        obj["created"] = datetime.datetime.fromisoformat(obj["created"])
    return obj

json_str = '{"name": "Alice", "created": "2024-01-15T10:30:00"}'

data = json.loads(json_str, object_hook=custom_decoder)
print(data["created"])         # 2024-01-15 10:30:00
print(type(data["created"]))   # <class 'datetime.datetime'>
```

### Using `parse_float` and `parse_int`

```python
from decimal import Decimal

data = json.loads('{"price": 9.99}', parse_float=Decimal)
print(data["price"])        # 9.99
print(type(data["price"]))  # <class 'decimal.Decimal'>
```

---

## 12. Working with JSON Arrays

```python
import json

# List of objects
users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"}
]

json_str = json.dumps(users, indent=2)
parsed = json.loads(json_str)

for user in parsed:
    print(f"{user['id']}: {user['name']}")
```

---

## 13. Pretty Print an Existing JSON String

```python
import json

raw = '{"name":"Alice","age":30,"tags":["python","dev"]}'

pretty = json.dumps(json.loads(raw), indent=4, sort_keys=True)
print(pretty)
```

---

## 14. Reading & Writing JSON Lines (`.jsonl`)

JSON Lines format stores one JSON object per line — common in logs and data pipelines.

```python
import json

# Write JSON Lines
records = [
    {"id": 1, "event": "login"},
    {"id": 2, "event": "purchase"},
    {"id": 3, "event": "logout"},
]

with open('events.jsonl', 'w') as f:
    for record in records:
        f.write(json.dumps(record) + '\n')

# Read JSON Lines
with open('events.jsonl', 'r') as f:
    for line in f:
        record = json.loads(line.strip())
        print(record)
```

---

## 15. Merging & Updating JSON Data

```python
import json

# Deep merge two dicts
base = {"name": "Alice", "settings": {"theme": "dark", "lang": "en"}}
update = {"age": 30, "settings": {"lang": "fr"}}

# Shallow merge (settings key gets completely replaced)
merged = {**base, **update}

# Deep merge settings manually
merged["settings"] = {**base["settings"], **update["settings"]}
print(json.dumps(merged, indent=2))
```

---

## 16. Validating JSON

```python
import json

def is_valid_json(text):
    try:
        json.loads(text)
        return True
    except json.JSONDecodeError:
        return False

print(is_valid_json('{"key": "value"}'))   # True
print(is_valid_json("not json at all"))    # False
print(is_valid_json("{'key': 'value'}"))   # False (single quotes)
```

---

## 17. Encoding Options Summary

```python
json.dumps(
    obj,
    skipkeys=False,      # Skip dict keys that aren't basic types (instead of raising TypeError)
    ensure_ascii=True,   # Escape non-ASCII chars; set False to allow Unicode
    check_circular=True, # Check for circular references
    allow_nan=True,      # Allow float('nan'), float('inf'), float('-inf')
    sort_keys=False,     # Sort dict keys alphabetically
    indent=None,         # Pretty print with given indent level
    separators=None,     # (item_separator, key_separator) tuple
    default=None,        # Function to handle non-serializable types
)
```

### Unicode example

```python
data = {"city": "München", "emoji": "🐍"}

print(json.dumps(data))                      # {"city": "M\\u00fcnchen", "emoji": "\\ud83d\\udc0d"}
print(json.dumps(data, ensure_ascii=False))  # {"city": "München", "emoji": "🐍"}
```

---

## 18. Practical Examples

### Config File Read/Write

```python
import json
import os

CONFIG_FILE = 'config.json'

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

config = load_config()
config["debug"] = True
config["version"] = "1.0.0"
save_config(config)
```

### Parse an API Response

```python
import json
import urllib.request

url = "https://api.github.com/users/python"
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read().decode())

print(data["name"])
print(data["public_repos"])
```

### Deep Copy via JSON (for simple data)

```python
import json

original = {"a": [1, 2, 3], "b": {"x": 10}}
copy = json.loads(json.dumps(original))

copy["a"].append(99)
print(original["a"])  # [1, 2, 3] — unaffected
print(copy["a"])      # [1, 2, 3, 99]
```

> ⚠️ This only works for JSON-serializable types. For complex objects use `copy.deepcopy()`.

---

## 19. Quick Reference

| Function        | Description                          |
|-----------------|--------------------------------------|
| `json.dumps()`  | Python object → JSON string          |
| `json.loads()`  | JSON string → Python object          |
| `json.dump()`   | Python object → JSON file            |
| `json.load()`   | JSON file → Python object            |
| `indent`        | Pretty-print with indentation        |
| `sort_keys`     | Sort dictionary keys alphabetically  |
| `default`       | Handle non-serializable types        |
| `object_hook`   | Transform dicts during decoding      |
| `ensure_ascii`  | Allow/escape non-ASCII characters    |
| `parse_float`   | Custom type for float values         |
| `JSONDecodeError` | Exception for invalid JSON input   |

---

> 💡 **Tip:** For more complex or schema-validated JSON handling, look into third-party libraries like `pydantic`, `marshmallow`, or `jsonschema`.
