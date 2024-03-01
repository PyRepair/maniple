The bug in the `_try_convert_to_date` function is causing the `new_data` variable to not be updated correctly when trying to convert it into a date format. As a result, the function is not returning the expected output.

To fix the bug, we need to ensure that the new_data variable is updated properly after conversion attempts. We also need to handle the case where the data dtype is "object" correctly.

Here is the corrected version of the function:

```python
class Parser():
    def _try_convert_to_date(self, data):
        if not len(data):
            return data, False

        new_data = data
        if new_data.dtype == "object":
            try:
                new_data = pd.to_numeric(new_data, errors='coerce')
            except (ValueError, TypeError):
                pass

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
                new_data = pd.to_datetime(new_data, errors='raise', unit=date_unit)
            except (ValueError, OverflowError):
                continue
            return new_data, True
        return data, False
```

This corrected version handles the object dtype conversion correctly using `pd.to_numeric` and updates the `new_data` variable with the result of conversions.