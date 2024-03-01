### Bug Explanation
The bug in the `table_exists` function arises from the way the function checks for the existence of a table in the Hive database. When the function uses the `run_hive_cmd` function to execute a Hive command and then checks if the table name exists in the output, it does not handle case sensitivity properly. In Case 2 and Case 4, the function fails to detect the table 'MyTable' because the comparison is case-sensitive and the table name is stored in lowercase in the output.

### Bug Fix Strategy
To fix this bug, we need to ensure that the comparison between the table name and the output is case-insensitive. One way to achieve this is by converting both strings to lowercase (or uppercase) before comparing them.

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

By converting both the table name and the output to lowercase before comparison, the corrected function ensures a case-insensitive check for the existence of the table within the Hive database.