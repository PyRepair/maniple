The issue arises from the `_recache` method of the `MarkerStyle` class. When the `fillstyle` is set to `'none'`, the `_filled` attribute should be False, indicating that the marker should not be filled. However, in the current implementation, it always sets `_filled` to True, resulting in the markers not being hollow as expected.

To address this issue, we need to update the `_filled` attribute based on the `fillstyle` parameter. If the `fillstyle` is set to `'none'`, then `_filled` should be False, and if it is set to any other value (indicating filled marker), then `_filled` should be True.

Here's the corrected version of the `_recache` method of the `MarkerStyle` class:

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
    
    # Update _filled based on fillstyle
    if self._fillstyle == 'none':
        self._filled = False
    else:
        self._filled = True
    
    self._marker_function()
```

By incorporating the logic to update the `_filled` attribute based on the `fillstyle`, we ensure that the markers will be hollow when `fillstyle` is set to `'none'`, addressing the bug.