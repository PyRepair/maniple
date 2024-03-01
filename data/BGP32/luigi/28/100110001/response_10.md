The bug in the provided `table_exists` function seems to be related to how it checks for the existence of a table under specific conditions. Let's break it down:

1. In the `if partition is None:` block, the function runs a Hive command to check for table existence by matching the table name in the output. However, the logic for checking the existence is incorrect. It should be checking if the table name is anywhere in the `stdout` output, not an exact match. This is why the test fails when the mock return value is `"OK\nmytable"`, as it expects an exact match.

2. In the `else:` block, the function runs a different Hive command to check for table existence when there is a partition specified. It checks if the `stdout` exists, but it should be checking for the presence of the actual partition in the `stdout` instead of just testing for its truthiness.

To fix the bug:
- For the `if partition is None:` block:
  - Update the condition to check if the table name is in the `stdout` output.
- For the `else:` block:
  - Check if the specific partition exists in the `stdout` output.

Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        return partition in stdout
```

This corrected version should address the issues identified and pass the failing test cases.