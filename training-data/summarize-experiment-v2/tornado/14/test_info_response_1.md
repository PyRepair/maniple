The provided error message is a stack trace.
- The failing test function `test_force_current` is trying to create a new `IOLoop` instance with `make_current=True`.
- The stack trace shows that the until that raises the exception is inside the `initialize` function in the `tornado/ioloop.py` file, and more specifically, it indicates that the exception is being raised in `tornado/ioloop.py` at line 253.
- The original error message is: `RuntimeError: current IOLoop already exists`.

Simplified error message:
```
Error: current IOLoop already exists
```