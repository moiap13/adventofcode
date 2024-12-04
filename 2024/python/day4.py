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

SEARCHED_WORD_PART_2 = "MAS"
WORD_LEN_PART_2 = len(SEARCHED_WORD_PART_2)-1

def _parse_data(data: list[str]) -> np.ndarray:
  return np.array([list(line.strip()) for line in data])

@timeit
def part1(data: list[str]) -> int:
  def _create_string(loc: tuple[int, int]) -> np.ndarray[str]:
    # we define some constants; r=row, c=column
    r, c = loc
    # The booleans constants defines wichi directions are valid
    verticals_valid_asc: bool = r+(WORD_LEN-1) <= len(data)-1
    verticals_valid_dsc: bool = 0 <= r-(WORD_LEN-1)
    horizontals_valid_asc: bool = c+(WORD_LEN-1) <= len(data[r])-1
    horizontals_valid_dsc: bool = 0 <= c-(WORD_LEN-1)

    horizontals: np.ndarray[str] = np.concatenate((
      np.array(["".join(data[r, c:c-WORD_LEN:-1]) if horizontals_valid_dsc else ""]), # matches for "SAMX"
      np.array(["".join(data[r, c:c+WORD_LEN]) if horizontals_valid_asc else ""])     # matches for "XMAS"
    ))
    
    verticals: np.ndarray[str] = np.concatenate((
      np.array(["".join(data[r:r-WORD_LEN:-1, c]) if verticals_valid_dsc else ""]), # matches for "SAMX"
      np.array(["".join(data[r:r+WORD_LEN, c]) if verticals_valid_asc else ""])     # matches for "XMAS"
    ))

    def _compute_diagonal(loc: tuple[int, int], incrementation: tuple[int, int], iteration: int = 0) -> str:
      if iteration == WORD_LEN:
        return ""
      return data[loc[0], loc[1]] + _compute_diagonal((loc[0]+incrementation[0], loc[1]+incrementation[1]), incrementation, iteration+1)

    diagonals: np.ndarray[str] = np.array([ # same logic as for horizontals and verticals
      _compute_diagonal(loc, (-1, -1)) if verticals_valid_dsc and horizontals_valid_dsc else "", #1  # 1\   /4   
      _compute_diagonal(loc, (1, -1)) if verticals_valid_asc  and horizontals_valid_dsc else"",  #2  #   \ /
                                                                                                     #    X
      _compute_diagonal(loc, (1, 1)) if verticals_valid_asc and horizontals_valid_asc else "",   #3  #   / \
      _compute_diagonal(loc, (-1, 1)) if verticals_valid_dsc and horizontals_valid_asc else ""   #4  # 2/   \3
    ])

    # we concatenante all the string for the directions, this returns an array of 8 string either "XMAS", "SAMX", "[A-Z]{4}", ""
    all_strings: np.ndarray[str] = np.concatenate((horizontals, verticals, diagonals)) 

    # finally we filter by the searched word, this ensure returning an array containing only words "XMAX" or []
    return  all_strings[all_strings == SEARCHED_WORD]
    
  data: list[list[str]] = _parse_data(data)
  x_indices: list[list[int]] = [_find_all(list(line), 'X') for line in data] # this create a list[list[int]] containing the indices of an 'X' position
  # The for each position of an 'X', we check all the possible 'XMAS' (8 at maximum)
  # if there is a least one 'XMAS' we add the length of the number of 'XMAS' ([1; 8]) to the list
  # FInally we sum the length of all matching 'XMAS' for a given 'X'
  return sum([len(subs) for r in range(len(x_indices)) for c in x_indices[r] if len(subs := _create_string((r, c))) > 0])
          
@timeit
def part2(data: list[str]) -> int:
  def _create_string(loc: tuple[int, int]) -> np.ndarray[str]:
    r, c = loc
    verticals_valid: bool = 0 <= r-(WORD_LEN_PART_2-1) < r+(WORD_LEN_PART_2-1) <= len(data)-1
    horizontals_valid: bool = 0 <= c-(WORD_LEN_PART_2-1) < c+(WORD_LEN_PART_2-1) <= len(data[r])-1

    diagonals: np.ndarray[str] = np.array([
      data[loc[0]-1, loc[1]-1] + data[loc[0], loc[1]] + data[loc[0]+1, loc[1]+1],
      data[loc[0]+1, loc[1]-1] + data[loc[0], loc[1]] + data[loc[0]-1, loc[1]+1],
      data[loc[0]+1, loc[1]+1] + data[loc[0], loc[1]] + data[loc[0]-1, loc[1]-1],
      data[loc[0]-1, loc[1]+1] + data[loc[0], loc[1]] + data[loc[0]+1, loc[1]-1],
    ] if verticals_valid and horizontals_valid else np.array([""]))

    return  diagonals[nb_diagonals] if np.sum(nb_diagonals := (diagonals == SEARCHED_WORD_PART_2)) == 2 else np.array([])
  
  data: list[list[str]] = _parse_data(data)
  x_indices: list[list[int]] = [_find_all(list(line), 'A') for line in data]
  return sum([1 for r in range(len(x_indices)) for c in x_indices[r] if len(subs := _create_string((r, c))) > 0])

if __name__ == "__main__":
  with open(f"{DIR_2024}/data/day{DAY}.txt") as f:
    data: list[str] = f.readlines()
  
  print(f"part1: {part1(data)}")
  print(f"part2: {part2(data)}")
