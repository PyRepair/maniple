To fix the bug in the `_recache` function of the `MarkerStyle` class, we need to address the incorrect behavior related to the `fillstyle` parameter and ensure that markers are displayed as hollow when set to `'none'`.

### Analysis:
The function `_recache` is responsible for resetting several attributes of the `MarkerStyle` object. However, the issue arises when setting the `_filled` attribute to `True` unconditionally, which contradicts the intended behavior specified in the expected cases.

### Bug Cause:
The bug is caused by setting `_filled` to `True` regardless of the `fillstyle` parameter, leading to markers not being displayed as hollow when the `fillstyle` is set to `'none'`.

### Strategy for Fixing the Bug:
1. Update the `_filled` attribute based on the `fillstyle` parameter to correctly reflect whether the markers should be filled or hollow.
2. Ensure that the `_filled` attribute is set to `False` when the `fillstyle` is `'none'`.

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

By updating the `_filled` attribute based on the `fillstyle` parameter in the `_recache` function, the corrected version ensures that markers will be displayed as hollow when `fillstyle` is set to `'none', resolving the issue reported on GitHub.