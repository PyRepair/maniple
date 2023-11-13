The functions inside test file that is used for testing are:

```python
def call_galaxy_cli(args):

def artifact_json(namespace, name, version, dependencies, server):

def artifact_versions_json(namespace, name, versions, galaxy_api, available_api_versions=None):

def error_json(galaxy_api, errors_to_return=None, available_api_versions=None):

def reset_cli_args():

def collection_artifact(request, tmp_path_factory):

def galaxy_server():

def test_build_requirement_from_path(collection_artifact):

def test_build_requirement_from_path_with_manifest(version, collection_artifact):

def test_build_requirement_from_path_invalid_manifest(collection_artifact):

def test_build_requirement_from_path_no_version(collection_artifact, monkeypatch):

def test_build_requirement_from_tar(collection_artifact):

def test_build_requirement_from_tar_fail_not_tar(tmp_path_factory):

def test_build_requirement_from_tar_no_manifest(tmp_path_factory):

def test_build_requirement_from_tar_no_files(tmp_path_factory):

def test_build_requirement_from_tar_invalid_manifest(tmp_path_factory):

def test_build_requirement_from_name(galaxy_server, monkeypatch):

def test_build_requirement_from_name_with_prerelease(galaxy_server, monkeypatch):

def test_build_requirment_from_name_with_prerelease_explicit(galaxy_server, monkeypatch):

def test_build_requirement_from_name_second_server(galaxy_server, monkeypatch):

def test_build_requirement_from_name_missing(galaxy_server, monkeypatch):

def test_build_requirement_from_name_401_unauthorized(galaxy_server, monkeypatch):

def test_build_requirement_from_name_single_version(galaxy_server, monkeypatch):

def test_build_requirement_from_name_multiple_versions_one_match(galaxy_server, monkeypatch):

def test_build_requirement_from_name_multiple_version_results(galaxy_server, monkeypatch):

def test_add_collection_requirements(versions, requirement, expected_filter, expected_latest):

def test_add_collection_requirement_to_unknown_installed_version(monkeypatch):

def test_add_collection_wildcard_requirement_to_unknown_installed_version():

def test_add_collection_requirement_with_conflict(galaxy_server):

def test_add_requirement_to_existing_collection_with_conflict(galaxy_server):

def test_add_requirement_to_installed_collection_with_conflict():

def test_add_requirement_to_installed_collection_with_conflict_as_dep():

def test_install_skipped_collection(monkeypatch):

def test_install_collection(collection_artifact, monkeypatch):

def test_install_collection_with_download(galaxy_server, collection_artifact, monkeypatch):

def test_install_collections_from_tar(collection_artifact, monkeypatch):

def test_install_collections_existing_without_force(collection_artifact, monkeypatch):

def test_install_collection_with_circular_dependency(collection_artifact, monkeypatch):
```
