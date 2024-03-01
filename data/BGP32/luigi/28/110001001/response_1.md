### Bug Explanation
The bug in the `table_exists` function lies in the condition used to check if the table exists. In both cases, the function checks if `stdout` contains the table name, which is not a reliable way to determine the existence of a table. This is because the `show tables like "{1}"` command in Hive returns a list of tables that match the pattern, which means that even if the table doesn't exist, the command will still return a non-empty result with potentially multiple tables listed.

### Bug Fix
To fix this bug, we need to modify the condition to check for an exact match of the table name in the output of the `show tables` command. We can achieve this by splitting the `stdout` based on newline characters and then performing an exact match check.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))
        tables = stdout.split('\n')
        return table in tables
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

This corrected version splits the output of the `show tables` command into a list of tables and then checks if the specified table is among those retrieved. This approach ensures that the function accurately determines the existence of the table in the specified database.