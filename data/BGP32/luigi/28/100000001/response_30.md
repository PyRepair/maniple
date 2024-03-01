The potential error locations within the buggy function are:
1. In the else condition, the string formatting might not be correct.
2. The `run_hive_cmd` function is being called without any definition provided, which can cause an error.

The cause of the bug in this function is that the string formatting in the `else` block is incorrect, which can lead to an error when executing the query.

To fix the bug:
1. Define the `run_hive_cmd` function or import it from a module where it is defined.
2. Correct the string formatting in the `else` block by using `%` formatting or `.format()` method to ensure the correct query execution.

Here is the corrected version of the function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd('use {0}; show partitions {1} partition ({2})'.format(database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
``` 

Make sure to define or import the `run_hive_cmd` function correctly for this corrected version to work as expected.