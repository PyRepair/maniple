The bug in the `_recache` function of the `MarkerStyle` class is causing the markers not to appear as hollow even when `fillstyle` is set to `'none'`. The function is setting `_filled` to `True` unconditionally, which is incorrect.

### Cause of the Bug:
The bug is that the `_filled` attribute is always set to `True` in the `_recache` function without considering the `fillstyle`. As a result, the markers are always filled regardless of the `fillstyle` value.

### Strategy for Fixing the Bug:
To fix the bug, we need to ensure that the `_filled` attribute reflects the `fillstyle` value properly. If `fillstyle` is set to `'none'`, `_filled` should be set to `False`.

### Corrected Version of the Function:
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
        
        if self._fillstyle == 'none':
            self._filled = False
        else:
            self._filled = True
        
        self._marker_function()
```

By updating the `_recache` function as shown above, the `MarkerStyle` object will correctly reflect the `fillstyle` setting, ensuring that markers are displayed as hollow when `fillstyle` is set to `'none'`.