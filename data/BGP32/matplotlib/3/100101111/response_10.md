### Analysis
1. The `_recache` function is called by the `MarkerStyle` class to reset certain properties, including `_filled`.
2. The bug lies in the fact that `_filled` is always set to `True` regardless of the `fillstyle` parameter passed to `MarkerStyle`.
3. This bug is causing markers to always appear filled, even when the intention is to have them hollow.
4. To fix the bug, we need to update the assignment of `_filled` based on the `fillstyle` parameter.

### Update the `_recache` function
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
    if self._fillstyle and self._fillstyle.lower() == 'none':
        self._filled = False
    else:
        self._filled = True
        
    self._marker_function()
```

By updating the `_filled` property based on the `fillstyle` parameter passed to `MarkerStyle`, the markers will now appear hollow when the `fillstyle` is set to `'none'`.

This fix addresses the issue reported on GitHub, where the markers were not appearing hollow when `fillstyle` was set to `'none'`.