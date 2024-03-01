### Bug Analysis
The bug in the `table_exists` function lies in the condition where it checks if the table exists in the stdout output of the `run_hive_cmd` function. The current implementation checks if the table name is directly present in the stdout, which causes an issue when there are multiple lines in the stdout (as seen in Case 2).

### Bug Cause
1. In Case 1, the `stdout` variable contains only `'OK'`, and the condition `table in stdout` fails as the table name is not directly in the stdout.
2. In Case 2, the `stdout` variable contains `'OK\nmytable'`, and the condition `table in stdout` passes because the table name is in the output.
3. In Case 3 and Case 4, similar issues exist as in Case 1 and Case 2, causing incorrect results.

### Bug Fix Strategy
To fix this bug, we need to modify the condition to check if the table name is in any line of the stdout output. We can split the stdout by line breaks and then check if the table exists in any of those lines.

### Corrected Version
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

By using the `any` function and splitting the stdout into lines, the corrected function will accurately determine if the table exists based on the table name in the output.