To fix the bug in the `_recache` function of the `MarkerStyle` class, we need to address the issue where the `_filled` attribute is always set to `True`. The expected behavior is to set `_filled` to `False` when the `fillstyle` is set to `'none'`.

The cause of the bug is that the `_filled` attribute is always set to `True` regardless of the `fillstyle` parameter value. This leads to markers not being hollow when `fillstyle='none'` is specified.

To fix this bug, we need to modify the `_recache` function to check the `fillstyle` attribute and set the `_filled` attribute accordingly.

Here is the corrected version of the `_recache` function:
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

By adding the conditional check for the `fillstyle` attribute, we ensure that the `_filled` attribute is set correctly based on the specified `fillstyle`. This modification resolves the issue where markers are not hollow when `fillstyle='none'` is used.