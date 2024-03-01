### Bug Analysis
The bug in the `table_exists` function appears to be related to the comparison between the table name and the output from the `run_hive_cmd` function. The function is not handling the case where the table name is present in the output after splitting by newline characters.

The issue arises when the table name is not found in the stdout variable, causing the function to return `False` incorrectly.

### Bug Description
The bug occurs because the function incorrectly checks the existence of the table in the output of `run_hive_cmd` by simply using a string comparison. If the table name is found in the output but not as the only value (i.e., there are other entries present), the function incorrectly returns `False`.

### Suggested Fix
To fix the bug, we need to modify the logic in the behavior when the table name is present in the output. Instead of just checking if the table name is in the output variable, we should split the output by newline characters and then check if the table name is present in the list of values obtained after splitting.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                                (%s)""" % (database, table, self.partition_spec(partition)))
    
        if stdout:
            return True
        else:
            return False
```

By splitting the `stdout` variable by newline characters, we ensure that we are properly checking if the table name exists in the list of values obtained from the `run_hive_cmd` output. This modification should resolve the issue and make the `table_exists` function work correctly.