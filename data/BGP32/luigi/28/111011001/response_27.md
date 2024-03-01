### Bug Explanation
The bug in the `table_exists` function is due to the comparison being done based on the entire `stdout` string instead of checking if the `table` name is present in the `stdout` string when analyzing the return values.

### Bug Fix Strategy
To fix the bug, we need to modify the condition where we check if the `table` name exists in the `stdout` string instead of just comparing the entire string.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return table in stdout  # Fix the condition to check if table is in stdout
        else:
            return False
``` 

### Correction
The bug has been fixed by updating the condition to `return table in stdout` instead of `if stdout:` in the else block, ensuring that the function now correctly checks for the presence of the `table` in the `stdout` string.