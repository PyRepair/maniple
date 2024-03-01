### Potential Error Location
The potential error lies in how the function checks for the presence of the table in the output received from the `run_hive_cmd`. The function is currently checking whether the table name is directly in the entire output string, which may cause issues if the table name is part of a larger string or if there are additional characters present.

### Bug Explanation
The function `table_exists` in `luigi/contrib/hive.py` is not correctly handling the output received from the `run_hive_cmd` function. It expects the table name to be directly in the output string, which can lead to false positives or negatives.

For instance, in the failing test case where `table_exists("MyTable")` is called, the function expects a direct match in the output string, leading to incorrect results.

### Bug Fix Strategy
1. Modify the function to properly parse the output received from `run_hive_cmd` and check if the table name exists as a separate entity in the output.
2. Use a more robust method to extract the table name from the `stdout` variable before checking if it exists.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout.strip() == table
    else:
        table_exists_query = 'use {0}; show tables like "{1}";'.format(database, table)
        table_partition_spec = self.partition_spec(partition)
        partition_query = "show partitions {0} partition ({1})".format(table, table_partition_spec)

        stdout = run_hive_cmd(table_exists_query)
        if table in stdout:
            partition_output = run_hive_cmd(partition_query)
            return table in partition_output
        
        return False
```

This corrected version of the `table_exists` function properly handles the output received from `run_hive_cmd` and ensures that the table name is checked in a more reliable way, both for the table existence and partition query cases.