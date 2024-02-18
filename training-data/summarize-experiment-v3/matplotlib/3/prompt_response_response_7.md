## Bug's Cause
The bug likely arises from the unconditional setting of `self._filled` to `True` within the `_recache` function. This leads to the markers being filled even when `fillstyle` is set to 'none'.


## Fixing the Bug
To fix the bug, the `self._filled` attribute should be updated based on the `fillstyle` parameter. If `fillstyle` is set to 'none', `self._filled` should be set to `False` to ensure the markers are hollow when desired.


## Corrected Code
```python
def _recache(self):
    if self._marker_function is None:
        return
    self._path = _empty_path
    self._transform = IdentityTransform()
    self._alt_path = None
    self._alt_transform = None
    self._snap_threshold = float('inf')  # Update to set snap_threshold to infinity
    self._joinstyle = 'round'
    self._capstyle = 'butt'
    
    if self._fillstyle == 'none':
        self._filled = False  # Update to set filled to False for 'none' fillstyle
    else:
        self._filled = True
    
    self._marker_function()
```