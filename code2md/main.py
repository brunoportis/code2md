import ast
import os
from pathlib import Path
from typing import Optional, List

import typer
from rich.console import Console

app = typer.Typer(help="code2md tool")
console = Console()

@app.command()
def version():
    """Show the version of code2md."""
    console.print("code2md version 0.1.0")

class CodeStructureVisitor(ast.NodeVisitor):
    def __init__(self):
        self.structure = []
        self.current_class = None

    def visit_ClassDef(self, node):
        class_info = {
            "type": "class",
            "name": node.name,
            "methods": []
        }
        self.structure.append(class_info)
        self.current_class = class_info
        self.generic_visit(node)
        self.current_class = None

    def visit_FunctionDef(self, node):
        params = []
        for arg in node.args.args:
            arg_name = arg.arg
            arg_type = ""
            if arg.annotation:
                if isinstance(arg.annotation, ast.Name):
                    arg_type = f": {arg.annotation.id}"
                elif isinstance(arg.annotation, ast.Constant):
                    arg_type = f": {arg.annotation.value}"
                # Add more annotation parsing if needed (e.g., Subscript for List[str])
            params.append(f"{arg_name}{arg_type}")

        func_info = {
            "type": "function",
            "name": node.name,
            "params": params
        }

        if self.current_class:
            self.current_class["methods"].append(func_info)
        else:
            self.structure.append(func_info)

def parse_python_file(file_path: Path) -> List[dict]:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
        visitor = CodeStructureVisitor()
        visitor.visit(tree)
        return visitor.structure
    except Exception as e:
        console.print(f"[red]Error parsing {file_path}: {e}[/red]")
        return []

def format_as_markdown(project_structure: dict) -> str:
    lines = []
    for file_path, structure in project_structure.items():
        lines.append(f"## 📄 `{file_path}`\n")
        for item in structure:
            if item["type"] == "class":
                lines.append(f"- 📦 **Class** `{item['name']}`")
                for method in item["methods"]:
                    lines.append(f"  - ⚡ **Method** `{method['name']}`")
                    for param in method["params"]:
                        lines.append(f"    - 🔹 `{param}`")
            elif item["type"] == "function":
                lines.append(f"- ⚡ **Function** `{item['name']}`")
                for param in item["params"]:
                    lines.append(f"  - 🔹 `{param}`")
        lines.append("") # Add a blank line between files
    return "\n".join(lines)

@app.command()
def summary(
    path: Path = typer.Argument(..., help="Path to the project directory"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output Markdown file"),
    ignore: List[str] = typer.Option([], "--ignore", "-i", help="Directories to ignore (e.g. migrations/)"),
):
    """
    Generate a markdown summary of the project structure.
    """
    if not path.is_dir():
        console.print(f"[red]Error: {path} is not a directory.[/red]")
        raise typer.Exit(1)

    project_structure = {}

    for root, dirs, files in os.walk(path):
        # Skip hidden directories, common ones, and user-specified ones
        to_ignore = {'__pycache__', '.venv', 'node_modules'}.union(
            {i.rstrip('/') for i in ignore}
        )
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in to_ignore]
        
        for file in files:
            if file.endswith(".py"):
                file_path = Path(root) / file
                relative_path = file_path.relative_to(path)
                structure = parse_python_file(file_path)
                if structure:
                    project_structure[str(relative_path)] = structure

    markdown_content = format_as_markdown(project_structure)

    if output:
        output.write_text(markdown_content, encoding="utf-8")
        console.print(f"[green]Summary generated successfully in {output}[/green]")
    else:
        console.print(markdown_content)

if __name__ == "__main__":
    app()
