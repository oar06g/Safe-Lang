class Compiler:
    def __init__(self, source_code):
      ...


# Example usage
source = """
print("Hello, World!")
"""
compiler = Compiler(source)
bytecode = compiler.compile()
print(bytecode)