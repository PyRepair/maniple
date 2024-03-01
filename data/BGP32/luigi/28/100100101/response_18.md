### Bug Explanation:
The bug in the `table_exists` function is caused by the incorrect condition for checking the existence of a table. The function is currently returning `True` if the output of the `run_hive_cmd` function is not empty, and `False` otherwise. This logic is incorrect because the function should return `True` if the table name is found in the output and `False` otherwise. 

### Fix Strategy:
To fix the bug, we need to check if the table name exists in the output of the `run_hive_cmd` function, rather than just checking if the output is not empty. Additionally, we should match the table name case-insensitively to adhere to the test case.

### Corrected Version:
```python
# The relative path of the buggy file: luigi/contrib/hive.py

def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table.lower() in map(str.strip, stdout.lower().split('\n'))
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))
        
        return stdout != ""

```

By correcting the condition inside the `table_exists` function to check if the table name exists in the output correctly and adding case-insensitive matching, the function now behaves as expected and passes the provided test cases.