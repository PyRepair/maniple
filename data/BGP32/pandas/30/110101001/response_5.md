### Explanation:
The bug in the `_try_convert_to_date` function is causing it to return the original `data` instead of the converted `new_data`. This is due to the incorrect logic flow within the function that is not updating the `new_data` variable properly after conversion attempts.

1. The function first checks if the input `data` is empty, if not, it attempts to convert it to `int64` dtype if it is of object type.
2. Then it checks if the dtype of `new_data` is a number, and if not all values are in range, it returns the original `data` without updating `new_data`.
3. Finally, it attempts to convert `new_data` to datetime using different units but returns the original `data` if it fails.

The issue lies in how `new_data` is handled and updated throughout the function, leading to the incorrect output being returned.

### Strategy for fixing the bug:
To fix this bug, we need to ensure that `new_data` is correctly updated after each conversion attempt, and if the conversion is successful, return the updated `new_data`. 

### Corrected version of the function:
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
            new_data = new_data.astype("int64")
        except (TypeError, ValueError, OverflowError):
            pass

    # ignore numbers that are out of range
    if issubclass(new_data.dtype.type, np.number):
        in_range = (
            isna(new_data._values)
            | (new_data > self.min_stamp)
            | (new_data._values == iNaT)
        )
        if not in_range.all():
            return new_data, False

    date_units = (self.date_unit,) if self.date_unit else self._STAMP_UNITS
    for date_unit in date_units:
        try:
            converted_data = to_datetime(new_data, errors="raise", unit=date_unit)
            return converted_data, True
        except (ValueError, OverflowError):
            continue
    return new_data, False
```

In this corrected version:
- We correctly update `new_data` after conversion attempts.
- If a conversion is successful, we return the updated `new_data`.
- This will ensure that the function returns the converted data when successful.