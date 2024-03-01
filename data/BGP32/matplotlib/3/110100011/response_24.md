### Analysis:
1. The buggy function `_recache` within the `MarkerStyle` class is responsible for re-calculating the marker style attributes.
2. The issue reported on GitHub indicates that setting `fillstyle='none'` is not making the markers hollow as expected when using `ax.scatter()` with a custom `MarkerStyle`.
3. The buggy function `_recache` sets `self._filled = True` unconditionally, which causes the markers to be filled regardless of the `fillstyle` parameter.
   
### Bug Cause:
The bug is caused by the `_recache` function always setting the `_filled` attribute to `True` regardless of the `fillstyle` provided.

### Strategy for Fixing:
To fix the bug, we need to update the `_recache` function to consider the `fillstyle` parameter when determining if the marker should be filled or not.

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
        
        # Update to consider fillstyle when determining if the marker should be filled
        if self._fillstyle == 'full':
            self._filled = True
        else:
            self._filled = False
        
        self._marker_function()
```

By making this change, the `MarkerStyle` will now correctly determine whether the marker should be filled based on the `fillstyle` parameter passed during initialization.