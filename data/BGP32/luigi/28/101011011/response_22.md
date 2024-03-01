### Bug Explanation
The bug is caused by the table_exists function not handling case sensitivity properly. In the failing test cases, the expected table names are in mixed case (for example, 'mytable' and 'MyTable'), but the function compares them directly to the names returned from running the hive command, leading to failures due to case differences.

### Bug Fix Strategy
To fix the bug, the table names should be converted to lowercase before comparing them to the output from the hive command. This will make the comparison case-insensitive.

### Corrected Version of the Function
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

By converting both the table name and the output of the command to lowercase before comparison, the function will now correctly handle case-insensitive comparisons, fixing the failing tests.