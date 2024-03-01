### Analysis:
1. The buggy function `table_exists` checks if a table exists in the specified database by running a Hive command and checking the output against the provided table name. The issue mentioned on GitHub highlights the case sensitivity problem with table names.
2. The bug arises from not considering the case sensitivity of table names. The comparison between the table name and the output of the Hive command is done directly without any case conversion.
3. When the table name is not in lower case in the stdout returned by the Hive command, the comparison fails, leading to incorrect results.
4. To fix the bug, we need to convert both the table name and the stdout to lowercase for a case-insensitive comparison.
5. Below is the corrected version of the `table_exists` function that handles case sensitivity issues.

### Corrected Version:
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

By converting both the table name and the stdout to lowercase before comparison, the corrected function ensures a case-insensitive match, addressing the issue reported on GitHub.