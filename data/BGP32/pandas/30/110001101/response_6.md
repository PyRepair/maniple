The bug in the function `_try_convert_to_date` lies in the logic where it checks if the values are within range for converting to datetime. The function incorrectly checks the condition `new_data > self.min_stamp` instead of `new_data < self.min_stamp` to determine if the values are within range. Additionally, the function needs to handle boolean type data appropriately to avoid the ValueError when converting it to int64.

To fix the bug, we need to update the logic to check if the values are less than `self.min_stamp` and also handle boolean data types appropriately.

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
        elif new_data.dtype == "bool":
            new_data = new_data.astype("int64")

        if issubclass(new_data.dtype.type, np.number):
            in_range = (
                isna(new_data._values)
                | (new_data < self.min_stamp)
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

This correction ensures that boolean data is appropriately handled and the values are checked against the correct threshold for conversion to datetime.