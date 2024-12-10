from lexer import CommandType
import subprocess
import platform
import time
import os
import func

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
        print(result.stdout)
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
    
    elif tokens[0] == CommandType.INIT.value and len(tokens) :
      print("initialization ...")
      func.init()
    
    else:
      print("Invalid command. Use 'exists <path>', 'run <command>', 'clear', or '@sleep <seconds>'.")
