### Explanation:

The bug in the `table_exists` function is that it does a case-sensitive check when checking if a table exists in Hive. Due to Hive being case insensitive, the function should perform a case-insensitive check to accurately determine if a table exists.

The issue reported on GitHub highlights this problem and suggests a solution to make the `table_exists` function case insensitive when checking for table existence.

### Strategy for Fixing the Bug:
1. Modify the `table_exists` function to convert both the `table` name and the values from `stdout` to lowercase before performing the comparison.
2. Use the `lower()` method on both strings for a case-insensitive comparison.
3. Check if the lowercase `table` name is present in the lowercase `stdout` string to accurately determine if the table exists in Hive.

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

This corrected version will resolve the issue of case sensitivity when checking for table existence in Hive and align with the suggestion provided in the GitHub issue.