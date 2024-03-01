### Bug Explanation
The bug lies in the comparison logic within the `table_exists` function. When checking if the table exists, the function incorrectly returns `False` if the table name is not found within the output. This results in incorrect behavior in the test cases where the expected output should be `True`. 

### Bug Fix Strategy
To fix the bug, we need to update the comparison logic in the `table_exists` function to properly handle the case where the table name is found in the output. We should return `True` in this case and return `False` only when the table name is not found.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))

        return True if stdout else False
``` 

By updating the return statements to directly return the outcome of the condition, we ensure that the function behaves correctly for all test cases.