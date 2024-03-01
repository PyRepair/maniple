## Analysis:
The issue reported on GitHub indicates that setting the `fillstyle='none'` in `markers.MarkerStyle` does not result in hollow markers when using `ax.scatter()`. This indicates a potential issue with the `_recache` function in the `markers.py` file, where the `_filled` attribute is always set to `True` regardless of the `fillstyle` specified in `MarkerStyle`.

## Identified Error Location:
The `_filled` attribute in the `_recache` function is always set to `True`, which may be causing the markers to be filled even when `fillstyle='none'` is specified.

## Cause of the Bug:
The bug is caused by the `_filled` attribute being set to `True` by default in the `_recache` function. This overrides the `fillstyle='none'` parameter set in `markers.MarkerStyle`, resulting in filled markers instead of hollow ones.

## Suggested Fix:
To fix the bug, the `_filled` attribute should be set based on the `fillstyle` parameter provided in `MarkerStyle`. If `fillstyle='none'`, then `_filled` should be set to `False`.

## Corrected Version:
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
    self._filled = self.get_fillstyle() != 'none'  # Check fillstyle to determine if filled
    self._marker_function()
    
    def get_fillstyle(self):
        if hasattr(self, '_fillstyle'):
            return self._fillstyle
        else:
            return ''
```

By updating the `_recache` function to check the `fillstyle` provided in `MarkerStyle` and setting the `_filled` attribute accordingly, the issue reported on GitHub should be resolved. The added method `get_fillstyle` helps access the `fillstyle` parameter correctly.