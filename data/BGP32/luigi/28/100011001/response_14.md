### Bug Explanation:

The bug in the `table_exists` function lies in the conditional checks for the presence of the table in the `stdout` variable after running the Hive commands. The bug occurs because the function checks if the table is in the `stdout` string as a whole, which may lead to incorrect results when the table name is a substring of another table name in the `stdout`. For example, in Case 2, when checking for the table `'MyTable'`, the function incorrectly returns `False` because it finds `'MyTable'` as part of the string `"OK\nmytable"`, which contains `'mytable'`.

### Bug Fix Strategy:

To fix the bug, we need to improve the logic of checking whether the table exists in the Hive command output accurately. One possible solution is to split the `stdout` string into lines and then check if any line exactly matches the table name we are looking for.

### Corrected Function:

```python
# The relative path of the corrected file: luigi/contrib/hive.py

def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        if stdout:
            return any(line.strip() == table for line in stdout.split('\n'))
        else:
            return False
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

By splitting the `stdout` string into lines and checking for an exact match with the table name in each line, we ensure that the function accurately detects the presence of the table in the output. This correction should address the bug and make the `table_exists` function behave as expected.