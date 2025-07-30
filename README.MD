# ENG Language

## 🚀 Getting Started with ENG

ENG is a beginner-friendly interpreted language designed for education, scripting, and experimentation. Here's how to set it up and run your first ENG program.

---

### 🔧 Requirements

- Python 3.7 or later
- A terminal or command prompt
- A text editor (e.g., VS Code, Notepad++, Sublime Text)

---

### 📦 Installation

1. **Clone or Download the Project:**

```bash
git clone https://github.com/yourusername/eng-language.git
cd eng-language
```

2. **Ensure the directory structure includes**:

```
eng-language/
│
├── interpreter/
│   ├── __init__.py
│   ├── runtime.py
│   ├── parser.py
│   ├── evaluator.py
│   └── ...
├── example.eng
└── README.md
```

3. **Run a sample ENG program**:

```bash
python -m interpreter example.eng
```

---

### 🧪 First Program (example.eng)

```eng
let name = input "What is your name" str
say "Hello, " + name
```

**Sample Output:**
```
What is your name: Alice
Hello, Alice
```

---

## 📚 Language Syntax Guide

### ✅ `let` — Variable Assignment

```eng
let name = "Ashwanth"
let age = 25
let valid = true
```

### ✅ `say` — Output to Console

```eng
say "Hello, " + name
say str(age + 1)
```

---

### 📥 Input with Type

```eng
let age = input "Enter your age" int
let happy = input "Are you happy?" bool
```

Valid types: `str`, `int`, `float`, `bool`

---

### 🔁 Repeating Loops

```eng
repeat 3 times:
  say "Running..."
end
```

---

### ❓ Conditionals

```eng
if age >= 18:
  say "You're an adult."
end
```

---

### 🧩 Functions

```eng
define greet(person):
  say "Hi " + person
end

call greet("Bob")
```

---

### 🧺 List Support

```eng
let fruits = list()
call fruits.append("apple")
call fruits.append("banana")
say str(fruits)
```

Available List Methods:
- `append()`
- `pop()`
- `remove()`
- `insert()`
- `clear()`
- `index()`
- `count()`

---

### 🗃️ Dictionary Support

```eng
let user = dict()
call user.update({"name": "Joe", "age": 30})
say user.get("name")
```

Available Dict Methods:
- `get()`
- `update()`
- `keys()`
- `values()`
- `items()`
- `pop()`
- `clear()`

---

## 📜 License Summary

```
ENG is © 2025 Ashwanth. You may use, modify, and distribute it for educational and personal projects only.

Commercial use or plagiarism is prohibited without written permission.
```

For full terms, see the [LICENSE](https://github.com/yourusername/eng-language/wiki/License) page.

---

## 🔗 Resources

- [Full Wiki](https://github.com/yourusername/eng-language/wiki)
- [Sample Scripts](https://github.com/yourusername/eng-language/examples)
- [License Terms](https://github.com/yourusername/eng-language/wiki/License)