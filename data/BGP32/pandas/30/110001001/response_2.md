## Bug Explanation
The bug in the `_try_convert_to_date` function arises from not properly handling the conversion of data that is already in the correct format to datetime. In this case, the function checks if the data is in the object datatype and tries to convert it to int64, even if it is already in the correct format. This unnecessary conversion can lead to incorrect results and the function returning the original data instead of converting it to a datetime object.

## Bug Fix
To fix the bug, we should first check if the data is already in a numeric type before attempting any conversion. If the data is already in the correct format, we can skip the conversion step and directly try to convert it to a datetime object. Here is the corrected version of the `_try_convert_to_date` function:

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

    if issubclass(data.dtype.type, np.number):
        in_range = (
            isna(data._values)
            | (data > self.min_stamp)
            | (data._values == iNaT)
        )
        if not in_range.all():
            return data, False
    else:
        new_data = data
        if new_data.dtype == "object":
            try:
                new_data = data.astype("int64")
            except (TypeError, ValueError, OverflowError):
                pass

    date_units = (self.date_unit,) if self.date_unit else self._STAMP_UNITS
    for date_unit in date_units:
        try:
            new_data = to_datetime(new_data, errors="raise", unit=date_unit)
        except (ValueError, OverflowError):
            continue
        return new_data, True
    return data, False
```

With this fix, we first check if the data is already of a numeric type before attempting any conversion. This ensures that unnecessary conversions are avoided and only the necessary conversions are performed, leading to correct results.