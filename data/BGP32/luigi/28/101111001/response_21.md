### Bug Explanation
The bug in the `table_exists` function lies in the check for the existence of a table in the stdout returned by `run_hive_cmd`. The function checks if the table name is in the stdout, but it doesn't handle cases where the table name is a substring of another table name. This causes the function to incorrectly return a truthy value even when the table doesn't truly exist in the stdout.

### Bug Fix Strategy
To fix the bug, we need to modify the check for the table name in the stdout to ensure an exact match. This can be done by splitting the `stdout` into lines and then checking if any line exactly matches the table name.

### Corrected Version of the `table_exists` function

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

By splitting the `stdout` into lines and checking for an exact match in each line, we ensure that the function accurately determines the existence of the table in the output, fixing the bug.