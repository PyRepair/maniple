### Bug Explanation
The buggy function `table_exists` has a bug where it compares the table name directly to the output from Hive without considering case sensitivity. This causes an issue when the table names are in different cases, resulting in failed tests.

### Bug Fix Strategy
To fix the bug, it is necessary to make the comparison case-insensitive. This can be achieved by converting both the table name and the output from Hive to lowercase before the comparison.

### Corrected Function
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

This corrected function converts both the table name and the output from Hive to lowercase before doing the comparison, making it case-insensitive.