### Bug Explanation
The bug in the `table_exists` function lies in the incorrect condition check for the presence of the table in the `stdout`. In the first part, the function checks if the `table` is in the stdout, but it should actually check if the `table` string is in the `stdout` string. In the second part, the function checks if the `stdout` is not empty, which is incorrect. The condition should check if the `table` is in the `stdout`.

### Bug Fix Strategy
- In the first part of the function, modify the condition to check if the `table` string is in the `stdout` string.
- In the second part of the function, modify the condition to check if the `table` string is in the `stdout` string.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))

        return stdout and table in stdout
```