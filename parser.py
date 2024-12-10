from lexer import Lexer, CommandType
from interpreter import Interpreter

class Parser:
  @staticmethod
  def parse_file(filename):
    with open(filename, "r") as code_file:
      first_line = code_file.readline().strip()
      if first_line != CommandType.START.value:
        print("The file must start with @start.")
        return
      
      for line in code_file:
        tokens = Lexer.tokenize(line.strip())
        if tokens == [CommandType.ECHO_OFF.value]:
          break
        Interpreter.interpret(tokens)