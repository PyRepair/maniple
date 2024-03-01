### Bug Explanation:
The bug in the `table_exists` function stems from the incorrect handling of the `stdout` variable in the conditionals. The function checks if the `stdout` variable contains the table name, but it does not account for cases where the table name is part of another string in the output. This results in incorrect evaluations and the failing of test cases.

### Bug Fix Strategy:
To fix the bug, we need to modify the conditionals in the function to ensure that the table name is not just present in the `stdout` variable, but is an exact match. This can be achieved by splitting the `stdout` variable by lines and then checking for an exact match of the table name in the resulting list of strings.

### Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        
        # Split the stdout by lines
        tables = stdout.split('\n')

        # Check for exact match of the table name in the list of tables
        return table in tables
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        
        # Check for presence of stdout (indicating that the table exists)
        return bool(stdout)
```

By making these changes, the function will correctly handle the check for table existence and the corrected version should pass the failing test cases.