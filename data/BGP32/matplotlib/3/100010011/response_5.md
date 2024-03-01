## Analysis:
The `_recache` function is setting `self._filled` to `True` irrespective of the `fillstyle` value, which causes the markers to be filled when the `fillstyle` is set to 'none'. This leads to the failing test where `assert not marker_style.is_filled()` fails since the `filled` property is True.

## Bug Cause:
The bug is caused by the `_recache` function not correctly handling the `fillstyle` parameter when determining whether the marker should be filled or not.

## Fix Strategy:
To fix the bug, we need to modify the `_recache` function to correctly handle the `fillstyle` parameter and set the `_filled` property accordingly.

## The corrected version of the function:

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
    
    if self.get_fillstyle() == 'none':
        self._filled = False
    else:
        self._filled = True
    
    self._marker_function()
```

By checking the `fillstyle` value in the `_recache` function and setting the `_filled` property accordingly, the corrected version addresses the bug where markers were not hollow when `fillstyle` was set to 'none'.