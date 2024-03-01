### Bug Explanation
The bug in the `table_exists` function is due to the incorrect comparison logic when checking if the table exists in the output obtained from `run_hive_cmd`. The function expects the table name to be an exact match in the output, while in some cases, it appears within a string containing multiple table names, separated by newline characters.

### Bug Fix Strategy
To fix the bug, we need to adjust the comparison logic to properly handle cases where the table name appears in a multi-line string in the output.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and table in stdout.split("\n")
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                                (%s)""" % (database, table, self.partition_spec(partition)))
    
        if stdout:
            return True
        else:
            return False
```

By splitting the output on newline characters, we can properly check if the table name exists within the returned strings. This correction should address the failing test cases and ensure that the function behaves as expected.