### Explanation:
The bug in the `table_exists` function lies in the condition where the function checks if the table exists in the output of the `run_hive_cmd` function. 

In the cases provided:
1. In Case 1, when the table name is in lowercase in both the input and the output, the function correctly identifies the table existence.
2. In Case 2, when the table name is in uppercase in the input but lowercase in the output, the function fails to recognize the table existence due to case sensitivity.
3. In Case 3, similar to Case 1 but with a different table name.
4. In Case 4, similar to Case 2 but with a different table name. 

### Bug Fix Strategy:
To fix the bug, we need to make the comparison case-insensitive so that it doesn't fail based on the case of the table name in the output of the `run_hive_cmd` function.

### Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
``` 

Now, in the corrected version, both the table name being checked and the table names in the output are converted to lowercase before comparison, making the check case-insensitive.