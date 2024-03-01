To fix the bug in the `_try_convert_to_date` function, we need to address the issue where the function incorrectly returns the original data without converting it to date when it should. This could happen if the `new_data` dtype is not an object type but the function still needs to convert it to a date. 

The strategy for fixing the bug is to first check if the `new_data` dtype is not an object type and then proceed with the conversion to a date column using the specified date units.

Here is the corrected version of the `_try_convert_to_date` function:

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

        date_units = (self.date_unit,) if self.date_unit else self._STAMP_UNITS
        if new_data.dtype != "object":  # Added check for dtype not being object
            for date_unit in date_units:
                try:
                    new_data = to_datetime(new_data, errors="raise", unit=date_unit)
                    return new_data, True
                except (ValueError, OverflowError):
                    continue

        return new_data, False
```

This corrected version of the function now properly checks if the `new_data` dtype is not an object type before attempting to convert it to a date using the specified date units.