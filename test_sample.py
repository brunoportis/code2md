class MyClass:
    def __init__(self, name: str, age: int = 30):
        self.name = name
        self.age = age

    def hello(self, greeting: str):
        print(f"{greeting}, {self.name}")

def module_function(a: int, b: float) -> float:
    return a + b
