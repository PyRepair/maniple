### Analysis:
The buggy function `table_exists` is failing to correctly handle the condition where the `partition` parameter is provided. It seems to be constructing the Hive command incorrectly when `partition` is not None.

The issue arises from the incorrect formatting of the Hive command when `partition` is provided, causing the function to always return `False` when it should be returning `True` if a matching partition is found.

### Bug:
When the `partition` parameter is not None, the Hive command being constructed in the `else` block is not correctly formatted. This leads to incorrect processing and the function always returning `False`.

### Fix:
1. Correctly format the Hive command within the `else` block to handle the case when the `partition` parameter is provided.
2. Update the return statement within the `else` block to return `True` if `stdout` is not empty.

### Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use {0}; show partitions {1} partition 
                            ({2})""".format(database, table, self.partition_spec(partition)))

        return stdout is not None
``` 

By fixing the Hive command formatting and updating the return statement, the corrected version should now properly handle the case when the `partition` parameter is provided, returning `True` if a matching partition is found.