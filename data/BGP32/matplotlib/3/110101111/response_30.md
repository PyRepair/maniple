## Bug Explanation:

The bug in the `_recache` function of the `MarkerStyle` class is related to the setting of the `_filled` attribute. In the provided code, the `_filled` attribute is always set to `True` unconditionally, regardless of the `fillstyle` specified during the creation of the `MarkerStyle` object. This causes the marker to always be filled, even when `fillstyle='none'` is expected.

## Bug Fix Strategy:

To fix the bug, we need to ensure that the `_filled` attribute is set based on the `fillstyle` specified when creating the `MarkerStyle` object. If `fillstyle` is 'none', then `_filled` should be set to `False`, indicating that the marker should not be filled.

## Corrected Version:

```python
class MarkerStyle:
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
        self._filled = True if self._fillstyle != 'none' else False
        self._marker_function()
```

With this correction, the `_filled` attribute will be set based on the `fillstyle` parameter provided when creating the `MarkerStyle` object. It will correctly reflect whether the marker should be filled or not. This change will resolve the issue where markers are not hollow when `ax.scatter()` is used with `fillstyle='none'`.