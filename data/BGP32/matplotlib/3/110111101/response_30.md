### Analysis:
The `_recache` method in the `MarkerStyle` class is not correctly updating the `_filled` attribute based on the value of `_fillstyle`. This leads to the failing test where `assert not marker_style.is_filled()` is failing because `_filled` is not being set to `False` when `fillstyle='none'`.

### Bug:
The bug in the code is that the `_filled` attribute is always set to `True` regardless of the value of `fillstyle`.

### Fix:
Update the `_recache` method to evaluate the value of `_fillstyle` and set `_filled` accordingly.

### Corrected code:
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
```