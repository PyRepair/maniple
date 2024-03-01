### Bug Explanation:
The bug in the `table_exists` function lies in the comparison of the `table` name with the output from the `run_hive_cmd` function. The current check `table in stdout` is case-sensitive, which can lead to false negatives if the case of the `table` name does not match exactly with the case in the `stdout`.

### Fix Strategy:
To fix this bug, the comparison between the `table` name and the `stdout` should be case-insensitive. One way to achieve this is by converting both strings to lowercase before comparing them.

### Corrected Version:
```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

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

By converting both the `table` and `stdout` to lowercase before comparison, the function will now correctly determine if the table exists in a case-insensitive manner.