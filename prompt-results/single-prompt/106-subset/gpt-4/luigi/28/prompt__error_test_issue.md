You need to fix a bug in a python code snippet.

The buggy source code is following, and you should follow all specifications in comment if there exists comment:

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



Part of class definition that might be helpful for fixing bug is:

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

            return stdout and table in stdout
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



The test error on command line is following:





The test source code is following:

    @mock.patch("luigi.contrib.redshift.S3CopyToTable.copy")
    @mock.patch("luigi.contrib.redshift.RedshiftTarget")
    def test_s3_copy_to_table(self, mock_redshift_target, mock_copy):
        task = DummyS3CopyToTable()
        task.run()

        # The mocked connection cursor passed to
        # S3CopyToTable.copy(self, cursor, f).
        mock_cursor = (mock_redshift_target.return_value
                                           .connect
                                           .return_value
                                           .cursor
                                           .return_value)

        # `mock_redshift_target` is the mocked `RedshiftTarget` object
        # returned by S3CopyToTable.output(self).
        mock_redshift_target.assert_called_with(database=task.database,
                                                host=task.host,
                                                update_id='DummyS3CopyToTable()',
                                                user=task.user,
                                                table=task.table,
                                                password=task.password)

        # Check if the `S3CopyToTable.s3_load_path` class attribute was
        # successfully referenced in the `S3CopyToTable.run` method, which is
        # in-turn passed to `S3CopyToTable.copy` and other functions in `run`
        # (see issue #995).
        mock_copy.assert_called_with(mock_cursor, task.s3_load_path)

        # Check the SQL query in `S3CopyToTable.does_table_exist`.
        mock_cursor.execute.assert_called_with("select 1 as table_exists "
                                               "from pg_table_def "
                                               "where tablename = %s limit 1",
                                               (task.table,))

        return



The raised issue description for this bug is:
hive table_exists should be case insensitive?

Any thoughts on this one?\n\nIn https://github.com/spotify/luigi/blob/master/luigi/contrib/hive.py#L141\n(possibly here too, but we're not on CDH: https://github.com/spotify/luigi/blob/master/luigi/contrib/hive.py#L192)\n\nSometimes we have tables that are defined as capitalized, rather than lower case underscored names. These are easier to read in code if left capitalized, though hive is case insensitive, and will return them as lower case.\n\nE.g. when checking for an existing table table = 'FooBar', stdout will return with foobar and the test will fail\n\nThis wasn't an issue in older versions, which just checked for string \"does not exist\" or \"Table not found\" in stdout.\n\nWould be easy to fix using return stdout and table.lower() in stdout or return stdout and table.lower() in stdout.lower()\n\nLet me know your thoughts on this. I can supply a pull request if necessary.\n\nThanks,\nLin.
The raised issue description for this bug is:
Fix #896: make table_exists case insensitive

Check stdout against table.lower() to avoid case issues