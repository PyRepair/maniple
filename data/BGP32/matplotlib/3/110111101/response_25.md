### Bug Explanation
In the `_recache` function of the `MarkerStyle` class, the bug is related to the `_filled` attribute. It is always initialized as `True`, regardless of the value of `fillstyle` passed to the `MarkerStyle` constructor. This leads to the `is_filled()` method always returning `True`, causing the failing test.

### Bug Fix Strategy
To fix the bug, we need to ensure that the `_filled` attribute reflects the actual fillstyle of the marker. If the `fillstyle` is `'none'`, `_filled` should be set to `False`.

### Corrected Version
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
        self._filled = True

        if self._fillstyle == 'none':
            self._filled = False

        self._marker_function()
``` 

This corrected version includes setting the `_filled` attribute based on the `fillstyle` parameter passed to the `MarkerStyle` constructor. With this adjustment, the failing test `test_marker_fillstyle` should pass successfully.