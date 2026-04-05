# Python `re` Module – Full Tutorial

> The `re` module provides support for regular expressions (regex) in Python. It allows you to search, match, split, and manipulate strings using powerful pattern syntax. Part of the standard library — no installation needed.

---

## 1. Importing

```python
import re
```

---

## 2. What is a Regular Expression?

A regular expression is a sequence of characters that defines a search pattern. It can be used to check if a string contains a certain pattern, extract parts of a string, or replace text.

```python
# Does the string contain a 4-digit number?
pattern = r'\d{4}'
text = "My PIN is 4821"
print(re.search(pattern, text))  # <re.Match object ...>
```

> 💡 Always use raw strings (`r"..."`) for regex patterns to avoid issues with Python's own backslash handling.

---

## 3. Core Functions

| Function          | Description                                          |
|-------------------|------------------------------------------------------|
| `re.match()`      | Match pattern at the **beginning** of string         |
| `re.search()`     | Search entire string, return **first** match         |
| `re.findall()`    | Return **all** matches as a list                     |
| `re.finditer()`   | Return all matches as an **iterator of Match objects**|
| `re.sub()`        | Replace matches with a string                        |
| `re.subn()`       | Replace matches, also return replacement count       |
| `re.split()`      | Split string by pattern                              |
| `re.compile()`    | Compile a pattern into a reusable regex object       |
| `re.fullmatch()`  | Match pattern against the **entire** string          |
| `re.escape()`     | Escape special regex characters in a string          |

---

## 4. `re.match()` – Match at the Start

```python
import re

result = re.match(r'\d+', '123abc')
print(result)         # <re.Match object; span=(0, 3), match='123'>
print(result.group()) # 123

# Returns None if no match at start
result = re.match(r'\d+', 'abc123')
print(result)         # None
```

---

## 5. `re.search()` – Search Anywhere

```python
result = re.search(r'\d+', 'abc 123 def')
print(result.group()) # 123
print(result.span())  # (4, 7)
print(result.start()) # 4
print(result.end())   # 7
```

---

## 6. `re.findall()` – Find All Matches

```python
text = "Call 1234 or 5678 or 9999"

numbers = re.findall(r'\d+', text)
print(numbers)  # ['1234', '5678', '9999']

# With groups — returns list of tuples
dates = re.findall(r'(\d{4})-(\d{2})-(\d{2})', '2024-01-15 and 2023-12-31')
print(dates)  # [('2024', '01', '15'), ('2023', '12', '31')]
```

---

## 7. `re.finditer()` – Iterator of Match Objects

```python
text = "foo bar baz"

for match in re.finditer(r'\b\w{3}\b', text):
    print(match.group(), match.start(), match.end())
# foo 0 3
# bar 4 7
# baz 8 11
```

---

## 8. `re.sub()` – Replace Matches

```python
# Basic replacement
result = re.sub(r'\d+', 'NUM', 'I have 3 cats and 12 dogs')
print(result)  # I have NUM cats and NUM dogs

# Limit replacements with count
result = re.sub(r'\d+', 'NUM', 'I have 3 cats and 12 dogs', count=1)
print(result)  # I have NUM cats and 12 dogs

# Using a function as replacement
def double(match):
    return str(int(match.group()) * 2)

result = re.sub(r'\d+', double, '3 cats and 12 dogs')
print(result)  # 6 cats and 24 dogs
```

---

## 9. `re.subn()` – Replace and Count

```python
result, count = re.subn(r'\d+', 'NUM', 'I have 3 cats and 12 dogs')
print(result)  # I have NUM cats and NUM dogs
print(count)   # 2
```

---

## 10. `re.split()` – Split by Pattern

```python
# Split on one or more spaces
parts = re.split(r'\s+', 'one   two\tthree\nfour')
print(parts)  # ['one', 'two', 'three', 'four']

# Split on comma or semicolon
parts = re.split(r'[,;]', 'a,b;c,d')
print(parts)  # ['a', 'b', 'c', 'd']

# Include the delimiter in results using a group
parts = re.split(r'(\s+)', 'one two three')
print(parts)  # ['one', ' ', 'two', ' ', 'three']
```

---

## 11. `re.fullmatch()` – Match Entire String

```python
# Valid if the entire string matches
print(re.fullmatch(r'\d{4}', '2024'))    # Match object
print(re.fullmatch(r'\d{4}', '20245'))   # None (too long)
print(re.fullmatch(r'\d{4}', 'x024'))    # None (non-digit)
```

---

## 12. `re.compile()` – Reusable Patterns

Compiling a pattern is more efficient when you use it multiple times.

```python
pattern = re.compile(r'\b[A-Z][a-z]+\b')

text1 = "Hello World from Python"
text2 = "Alice and Bob went to Paris"

print(pattern.findall(text1))  # ['Hello', 'World', 'Python']
print(pattern.findall(text2))  # ['Alice', 'Bob', 'Paris']
```

---

## 13. Match Object Methods

```python
match = re.search(r'(\d{4})-(\d{2})-(\d{2})', 'Date: 2024-01-15')

match.group()     # '2024-01-15'  — full match
match.group(0)    # '2024-01-15'  — same as group()
match.group(1)    # '2024'        — first capture group
match.group(2)    # '01'          — second capture group
match.group(3)    # '15'          — third capture group
match.groups()    # ('2024', '01', '15')
match.start()     # 6
match.end()       # 16
match.span()      # (6, 16)
match.string      # 'Date: 2024-01-15'  — original string
```

---

## 14. Regex Special Characters (Meta Characters)

| Character | Meaning                                 |
|-----------|-----------------------------------------|
| `.`       | Any character except newline            |
| `^`       | Start of string                         |
| `$`       | End of string                           |
| `*`       | 0 or more repetitions                   |
| `+`       | 1 or more repetitions                   |
| `?`       | 0 or 1 repetition (also makes lazy)     |
| `{n}`     | Exactly n repetitions                   |
| `{n,m}`   | Between n and m repetitions             |
| `[]`      | Character class (set)                   |
| `|`       | Alternation (OR)                        |
| `()`      | Grouping / capturing                    |
| `\`       | Escape special character                |

---

## 15. Character Classes

```python
re.findall(r'[aeiou]', 'hello world')       # Vowels: ['e', 'o', 'o']
re.findall(r'[^aeiou\s]', 'hello world')    # Non-vowels, non-space: ['h', 'l', 'l', 'w', 'r', 'l', 'd']
re.findall(r'[a-z]', 'Hello World 123')     # Lowercase letters
re.findall(r'[A-Z]', 'Hello World 123')     # Uppercase letters
re.findall(r'[0-9]', 'Hello World 123')     # Digits
re.findall(r'[a-zA-Z0-9]', 'Hi! 99.')       # Alphanumeric
```

---

## 16. Shorthand Character Classes

| Shorthand | Equivalent       | Meaning                      |
|-----------|------------------|------------------------------|
| `\d`      | `[0-9]`          | Digit                        |
| `\D`      | `[^0-9]`         | Non-digit                    |
| `\w`      | `[a-zA-Z0-9_]`   | Word character               |
| `\W`      | `[^a-zA-Z0-9_]`  | Non-word character           |
| `\s`      | `[ \t\n\r\f\v]`  | Whitespace                   |
| `\S`      | `[^ \t\n\r\f\v]` | Non-whitespace               |
| `\b`      | —                | Word boundary                |
| `\B`      | —                | Non-word boundary            |

```python
re.findall(r'\d+', 'abc 123 def 456')   # ['123', '456']
re.findall(r'\w+', 'hello, world!')     # ['hello', 'world']
re.findall(r'\b\w+\b', 'say hi there') # ['say', 'hi', 'there']
```

---

## 17. Anchors

```python
re.findall(r'^\d+', '123 abc')         # ['123']  — start of string
re.findall(r'\d+$', 'abc 123')         # ['123']  — end of string
re.findall(r'\bcat\b', 'cat cats concatenate')  # ['cat']  — whole word
```

---

## 18. Quantifiers

```python
re.findall(r'ab*',  'a ab abb abbb')   # ['a', 'ab', 'abb', 'abbb']  (0 or more b)
re.findall(r'ab+',  'a ab abb abbb')   # ['ab', 'abb', 'abbb']       (1 or more b)
re.findall(r'ab?',  'a ab abb abbb')   # ['a', 'ab', 'ab', 'ab']     (0 or 1 b)
re.findall(r'ab{2}', 'ab abb abbb')    # ['abb']                     (exactly 2 b)
re.findall(r'ab{2,3}', 'ab abb abbb abbb') # ['abb', 'abbb']         (2 to 3 b)
```

### Greedy vs Lazy

```python
text = '<h1>Title</h1>'

re.findall(r'<.*>',  text)   # ['<h1>Title</h1>']  — greedy (as much as possible)
re.findall(r'<.*?>', text)   # ['<h1>', '</h1>']   — lazy (as little as possible)
```

---

## 19. Groups

### Capturing Groups `()`

```python
match = re.search(r'(\w+)@(\w+)\.(\w+)', 'user@example.com')
print(match.groups())   # ('user', 'example', 'com')
print(match.group(1))   # user
print(match.group(2))   # example
```

### Non-Capturing Groups `(?:...)`

```python
# Group for structure, but don't capture
result = re.findall(r'(?:Mr|Ms|Dr)\.? (\w+)', 'Mr. Smith and Dr. Jones')
print(result)  # ['Smith', 'Jones']
```

### Named Groups `(?P<name>...)`

```python
match = re.search(r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})', '2024-01-15')
print(match.group('year'))   # 2024
print(match.group('month'))  # 01
print(match.group('day'))    # 15
print(match.groupdict())     # {'year': '2024', 'month': '01', 'day': '15'}
```

### Backreferences `\1`, `\2`, …

```python
# Match repeated words
result = re.search(r'\b(\w+)\s+\1\b', 'the the quick brown fox')
print(result.group())   # the the
```

---

## 20. Lookahead & Lookbehind (Assertions)

| Syntax      | Name               | Description                              |
|-------------|--------------------|------------------------------------------|
| `(?=...)`   | Positive lookahead | Match if followed by pattern             |
| `(?!...)`   | Negative lookahead | Match if NOT followed by pattern         |
| `(?<=...)`  | Positive lookbehind| Match if preceded by pattern             |
| `(?<!...)`  | Negative lookbehind| Match if NOT preceded by pattern         |

```python
# Positive lookahead — price followed by USD
re.findall(r'\d+(?= USD)', '100 USD and 200 EUR')   # ['100']

# Negative lookahead — number NOT followed by USD
re.findall(r'\d+(?! USD)', '100 USD and 200 EUR')   # ['200']

# Positive lookbehind — number preceded by $
re.findall(r'(?<=\$)\d+', 'Price: $100 and €200')   # ['100']

# Negative lookbehind — number NOT preceded by $
re.findall(r'(?<!\$)\d+', 'Price: $100 and 200')    # ['200']
```

---

## 21. Flags

Flags modify how patterns are matched.

| Flag              | Short | Description                              |
|-------------------|-------|------------------------------------------|
| `re.IGNORECASE`   | `re.I`| Case-insensitive matching                |
| `re.MULTILINE`    | `re.M`| `^` and `$` match each line             |
| `re.DOTALL`       | `re.S`| `.` matches newline too                  |
| `re.VERBOSE`      | `re.X`| Allow whitespace and comments in pattern |
| `re.ASCII`        | `re.A`| `\w`, `\d`, etc. match ASCII only        |
| `re.UNICODE`      | `re.U`| `\w`, `\d` match Unicode (default)       |

```python
# Case-insensitive
re.findall(r'hello', 'Hello HELLO hello', re.IGNORECASE)  # ['Hello', 'HELLO', 'hello']

# Multiline
text = "start\nhello\nend"
re.findall(r'^hello', text, re.MULTILINE)  # ['hello']

# Dotall — dot matches newline
re.findall(r'start.+end', 'start\nend', re.DOTALL)  # ['start\nend']

# Verbose — readable pattern with comments
pattern = re.compile(r"""
    (\d{4})   # year
    -         # separator
    (\d{2})   # month
    -         # separator
    (\d{2})   # day
""", re.VERBOSE)

# Combine flags with |
re.findall(r'hello', 'Hello\nHELLO', re.IGNORECASE | re.MULTILINE)
```

---

## 22. `re.escape()` – Escape Special Characters

Use when building patterns dynamically from user input.

```python
user_input = "hello.world (test)"

# Without escape — '.' and '(' are special
pattern = re.compile(user_input)  # dangerous

# With escape — treats all chars as literals
safe_pattern = re.compile(re.escape(user_input))
print(safe_pattern.pattern)  # hello\.world\ \(test\)
```

---

## 23. Common Regex Patterns

```python
# Email address
re.findall(r'[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}', 'Send to user@example.com or admin@test.org')

# URL
re.findall(r'https?://[^\s]+', 'Visit https://python.org or http://example.com')

# IPv4 address
re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', 'Server: 192.168.1.1 and 10.0.0.1')

# Phone number (US style)
re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', 'Call (123) 456-7890 or 987.654.3210')

# Date (YYYY-MM-DD)
re.findall(r'\d{4}-\d{2}-\d{2}', 'Event on 2024-01-15 and 2023-12-31')

# Hex color
re.findall(r'#[0-9a-fA-F]{6}', 'Colors: #FF5733 and #1a2b3c')

# Zip code (US)
re.findall(r'\b\d{5}(?:-\d{4})?\b', 'ZIP: 90210 or 10001-1234')

# HTML tag
re.findall(r'<[^>]+>', '<h1>Title</h1><p>Text</p>')

# Word repeated twice
re.findall(r'\b(\w+)\s+\1\b', 'the the quick brown fox fox')
```

---

## 24. Practical Examples

### Extract All Emails from Text

```python
import re

text = "Contact us at support@example.com or sales@company.org for help."
emails = re.findall(r'[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}', text)
print(emails)  # ['support@example.com', 'sales@company.org']
```

### Validate a Password

```python
def validate_password(pwd):
    checks = {
        "min 8 chars":        r'.{8,}',
        "uppercase letter":   r'[A-Z]',
        "lowercase letter":   r'[a-z]',
        "digit":              r'\d',
        "special character":  r'[!@#$%^&*]',
    }
    results = {name: bool(re.search(pat, pwd)) for name, pat in checks.items()}
    return results

print(validate_password("MyP@ss99"))
```

### Clean & Normalize Whitespace

```python
text = "Hello    world  \n\t  from   Python"
clean = re.sub(r'\s+', ' ', text).strip()
print(clean)  # Hello world from Python
```

### Parse Log Lines

```python
log = '2024-01-15 10:30:45 ERROR Failed to connect to database'

pattern = re.compile(
    r'(?P<date>\d{4}-\d{2}-\d{2})\s+'
    r'(?P<time>\d{2}:\d{2}:\d{2})\s+'
    r'(?P<level>\w+)\s+'
    r'(?P<message>.+)'
)

match = pattern.match(log)
if match:
    print(match.group('date'))     # 2024-01-15
    print(match.group('level'))    # ERROR
    print(match.group('message'))  # Failed to connect to database
```

### Censor Sensitive Data

```python
text = "SSN: 123-45-6789 and card: 4111-1111-1111-1111"

# Mask SSN
text = re.sub(r'\d{3}-\d{2}-\d{4}', 'XXX-XX-XXXX', text)
# Mask credit card
text = re.sub(r'\d{4}-\d{4}-\d{4}-\d{4}', 'XXXX-XXXX-XXXX-XXXX', text)
print(text)  # SSN: XXX-XX-XXXX and card: XXXX-XXXX-XXXX-XXXX
```

---

## 25. Performance Tips

```python
# ✅ Compile patterns used multiple times
pattern = re.compile(r'\d+')
for line in lines:
    pattern.findall(line)

# ✅ Use non-capturing groups when you don't need the group value
re.findall(r'(?:foo|bar)', text)  # faster than (foo|bar) if group not needed

# ✅ Be specific — avoid overly broad patterns like .*
re.findall(r'\d{4}-\d{2}-\d{2}', text)  # better than .*

# ✅ Anchor patterns when possible
re.match(r'\d+', text)   # match only checks the start (faster than search for this case)

# ⚠️  Avoid catastrophic backtracking with nested quantifiers like (a+)+
```

---

## 26. Quick Reference

| Task                         | Code                                         |
|------------------------------|----------------------------------------------|
| Match at start               | `re.match(pattern, string)`                  |
| Search anywhere              | `re.search(pattern, string)`                 |
| Find all matches             | `re.findall(pattern, string)`                |
| Iterate matches              | `re.finditer(pattern, string)`               |
| Replace matches              | `re.sub(pattern, repl, string)`              |
| Split by pattern             | `re.split(pattern, string)`                  |
| Match whole string           | `re.fullmatch(pattern, string)`              |
| Compile for reuse            | `re.compile(pattern)`                        |
| Escape special chars         | `re.escape(string)`                          |
| Case-insensitive             | `re.findall(p, s, re.I)`                     |
| Multiline mode               | `re.findall(p, s, re.M)`                     |
| Dot matches newline          | `re.findall(p, s, re.S)`                     |
| Named group                  | `(?P<name>...)`                              |
| Non-capturing group          | `(?:...)`                                    |
| Positive lookahead           | `(?=...)`                                    |
| Negative lookahead           | `(?!...)`                                    |
| Positive lookbehind          | `(?<=...)`                                   |
| Negative lookbehind          | `(?<!...)`                                   |

---

> 💡 **Tip:** Use [regex101.com](https://regex101.com) to test and debug your regex patterns interactively with Python flavor selected.
