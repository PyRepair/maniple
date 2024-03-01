The bug in the provided function is that it incorrectly returns the original data array even when the date conversion is successful. This leads to incorrect output values in the expected cases.

The strategy to fix this bug is to properly update the 'data' variable with the converted date values when the conversion is successful, and then return the updated 'data' along with a boolean flag indicating the success of the conversion.

Here is the corrected version of the function:

```python
class Parser():

    def _try_convert_to_date(self, data):
        if not len(data):
            return data, False
        
        new_data = data.copy()
        if new_data.dtype == "object":
            try:
                new_data = new_data.astype("int64")
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
        
        date_units = (self.date_unit,) if self.date_unit else self._STAMP_UNITS
        for date_unit in date_units:
            try:
                new_data = to_datetime(new_data, errors="raise", unit=date_unit)
            except (ValueError, OverflowError):
                continue
            return new_data, True

        return data, False
```

This corrected version properly updates the 'data' variable with the converted date values when the conversion is successful, and returns the updated 'data' along with the boolean flag indicating the success of the conversion.