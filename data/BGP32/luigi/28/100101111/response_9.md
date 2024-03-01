To fix the bug in the `table_exists` function, we need to make the comparison between the table name and the table names retrieved from the Hive command case-insensitive. This will ensure that the function correctly identifies existing tables regardless of the case of the table name.

Here is the corrected version of the `table_exists` function:

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

Explanation:
- In the corrected version, we convert both the `table` name and the table names retrieved from Hive to lowercase using the `lower()` method before comparison. This ensures that the comparison is case-insensitive.
- By splitting the `stdout` by newline characters (`\n`) and then mapping each value to lowercase, we can handle cases where multiple table names are returned.
- This modification addresses the issue reported in GitHub and makes the `table_exists` function case-insensitive for table name comparisons.

The corrected version of the function should now pass the failing test cases and satisfy the expected input/output values.