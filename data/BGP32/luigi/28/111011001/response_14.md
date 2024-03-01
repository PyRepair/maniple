### Bug Explanation
The bug in the `table_exists` function lies in how it checks for the existence of a table in the database. The function currently checks if the table name is directly in the output of the `run_hive_cmd` function. However, this check is faulty because it doesn't account for cases where the table name appears as part of a larger string that the `run_hive_cmd` function returns.

### Bug Fix Strategy
To fix the bug, we need to modify the logic of the `table_exists` function to properly parse the output of the `run_hive_cmd` function and check if the table name exists within it. One way to do this is to split the output by newline characters and then check each line for the presence of the table name.

### Corrected Version

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        if stdout:
            return any(line.strip() == table for line in stdout.split('\n'))
        else:
            return False
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

By splitting the `stdout` by newline characters and checking each line for the exact table name, we ensure a more accurate check for table existence. This corrected version should pass the failing tests.