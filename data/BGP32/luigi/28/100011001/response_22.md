### Bug Explanation
The buggy function `table_exists` is failing to correctly check if a table exists in the database. The issue arises from the way the function is checking the presence of the table in the output of the `run_hive_cmd` function. The function is checking for the exact presence of the table name in the output, which can lead to false negatives due to differences in whitespace, case sensitivity, or other formatting issues in the output.

### Bug Fix Strategy
To fix this bug, we need to adjust the logic in the `table_exists` function to properly handle the output check. Instead of directly comparing the table name in the output, we should search for the table name in the output, allowing for flexibility in formatting.

### Corrected Function
Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout is not None and any(table in line for line in stdout.split('\n'))
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return stdout is not None
```

In this corrected version:
- We use `any(table in line for line in stdout.split('\n'))` to search for the table name in the output line by line, which allows for flexible matching.
- We return `True` if the table is found in the output and `False` otherwise.