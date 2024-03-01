### Issue:
The buggy function `table_exists` is not correctly checking for the existence of a table in the database. The function is returning `True` if the table name is found in the output of the `run_hive_cmd` function, which is incorrect. It should return `True` only if the exact table name matches.

### Strategy for Fixing the Bug:
To fix the bug, we need to modify the condition where the function checks if the table name is in the stdout. Instead of a simple check, we should split the stdout into lines and check if any line exactly matches the table name. This way, we ensure that we are only returning `True` if the table exists with an exact match.

### Corrected Version of the Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))
        tables = stdout.split('\n')
        return any(t == table for t in tables)
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

By making this modification, the function will now correctly check for the existence of a table and return `True` only if the table name matches exactly. This corrected version should fix the bug and make the failing tests pass.