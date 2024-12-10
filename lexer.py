from enum import Enum

class CommandType(Enum):
  EXISTS = "exists"
  RUN = "run"
  CLEAR = "clear"
  SLEEP = "@sleep"
  ECHO_OFF = "@echo off"
  START = "@start"
  INIT = "init"
  LET_LIST = "let_list"
  COMPILER = "compiler"


class Lexer:
  @staticmethod
  def tokenize(line):
    return line.strip().split()