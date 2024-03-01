To fix the bug in the `table_exists` function, we need to make the comparison case-insensitive by converting both the table name and the output from Hive commands to lowercase before comparison. This will ensure that the function works correctly regardless of the case of the table name.

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

Explanation:
1. We modified the return statement in the first block of the function to check if the lowercase version of `table` is in the lowercase version of `stdout`. This makes the comparison case-insensitive.

2. In the second block of the function, we simplified the return statement to directly return the boolean evaluation of `stdout`.

By making these changes, the function now correctly handles table existence checks in a case-insensitive manner and should pass the failing test cases provided. This approach aligns with the GitHub issue #896, which suggests making the `table_exists` function case-insensitive.