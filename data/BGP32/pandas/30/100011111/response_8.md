### Bug Explanation
The bug occurs in the `_try_convert_to_date` function when trying to convert boolean values to datetime using the `to_datetime` function. The error message `TypeError: <class 'bool'> is not convertible to datetime` is raised because the function is attempting to convert boolean values to datetime, which is not a valid operation. This bug is triggered when using `read_json` with `typ="series"` on a JSON list containing boolean values. 

### Bug Fix Strategy
To fix the bug, we need to make sure that when the input data contains boolean values, the function does not attempt to convert them to datetime. We should identify boolean values and return them as they are in a Series without any conversion to datetime.

### Corrected Function
```python
def _try_convert_to_date(self, data):
    if not len(data):
        return data, False
    
    if data.dtype == "object":
        try:
            new_data = data.astype("int64")
        except (TypeError, ValueError, OverflowError):
            pass
    else:
        new_data = data
    
    # Perform conversion for non-boolean values
    if issubclass(new_data.dtype.type, np.number):
        in_range = (
            isna(new_data._values)
            | (new_data > self.min_stamp)
            | (new_data._values == iNaT)
        )
        if not in_range.all():
            return data, False

    # Skip datetime conversion for boolean values
    if new_data.dtype == 'bool':
        return new_data, False

    date_units = (self.date_unit,) if self.date_unit else self._STAMP_UNITS
    for date_unit in date_units:
        try:
            new_data = to_datetime(new_data, errors="raise", unit=date_unit)
        except (ValueError, OverflowError):
            continue
        return new_data, True
    
    return data, False
```

After applying this fix, the function will correctly handle boolean values and avoid trying to convert them to datetime, resolving the TypeError issue.