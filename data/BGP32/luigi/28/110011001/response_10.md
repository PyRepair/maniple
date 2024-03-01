### Bug Explanation
The bug in the `table_exists` function lies in the condition for checking the existence of a table. The function checks if the output of the `run_hive_cmd` function contains the table name, which is not a reliable way to determine table existence. The bug causes the function to incorrectly return `False` even when the table exists, leading to failing tests where the expected result is `True`.

### Bug Fix Strategy
To fix the bug, we need to modify the way we check for table existence. Instead of checking if the table name is in the output, we should check if the output contains the table name followed by a newline character. This ensures that we are specifically matching the table name and not just a substring.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}\n";'.format(database, table))

        return stdout and table+'\n' in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                              (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

By making this change, we ensure that the function correctly checks for the existence of the table name followed by a newline character in the output of the `run_hive_cmd` function. This fix should resolve the bug and make the tests pass successfully.