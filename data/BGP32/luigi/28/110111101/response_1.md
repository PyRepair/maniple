### Bug Explanation:
The bug in the `table_exists` function lies in the logic when checking if a table exists based on the returned value from `run_hive_cmd`. In the current implementation, the function only checks if the stdout is present or not, but it does not correctly determine if the table name is in the output. This leads to incorrect evaluation of the table existence.

### Bug Location:
The bug is in the conditional statements that handle the stdout from `run_hive_cmd`. The function simply checks if the stdout exists without properly parsing it to check for the table name.

### Bug Fix:
To fix the bug, we need to properly check if the table name exists in the stdout returned by `run_hive_cmd`. We can split the output by newlines and then check if the table name is present in the resulting list.

### Corrected Function:
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

With this correction, the function should now correctly evaluate whether the table exists based on the output from `run_hive_cmd`.