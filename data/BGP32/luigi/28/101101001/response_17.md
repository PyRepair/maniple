The bug in the `table_exists` function is due to the condition `return stdout and table in stdout`. In the case where `stdout` is "OK", the condition evaluates to True regardless of the value of `table`, causing the function to return True incorrectly. 

To fix this bug, we should check if `table` is in `stdout` only when `stdout` contains table names, not just a status like "OK". We can modify the condition to check if `table` exists in a list of table names extracted from the `stdout`.

Here is the corrected version of the `table_exists` function:

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

This corrected version splits the `stdout` by newline character and checks if `table` exists in the list of table names retrieved from the command output.

By modifying the condition to consider the actual table names present in the `stdout`, the function will now return the correct result in all scenarios, fixing the bug.