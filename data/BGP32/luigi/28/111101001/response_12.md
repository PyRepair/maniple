### Bug Explanation
The bug in the `table_exists` function stems from the logic used to check if a table exists in the given database. The issue lies in the condition checking the presence of the table name in the `stdout` variable after running the hive command. The current implementation checks if the table name is a substring of the entire stdout, which can lead to incorrect results, especially in Case 2 where the table name 'MyTable' is present in the middle of the stdout.

### Bug Fix Strategy
To fix this bug, we should modify the logic to properly parse the output of the hive command and check if the table name exists as a separate word in the stdout. One possible approach is to split the stdout into lines and then check if the table name exists in any of those lines.

### Corrected Version
```python
class HiveCommandClient(HiveClient):
    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
            return any(table == line.strip() for line in stdout.split('\n'))
        else:
            partition_str = self.partition_spec(partition)
            stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, partition_str))
    
            return any(partition_str == line.strip() for line in stdout.split('\n'))
```

By splitting the stdout into lines and then checking if the table name or partition spec exists as a separate word in any of those lines, we ensure more accurate validation of table existence. This corrected version should address the bug and pass the failing test cases.