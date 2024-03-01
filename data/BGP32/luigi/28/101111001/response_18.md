### Bug Explanation
The bug in the `table_exists` function is due to the comparison check on the `stdout` variable. The function expects the `stdout` to contain the table name if it exists. However, the current implementation incorrectly checks if the table name is directly present in `stdout` without considering the formatting of the output returned by `run_hive_cmd`.

In Cases 2 and 4, the `stdout` variable contains the table name along with other text, separated by a newline character. Due to this formatting, the comparison `table in stdout` fails because the entire `stdout` string does not exactly match the table name.

### Bug Fix Strategy
To fix the bug, we need to modify the comparison logic in the `table_exists` function to correctly check if the table name is present in the formatted `stdout` string.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in [line.strip() for line in stdout.split('\n') if line]

    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        return bool(stdout)
```

In the corrected version:
- The `stdout` is split by '\n' to handle multiple lines of output.
- The table name check is modified to look for the table name within the list of stripped lines obtained from splitting the `stdout`.
- For the partitioned case, the function now returns `True` if `stdout` is not empty, indicating that the table exists.