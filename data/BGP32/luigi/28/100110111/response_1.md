### Bug Analysis
The buggy function `table_exists` in `luigi/contrib/hive.py` is failing the test due to case sensitivity when checking if a table exists. The function should be case insensitive to match the table name with the one returned by Hive, considering that Hive is case insensitive.

The failing test `test_table_exists` in `test/contrib/hive_test.py` is checking the behavior of the `table_exists` function with different table names, including a case where the table name is capitalized. The function is expected to return `True` if the table exists, regardless of the case.

The expected input/output values provided for the failing test cases demonstrate the need for case insensitivity in the comparison between the table name and the one returned by Hive.

The GitHub issue #896 raised the problem and suggested a solution to make the `table_exists` function case insensitive.

### Bug Fix Strategy
To fix the bug, we need to implement case insensitivity in the comparison between the table name and the one returned by Hive. We should convert both names to lowercase before comparing them. This approach will resolve the case sensitivity issue and ensure that the function behaves correctly in all scenarios.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table.lower()))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table.lower(), self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

### Summary
The corrected version of the `table_exists` function implements case insensitivity by converting both the table name and the one returned by Hive to lowercase before comparison. This modification ensures that the function passes the failing test cases where the table names vary in their case. By following the bug fix strategy and making the function case insensitive, we address the issue reported in GitHub and ensure the correct behavior of the `table_exists` function.