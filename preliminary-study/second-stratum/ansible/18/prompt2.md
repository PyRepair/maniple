Fact used: ../../repair_template, ../../cot, f1-1-1, f2-2-1

# Prompt
Please fix the code provided below and provide the corrected code as the output.

Provide your answer in the following steps:
1. Analyze the test case and its relationship with the error message, if applicable.
2. Identify the potential error location within the problematic function.
3. Explain the reasons behind the occurrence of the bug.
4. Suggest possible approaches for fixing the bug.
5. Present the corrected code for the problematic function.

The buggy code is:

```python
def execute_init(self):
    galaxy_type = context.CLIARGS['type']
    init_path = context.CLIARGS['init_path']
    force = context.CLIARGS['force']
    obj_skeleton = context.CLIARGS['{0}_skeleton'.format(galaxy_type)]

    obj_name = context.CLIARGS['{0}_name'.format(galaxy_type)]

    inject_data = dict(
        description='your description',
        ansible_plugin_list_dir=get_versioned_doclink('plugins/plugins.html'),
    )
    if galaxy_type == 'role':
        inject_data.update(dict(
            author='your name',
            company='your company (optional)',
            license='license (GPL-2.0-or-later, MIT, etc)',
            role_name=obj_name,
            role_type=context.CLIARGS['role_type'],
            issue_tracker_url='http://example.com/issue/tracker',
            repository_url='http://example.com/repository',
            documentation_url='http://docs.example.com',
            homepage_url='http://example.com',
            min_ansible_version=ansible_version[:3],  # x.y
        ))

        obj_path = os.path.join(init_path, obj_name)
    elif galaxy_type == 'collection':
        namespace, collection_name = obj_name.split('.', 1)

        inject_data.update(dict(
            namespace=namespace,
            collection_name=collection_name,
            version='1.0.0',
            readme='README.md',
            authors=['your name <example@domain.com>'],
            license=['GPL-2.0-or-later'],
            repository='http://example.com/repository',
            documentation='http://docs.example.com',
            homepage='http://example.com',
            issues='http://example.com/issue/tracker',
        ))

        obj_path = os.path.join(init_path, namespace, collection_name)

    b_obj_path = to_bytes(obj_path, errors='surrogate_or_strict')

    if os.path.exists(b_obj_path):
        if os.path.isfile(obj_path):
            raise AnsibleError("- the path %s already exists, but is a file - aborting" % to_native(obj_path))
        elif not force:
            raise AnsibleError("- the directory %s already exists. "
                                "You can use --force to re-initialize this directory,\n"
                                "however it will reset any main.yml files that may have\n"
                                "been modified there already." % to_native(obj_path))

    if obj_skeleton is not None:
        own_skeleton = False
        skeleton_ignore_expressions = C.GALAXY_ROLE_SKELETON_IGNORE
    else:
        own_skeleton = True
        obj_skeleton = self.galaxy.default_role_skeleton_path
        skeleton_ignore_expressions = ['^.*/.git_keep$']

    obj_skeleton = os.path.expanduser(obj_skeleton)
    skeleton_ignore_re = [re.compile(x) for x in skeleton_ignore_expressions]

    if not os.path.exists(obj_skeleton):
        raise AnsibleError("- the skeleton path '{0}' does not exist, cannot init {1}".format(
            to_native(obj_skeleton), galaxy_type)
        )

    template_env = Environment(loader=FileSystemLoader(obj_skeleton))

    # create role directory
    if not os.path.exists(b_obj_path):
        os.makedirs(b_obj_path)

    for root, dirs, files in os.walk(obj_skeleton, topdown=True):
        rel_root = os.path.relpath(root, obj_skeleton)
        rel_dirs = rel_root.split(os.sep)
        rel_root_dir = rel_dirs[0]
        if galaxy_type == 'collection':
            # A collection can contain templates in playbooks/*/templates and roles/*/templates
            in_templates_dir = rel_root_dir in ['playbooks', 'roles'] and 'templates' in rel_dirs
        else:
            in_templates_dir = rel_root_dir == 'templates'

        dirs[:] = [d for d in dirs if not any(r.match(d) for r in skeleton_ignore_re)]

        for f in files:
            filename, ext = os.path.splitext(f)

            if any(r.match(os.path.join(rel_root, f)) for r in skeleton_ignore_re):
                continue
            elif galaxy_type == 'collection' and own_skeleton and rel_root == '.' and f == 'galaxy.yml.j2':
                # Special use case for galaxy.yml.j2 in our own default collection skeleton. We build the options
                # dynamically which requires special options to be set.

                # The templated data's keys must match the key name but the inject data contains collection_name
                # instead of name. We just make a copy and change the key back to name for this file.
                template_data = inject_data.copy()
                template_data['name'] = template_data.pop('collection_name')

                meta_value = GalaxyCLI._get_skeleton_galaxy_yml(os.path.join(root, rel_root, f), template_data)
                b_dest_file = to_bytes(os.path.join(obj_path, rel_root, filename), errors='surrogate_or_strict')
                with open(b_dest_file, 'wb') as galaxy_obj:
                    galaxy_obj.write(to_bytes(meta_value, errors='surrogate_or_strict'))
            elif ext == ".j2" and not in_templates_dir:
                src_template = os.path.join(rel_root, f)
                dest_file = os.path.join(obj_path, rel_root, filename)
                template_env.get_template(src_template).stream(inject_data).dump(dest_file, encoding='utf-8')
            else:
                f_rel_path = os.path.relpath(os.path.join(root, f), obj_skeleton)
                shutil.copyfile(os.path.join(root, f), os.path.join(obj_path, f_rel_path))

        for d in dirs:
            b_dir_path = to_bytes(os.path.join(obj_path, rel_root, d), errors='surrogate_or_strict')
            if not os.path.exists(b_dir_path):
                os.makedirs(b_dir_path)

    display.display("- %s was created successfully" % obj_name)
```

The error message is:

```text
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


# Response
1. The test case is trying to load metadata from a file called `galaxy.yml` and assert its content. The error message indicates that the test failed because the expected description value does not match the actual description value from the metadata file.

2. The potential error location is likely in the function `execute_init` where the `description` attribute is added to the `inject_data` dictionary.

3. The bug occurs because the `description` field in the `inject_data` dictionary is hardcoded to `'your description'` without considering the galaxy type (collection or role) and is not being set based on the galaxy type.

4. To fix the bug, we need to dynamically set the `description` field based on the galaxy type (collection or role). Additionally, we should also ensure that the metadata generated matches the expected format.

5. Here's the corrected code for the `execute_init` function:

```python
def execute_init(self):
    galaxy_type = context.CLIARGS['type']
    init_path = context.CLIARGS['init_path']
    force = context.CLIARGS['force']
    obj_skeleton = context.CLIARGS['{0}_skeleton'.format(galaxy_type)]

    obj_name = context.CLIARGS['{0}_name'.format(galaxy_type)]

    inject_data = dict(
        ansible_plugin_list_dir=get_versioned_doclink('plugins/plugins.html'),
    )
    if galaxy_type == 'role':
        inject_data.update(dict(
            description='your role description',
            author='your name',
            company='your company (optional)',
            license='license (GPL-2.0-or-later, MIT, etc)',
            role_name=obj_name,
            role_type=context.CLIARGS['role_type'],
            issue_tracker_url='http://example.com/issue/tracker',
            repository_url='http://example.com/repository',
            documentation_url='http://docs.example.com',
            homepage_url='http://example.com',
            min_ansible_version=ansible_version[:3],  # x.y
        ))

        obj_path = os.path.join(init_path, obj_name)
    elif galaxy_type == 'collection':
        namespace, collection_name = obj_name.split('.', 1)

        inject_data.update(dict(
            description='your collection description',
            namespace=namespace,
            collection_name=collection_name,
            version='1.0.0',
            readme='README.md',
            authors=['your name <example@domain.com>'],
            license=['GPL-2.0-or-later'],
            repository='http://example.com/repository',
            documentation='http://docs.example.com',
            homepage='http://example.com',
            issues='http://example.com/issue/tracker',
        ))

        obj_path = os.path.join(init_path, namespace, collection_name)
    
    # Rest of the code remains unchanged
```

In this corrected code, the `description` field in the `inject_data` dictionary is set based on the galaxy type, ensuring the correct description is used for each type. This should resolve the issue with the incorrect metadata being used in the test case.

