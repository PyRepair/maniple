### Bug Explanation:
The bug in the `table_exists` function arises from the condition being checked after running the `run_hive_cmd` function. When the `stdout` variable is populated with the result from `run_hive_cmd`, the condition `stdout and table in stdout` checks if the table exists in the output. However, this check is incorrect as it only checks if the table name appears in the output once. Instead, it should check if the table name appears as a standalone word in the output.

### Bug Fix Strategy:
To fix the bug, we need to modify the condition checking in the `table_exists` function to accurately determine if the table name exists in the output of `run_hive_cmd`. We can split the output by newline characters and then check if the table name is a standalone word in the output.

### Corrected Code:
```python
# Fix the bug in the table_exists function
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        
        return stdout and any(t.strip() == table for t in stdout.split('\n'))
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

By modifying the condition to `any(t.strip() == table for t in stdout.split('\n'))`, we ensure that the table name appears as a standalone word in the output, fixing the bug in the function.