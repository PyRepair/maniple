The bug in the `_try_convert_to_date` function lies in the incorrect handling of boolean arrays. The function wrongly treats boolean arrays as numeric data when converting to datetime, leading to an incorrect conversion of boolean values.

To fix this bug, we need to add an additional condition to correctly handle boolean arrays before attempting to convert to datetime.

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

        # Handle boolean arrays separately
        if new_data.dtype == "bool":
            new_data = new_data.astype("int64")

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

With this corrected version of the function, the provided failing test case should now pass successfully.