```python
import numpy as np
from pandas import to_datetime

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
    if new_data.dtype == "object":
        try:
            new_data = data.astype("int64")
        except (TypeError, ValueError, OverflowError):
            pass
    
    # ignore numbers that are out of range
    if np.issubdtype(new_data.dtype, np.number):
        in_range = (
            np.isnan(new_data._values)
            | (new_data > self.min_stamp)
            | (np.isnat(new_data._values))
        )
        if not np.all(in_range):
            return data, False
    
    date_units = (self.date_unit,) if self.date_unit else self._STAMP_UNITS
    for date_unit in date_units:
        try:
            new_data = to_datetime(new_data, errors="coerce", unit=date_unit)
            # Check if the resulting data contains any NaT values
            if np.any(pd.isnull(new_data)):
                raise ValueError
        except (ValueError, OverflowError):
            continue
        return new_data, True
    
    return data, False
```

Explanation:
1. Import the necessary modules (`numpy` and `pandas`) and functions (`to_datetime`).
2. Replace `issubclass()` with `np.issubdtype()` to check if the `dtype` of `new_data` is a subdtype of `np.number`.
3. Replace `isna()` with `np.isnan()` to check for NaN values in `new_data`.
4. Replace `_values == iNaT` with `np.isnat(_values)` to check for NaT values in `new_data`.
5. Use `pd.isnull()` instead of `isna()` to check for NaT values in `new_data` after applying `to_datetime()`.
6. Modify the `errors` parameter in `to_datetime()` to `"coerce"` to replace non-convertible values with NaT.
7. Add a check to ensure that the resulting `new_data` does not contain any NaT values, and raise a `ValueError` if it does.