To fix the bug in the `_recache` function in the `MarkerStyle` class, we need to ensure that the `is_filled` method returns the correct value based on the `fillstyle` parameter. Currently, the bug is in the `_recache` function that sets `self._filled` to `True` unconditionally.

### Bug Explanation:
- The `_recache` function sets `self._filled` to `True` regardless of the `fillstyle` parameter being set to `'none'`, causing the `is_filled` method to return `True` incorrectly when it should return `False`.

### Fix Strategy:
- Update the `_recache` function to set `self._filled` based on the `fillstyle` parameter value. If `fillstyle` is set to `'none'`, then `self._filled` should be set to `False`.

### Corrected Version:
```python
class MarkerStyle():

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
        self._filled = self._fillstyle != 'none'
        self._marker_function()
```

By updating the `_recache` function in the `MarkerStyle` class as shown above, the `is_filled` method will now correctly return `False` when the `fillstyle` parameter is set to `'none'`. This correction should resolve the issue reported on GitHub and make the failing test `test_marker_fillstyle` pass as expected.