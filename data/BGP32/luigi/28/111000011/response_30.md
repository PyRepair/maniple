## Bug Analysis:
1. The `table_exists` function in the `HiveCommandClient` class is supposed to check if a table exists in the specified database. However, the comparison is case-sensitive, which causes issues when dealing with tables named in different cases.
2. The function uses the output from the `run_hive_cmd` function to check if the table exists, but it directly compares the table name to the output without considering case sensitivity.
3. The GitHub issue highlights the problem of case sensitivity in table name comparisons in Hive, and suggests using `table.lower()` when checking against the output.
4. To fix the bug, we need to convert both the table name and the output to lowercase before comparing them.

## Bug Fix Strategy:
1. Modify the `table_exists` function to convert both the `table` and the `stdout` to lowercase before checking if the table exists.
2. Update the function to check if the lowercase table name is in the lowercase stdout.

## Corrected Version of the Function:
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

By making these changes, the `table_exists` function will now check for the lowercase table name in the lowercase output, making the comparison case-insensitive as requested in the GitHub issue.