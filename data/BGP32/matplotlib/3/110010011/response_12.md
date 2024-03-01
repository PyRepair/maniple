### Analysis:
1. The buggy function `_recache` in the `MarkerStyle` class is responsible for setting various attributes when called, including `_filled` which determines whether the marker is filled or not.
2. The failing test is checking whether `is_filled` method returns `False` when `fillstyle='none'` is set.
3. The error message shows that the `is_filled` method is returning `True` instead of `False`, indicating that the marker is being filled even when `fillstyle='none'` is set.
4. The GitHub issue also confirms the problem where setting `fillstyle='none'` does not result in hollow markers when using `ax.scatter`.
   
### Bug Cause:
The bug is caused by not updating the `_filled` attribute of `MarkerStyle` appropriately based on the `fillstyle` parameter. The `_filled` attribute is always set to `True`, leading to filled markers instead of hollow ones when using `fillstyle='none'`.

### Fix Strategy:
To fix the bug, we need to update the `_recache` function to correctly set the `_filled` attribute based on the `fillstyle` parameter value. This will ensure that hollow markers are displayed when `fillstyle='none'` is set.

### Corrected Version:
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
        
        if self._fillstyle in ['full', 'left', 'right']:
            self._filled = True
        else:
            self._filled = False
        
        self._marker_function()
```

By updating the `_recache` function to consider the `fillstyle` parameter, we ensure that the `_filled` attribute is correctly set to `False` when `fillstyle='none'`. This will fix the bug and make the markers hollow as expected.