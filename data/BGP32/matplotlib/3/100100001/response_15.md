## Explanation:
The `_recache` function in the `markers.py` file is responsible for resetting certain attributes of a marker style. The bug in this function is that after resetting the `_transform` attribute to `IdentityTransform()`, it doesn't recache the `_alt_transform` attribute as well.

In the failing test `test_marker_fillstyle()`, the `MarkerStyle` object is created with `fillstyle='none'`, which should result in the marker not being filled. However, due to the bug in the `_recache` function, the `_alt_transform` attribute is not properly reset, causing an issue with the fill style check.

## Fix:
To fix the bug, we need to ensure that the `_alt_transform` attribute is properly reset to `None` in the `_recache` function after resetting the `_transform` attribute. This will align the state of both transform attributes and allow the fill style check in the test to work correctly.

Here is the corrected version of the `_recache` function:

```python
def _recache(self):
    if self._marker_function is None:
        return
    self._path = _empty_path
    self._transform = IdentityTransform()
    self._alt_path = None
    self._alt_transform = None  # Reset _alt_transform to None
    self._snap_threshold = None
    self._joinstyle = 'round'
    self._capstyle = 'butt'
    self._filled = True
    self._marker_function()
```

With this fix, the `_alt_transform` attribute will be properly reset, and the failing test `test_marker_fillstyle()` should now pass.