import os
import re
from functools import reduce

from _decorators import timeit

DIR_2024 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DAY = 3
MUL_REGEX = re.compile(r"mul\([0-9]{1,3},[0-9]{1,3}\)")
NUM_REGEX = re.compile(r"\d{1,3}")
DONT_REGEX = re.compile(r"don't\(\)")
DO_REGEX = re.compile(r"do\(\)")

def _parse_data(data: list[str]) -> str:
  return reduce(lambda pv, cv: pv + cv.replace("\n", ""), data, "")

def _mul(a: int, b: int) -> int:
  return a * b
@timeit
def part1(data: list[str]) -> int:
  return sum([_mul(*[int(i) for i in re.findall(NUM_REGEX, mul)]) for mul in re.findall(MUL_REGEX, _parse_data(data))])

@timeit
def part2(data: list[str]) -> int:
  return part1([re.split(DONT_REGEX, do)[0] for do in re.split(DO_REGEX, _parse_data(data))])

if __name__ == "__main__":
  with open(f"{DIR_2024}/data/day{DAY}.txt") as f:
    data: list[str] = f.readlines()
  
  print(f"part1: {part1(data)}")
  print(f"part2: {part2(data)}")