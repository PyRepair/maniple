### Bug Explanation
The bug in the `table_exists` function arises from the condition checks in the function. In the first case, when `partition` is `None`, the function checks if the table exists by searching for the table name in the output of the hive command. However, the comparison `table in stdout` doesn't handle case sensitivity correctly. In the second case, when a `partition` is specified, the function constructs a hive command using the `partition_spec` method but doesn't properly handle the result check.

### Bug Fix Strategy
1. Modify the comparison `table in stdout` to handle case sensitivity correctly.
2. Implement a better result check for the case where a partition is specified.

### Corrected Code
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

By updating the code to handle case insensitivity in the table name comparisons and simplifying the result check when a partition is specified, the corrected function should now behave as expected and pass all test cases.