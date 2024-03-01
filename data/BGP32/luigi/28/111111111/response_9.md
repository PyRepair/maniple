Based on the information provided, the bug in the `table_exists` function is that it doesn't account for case sensitivity when checking if a table exists. The function compares the table name directly with the output from Hive without considering case differences, leading to test failures.

To fix this bug, we need to modify the `table_exists` function to perform a case-insensitive check when verifying if the table exists. We can achieve this by converting both the table name and the output from Hive to lowercase before comparison.

Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)  # 'bool' as there was no specific condition in return

```

In this corrected version, the comparison between the table name and the Hive output is done in a case-insensitive manner by converting both to lowercase using `lower()`.

This fix ensures that the function behaves correctly in scenarios where the table names have different cases and aligns with the expected behavior described in the GitHub issue #896.