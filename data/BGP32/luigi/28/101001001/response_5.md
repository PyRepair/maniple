### Bug Explanation
The bug in the `table_exists` function lies in how the function checks if the table exists. When the function runs the `run_hive_cmd` function to query the tables in the database, it does a case-sensitive check to see if the table name is in the list of tables. This can lead to incorrect results when the case of the table name does not match exactly with what is returned by the query.

### Bug Fix
To fix this bug and make the table existence check case-insensitive, we can modify the `table_exists` function to ensure that the comparison between the table name and the list of tables retrieved from the query is done in a case-insensitive manner.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        if stdout:
            return any(t.lower() == table.lower() for t in stdout.split())
        return False
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))
        return bool(stdout)
``` 

In the corrected version above, we use `lower()` to convert both the table names returned from the query and the table name provided during the function call to lowercase for a case-insensitive comparison. This ensures that the check for table existence is done irrespective of the case of the table name.