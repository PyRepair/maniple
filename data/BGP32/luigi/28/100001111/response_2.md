The bug in the `table_exists` function is related to case sensitivity when checking if a table exists in Hive. The function is currently comparing the table name provided with the output from Hive without considering case differences, leading to test failures when tables are named differently in terms of case.

Here's a summary of the bug and its potential fix:
- The function should perform a case-insensitive comparison between the table name and the tables listed in the Hive output.
- The fix involves converting both the table name and the tables listed in the output to lowercase before comparison.

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in map(str.lower, stdout.split())
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

This corrected version of the function ensures that both the table name and the tables listed in the Hive output are treated in a case-insensitive manner, addressing the issue reported on GitHub.