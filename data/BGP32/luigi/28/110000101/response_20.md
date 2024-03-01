### Bug Explanation
The bug in the `table_exists` function is that the condition to check if a table exists in the database is not correctly checking the output of the `run_hive_cmd` function. The function is returning the output of the command and then checking if the table name is present in that output. However, the output may contain multiple lines, and the function is only checking if the table name is present in the entire output, which may lead to incorrect results.

### Bug Fix Strategy
To fix the bug, we need to split the output of the `run_hive_cmd` function and check if the table name is present in any of the lines. This way, we can ensure that we are correctly verifying the existence of the table in the database.

### Corrected Version

```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
            if stdout:
                return any(line.strip() == table for line in stdout.split('\n'))
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

This corrected version ensures that each line of the output is checked individually to see if the table name is present, improving the accuracy of the `table_exists` function.