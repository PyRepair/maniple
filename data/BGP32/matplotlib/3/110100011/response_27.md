### Analysis:
- The buggy function `_recache` in the `MarkerStyle` class is responsible for re-calculating the marker style attributes.
- The failing test `test_marker_fillstyle` creates a `MarkerStyle` object with `fillstyle='none'` and checks if the `get_fillstyle` method returns `'none'` and if the marker is not filled.
- The GitHub issue reports that setting `fillstyle='none'` does not result in hollow markers when used with `ax.scatter()`.

### Bug Cause:
- The buggy function `_recache` sets `_filled = True` regardless of the `fillstyle` provided, leading to filled markers.
- The failing test aims to check if setting `fillstyle='none'` results in unfilled markers, but this is not the case due to the bug.

### Fix Strategy:
- Update the implementation in the `_recache` function to consider the `fillstyle` when determining the fill status of the marker.
- Modify the assignment to `_filled` based on the value of `fillstyle`.

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
        self._filled = self.get_fillstyle() != 'none'
        self._marker_function()
```

By updating the `_recache` function to set `_filled` based on the `fillstyle` value, the markers will appear hollow when `fillstyle='none'` is set, resolving the issue reported on GitHub.