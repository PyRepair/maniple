### Bug Explanation
The bug in the `table_exists` function is due to the incorrect comparison of the `stdout` value after running a Hive command. The function is checking if `stdout` is non-empty and if `table` is in it, which is not the correct way to determine table existence in Hive. The condition `return stdout and table in stdout` in the first case is not sufficient to accurately check if the table exists.

### Bug Fix Strategy
To fix the bug, we should modify the function to properly check whether the table exists in Hive based on the command output. We can utilize the fact that Hive returns an empty string if the table does not exist. Therefore, we need to check if `stdout` is not empty (indicating the table exists) and if the table is exactly equal to the output (ignoring any extra characters like newlines).

### Corrected Function
```python
# The corrected function
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout.strip() == table
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout.strip())
``` 

By trimming any extra characters from the `stdout`, the corrected function will now accurately determine if the table exists in Hive. This should resolve the failing test cases.