After analyzing the provided code and test, it is evident that the issue lies in the `_recache` method of the `MarkerStyle` class. The problem arises from the fact that the `is_filled` method does not correctly reflect the state of the `fillstyle` parameter. 

Here's the cause of the bug:
- The `_recache` method of the `MarkerStyle` class sets the `_filled` attribute to `True` regardless of the `fillstyle` parameter value.
- The `is_filled` method checks the `_filled` attribute, leading to a mismatch when `fillstyle` is set to `'none'`.
- This mismatch causes the failing test as `is_filled` incorrectly returns `True` when it should return `False` for the 'none' fillstyle.

To fix the bug, we need to update the `_filled` attribute based on the `fillstyle` parameter value. This will ensure that the `is_filled` method accurately reflects the `'none'` fillstyle.

Here is the corrected version of the `_recache` method in the `MarkerStyle` class:

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

By updating the `_filled` attribute based on the `fillstyle` parameter value, the `is_filled` method will now return the correct value according to the fillstyle set. This correction should address the failing test scenario and resolve the issue reported on GitHub regarding markers not being hollow.