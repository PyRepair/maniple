### Bug Explanation
The bug in the `table_exists` function lies in the conditional check in the `if` block. The function is returning the result of `table in stdout` which is incorrect because in some cases `table in stdout` might return `True` even if the table name is not an exact match due to partial string matching.

### Bug Fix Strategy
To fix the bug, we should modify the conditional checks in both branches of the `if` statement to ensure exact table name matching.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        # Check if the exact table name exists in the stdout
        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            # Check if the exact partition exists in the stdout
            return table in stdout.split('\n')
        else:
            return False
```

This corrected version splits the `stdout` string on newline characters before checking if the table name (or partition name) is an exact match. This change ensures that the function returns the correct result based on the exact matching of table and partition names.