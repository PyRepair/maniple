### Bug Explanation
The bug occurs because the `_try_convert_to_date` function incorrectly treats boolean values as if they were numeric or datetime values. This leads to an unintended conversion attempt that causes errors when dealing with boolean data in the case of `typ="series"`.

### Bug Fix Strategy
To fix the bug, we need to handle boolean values differently from numeric or datetime values. We should ensure that boolean values are directly converted to the correct type without any unnecessary conversion attempts.

### Corrected Version of the Function
Here is the corrected version of the `_try_convert_to_date` function:

```python
def _try_convert_to_date(self, data):
    """
    Try to parse a ndarray like into a date column.

    Try to coerce object in epoch/iso formats and integer/float in epoch
    formats. Return a boolean if parsing was successful.
    """
    # no conversion on empty
    if not len(data):
        return data, False

    new_data = data
    if new_data.dtype == "object":
        try:
            new_data = data.astype("int64")
        except (TypeError, ValueError, OverflowError):
            pass
    
    if new_data.dtype == "bool":
        return new_data, True
    
    # ignore numbers that are out of range
    if issubclass(new_data.dtype.type, np.number):
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

This corrected version now explicitly handles boolean values and returns them without attempting any unnecessary conversions. This fix should resolve the issue reported on GitHub and pass the failing test case provided.