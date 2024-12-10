import click
from lexer import Lexer
from interpreter import Interpreter
from parser import Parser

@click.command()
@click.argument('filename', required=False)
def check_file(filename):
  if filename:
    if filename.endswith('.sl'):
      Parser.parse_file(filename)
    else:
      print("This is not a valid .sl file.")
  else:
    while True:
      command = input(">> ")
      if command.lower() == "exit":
        break
      tokens = Lexer.tokenize(command)
      Interpreter.interpret(tokens)

if __name__ == '__main__':
    check_file()
