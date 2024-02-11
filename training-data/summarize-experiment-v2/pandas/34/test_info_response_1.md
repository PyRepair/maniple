The original error message shows an issue with the time bins while running the failing test case.

The functions identified in this error message are several frames, and only the most closely related ones are selected.

The function `_get_time_bins` is called from `pandas/core/resample.py` and raises a TypeError for datetime index checks.

Simplified error message:
```
TypeError: 'axis' must be a DatetimeIndex, but got an instance of which is not a DatetimeIndex
```