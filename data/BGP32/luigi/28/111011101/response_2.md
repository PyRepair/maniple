### Bug Explanation
The bug in the `table_exists` function stems from the conditional check on the return value of the `run_hive_cmd` function. The function expects the output from `run_hive_cmd` to contain the table name if it exists. In the failing tests, the return value of `run_hive_cmd` does not match the expected format, leading to incorrect evaluation of table existence.

### Bug Fix Strategy
1. Ensure that the `run_hive_cmd` function returns the expected output format containing the table name.
2. Modify the conditional statements in the `table_exists` function to appropriately handle the response from `run_hive_cmd`.
3. Adjust the logic to correctly determine table existence based on the response from `run_hive_cmd`.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables in {1};'.format(database, table))

        return stdout and table in stdout
    else:
        partition_spec_str = ','.join(['{0}={1}'.format(k, v) for k, v in partition.items()])
        stdout = run_hive_cmd('use {0}; show partitions {1} partition ({2});'.format(database, table, partition_spec_str))

        return bool(stdout) # Directly convert stdout to boolean as it already has the required information
```

By following the steps mentioned above and updating the `table_exists` function as shown, the function should now correctly handle the output from `run_hive_cmd` and determine table existence accurately based on the given input parameters.