The issue seems to be with how the `make_current` argument is being handled in the `initialize` method of the `IOLoop` class. When `make_current` is set to `True`, the function should only make the current `IOLoop` instance if one doesn't already exist. However, the current implementation is not handling this case correctly and is raising a `RuntimeError` even when a current `IOLoop` instance already exists.

To fix this issue, we need to modify the `initialize` method to correctly check for the presence of a current `IOLoop` instance before attempting to make the current instance. Additionally, the check for `make_current is None` also needs to be corrected to handle the case where a current instance already exists.

Here's the corrected code for the `initialize` method:

```python
def initialize(self, make_current=None):
    if make_current is None:
        if IOLoop.current(instance=False) is None:
            self.make_current()
    elif make_current:
        if IOLoop.current(instance=False) is not None:
            raise RuntimeError("current IOLoop already exists")
        self.make_current()
```

This modification ensures that when `make_current` is set to `True`, the function only attempts to make the current `IOLoop` instance if one doesn't already exist. This should fix the issue and make the failing test pass.

With this correction, the updated GitHub issue title and description would be:

## GitHub Issue Title
`IOLoop.initialize` does not handle existing current instance correctly

## Github Issue Description
In the `IOLoop.initialize` method, the check for existing current `IOLoop` instance is not handled correctly when `make_current` is set to `True`, leading to a `RuntimeError` being raised even when a current instance already exists. This needs to be fixed to ensure proper handling of the `make_current` argument.