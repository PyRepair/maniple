## Bugs identified in the buggy function:
1. In the else block, there is a missing semi-colon at the end of the SQL query in the `run_hive_cmd` function.
2. The `self.partition_spec(partition)` call seems to be incorrectly positioned within the SQL query.

## Explanation of the bug:
The buggy function has a syntax error in the SQL query when checking for table existence using Hive. The missing semi-colon and incorrect placement of the `partition_spec` function are causing the query to be executed incorrectly, leading to inaccurate results.

## Strategy to fix the bug:
1. Add a semi-colon at the end of the SQL query to ensure proper termination.
2. Correctly position the `self.partition_spec(partition)` within the query for accurate execution.

## Corrected version of the function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s);""" % (database, table, self.partition_spec(partition)))
        return bool(stdout)
``` 

This corrected version includes the missing semi-colon and correctly positions the `self.partition_spec(partition)` in the SQL query.