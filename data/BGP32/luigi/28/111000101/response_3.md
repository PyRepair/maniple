### Analysis
The `table_exists` function checks for the existence of a table or a partition in a Hive database. The bug seems to be related to the logic inside the function when handling partitions.

### Bug
The bug occurs when checking for the existence of a partition. In the else branch of the function, when formatting the Hive command to check for partitions, there is a missing `%` sign in the string formatting, causing the command to be incorrectly formatted.

### Fix
To fix the bug, we need to add the missing `%` sign in the string formatting of the Hive command to check for partitions.

### Corrected Version of the Function

```python
# The relative path of the corrected file: luigi/contrib/hive.py

def run_hive_cmd(hivecmd, check_return_code=True):
    # Please ignore the body of this function

class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

    def partition_spec(self, partition):
        # Please ignore the body of this function

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
            return stdout and table in stdout
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                                (%s)""" % (database, table, self.partition_spec(partition)))
    
            if stdout:
                return True
            else:
                return False
```

With this fix, the `%` sign is correctly inserted in the string formatting of the Hive command to check for partitions. This should resolve the bug and make the function work as expected in all the provided test cases.