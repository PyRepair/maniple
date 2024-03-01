The bug in the `_try_convert_to_date` function seems to be related to the handling of boolean data. The function is trying to coerce boolean data into integers, which is causing issues with the conversion to date format. We need to adjust the function to handle boolean data correctly and avoid unnecessary conversions.

Here's a corrected version of the `_try_convert_to_date` function:

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
                | (new_data > self.min_stamp)
                | (new_data._values == iNaT)
            )
            if not in_range.all():
                return data, False

        if new_data.dtype == "bool":
            new_data = new_data.astype("int64")

        date_units = (self.date_unit,) if self.date_unit else self._STAMP_UNITS
        for date_unit in date_units:
            try:
                new_data = to_datetime(new_data, errors="raise", unit=date_unit)
            except (ValueError, OverflowError):
                continue
            return new_data, True

        return data, False
```

This corrected version adds a check to handle boolean data specifically by converting it to integer format before attempting to parse it as a date. This should resolve the issue with boolean data causing the function to return incorrect results.

By making this adjustment, the function should now pass the failing test provided.