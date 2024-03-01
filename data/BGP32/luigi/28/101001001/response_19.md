### Bug Explanation:

The bug in the `table_exists` function occurs due to the way the function checks for the existence of a table in Hive. In the first part of the function, when no partition is provided, it checks for a table by running a Hive command and then verifying if the table name exists in the output. 

The bug arises from how the function checks the existence of the table based on the `stdout` value returned from the `run_hive_cmd` function. The function checks if `stdout` exists and if the table name is in `stdout`. The issue here is that even if the table name is not present in the output, the function will still return `True` if `stdout` is not empty.

### Bug Fix:

To fix the bug, we should modify the first part of the `table_exists` function to explicitly check if the table name is in `stdout` without relying on the truthiness of `stdout`. This will ensure that the function accurately determines the existence of the table in Hive.

### Corrected Version:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return table in stdout  # Check if the table name is in stdout
    else:
        stdout = run_hive_cmd(
            """use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition))
        )

        return stdout is not None  # Check if stdout exists to determine table existence
``` 

By explicitly checking if the `table` is in the `stdout` and using `stdout is not None` in the return statement, the corrected version of the function will accurately determine the existence of the table in Hive.