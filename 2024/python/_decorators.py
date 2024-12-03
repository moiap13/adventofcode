from functools import wraps
from time import time_ns

def timeit(f):
  @wraps(f)
  def inner_func(*arg, **kwargs):
    start = time_ns()
    result = f(*arg, **kwargs)
    end = time_ns()
    print(f"function {f.__name__} took {(end-start)/10e6: .2f} ms")
    return result
  return inner_func