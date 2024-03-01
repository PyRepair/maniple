## Bug Explanation
The bug in the `table_exists` function lies in how the conditionals are structured. The function currently returns `False` when stdout is not empty, which is the opposite of the expected behavior. This inconsistency causes the failing tests where `self.assertTrue(returned)` does not pass even when the table exists.

## Bug Fix Strategy
To fix the bug, we need to correct the logic inside the function. The function should return `True` when the table exists and `False` when it doesn't. Adjust the conditional statements to reflect this logic.

## Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))
        return bool(stdout)
``` 

Now, with this corrected logic, the function should return `True` if the table exists and `False` if it doesn't, passing the failing tests.