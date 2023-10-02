Let's fix the bug by converting both the table name and the output of the hive command to lower case when performing the comparison. 

Here is the properly fixed code:

```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

    def table_location(self, table, database='default', partition=None):
        cmd = "use {0}; describe formatted {1}".format(database, table)
        if partition is not None:
            cmd += " PARTITION ({0})".format(self.partition_spec(partition))

        stdout = run_hive_cmd(cmd)

        for line in stdout.split("\n"):
            if "Location:" in line:
                return line.split("\t")[1]

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

    def table_schema(self, table, database='default'):
        describe = run_hive_cmd("use {0}; describe {1}".format(database, table))
        if not describe or "does not exist" in describe:
            return None
        return [tuple([x.strip() for x in line.strip().split("\t")]) for line in describe.strip().split("\n")]

    def partition_spec(self, partition):
        """
        Turns a dict into the a Hive partition specification string.
        """
        return ','.join(["{0}='{1}'".format(k, v) for (k, v) in
                         sorted(six.iteritems(partition), key=operator.itemgetter(0))])
```

This change equates the table name into lower case while making comparison, hence resolving the issue of case-sensitivity and making sure the comparison is accurate, whether the table name is capitalized or not.