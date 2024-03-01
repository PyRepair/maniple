### Bug Explanation
The bug in the `table_exists` function lies in the conditional checks for the presence of the table in the output of the `run_hive_cmd` function. The function is expecting the output to contain the table name without any additional characters or new lines. This causes the failing tests when additional characters or new lines are present in the output which is not handled properly by the function.

### Bug Fix Strategy
To fix the bug, we need to modify the conditional checks to properly handle cases where the table name might have additional characters or be followed by a new line character. Additionally, we need to ensure that the partition specification is properly formatted before checking for its existence.

### Corrected Function
```python
class HiveCommandClient(HiveClient):
    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
            return stdout and table in stdout.strip().split('\n')
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))
    
            return bool(stdout)
```

By splitting the table names by newline characters and stripping extra characters, we ensure that we correctly identify the table name in the command output, addressing the bug.