import os
import re
from functools import reduce
import numpy as np

from _decorators import timeit
from _utils import _find_all

DIR_2024 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DAY = 4

SEARCHED_WORD = "XMAS"
WORD_LEN = len(SEARCHED_WORD)

def _parse_data(data: list[str]) -> np.ndarray:
  return [line for line in data]

@timeit
def part1(data: list[str]) -> int:
  s = 0
  for row in data:
    s += len(re.findall("XMAS", row)) + len(re.findall("SAMX", row))
  print(s)

  for col in range(len(data[0])-1):
    st = ""
    for row in range(len(data)):
      st += data[row][col]

    s += len(re.findall("XMAS", st)) + len(re.findall("SAMX", st))
  print(s)
    
  for row in range(len(data)-(WORD_LEN-1)):
    for col in range(len(data[0])-WORD_LEN):
      st = ""
      for i in range(WORD_LEN):
        st += data[row+i][col+i]

      s += len(re.findall("XMAS", st)) + len(re.findall("SAMX", st))
  print(s)

  for row in range(WORD_LEN-1, len(data)):
    for col in range(len(data[0])-WORD_LEN):
      st = ""
      for i in range(WORD_LEN):
        st += data[row-i][col+i]

      s += len(re.findall("XMAS", st)) + len(re.findall("SAMX", st))
  print(s)

  return s

@timeit
def part2(data: list[str]) -> int:
  return
  # return part1([re.split(DONT_REGEX, do, maxsplit=1)[0] for do in re.split(DO_REGEX, _parse_data(data))])

if __name__ == "__main__":
  with open(f"{DIR_2024}/data/day{DAY}.txt") as f:
    data: list[str] = f.readlines()
  
  print(f"part1: {part1(data)}")
  # print(f"part2: {part2(data)}")
