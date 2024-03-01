## Bug Explanation
The bug in the `table_exists` function lies in the comparison logic when checking if the table exists in the database. The function currently checks if the table name is present in the output of the Hive command, which can lead to false positives as it only checks for substring match.

## Bug Fix Strategy
To fix the bug, we need to modify the comparison logic to ensure an exact match between the table name and the tables listed in the output of the Hive command.

## Corrected Version of the Function
```python
# The relative path of the corrected file: luigi/contrib/hive.py

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

## Fix Description
In the corrected version of the function, the comparison logic `table in stdout.split('\n')` ensures that a full match is done with the table names listed in the output of the Hive command. This fix prevents false positives that could occur due to substring matches.