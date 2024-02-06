```python
# class declaration containing the fixed function
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

    # ... omitted code ...


    # signature of the fixed function in this class
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