It seems that the problem is caused by the `raw` parameter not being passed to the `_apply` function correctly. The issue can be fixed by modifying the `_apply` function call inside the `apply` function. Instead of passing `center=False`, we should be passing `raw=raw`. Here's the fixed function:

```python
def apply(
    self,
    func,
    raw: bool = False,
    engine: str = "cython",
    engine_kwargs: Optional[Dict] = None,
    args: Optional[Tuple] = None,
    kwargs: Optional[Dict] = None,
):
    if args is None:
        args = ()
    if kwargs is None:
        kwargs = {}
    kwargs.pop("_level", None)
    kwargs.pop("floor", None)
    window = self._get_window()
    offset = calculate_center_offset(window) if self.center else 0
    if not is_bool(raw):
        raise ValueError("raw parameter must be `True` or `False`")

    if engine == "cython":
        if engine_kwargs is not None:
            raise ValueError("cython engine does not accept engine_kwargs")
        apply_func = self._generate_cython_apply_func(
            args, kwargs, raw, offset, func
        )
    elif engine == "numba":
        if raw is False:
            raise ValueError("raw must be `True` when using the numba engine")
        if func in self._numba_func_cache:
            # Return an already compiled version of roll_apply if available
            apply_func = self._numba_func_cache[func]
        else:
            apply_func = generate_numba_apply_func(
                args, kwargs, func, engine_kwargs
            )
    else:
        raise ValueError("engine must be either 'numba' or 'cython'")

    # Pass raw parameter to the _apply function
    return self._apply(
        apply_func,
        raw=raw,
        floor=0,
        name=func,
        use_numba_cache=engine == "numba",
    )
```

This change should fix the issue without affecting any other tests and can be applied easily to the original project.