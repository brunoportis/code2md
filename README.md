# 📄 code2md

A simple CLI tool that parses Python projects and generates a rich, hierarchical Markdown summary of the project's architecture (classes, functions, methods, and parameters).

## 🚀 Installation

Ensure you have [uv](https://github.com/astral-sh/uv) installed, then run:

```bash
uv tool install -e .
```

## 🛠️ Usage

Run the tool pointing to the desired directory:

```bash
# Output to console
code2md summary .

# Output to a file
code2md summary . --output summary.md

# Ignore specific directories (e.g. migrations or custom folders)
code2md summary . --ignore migrations --ignore utils/
```

## 📝 Example Output

The generated markdown uses emojis, lists, and inline code blocks for better readability:

```markdown
## 📄 `main.py`

- 📦 **Class** `CodeStructureVisitor`
  - ⚡ **Method** `visit_ClassDef`
    - 🔹 `self`
    - 🔹 `node`
- ⚡ **Function** `parse_python_file`
  - 🔹 `file_path: Path`
```

## ⚙️ How it Works

`code2md` uses Python's built-in `ast` (Abstract Syntax Tree) module to statically analyze your `.py` files without executing them.
