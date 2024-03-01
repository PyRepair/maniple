### Bug Explanation:
The bug in the `table_exists` function lies in the condition used to determine if a table exists. The function relies on checking if the table name is present in the output received from running a Hive command. However, the implementation does not correctly handle the case when the table name is a substring of another table name in the output, leading to incorrect results.

### Bug Fix Strategy:
To address the bug, we need to ensure that the function correctly identifies the exact presence of the table name in the command output. One way to achieve this is by splitting the output based on line breaks and checking each line individually for an exact match with the table name.

### Corrected Version of the Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        
        if stdout:
            return table in stdout.split('\n')
        else:
            return False
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

By splitting the `stdout` string based on line breaks and checking for an exact match, we ensure that the function accurately determines the existence of a table. This corrected version should pass the failing test cases provided.