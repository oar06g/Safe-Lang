import os
import subprocess
import platform
import click
import time
from enum import Enum

# تعريف الأوامر
class CommandType(Enum):
  EXISTS = "exists"
  RUN = "run"
  CLEAR = "clear"
  SLEEP = "@sleep"
  ECHO_OFF = "@echo off"
  START = "@start"

# Lexer لتحليل النص إلى رموز
class Lexer:
  @staticmethod
  def tokenize(line):
    return line.strip().split()

# مفسر الأوامر
class Interpreter:
  @staticmethod
  def interpret(tokens):
    if len(tokens) == 2 and tokens[0] == CommandType.EXISTS.value:
      path = tokens[1]
      if os.path.exists(path):
        print(f"{path} exists.")
      else:
        print(f"{path} does not exist.")
    
    elif tokens[0] == CommandType.RUN.value and len(tokens) > 1:
      command_to_run = ' '.join(tokens[1:])
      try:
        result = subprocess.run(command_to_run, shell=True, check=True, text=True, capture_output=True)
        print(result.stdout)  # طباعة المخرجات
      except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e.stderr}")
    
    elif tokens[0] == CommandType.CLEAR.value:
      os.system('cls' if platform.system() == "Windows" else 'clear')
    
    elif tokens[0] == CommandType.SLEEP.value and len(tokens) == 2:
      try:
        seconds = int(tokens[1])
        print(f"Sleeping for {seconds} seconds...")
        time.sleep(seconds)
      except ValueError:
        print("Invalid argument for @sleep. Please provide a number.")
    
    else:
      print("Invalid command. Use 'exists <path>', 'run <command>', 'clear', or '@sleep <seconds>'.")

# محلل الأوامر
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
          print("Execution stopped due to @echo off.")
          break
        Interpreter.interpret(tokens)

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
