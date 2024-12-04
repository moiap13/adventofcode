from typing import Any, Iterable

def flatten_list(l: list[list[Any]]) -> list[Any]:
  return [item for sublist in l for item in sublist]

def _find_all(iter: Iterable[Any] = [], searched_obj: str = "", start_idx: int = 0) -> list[int]:
  try:
    idx = iter.index(searched_obj, start_idx)
  except:
    return []

  return [idx] + _find_all(iter, searched_obj, idx+1)

if __name__ == "__main__":
  print(flatten_list([[1, 2], [3, 4]]))
  print(_find_all([1, 2, 3, 4, 5, 3], 1))