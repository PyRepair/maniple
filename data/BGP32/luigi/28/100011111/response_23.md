### Bug analysis:
The bug in the `table_exists` function arises from a case sensitivity issue when comparing the table name with the output from the `run_hive_cmd`. The function does not handle the case where the table names are provided with different capitalizations, leading to failing tests.

### Bug location:
The bug is located in the comparison between the `table` variable and the `stdout` variable before returning the result. The comparison should be case insensitive to address the failing tests.

### Bug explanation:
The failing tests reveal that when the table name and the output from `run_hive_cmd` do not match due to case differences, the function returns incorrect results. The function currently performs a direct case-sensitive comparison between the `table` name and `stdout`, leading to False negatives in table existence checks.

### Bug fix strategy:
To address the case sensitivity issue, update the comparison between the `table` name and the `stdout` output to be case insensitive. This adjustment will ensure that the function correctly identifies table existence regardless of the capitalization of the table names.

### Corrected function:
Here is the corrected version of the `table_exists` function:

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

By comparing the lowercase versions of the `table` name and `stdout`, the table existence check becomes case insensitive, fixing the failing tests reported.