### Bug Explanation:

The bug arises when trying to convert a categorical series containing NaN values to an integer dtype. The current implementation of the `astype_nansafe` function fails to handle NaN values correctly during this conversion, resulting in unexpected negative integers instead of NaN.

### Bug Location:

The error likely stems from the following block of code:
```python
if np.issubdtype(arr.dtype, np.floating) and np.issubdtype(dtype, np.integer):
    if not np.isfinite(arr).all():
        raise ValueError("Cannot convert non-finite values (NA or inf) to integer")
```
The issue is that the condition checks for floating dtype and integer dtype, but it does not account for handling NaN values when converting to integers.

### Bug Fix Strategy:

To fix the bug, we need to modify the condition that checks for floating dtype and integer dtype, adding a check to handle NaN values appropriately during the conversion. We should update this block of code to include a check for NaN values before converting to integers.

### Corrected Version:

Here is the corrected version of the `astype_nansafe` function:

```python
def astype_nansafe(arr, dtype, copy: bool = True, skipna: bool = False):
    """
    Cast the elements of an array to a given dtype in a nan-safe manner.
    
    Parameters
    ----------
    arr : ndarray
    dtype : np.dtype
    copy : bool, default True
        If False, a view will be attempted but may fail if the item sizes don't align.
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
    
    elif is_datetime64_dtype(arr):
        if is_object_dtype(dtype):
            return tslib.ints_to_pydatetime(arr.view(np.int64))
        elif dtype == np.int64:
            return arr.view(dtype)
        
        # allow frequency conversions
        if dtype.kind == "M":
            return arr.astype(dtype)
        
        raise TypeError(f"cannot astype a datetimelike from [{arr.dtype}] to [{dtype}]")
    
    elif is_timedelta64_dtype(arr):
        if is_object_dtype(dtype):
            return tslibs.ints_to_pytimedelta(arr.view(np.int64))
        elif dtype == np.int64:
            return arr.view(dtype)
        
        if dtype not in [_INT64_DTYPE, _TD_DTYPE]:
            
            # handle NaN values during conversion
            if np.isnan(arr).any():
                return arr.astype(dtype)
            
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
        # handle NaN values properly during conversion
        if np.isnan(arr).any():
            return arr.astype(dtype)
        
        if not np.isfinite(arr).all():
            raise ValueError("Cannot convert non-finite values (NA or inf) to integer")
    
    if is_object_dtype(arr):
        
        # work around NumPy brokenness, #1987
        if np.issubdtype(dtype.type, np.integer):
            return lib.astype_intsafe(arr.ravel(), dtype).reshape(arr.shape)
        
        # if we have a datetime/timedelta array of objects
        # then coerce to a proper dtype and recall astype_nansafe
        
        elif is_datetime64_dtype(dtype):
            from pandas import to_datetime
            
            return astype_nansafe(to_datetime(arr).values, dtype, copy=copy)
        elif is_timedelta64_dtype(dtype):
            from pandas import to_timedelta
            
            return astype_nansafe(to_timedelta(arr).values, dtype, copy=copy)
    
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

By incorporating the check for NaN values before converting to integers, the corrected version of the function should now handle the conversion of categorical series containing NaN values to integer dtypes correctly.