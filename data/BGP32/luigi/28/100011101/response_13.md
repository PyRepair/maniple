### Bug Explanation:
The bug in the `table_exists` function occurs due to incorrect comparison logic when checking the existence of a table in the Hive database. In the first part of the function, when there is no specified partition, it checks if the table name appears in the output of the Hive command. However, the buggy comparison `return stdout and table in stdout` is problematic because a non-empty string `stdout` will always evaluate to `True`, causing the function to return `True` even if the table does not exist.

### Bug Fix Strategy:
To fix this bug, the comparison logic needs to be adjusted to correctly check if the table exists in the stdout and return `True` only in that case. Additionally, the second part of the function where partition information is provided needs to be checked and corrected to ensure accurate table existence validation.

### Corrected Code:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        
        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)  # any non-empty string evaluates to True
``` 

The corrected code splits the stdout by a newline character and checks if the table name exists in the resulting list. This modification ensures that the function accurately determines the existence of a table in the Hive database.