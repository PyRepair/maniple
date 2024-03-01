### Buggy Function Analysis
The buggy function `table_exists` is intended to check if a table exists in a given database. It uses the `run_hive_cmd` function to execute a Hive command and analyze the result. The bug seems to be related to how the function processes the output of the Hive command.

### Bug Location
The bug is likely in the comparison logic where the function checks if the table name exists in the output of the Hive command.

### Bug Cause
The bug occurs because the function incorrectly checks for the table name within the entire output string returned by the `run_hive_cmd` function. It does not handle the case where the table name is a substring of a larger string in the output.

### Fix Strategy
To fix the bug, we need to modify the comparison logic to search for the exact presence of the table name within the output string. This can be achieved by spliting the output string into lines and then checking if the table name is present in any of those lines.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        if stdout:
            return any(table == line.strip() for line in stdout.split('\n'))
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

With this correction, the function checks each line of the Hive command output individually, ensuring that it only returns `True` if the exact table name is found in one of the lines. This should fix the bug and make the failing tests pass.