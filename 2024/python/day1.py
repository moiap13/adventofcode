import os
from functools import reduce

DIR_2024 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _parse_data(data: list[str]) -> tuple[tuple[int], tuple[int]]:
  return zip(*[(int(parts[0]), int(parts[1])) for line in data if (parts := line.strip().split("   "))])

def part1(data: list[str]) -> int:
  l, r = _parse_data(data)
  return sum([abs(t[0]-t[1]) for t in zip(sorted(l), sorted(r))])

def part2(data: list[str]) -> int:
  l, r = _parse_data(data)
  r_counts: dict[int, int] = reduce(lambda pv, cv: pv | {cv: pv.get(cv, 0) + 1}, r, {})
  return sum([li * r_counts.get(li, 0) for li in l])

if __name__ == "__main__":
  with open(f"{DIR_2024}/data/day1.txt") as f:
    data: list[str] = f.readlines()

  print(f"part1: {part1(data)}")
  print(f"part2: {part2(data)}")