The bug in the `_recache` function is that it initializes `_filled` as `True` regardless of the `fillstyle` set by the user. This leads to markers not appearing hollow even when `fillstyle='none'` is set.

### Cause of the Bug
When `_recache` is called, it sets `_filled` to `True` unconditionally, which overrides any user-set `fillstyle`. This causes markers to always be filled, regardless of the desired appearance.

### Fix Strategy
To fix the bug, we need to check if the `fillstyle` is set to `'none'` and update the `_filled` attribute accordingly. If `fillstyle` is `'full'`, `_filled` should be set to `True`; otherwise, `_filled` should be set to `False`.

### Corrected Version of the Function
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
        if self._fillstyle == 'full':
            self._filled = True
        else:
            self._filled = False
        self._marker_function()
```

By updating the `_filled` attribute based on the `fillstyle` set by the user, the markers will now correctly appear as hollow when `fillstyle='none'` is used.