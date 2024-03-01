### Bug Explanation
The bug in the `table_exists` function lies in the condition for checking if a table exists. In the case where the `partition` parameter is not None, the function constructs a command to show partitions for the table but does not correctly parse the output to determine if the table exists. This leads to incorrect results in the test cases where the function should return `True` but returns `False`.

### Fix Strategy
To fix the bug, we need to ensure that the function correctly parses the output of the `run_hive_cmd` function to determine if the table exists. We should modify the function to check the content of `stdout` instead of just checking if it exists.

### Corrected Version
```python
class HiveCommandClient(HiveClient):
    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
            return stdout and table in stdout.split('\n')
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                                (%s)""" % (database, table, self.partition_spec(partition)))
            return stdout != ""
``` 

With this corrected version, the function properly splits the output by newlines and checks if the table exists in the list of tables in the output. Also, when checking partitions, it simply confirms if there is any output, indicating the existence of the table.