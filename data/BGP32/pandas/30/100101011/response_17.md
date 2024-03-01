### Potential Error Locations:
1. The conversion of data to `int64` within the `if new_data.dtype == "object"` block might not handle boolean values correctly.
2. The check for numbers out of range in the block following the dtype check may not work as intended.
3. The attempt to convert data to datetime within the loop might not be handling boolean values appropriately.

### Cause of the Bug:
The bug seems to stem from the incorrect handling of boolean values during conversion to `int64` and subsequent conversion to datetime. This causes the function to return unexpected results when dealing with boolean data leading to the failing test.

### Bug Fix Strategy:
1. Handle boolean values explicitly in the dtype conversion step.
2. Adjust the logic for checking numbers out of range to handle boolean values correctly.
3. Ensure that boolean values are appropriately converted to datetime.

### Corrected Version of the Function:
```python
def _try_convert_to_date(self, data):
    if not len(data):
        return data, False

    new_data = data
    if new_data.dtype == "object":
        try:
            # Explicitly handle boolean values by converting to int64 without errors being raised
            new_data = data.astype("int64", errors="ignore")
        except (TypeError, ValueError, OverflowError):
            pass

    # Ignore boolean values in numbers out of range check
    if issubclass(new_data.dtype.type, np.number) and not new_data.dtype == np.bool_:
        in_range = (
            isna(new_data._values)
            | (new_data > self.min_stamp)
            | (new_data._values == iNaT)
        )
        if not in_range.all():
            return data, False

    for date_unit in (self.date_unit,) if self.date_unit else self._STAMP_UNITS:
        try:
            if new_data.dtype == np.bool_:
                # Convert boolean values to datetime
                new_data = new_data.map({False: '1970-01-01', True: '1970-01-01'})
            else:
                new_data = to_datetime(new_data, errors="raise", unit=date_unit)
        except (ValueError, OverflowError):
            continue
        return new_data, True
    return data, False
```

By explicitly handling boolean values during conversion and adjusting the logic for numbers out of range check, the corrected function should now handle boolean data correctly and pass the failing test mentioned in the GitHub issue.