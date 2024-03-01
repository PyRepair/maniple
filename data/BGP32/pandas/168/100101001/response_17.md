### Bug Explanation:
The bug in the `_get_grouper` function arises from the handling of the `key` parameter when it is passed as a string or a list containing a single string. The function logic does not correctly handle this scenario, leading to a ValueError when trying to create the `Grouping` objects.

When `key` is a string or a list with a single string, it is not processed correctly to create the desired `Grouping` objects. This results in an empty `groupings` list, which causes a ValueError later in the function.

### Bug Fix Strategy:
To fix the bug, we need to ensure that when `key` is a string or a list containing a single string, it is processed correctly to create the `Grouping` objects. We should account for both scenarios and adjust the logic accordingly to correctly populate the `groupings` list.

### Corrected Version of the Function:
```python
def _get_grouper(
    obj,
    key=None,
    axis=0,
    level=None,
    sort=True,
    observed=False,
    mutated=False,
    validate=True,
):
    group_axis = obj._get_axis(axis)

    if level is not None:
        if isinstance(group_axis, MultiIndex):
            if is_list_like(level) and len(level) == 1:
                level = level[0]

            if key is None and is_scalar(level):
                key = group_axis.get_level_values(level)
                level = None
        else:
            if is_list_like(level):
                nlevels = len(level)
                if nlevels == 1:
                    level = level[0]
                elif nlevels == 0:
                    raise ValueError("No group keys passed!")
                else:
                    raise ValueError("multiple levels only valid with MultiIndex")

            if isinstance(level, str):
                if obj.index.name != level:
                    raise ValueError(
                        "level name {} is not the name of the index".format(level)
                    )
            elif not is_scalar(level) or (level != 0 and level != -1):
                raise ValueError("level must be 0 or -1 with a non-MultiIndex")

            level = None
            key = group_axis

    if isinstance(key, Grouper):
        binner, grouper, obj = key._get_grouper(obj, validate=False)
        return grouper, {key.key} if key.key is not None else [], obj

    elif isinstance(key, BaseGrouper):
        return key, [], obj

    if isinstance(key, tuple):
        msg = (
            "Interpreting tuple 'by' as a list of keys, rather than "
            "a single key. Use 'by=[...]' instead of 'by=(...)'. In "
            "the future, a tuple will always mean a single key."
        )
        warnings.warn(msg, FutureWarning, stacklevel=2)
        key = list(key)

    if not isinstance(key, list):
        keys = [key]
    else:
        keys = key

    for i, (gpr, level) in enumerate(zip(keys, [level] * len(keys)):
        if not _is_label_like(gpr):
            try:
                obj._data.items.get_loc(gpr)
            except Exception:
                raise KeyError(gpr)

        if is_categorical_dtype(gpr) and len(gpr) != obj.shape[axis]:
            raise ValueError(
                (
                    "Length of grouper ({len_gpr}) and axis ({len_axis})"
                    " must be the same length".format(
                        len_gpr=len(gpr), len_axis=obj.shape[axis]
                    )
                )
            )

        ping = Grouping(
            group_axis,
            gpr,
            obj=obj,
            name=None if _is_label_like(gpr) else gpr,
            level=level,
            sort=sort,
            observed=observed,
            in_axis=False if _is_label_like(gpr) else True,
        )
        groupings.append(ping)

    if len(groupings) == 0:
        raise ValueError("No group keys passed!")

    grouper = BaseGrouper(group_axis, groupings, sort=sort, mutated=mutated)
    return grouper, [], obj
```

The corrected version of the `_get_grouper` function should now correctly handle the `key` parameter when it is passed as a string or a list containing a single string, ensuring that the `Grouping` objects are created successfully. This fix should resolve the ValueError that was occurring in the buggy function.