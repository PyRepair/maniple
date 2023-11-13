Error messages are following:

```text
_________________________________________________ test_build_requirement_from_path_with_manifest[1.1] __________________________________________________

version = 1.1
collection_artifact = (b'/private/var/folders/ng/72llsm517x12c2p18htksyjc0000gn/T/pytest-of-jerry/pytest-6/test-\xc3\x85\xc3\x91\xc5\x9a\xc3...\xc3\x85\xc3\x91\xc5\x9a\xc3\x8c\xce\xb2\xc5\x81\xc3\x88 Collections Input1/ansible_namespace-collection-0.1.0.tar.gz')

    @pytest.mark.parametrize('version', ['1.1.1', 1.1, 1])
    def test_build_requirement_from_path_with_manifest(version, collection_artifact):
        manifest_path = os.path.join(collection_artifact[0], b'MANIFEST.json')
        manifest_value = json.dumps({
            'collection_info': {
                'namespace': 'namespace',
                'name': 'name',
                'version': version,
                'dependencies': {
                    'ansible_namespace.collection': '*'
                }
            }
        })
        with open(manifest_path, 'wb') as manifest_obj:
            manifest_obj.write(to_bytes(manifest_value))
    
>       actual = collection.CollectionRequirement.from_path(collection_artifact[0], True)

test/units/galaxy/test_collection_install.py:184:
```

```text
self = <ansible.galaxy.collection.CollectionRequirement object at 0x7f9086505a50>, version = 1.1, requirements = 1.1, parent = None

    def _meets_requirements(self, version, requirements, parent):
        """
        Supports version identifiers can be '==', '!=', '>', '>=', '<', '<=', '*'. Each requirement is delimited by ','
        """
        op_map = {
            '!=': operator.ne,
            '==': operator.eq,
            '=': operator.eq,
            '>=': operator.ge,
            '>': operator.gt,
            '<=': operator.le,
            '<': operator.lt,
        }
    
>       for req in list(requirements.split(',')):
E       AttributeError: 'float' object has no attribute 'split'

lib/ansible/galaxy/collection.py:213: AttributeError
```

```text
version = 1
collection_artifact = (b'/private/var/folders/ng/72llsm517x12c2p18htksyjc0000gn/T/pytest-of-jerry/pytest-6/test-\xc3\x85\xc3\x91\xc5\x9a\xc3...\xc3\x85\xc3\x91\xc5\x9a\xc3\x8c\xce\xb2\xc5\x81\xc3\x88 Collections Input2/ansible_namespace-collection-0.1.0.tar.gz')

    @pytest.mark.parametrize('version', ['1.1.1', 1.1, 1])
    def test_build_requirement_from_path_with_manifest(version, collection_artifact):
        manifest_path = os.path.join(collection_artifact[0], b'MANIFEST.json')
        manifest_value = json.dumps({
            'collection_info': {
                'namespace': 'namespace',
                'name': 'name',
                'version': version,
                'dependencies': {
                    'ansible_namespace.collection': '*'
                }
            }
        })
        with open(manifest_path, 'wb') as manifest_obj:
            manifest_obj.write(to_bytes(manifest_value))
    
>       actual = collection.CollectionRequirement.from_path(collection_artifact[0], True)

test/units/galaxy/test_collection_install.py:184:
```
