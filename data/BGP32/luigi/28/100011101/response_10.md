## Bug Explanation
The bug in the `table_exists` function lies in the conditional statement that checks the presence of the table in the stdout. The bug occurs because the code checks for the table name as a whole string in the stdout, which may not be accurate due to potential variations in the output format.

## Bug Fix Strategy
To fix the bug, we need to modify the conditional check to ensure that we are correctly identifying the existence of the table in the stdout. One way to do this is to split the stdout by newline characters and then check if the table name appears in any of the lines. This approach will make the function more robust when dealing with potential variations in the output format.

## The Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        if stdout:
            tables = stdout.split('\n')
            return any(t.strip() == table for t in tables)
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

After implementing this fix, the function will split the stdout by newline characters and then check if the table name appears in any of the lines. This approach ensures that the function accurately detects the existence of the table based on the output received.