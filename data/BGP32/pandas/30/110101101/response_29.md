### Bug Explanation
The current implementation of the `_try_convert_to_date` function fails when trying to convert boolean values to datetime. The function incorrectly treats boolean values as numbers and attempts to convert them to integers, which is unnecessary and causes the function to return the input data without converting it to datetime.

### Bug Fix Strategy
To fix the bug, we need to check the data type of the input `data` correctly and handle boolean values as a separate case to convert them to datetime. 

### Corrected Version of the Function
```python
def _try_convert_to_date(self, data):
    """
    Try to parse a ndarray like into a date column.

    Try to coerce object in epoch/iso formats and integer/float in epoch
    formats. Return a boolean if parsing was successful.
    """
    if not len(data):
        return data, False

    if data.dtype == "bool":
        new_data = data.astype("int64")
    else:
        new_data = data

    if issubclass(new_data.dtype.type, np.number):
        in_range = (
            isna(new_data)
            | (new_data > self.min_stamp)
            | (new_data == iNaT)
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

This corrected version of the function checks if the input data is of boolean type and converts it to integers before attempting to convert it to datetime. This will resolve the issue with boolean values and ensure the function can handle them correctly.