### Bug Explanation
The bug in the `_try_convert_to_date` function arises from the fact that it tries to convert boolean values to datetime, which is not a valid operation. The error message `TypeError: <class 'bool'> is not convertible to datetime` indicates that the function is encountering boolean values and trying to convert them to datetime, resulting in an error.

### Bug Fix Strategy
To fix this bug, we need to handle boolean values separately and not try to convert them to datetime. We can modify the function to check the datatype of the input data and handle boolean values differently from other types.

### Corrected Version of the Function
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
        
        if new_data.dtype == "bool":  
            return data, False  # Handling boolean values separately

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

By adding a check for boolean values and returning early with the expected result, we prevent the function from trying to convert boolean values to datetime. This should fix the bug and make the function work correctly for the given test case.