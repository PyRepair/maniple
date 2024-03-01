### Bug Explanation:
The bug in the `table_exists` function lies in the condition checking logic. In the current implementation, the function checks for the presence of the table name in the output of a Hive command to determine if the table exists. However, the function fails to handle cases where the table name might be part of a larger string due to the way the input is processed.

### Bug Fix Strategy:
To fix the bug, the function should check if the exact table name exists in the output of the Hive command instead of just checking if it is present in the string. This can be achieved by splitting the output string by newlines and then checking for an exact match.

### Corrected Version of the Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout.split("\n")
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

By splitting the stdout by newlines and then checking for an exact match, the corrected function will correctly identify if the table exists in the Hive database and pass the failing test cases.