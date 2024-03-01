### Analysis
The bug occurs in the `_recache` function where the `_filled` attribute is always set to `True`, regardless of the `fillstyle` parameter passed in the `MarkerStyle` constructor. The failing test `test_marker_fillstyle` expects the marker to be hollow (`is_filled` should return `False`), but due to the bug, it always returns `True`. This discrepancy is causing the test to fail.

### Bug Cause
The `_filled` attribute in the `_recache` function is hardcoded to `True`, which is incorrect. It should depend on the value of `fillstyle` provided in the `MarkerStyle` constructor.

### Fix Strategy
1. Modify the `_recache` function to set the `_filled` attribute based on the `fillstyle` parameter.
2. Update the `MarkerStyle` constructor to store the `fillstyle` parameter and use it in the `_recache` function to determine the value of the `_filled` attribute.

### Corrected Version
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
    
    if self.get_fillstyle() == 'none':
        self._filled = False
    else:
        self._filled = True
    self._marker_function()
```

With this correction, the `_filled` attribute will be correctly determined based on the `fillstyle` parameter passed in the `MarkerStyle` constructor, fixing the issue with hollow markers not being displayed correctly.