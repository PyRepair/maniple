### Analysis:
1. The buggy function `table_exists` in `luigi/contrib/hive.py` has a bug that causes it to be case-sensitive when checking if a table exists in Hive.
2. The failing test `test_table_exists` in `test/contrib/hive_test.py` checks the behavior of the `table_exists` function with different input scenarios.
3. The error message indicates that in the test case where `table = 'MyTable'`, the function is returning `False` instead of `True`.
4. The cause of the bug is that the function does not handle case sensitivity when comparing the table name in the output of the Hive command.
5. To fix the bug, we need to compare the lowercase version of the table name with the lowercase version of the output from the Hive command.

### Bug Fix:
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

### Updated Expected Values:
- Expected case 2: The function will now correctly detect that `'MyTable'` exists in the Hive table list.
- Expected case 5: The updated function will handle case insensitivity correctly for table names like `'MyTable'`.

### GitHub Issue:
The provided bug fix addresses the issue reported in GitHub, making the `table_exists` function case insensitive as requested in GitHub issue #896.