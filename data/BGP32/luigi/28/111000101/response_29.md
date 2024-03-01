### Bug Analysis:
The bug in the `table_exists` function lies in how the query is being constructed and executed when the `partition` parameter is not None. The current code is using incorrect formatting for the Hive command. The placeholders `%s` are being used inappropriately, causing the query to be malformed and leading to incorrect results.

### Bug Explanation:
When the `partition` parameter is not None, the function tries to run a Hive command using the following code:
```python
stdout = run_hive_cmd("""use %s; show partitions %s partition
                    (%s)""" % (database, table, self.partition_spec(partition)))
```
Here, the formatting is incorrect. The intention seems to be to replace `%s` placeholders with values, but the use is incorrect. This results in the Hive command not being properly constructed, leading to incorrect queries being executed.

### Fix Strategy:
To fix this bug, we need to correctly format the Hive command string by using the `format` method. This will ensure that the variables are placed in the correct positions within the string.

### Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("use {0}; show partitions {1} partition ({2})".format(database, table, self.partition_spec(partition)))
        return bool(stdout)
``` 

By using the `format` method for string formatting, the Hive command will be constructed correctly, and the function should now return the expected results for all test cases.