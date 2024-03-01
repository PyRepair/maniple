## Bug Explanation
The bug in the function `table_exists` lies in the conditional statement where the function checks if `stdout` is not empty. In the first `if` block, the condition `stdout and table in stdout` will return `True` if `stdout` is not empty, regardless of whether `table` is in `stdout` or not. This leads to incorrect results. 

A similar issue occurs in the `else` block, where `stdout` is checked directly as a boolean value, which may not accurately reflect whether the table exists or not.

## Fix Strategy
- In order to fix this bug, we need to modify the condition checks to explicitly verify if the `table` exists in the output result `stdout`.
- Additionally, we should incorporate better conditional logic for checking the existence of tables based on the `stdout` output.

## Updated Code
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        
        return table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return any(partition in line for line in stdout.split('\n'))
``` 

This updated code fixes the condition checks in both cases and ensures that the returned result accurately reflects the existence of the specified `table` or `partition`.