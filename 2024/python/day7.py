import os
from typing import Callable
import numpy as np

# Set print options to display the full array
np.set_printoptions(threshold=np.inf)

from _decorators import timeit
from _utils import _find_all

DIR_2024 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DAY = 7

def _parse_data(data: list[str]) -> list[tuple[int, tuple[int]]]:
  return [(int(parts[0]), tuple([int(n) for n in parts[1].strip().split()])) for line in data if (parts := line.strip().split(":"))]

def _add(a: int, b: int) -> int: return a + b
def _mul(a: int, b: int) -> int: return a * b
def _concat(a: int, b: int) -> int: return int(str(a) + str(b))

def _traverse_numbers(numbers: tuple[int], target: int, current: int, op: Callable, ops: list[Callable]) -> bool:
  if (new_val := op(current, numbers[0])) == target and len(numbers) == 1:
    return True
  
  if new_val > target:
    return False

  if len(numbers) == 1:
    return False
  
  return any([_traverse_numbers(numbers[1:], target, new_val, op, ops) for op in ops])

@timeit
def part1(data: list[str]) -> int:
  ops: list[Callable] = [_add, _mul]
  return sum([
    target for target, numbers in _parse_data(data) 
    if any([_traverse_numbers(numbers[1:], target, numbers[0], op, ops) for op in ops])
  ])

@timeit
def part2(data: list[str]) -> int:
  ops: list[Callable] = [_add, _mul, _concat]
  return sum([
    target for target, numbers in _parse_data(data) 
    if any([_traverse_numbers(numbers[1:], target, numbers[0], op, ops) for op in ops])
  ])

if __name__ == "__main__":
  with open(f"{DIR_2024}/data/day{DAY}.txt") as f:
    data: list[str] = f.readlines()
  
  print(f"part1: {part1(data)}")
  print(f"part2: {part2(data)}")
