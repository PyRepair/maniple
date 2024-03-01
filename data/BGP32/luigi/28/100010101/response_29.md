### Bug Explanation
The bug in the `table_exists` function lies in the condition checks and the comparison of the stdout output with the expected table name. In the first part of the function, when partition is None, the function checks if the table name is contained in the stdout. However, it should check for the table name alone without any surrounding text which might be present in the stdout. In the second part, when partition is not None, the function checks if the stdout is not empty as an indicator of existence, which is not correct.

### Bug Fix Strategy
1. In the first section where `partition is None`, we need to modify the condition to check if the exact table name exists in stdout without any additional text.
2. In the second section where `partition is not None`, we can directly return the boolean value of `stdout` instead of using conditional checks.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout.split()

    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

By making the above changes, the function will check for the exact table name in stdout without any extra text and properly return the existence based on the stdout emptiness.