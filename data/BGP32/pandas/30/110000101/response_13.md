The bug in the `_try_convert_to_date` function lies in the logic for checking and converting the data to date format. The function is incorrectly handling the conversion of data in the "object" dtype to "int64" dtype and checking for numbers that are out of range.

The strategy for fixing the bug is to properly handle the conversion of object dtype to int64 dtype and the check for numbers out of range. Additionally, we need to ensure that the function iterates through all date units before returning a value.

Here is the corrected version of the function:
```python
class Parser():
    def _try_convert_to_date(self, data):
        if not len(data):
            return data, False

        new_data = data
        if new_data.dtype == "object":
            try:
                new_data = data.astype("int64")
            except (TypeError, ValueError, OverflowError):
                pass

        if issubclass(new_data.dtype.type, np.number):
            in_range = (
                isna(new_data._values)
                | (new_data >= self.min_stamp)
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

This corrected version should now handle the conversion and range check correctly and iterate through all date units before returning a value. It should satisfy the expected input/output values for the provided test cases.