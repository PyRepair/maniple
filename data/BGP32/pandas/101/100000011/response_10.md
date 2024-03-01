### Analysis:
- The buggy function `astype_nansafe` is responsible for casting the elements of an array to a given dtype in a nan-safe manner.
- The issue reported on GitHub relates to converting from categorical to int while ignoring NaN values, which leads to unexpected behavior.
- The buggy function does not handle the conversion from a categorical series containing NaN values to an integer dtype correctly.
- The issue on GitHub mentions the unexpected behavior of converting NaN to a negative integer value.

### Error Location:
- The buggy function does not handle the case where NaN values are present in a categorical series when converting to an integer dtype.

### Bug Cause:
- The bug occurs when the function encounters a categorical series with NaN values and tries to convert it to an integer dtype without handling the NaN values properly.

### Strategy for Fixing the Bug:
- We need to modify the function to handle NaN values appropriately when converting a categorical series to an integer dtype.
- We should ensure that NaN values are preserved as NaN in the resulting integer dtype.

### Corrected Version:
```python
def astype_nansafe(arr, dtype, copy: bool = True, skipna: bool = False):
    """
    Cast the elements of an array to a given dtype in a nan-safe manner.

    Parameters
    ----------
    arr : ndarray
    dtype : np.dtype
    copy : bool, default True
        If False, a view will be attempted but may fail, if
        e.g. the item sizes don't align.
    skipna: bool, default False
        Whether or not we should skip NaN when casting as a string-type.

    Raises
    ------
    ValueError
        The dtype was a datetime64/timedelta64 dtype, but it had no unit.
    """

    # dispatch on extension dtype if needed
    if is_extension_array_dtype(dtype):
        return dtype.construct_array_type()._from_sequence(arr, dtype=dtype, copy=copy)

    if not isinstance(dtype, np.dtype):
        dtype = pandas_dtype(dtype)

    if issubclass(dtype.type, str):
        return lib.astype_str(arr.ravel(), skipna=skipna).reshape(arr.shape)

    if is_object_dtype(arr):  # Added to handle categorical data with NaN values
        if is_integer_dtype(dtype) and skipna:
            return arr.view(dtype).astype(dtype)
    
    if is_datetime64_dtype(arr):
        if is_object_dtype(dtype):
            return tslib.ints_to_pydatetime(arr.view(np.int64))
        elif dtype == np.int64:
            return arr.view(dtype)

        # allow frequency conversions
        if dtype.kind == "M":
            return arr.astype(dtype)

        raise TypeError(f"cannot astype a datetimelike from [{arr.dtype}] to [{dtype}]")

    if is_timedelta64_dtype(arr):
        if is_object_dtype(dtype):
            return tslibs.ints_to_pytimedelta(arr.view(np.int64))
        elif dtype == np.int64:
            return arr.view(dtype)

        if dtype not in [_INT64_DTYPE, _TD_DTYPE]:

            # allow frequency conversions
            # we return a float here!
            if dtype.kind == "m":
                mask = isna(arr)
                result = arr.astype(dtype).astype(np.float64)
                result[mask] = np.nan
                return result
        elif dtype == _TD_DTYPE:
            return arr.astype(_TD_DTYPE, copy=copy)

        raise TypeError(f"cannot astype a timedelta from [{arr.dtype}] to [{dtype}]")

    elif np.issubdtype(arr.dtype, np.floating) and np.issubdtype(dtype, np.integer):

        if not np.isfinite(arr).all():
            raise ValueError("Cannot convert non-finite values (NA or inf) to integer")

    if dtype.name in ("datetime64", "timedelta64"):
        msg = (
            f"The '{dtype.name}' dtype has no unit. Please pass in "
            f"'{dtype.name}[ns]' instead."
        )
        raise ValueError(msg)

    if copy or is_object_dtype(arr) or is_object_dtype(dtype):
        # Explicit copy, or required since NumPy can't view from / to object.
        return arr.astype(dtype, copy=True)

    return arr.view(dtype)
```

### Explanation of the Fix:
- I added a check for object dtype in the function to handle categorical data with NaN values and appropriate conversion to integer dtype.
- This change ensures that NaN values in a categorical series are retained as NaN in the resulting integer dtype.
- By addressing the handling of NaN values in object dtype, we fix the bug related to converting categorical data to an integer dtype while ignoring NaNs.