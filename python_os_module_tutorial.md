# Python `os` Module – Full Tutorial

> The `os` module provides a portable way to interact with the operating system. It's part of Python's standard library — no installation needed.

---

## 1. Importing

```python
import os
```

---

## 2. Current Working Directory

```python
os.getcwd()               # Get current directory
os.chdir('/path/to/dir')  # Change directory
```

---

## 3. Environment Variables

```python
os.environ                        # Dict-like object of all env vars
os.environ.get('HOME')            # Safe get (returns None if missing)
os.environ['MY_VAR'] = 'value'    # Set an env var
os.getenv('PATH', 'default')      # Get with default fallback
```

---

## 4. File & Directory Operations

### Creating Directories

```python
os.mkdir('new_folder')               # Create single directory
os.makedirs('a/b/c', exist_ok=True)  # Create nested directories
```

### Removing Files & Directories

```python
os.remove('file.txt')               # Delete a file
os.rmdir('empty_folder')            # Delete empty directory
os.removedirs('a/b/c')              # Remove nested empty dirs
```

### Renaming / Moving

```python
os.rename('old.txt', 'new.txt')
os.renames('old/path', 'new/path')  # Recursive rename
```

### Listing Directory Contents

```python
os.listdir('.')     # Returns list of names
os.scandir('.')     # Returns iterator of DirEntry objects (faster)
```

---

## 5. Path Operations (`os.path`)

```python
os.path.join('folder', 'file.txt')        # → 'folder/file.txt'
os.path.abspath('file.txt')               # Absolute path
os.path.dirname('/home/user/file.txt')    # → '/home/user'
os.path.basename('/home/user/file.txt')   # → 'file.txt'
os.path.split('/home/user/file.txt')      # → ('/home/user', 'file.txt')
os.path.splitext('file.txt')             # → ('file', '.txt')

# Existence checks
os.path.exists('file.txt')   # Does it exist?
os.path.isfile('file.txt')   # Is it a file?
os.path.isdir('folder')      # Is it a directory?
os.path.isabs('/abs/path')   # Is it absolute?

# Size & time
os.path.getsize('file.txt')  # Size in bytes
os.path.getmtime('file.txt') # Last modified (Unix timestamp)
```

---

## 6. Walking a Directory Tree

`os.walk()` recursively traverses directories, yielding `(root, dirs, files)` tuples.

```python
for root, dirs, files in os.walk('/some/path'):
    print("In:", root)
    for f in files:
        print("  File:", os.path.join(root, f))
```

> 💡 Pass `topdown=False` to walk from the bottom up instead of top-down.

---

## 7. File Permissions & Stats

```python
os.stat('file.txt')            # Full stat result (size, mode, times...)
os.chmod('file.txt', 0o755)    # Change permissions
os.chown('file.txt', uid, gid) # Change owner (Unix only)

import stat
info = os.stat('file.txt')
print(stat.filemode(info.st_mode))  # e.g. '-rwxr-xr-x'
```

---

## 8. Low-Level File Descriptors

Usually you'd prefer the built-in `open()`, but `os.open()` gives lower-level control.

```python
fd = os.open('file.txt', os.O_RDWR | os.O_CREAT)  # Open file descriptor
os.write(fd, b'Hello World')
os.lseek(fd, 0, os.SEEK_SET)
data = os.read(fd, 1024)
os.close(fd)
```

---

## 9. Process Information

```python
os.getpid()    # Current process ID
os.getppid()   # Parent process ID
os.getuid()    # Current user ID (Unix)
os.getlogin()  # Login name of user
os.cpu_count() # Number of CPUs
```

---

## 10. Symbolic & Hard Links

```python
os.symlink('target.txt', 'link.txt')   # Create symbolic link
os.link('target.txt', 'hard.txt')      # Create hard link
os.readlink('link.txt')                # Read symlink target
os.unlink('link.txt')                  # Remove link (or file)
```

---

## 11. Running System Commands

```python
os.system('ls -la')   # Run shell command (simple, no output capture)

# Better: use subprocess to capture output
import subprocess
result = subprocess.run(['ls', '-la'], capture_output=True, text=True)
print(result.stdout)
```

---

## 12. Cross-Platform Constants

```python
os.sep        # Path separator: '/' on Unix, '\\' on Windows
os.linesep    # Line ending: '\n' on Unix, '\r\n' on Windows
os.pathsep    # Path list separator: ':' on Unix, ';' on Windows
os.curdir     # '.'
os.pardir     # '..'
os.devnull    # '/dev/null' or 'nul' on Windows
os.name       # 'posix', 'nt', or 'java'
```

---

## 13. Practical Examples

### Find All `.py` Files in a Project

```python
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d != '__pycache__']  # skip folders
    for f in files:
        if f.endswith('.py'):
            print(os.path.join(root, f))
```

### Ensure a Directory Exists Before Writing

```python
output_dir = 'reports/2024'
os.makedirs(output_dir, exist_ok=True)
with open(os.path.join(output_dir, 'report.txt'), 'w') as f:
    f.write('Hello')
```

### Get File Sizes of Everything in a Folder

```python
for entry in os.scandir('.'):
    if entry.is_file():
        print(f"{entry.name}: {entry.stat().st_size} bytes")
```

### Safely Read an Environment Variable with a Default

```python
debug_mode = os.getenv('DEBUG', 'false').lower() == 'true'
```

---

## 14. Quick Reference

| Task                     | Function(s)                              |
|--------------------------|------------------------------------------|
| Get/change directory     | `getcwd()`, `chdir()`                    |
| Create directories       | `mkdir()`, `makedirs()`                  |
| Delete files/dirs        | `remove()`, `rmdir()`, `removedirs()`   |
| List contents            | `listdir()`, `scandir()`                 |
| Walk directory tree      | `walk()`                                 |
| Build paths safely       | `os.path.join()`                         |
| Check existence/type     | `os.path.exists()`, `isfile()`, `isdir()`|
| Get file info            | `os.path.getsize()`, `getmtime()`        |
| Manage env vars          | `os.environ`, `getenv()`                 |
| Process info             | `getpid()`, `cpu_count()`               |
| Manage links             | `symlink()`, `link()`, `unlink()`        |
| Run shell commands       | `os.system()` / `subprocess`             |
| File permissions         | `chmod()`, `chown()`                     |

---

> 💡 **Tip:** For modern path handling, consider `pathlib.Path` — it provides an elegant object-oriented interface that wraps most `os.path` functionality in a cleaner API.
