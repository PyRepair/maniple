The issue is likely with the `MarkerStyle` class, specifically with the `is_filled` method which is not returning the correct value. This is evident in the error message `assert not True`.

The bug occurs because the `_recache` function is always setting `self._filled` to `True`, which is incorrect. The correct behavior should depend on the value of `fillstyle` in the `MarkerStyle` object. Therefore, the approach to fixing the bug is to modify the `_recache` function to take into account the `fillstyle` attribute of the `MarkerStyle` object and set `self._filled` accordingly.

The corrected code for the `_recache` function is as follows:

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
    if self._fillstyle == 'none':
        self._filled = False
    else:
        self._filled = True
    self._marker_function()
```

By checking the `fillstyle` attribute of the `MarkerStyle` object in the `_recache` function, we can set the `self._filled` attribute to `True` or `False` accordingly. This should resolve the issue with markers not being hollow when `fillstyle` is set to 'none'.

Replacing the original `_recache` function with the corrected version should fix the bug.