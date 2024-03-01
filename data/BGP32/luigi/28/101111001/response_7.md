### Bug Explanation:
The bug in the `table_exists` function is related to how the function checks for the existence of a table in Hive. The function makes a call to `run_hive_cmd` with the appropriate query to either show tables or show partitions based on whether a partition is specified. However, the function incorrectly checks the output of `run_hive_cmd` for table existence.

In the current implementation:
1. When checking for a table without partitions, the function checks if the table name is in the stdout, which may lead to false positives if the table name is a substring of another table name in the list.
2. When checking for a table with partitions, the function only checks if the stdout exists, leading to incorrect results.

### Bug Fix Strategy:
To fix the bug, we need to modify the logic of how the function checks for table existence based on whether partitions are specified or not. We should check the exact table name in the list returned by the Hive command.

### Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout.split()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        # Since we are checking for the existence of a table with partitions, we need to check the exact table name
        return stdout and table == stdout.strip()
``` 

By splitting the stdout and checking for the exact table name, we can avoid false positives when checking for table existence. This corrected version should now pass the failing tests.