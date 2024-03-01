### Bug Explanation:
The bug in the `table_exists` function arises from the `if` conditions where it checks if the `stdout` variable is truthy to determine if the table exists. In the first case, when `stdout` is 'OK', the condition `return stdout and table in stdout` evaluates to `True and True`, which results in `True`, even though the table might not actually exist.

### Bug Fix:
To fix this issue, we need to modify how we check for the existence of the table in the `stdout`. We should check if the table is contained within the lines of the `stdout` instead of simply checking if the `stdout` is not empty.

### Corrected Version of the Function:
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

By modifying the return statements to explicitly check if the table is present in the lines of `stdout`, we ensure a more accurate determination of table existence. Additionally, the use of `any` function allows us to check each line in `stdout` independently. This correction should now pass the failing tests.