import os

from _decorators import timeit

DIR_2024 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DAY = 2

def _parse_data(data: list[str]) -> list[list[int]]:
  return [[int(i) for i in line.strip().split()] for line in data]

def validate_level(level: list[int]) -> bool:
  direction: int = int(level[0] < level[1])*2 - 1
  return all([(1 <= direction*(level[i+1]-v) <= 3) for i, v in enumerate(level[:-1])])

def split_levels(level: list[int]) -> list[list[int]]:
  return [level[:i]+level[i+1:] for i in range(1, len(level))] + [level[1:]]

@timeit
def part1(data: list[str]) -> int:
  return sum([validate_level(levels) for levels in _parse_data(data)])

@timeit
def part2(data: list[str]) -> int:
  valid_paths: list[bool] = [validate_level(levels) for levels in _parse_data(data)]
  return sum(valid_paths) + sum([any([validate_level(splitted_level) for splitted_level in split_levels(level)]) for i, level in enumerate(_parse_data(data)) if not valid_paths[i]])

if __name__ == "__main__":
  with open(f"{DIR_2024}/data/day{DAY}.txt") as f:
    data: list[str] = f.readlines()
  
  print(f"part1: {part1(data)}")
  print(f"part2: {part2(data)}")
