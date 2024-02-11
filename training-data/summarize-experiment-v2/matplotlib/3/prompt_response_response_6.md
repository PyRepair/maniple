The problem in the `MarkerStyle` class is with the `is_filled` method not returning the expected value. Looking at the `_recache` method, it calls `self._marker_function()` regardless of the `self._filled` attribute. This is why the `is_filled()` method returns `True` when it should be returning `False` after setting `fillstyle='none'`.

To fix the bug, we need to update the `_recache` method to only call `self._marker_function()` if `self._filled` is `True`. Here's the corrected code for the `_recache` method:

```python
def _recache(self):
    if self._marker_function is None:
        return
    self._path = _empty_path
    self._transform = IdentityTransform()
    self._alt_path = None
    self._alt_transform = None
    self._snap_threshold = None
    self._joinstyle = 'round'
    self._capstyle = 'butt'
    if self._filled:
        self._marker_function()
```

This change ensures that `_marker_function` is only called when `self._filled` is `True`, which aligns with the expected behavior when `fillstyle='none'`.

After making this change, the failing test should pass, and the issue reported on GitHub should be resolved.