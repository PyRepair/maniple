### Bug Explanation
The bug in the `table_exists` function lies in the condition checks after running the `run_hive_cmd`. The function incorrectly returns based on the presence of the `table` string in the stdout rather than exact match, leading to incorrect results. The bug results in failing tests where the function should return `True` but instead returns `False`.

### Bug Fix Strategy
To fix the bug, we need to ensure that the function correctly checks for an exact match of the `table` string in the `stdout` returned from the `run_hive_cmd`. We can achieve this by splitting the `stdout` by newline characters and then checking if the `table` string is in the list of results. This modification will address the incorrect behavior and make the function return the expected results.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        tables = stdout.split('\n')
        return table in tables
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

By making this correction, the function should now pass all the failing test cases and return the expected results.