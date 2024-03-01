The bug in the provided `astype_nansafe` function occurs when handling the case where the input array (`arr`) contains NaN values and needs to be converted to an integer. The function is not properly checking for NaN values before attempting the conversion, leading to potential errors.

To fix this bug, we need to add a check for NaN values in the input array before attempting to convert it to an integer. If any NaN values are present, we should raise a `ValueError` with an appropriate message.

Here is the corrected version of the `astype_nansafe` function:

```python
def astype_nansafe(arr, dtype, copy=True, skipna=False):
    """
    Cast the elements of an array to a given dtype a nan-safe manner.

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
        Cannot convert NaN values to integer.
    """

    if np.isnan(arr).any():
        raise ValueError("Cannot convert NaN values to integer")

    # rest of the function remains the same
```

With this modification, the function will now properly check for NaN values in the input array before converting it to an integer. This fix should resolve the issue with the failing test case.