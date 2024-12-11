import os
import re
from functools import reduce
import numpy as np

from _decorators import timeit
from _utils import _find_all

DIR_2024 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DAY = 5

def _parse_data(data: list[str]) -> tuple[dict[int, set[int]], list[list[str]]]:
  idx: int = data.index("\n")
  por: list[tuple[str, str]] = [tuple(map(int, line.strip().split('|'))) for line in data[:idx]]
  return reduce(lambda pv, cv: pv | {cv[0]: pv.get(cv[0], set()) | {cv[1]}}, por, {}), [list(map(int, line.strip().split(","))) for line in data[idx+1:]]

def _traverse_update(adjancy_dict: dict[str, set[str]], update: list[str]) -> bool:
    if len(update) <= 1:
      return True

    curr, next = update[0], update[1]
    try:
      if next in adjancy_dict[curr]:
        return _traverse_update(adjancy_dict, update[1:])
    except KeyError:
      return False
    return False

@timeit
def part1(data: list[str]) -> int:
  adjancy_dict, updates = _parse_data(data)
  return sum([int(update[len(update)//2]) for update in updates if _traverse_update(adjancy_dict, update)])

@timeit
def part2(data: list[str]) -> int:
  from copy import deepcopy
  adjancy_dict, updates = _parse_data(data)

  # def _topological_sort(graph: dict[int, set[int]], node: int, sorted_nodes: list[int]):
  #   """
  #   Explanation: https://www.youtube.com/watch?v=7J3GadLzydI
  #   """
  #   print(node)
  #   if node in sorted_nodes:
  #     return sorted_nodes
    
  #   for n, nei in graph.items():
  #     nei -= {node}
    
  #   for nei in graph.get(node, []):
  #     sorted_nodes += _topological_sort(deepcopy(graph), nei, sorted_nodes.copy())
    
  #   sorted_nodes.append(node)
  #   return sorted_nodes
  

  def topological_sort(graph: dict[int, set[int]]) -> list[int]:
    """
    Topologically sorts the entire graph.
    
    Parameters:
        graph (dict[int, set[int]]): A dictionary where keys are nodes, and values are sets of neighboring nodes.
    
    Returns:
        list[int]: A topologically sorted list of nodes.
    """
    def _topological_sort(graph: dict[int, set[int]], node: int, visited: set[int], sorted_nodes: list[int]):
      """
      Perform a topological sort on the graph starting from the given node.
      
      Parameters:
          graph (dict[int, set[int]]): A dictionary where keys are nodes, and values are sets of neighboring nodes.
          node (int): The current node to process.
          visited (set[int]): A set to track visited nodes.
          sorted_nodes (list[int]): The list to store the sorted nodes.
      
      Returns:
          list[int]: A topologically sorted list of nodes.
      """
      if node in visited:
          return sorted_nodes
      
      visited.add(node)  # Mark the node as visited
      
      # Process all neighbors of the current node
      for neighbor in graph.get(node, []):
          _topological_sort(graph, neighbor, visited, sorted_nodes)
      
      # Add the current node to the sorted list (post-order)
      sorted_nodes.append(node)
      return sorted_nodes
    visited = set()
    sorted_nodes = []
    
    # Perform topological sort for each unvisited node in the graph
    for node in graph:
        if node not in visited:
            _topological_sort(graph, node, visited, sorted_nodes)
    
    return sorted_nodes[::-1]  # Reverse for correct topological order
  sorted_nodes = topological_sort(deepcopy(adjancy_dict))
  return sum([int(corrected_update[len(corrected_update)//2]) for corrected_update in [[s for s in sorted_nodes if update.count(s) > 0] for update in updates if not _traverse_update(adjancy_dict, update)]])


if __name__ == "__main__":
  with open(f"{DIR_2024}/data/day{DAY}.txt") as f:
    data: list[str] = f.readlines()
  
  print(f"part1: {part1(data)}")
  print(f"part2: {part2(data)}")
