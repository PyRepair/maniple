The difficulty for this bug is that the buggy code range across multiple functions:
change1: line 54 - line 229
change2: line 402 - line 528

Problem:
1. The test function and error message can only provide one fix location
2. Hard to generalize the fix. Usually provide `'your collection description'` instead of `f'your {galaxy_type} description'`. Ideally, I need to provide a better instruction. 

# Prompt 1

```text
This function has a bug so that I cannot pass the test, can you tell me the corrected code?
Note that your should ouput full resultant function code and your changes should be as minimal as possible. You may provide multiple fixes if possible. Your answer should be generalized to all possible inputs.

    def init_parser(self):
        ''' create an options parser for bin/ansible '''

        super(GalaxyCLI, self).init_parser(
            desc="Perform various Role related operations.",
        )

        ...

    def execute_init(self):
        """
        Creates the skeleton framework of a role or collection that complies with the Galaxy metadata format.
        Requires a role or collection name. The collection name must be in the format ``<namespace>.<collection>``.
        """
        galaxy_type = context.CLIARGS['type']
        init_path = context.CLIARGS['init_path']
        force = context.CLIARGS['force']
        obj_skeleton = context.CLIARGS['{0}_skeleton'.format(galaxy_type)]
        obj_name = context.CLIARGS['{0}_name'.format(galaxy_type)]

        inject_data = dict(
            description='your description',
            ansible_plugin_list_dir=get_versioned_doclink('plugins/plugins.html'),
        )

        ...

        display.display("- %s was created successfully" % obj_name)


The variable value before line of error is:

galaxy_type: collection
init_path: /private/var/folders/ng/72llsm517x12c2p18htksyjc0000gn/T/pytest-of-jerry/pytest-2/test-ÅÑŚÌβŁÈ Collections0
force: False
obj_skeleton: None
obj_name: ansible_test.my_collection


The error message is:

    @pytest.mark.parametrize('collection_skeleton', [
        ('ansible_test.my_collection', None),
    ], indirect=True)
    def test_collection_default(collection_skeleton):
        meta_path = os.path.join(collection_skeleton, 'galaxy.yml')
    
        with open(meta_path, 'r') as galaxy_meta:
            metadata = yaml.safe_load(galaxy_meta)
    
        assert metadata['namespace'] == 'ansible_test'
        assert metadata['name'] == 'my_collection'
        assert metadata['authors'] == ['your name <example@domain.com>']
        assert metadata['readme'] == 'README.md'
        assert metadata['version'] == '1.0.0'
>       assert metadata['description'] == 'your collection description'
E       AssertionError: assert 'your description' == 'your collection description'
E         - your collection description
E         + your description

```
