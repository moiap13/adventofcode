import os
from functools import reduce
import numpy as np

# Set print options to display the full array
np.set_printoptions(threshold=np.inf)

from _decorators import timeit
from _utils import _find_all

DIR_2024 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DAY = 6

def _parse_data(data: list[str]) -> np.ndarray:
  return np.array([list(line.strip()) for line in data])

@timeit
def part1(data: list[str]) -> int:
  orientation = 0
  data_map: np.ndarray = _parse_data(data)
  y, x = map(lambda a: a[0], np.where(data_map == "^"))
  c = 0
  while True:
    match orientation % 4:
      case 0:
        res = np.where(data_map[y-1::-1, x] == "#")
        if res[0].shape[0] == 0:
          data_map[y::-1, x] = "X"
        else:
          data_map[y:y-res[0][0]-1:-1, x] = "X"
          y -= res[0][0]
      case 1:
        res = np.where(data_map[y, x+1:] == "#")
        if res[0].shape[0] == 0:
          data_map[y, x+1:] = "X"
        else:
          data_map[y, x+1:x+res[0][0]+1] = "X"
          x += res[0][0]
      case 2:
        res = np.where(data_map[y+1:, x] == "#")
        if res[0].shape[0] == 0:
          data_map[y+1::, x] = "X"
        else:
          data_map[y+1:y+res[0][0]+1, x] = "X"
          y += res[0][0]
      case 3:
        res = np.where(data_map[y, x-1::-1] == "#")
        if res[0].shape[0] == 0:
          data_map[y, x-1::-1] = "X"
        else:
          data_map[y, x-1:x-res[0][0]-1:-1] = "X"
          x -= res[0][0]

    if res[0].shape[0] == 0:
      break

    orientation += 1
  return (data_map == "X").sum()

 


@timeit
def part2(data: list[str]) -> int:
  return

if __name__ == "__main__":
  with open(f"{DIR_2024}/data/day{DAY}.txt") as f:
    data: list[str] = f.readlines()
  
  print(f"part1: {part1(data)}")
  # print(f"part2: {part2(data)}")
