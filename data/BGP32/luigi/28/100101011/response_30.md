The buggy function `table_exists` in the `luigi/contrib/hive.py` file is failing due to case sensitivity when checking for table existence in the Hive database. The function compares the table name directly with the output from Hive, leading to test failures when the case of the table name does not match exactly with the output.

### Bug Explanation:
1. The function compares the table name without considering case sensitivity, leading to inconsistencies when checking for table existence.
2. The failing test cases expect case insensitivity in table name comparison, causing the tests to fail.
3. The GitHub issue highlighted this problem and suggested a fix to make the comparison case insensitive.

### Fix Strategy:
To resolve the bug, we need to modify the function to compare the table name in a case-insensitive manner with the output obtained from Hive. This way, the function will correctly determine the existence of the table regardless of the case used in the input table name.

### Corrected Version:
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

In the corrected version, we modify the comparison to check if the lowercase version of the table name is present in the lowercase version of the output obtained from Hive. This ensures a case-insensitive comparison for determining table existence.

By implementing this change, the `table_exists` function should now pass the failing test cases, resolving the issue reported on GitHub related to case sensitivity in table name comparison.