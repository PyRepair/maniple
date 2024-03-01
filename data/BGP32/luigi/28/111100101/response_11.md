### Bugs in the provided function:
1. In the `table_exists` function, the conditional check for `then` case is incorrect. It should return based on the presence of the table in the stdout if partition is specified.
2. The mock objects `self.client.partition_spec` and `self.apacheclient.partition_spec` are being used improperly as the function should be called directly in the `table_exists` function.

### Bug Fixing Strategy:
1. Correct the conditional check for the partition specification case to return based on the presence of the table in the stdout.
2. Remove the usage of the `self.client.partition_spec` and `self.apacheclient.partition_spec` mock objects and directly call the function within the `table_exists` function.

### Corrected Version of the Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout is not None and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))
    
        return table in stdout if stdout else False
```

By making the above corrections, the `table_exists` function should now pass the failing test cases and return the expected output values according to the provided test scenarios.