### Bug Explanation
The bug in the `table_exists` function arises from a case-sensitivity issue. The function checks if the provided table name exists in the output received from the `run_hive_cmd` function. However, the comparison is case-sensitive, leading to test failures when the table name's case does not match exactly with the one returned by Hive.

In the failing test cases, the function receives 'OK' or 'OK\nmytable' as stdout, but it expects to handle case insensitivity when comparing the table names.

### Fix Strategy
To fix the bug, we need to make the comparison case-insensitive. By converting both the table name and the entries in the stdout to lowercase before comparison, we can ensure that the function behaves correctly for different cases of table names.

### Corrected Version
Below is the corrected version of the `table_exists` function:

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

This corrected version converts both the table name and the output to lowercase for a case-insensitive comparison. This change addresses the issue raised in GitHub related to fixing the case sensitivity in `table_exists` function.