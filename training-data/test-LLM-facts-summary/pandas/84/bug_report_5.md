# Problem:

The `_unstack_multiple` function is intended to unstack a multi-indexed DataFrame, but it fails to handle the unstacking operation when tuple names are present in the MultiIndex. This results in a `KeyError` exception, specifically `'Level A not found`.

# Root Cause:

The issue lies in the `_unstack_multiple` function's inability to handle tuple names in the MultiIndex while unstacking. During the unstacking process, it tries to retrieve the level number of the specified level in the MultiIndex. However, it fails to recognize the tuple name and raises a `KeyError`.

# Suggested Solution:

The `_unstack_multiple` function needs to be modified to handle tuple names in a MultiIndex correctly. Specifically, the function should be updated to handle the scenario where the level to be unstacked is specified using a tuple name.

The `._get_level_number` method implementation in the `pandas.core.indexes.multi` module, which is called by the `_unstack_multiple` function to retrieve the level number, should also be reviewed and updated if necessary to handle tuple names correctly.

This fix will ensure that the unstacking operation can handle MultiIndexed DataFrames with tuple names, avoiding the `KeyError` exception.