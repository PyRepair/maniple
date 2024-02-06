```python
def _unstack_multiple(data, clocs, fill_value=None):
    if len(clocs) == 0:
        return data

    # NOTE: This doesn't deal with hierarchical columns yet

    index = data.index

    if isinstance(index, MultiIndex):
        clocs = [index._get_level_number(level) for level in clocs]

        # Rest of the code remains unchanged

        return unstacked
    else:
        return data.unstack(clocs, fill_value=fill_value)
```