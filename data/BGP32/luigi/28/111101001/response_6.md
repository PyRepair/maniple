### Bug Explanation
The bug in the `table_exists` function lies in the way the output of the `run_hive_cmd` function is checked for the existence of the table. The condition `return stdout and table in stdout` checks if the `stdout` string is not empty and if the `table` string is present in it. However, in some cases like in Case 2, when the function returns `OK\nmytable`, the presence of `\n` affects the check causing the test to fail.

### Fix Strategy
To fix the bug, we need to modify the way we check for the existence of the table in the `stdout` string to handle cases where there might be extra characters like `\n`. We can split the `stdout` string by lines and then check each line for the presence of the table.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return any(line.strip() == table for line in stdout.split('\n') if line.strip())
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

By implementing this correction, we are now splitting the `stdout` by lines and checking if any line exactly matches the `table` name, ensuring a more accurate check for the existence of the table.