### Bug Explanation
The bug in the `table_exists` function lies in the comparison of the `table` name with the string `stdout` returned from `run_hive_cmd`. The current comparison checks if the `table` name is present in the `stdout` string directly, which leads to incorrect results when the table name appears within other names or strings in `stdout`.

### Bug Fix Strategy
To fix the bug, we need to modify the comparison logic to ensure that we are checking the table name against only the table names present in the `stdout`. This can be achieved by splitting the `stdout` string into lines and then checking each line separately if it equals the table name.

### Corrected Version of the Function
```python
class HiveCommandClient(HiveClient):
    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        
            if stdout:
                tables = stdout.split('\n')
                return any(t.strip() == table for t in tables)
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        
            if stdout:
                return True
            else:
                return False
``` 

This corrected version splits the `stdout` string by line breaks, then checks each line to see if it exactly matches the `table` name, ensuring that we are accurately verifying the existence of the table.