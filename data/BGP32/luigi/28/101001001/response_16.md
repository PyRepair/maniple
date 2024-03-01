### Bug Explanation
The bug in the `table_exists` function is due to the comparison of the table name with the output of the `run_hive_cmd` function in the case where the table name is part of the output but not the exact match. Since the condition `table in stdout` is used for checking table existence, it fails when the table name is present in the output along with other text (such as `'OK\nmytable'`). This causes incorrect outcomes and leads to the function incorrectly determining table existence.

### Bug Fix
To fix the bug in the `table_exists` function, we need to modify the condition that checks for table existence. Instead of a simple string inclusion check, we should split the output on newlines and check if the table name exists in any of the lines.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and any(t.strip() == table for t in stdout.split('\n'))
    else:
        stdout = run_hive_cmd(
            """use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
``` 

With this change, the function now correctly checks if the exact table name is present in any of the lines returned by the `run_hive_cmd` function, ensuring a more accurate determination of table existence.