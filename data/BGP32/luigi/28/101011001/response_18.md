### Bug Explanation
The bug in the `table_exists` function lies in the comparison of the `table` name in the `stdout` obtained from the `run_hive_cmd` function. The method tries to match the `table` name exactly with the lines in the `stdout`, which causes issues when the `table` name is part of a longer line in the `stdout`.

In the failing test cases provided:
- Case 1: The function returns `False`, which is incorrect because the `table` name 'mytable' is present in the `stdout` 'OK'. The comparison fails because the function checks for an exact match between the `table` name and the `stdout`.
- Case 2: The incorrect comparison also affects this case where 'mytable' is found in the `stdout` 'OK\nmytable', resulting in a false negative.
- Case 3 and Case 4 indicate the same issue with correct `stdout` values but failing due to the exact match comparison.

### Bug Fix Strategy
To fix the bug:
1. Modify the comparison logic when checking if the `table` name exists in the `stdout`.
2. Implement a more robust check that can handle scenarios where the `table` name is part of a longer line in the `stdout`.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        
        return stdout and any(line.strip() == table for line in stdout.split('\n'))
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        
        return bool(stdout)
``` 

By splitting the `stdout` into lines and checking if the `table` name exists within any of those lines, the corrected version should now correctly identify the presence of the `table` name within the output.