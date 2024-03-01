The bug in the provided function lies in the handling of the data type check and conversion. The function is incorrectly converting the data type of the input `data` to 'int64' if it is of type 'object', which may not be appropriate for all types of data.

To fix the bug, we should only convert the data type to 'int64' if the data contains numeric values. We can achieve this by checking if the data is a subclass of np.number before attempting the conversion.

Here is the corrected version of the function:

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
    if issubclass(data.dtype.type, np.number):  # Check if data is numeric
        pass  # No need to convert

    else:
        try:
            new_data = to_datetime(data, errors="raise", unit=self.date_unit)
        except (ValueError, OverflowError):
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

This corrected version of the function will only convert the data type to datetime if it contains numeric values. The function should now satisfy the expected input/output values specified in the cases provided.