### Analysis
The buggy function `table_exists` is supposed to check if a table exists in a database. However, the bug seems to be related to how the function handles the output from the `run_hive_cmd` function. In the failing tests, the function is returning `False` when it should return `True` for one case and vice versa for another.

### Bug Explanation
1. In the failing test cases, the `run_hive_cmd` mock function is returning strings (`OK` and table names).
2. The function checks for the presence of the `table` in the `stdout` output; however, it is handling the presence detection incorrectly.

### Bug Fix Strategy
To fix the bug, we need to adjust the logic of how the function checks the presence of the table in the `stdout`. We can check if the table name is in the `stdout` output properly to return `True` if the table exists and `False` otherwise.

### Corrected Code
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return table in stdout  # Check if the table name is in the stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)  # Return True if stdout is not empty
``` 

By updating the return statements as shown above, the buggy function should now correctly determine if a table exists in the specified database.