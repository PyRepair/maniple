### Bug analysis
The bug in the `table_exists` function is that the comparison logic is incorrect. It checks whether the table name is directly in the `stdout` output, which can cause false positives. The function should check for the exact match of the table name in the lines of the `stdout`.

### Bug explanation
In the failing test case, when checking for the table `"MyTable"`, the function incorrectly returns `True` because it finds `"mytable"` within the `stdout` output. This is a false positive. The function should only return `True` if the exact table name is found in the `stdout`.

### Fix strategy
To fix the bug, we need to modify the comparison logic in the `table_exists` function to check for the exact match of the table name in each line of the `stdout` output.

### Corrected version of the function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and table in stdout.splitlines()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
    
        return bool(stdout)
```