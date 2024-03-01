### Bug Explanation
The bug in the `table_exists` function lies in the comparison of the `table` variable in the `stdout` string. The function is checking if the whole `table` string exists in the `stdout`, leading to incorrect results.

### Bug Fix Strategy
To fix the bug, we need to check if the `table` string exists as a whole word in the `stdout` string. We can achieve this by splitting the `stdout` string by newline characters and then checking if the `table` string exists in the resulting list.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))  # Replacing 'like "{1}"' with 'show tables' to get all table names

        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
``` 

By splitting the `stdout` string and checking if the `table` string exists in the resulting list, we ensure that we are evaluating the presence of the table name accurately. This correction should fix the bug and make the function behave correctly with the provided failing tests.