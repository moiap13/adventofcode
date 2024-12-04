from typing import TypeVar, Callable, Any, cast
from functools import wraps
from time import time_ns

F = TypeVar("F", bound=Callable[..., Any])

def timeit(f: F) -> F:
  @wraps(f)
  def inner_func(*arg: Any, **kwargs: Any) -> Any:
    start = time_ns()
    result = f(*arg, **kwargs)
    end = time_ns()
    print(f"function {f.__name__} took {(end-start)/10e6: .2f} ms")
    return result
  return cast(F, inner_func)
