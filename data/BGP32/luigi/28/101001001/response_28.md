### Bug Explanation
The bug in the `table_exists` function arises from the comparison between the table name and the output of the `run_hive_cmd` function. The comparison `table in stdout` is case-sensitive, so it fails when the case of the table name does not match the case in the output (e.g., `mytable` != `MyTable`). This issue causes the function to return incorrect results.

### Bug Fix
To fix the bug, we can modify the comparison to make it case-insensitive using the `lower()` or `upper()` method on both the table name and the output before comparison.

### Corrected Version

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()  # Case-insensitive comparison
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
``` 

By making the comparison case-insensitive, the corrected function should now provide the correct results for all test cases provided.