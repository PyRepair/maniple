### Identified Bug:
The bug in the `table_exists` function is that it is not case insensitive when checking if the table exists in Hive. This causes failures when the table names are in different cases (capitalized or lowercase).

### Cause of the Bug:
The bug arises from the comparison of the `table` and the `stdout` without considering case sensitivity. The function checks if the `table` string is present in the `stdout` string without converting them to a common case format (e.g., lowercase) for consistent comparison.

### Strategy for Fixing the Bug:
To fix the bug, we need to ensure that the comparison between the `table` name and the `stdout` result is case insensitive. This can be achieved by converting both strings to a common case format (e.g., lowercase) before comparing them.

### Corrected Version of the Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                                (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

In the corrected version:
- Both `table` and `stdout` strings are converted to lowercase before comparison using `lower()`.
- The comparison now checks if the lowercase version of `table` is in the lowercase version of `stdout`.
- The `bool()` function is used to convert the `stdout` result to a boolean value, ensuring consistency.