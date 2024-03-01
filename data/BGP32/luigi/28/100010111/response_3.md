### Analysis
- The `table_exists` function is supposed to check whether a table exists in Hive.
- The bug occurs because the function does not handle case sensitivity correctly when comparing table names.
- The test cases are failing because the function is not converting the names to lowercase before comparison.
- The GitHub issue #896 specifically mentions making the `table_exists` function case insensitive.

### Bug Fix Strategy
- Modify the function to convert both the table name and the command output to lowercase before comparing.
- This will ensure that the comparison is case insensitive as required.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

The corrected version of the function should pass all the failing test cases and address the issue mentioned in the GitHub discussion.