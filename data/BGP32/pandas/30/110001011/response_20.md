### Analysis:
1. The `self._try_convert_to_date` function is converting data to date columns by checking if it's in epoch/iso formats or integers/floats in epoch formats.
2. The bug is causing incorrect behavior when trying to convert bool values to datetime, leading to exceptions instead of returning a Series of bools.
3. The function is erroneously attempting to convert boolean values to datetime without proper handling, which results in an exception due to the mismatch in data types.
4. To fix the bug, we need to handle boolean data separately and ensure that it is not passed to the `to_datetime` function.

### Bug Fix:
Here is the corrected version of the `_try_convert_to_date` function:

```python
def _try_convert_to_date(self, data):
    """
    Try to parse a ndarray like into a date column.

    Try to coerce object in epoch/iso formats and integer/float in epoch
    formats. Return a boolean if parsing was successful.
    """
    if not len(data):
        return data, False

    new_data = data
    if new_data.dtype == "object":
        try:
            new_data = data.astype("int64")
        except (TypeError, ValueError, OverflowError):
            pass

    if not issubclass(new_data.dtype.type, np.number):
        return data, False

    if np.issubdtype(new_data.dtype, np.bool_):
        return data, False

    in_range = (
        isna(new_data._values)
        | (new_data > self.min_stamp)
        | (new_data._values == iNaT)
    )
    
    if not in_range.all():
        return data, False

    date_units = (self.date_unit,) if self.date_unit else self._STAMP_UNITS
    for date_unit in date_units:
        try:
            new_data = to_datetime(new_data, errors="raise", unit=date_unit)
        except (ValueError, OverflowError):
            continue
        return new_data, True
    return data, False
```

This fix includes a check to handle boolean data separately from the numeric data, preventing it from being passed to the `to_datetime` function and causing an error.