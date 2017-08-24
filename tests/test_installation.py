"""
Role tests
"""

import pytest
from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner('.molecule/ansible_inventory').get_hosts('all')


@pytest.mark.parametrize('name', [
    ('foo'),
    ('bar'),
])
def test_users(host, name):
    """
    Check users exists
    """

    assert host.user(name).exists


@pytest.mark.parametrize('item_type,path,target,user,group,mode', [
    (None, '/home/foo/.ssh', None, None, None, None),
    (None, '/home/foo/foo', None, None, None, None),
    (None, '/home/foo/bar', None, None, None, None),
    ('file', '/home/foo/.bashrc', None, 'foo', 'foo', 0o644),
    (None, '/home/bar/.bashrc', None, None, None, None),
    ('directory', '/home/bar/.ssh', None, 'bar', 'bar', 0o700),
    ('directory', '/home/bar/foo', None, 'bar', 'bar', 0o750),
    ('directory', '/home/bar/bar', None, 'bar', 'bar', 0o755),
    ('symlink', '/home/bar/bar/foolink', '/home/bar/foo', 'bar', 'bar', 0o777),
    ('file', '/home/bar/bar/foo.txt', None, 'bar', 'bar', 0o640),
    ('file', '/home/bar/bar/bar.txt', None, 'bar', 'bar', 0o640),
])
def test_users_items(host, item_type, path, target, user, group, mode):
    """
    Check foo user home files
    """

    current_item = host.file(path)

    if item_type is None:
        assert current_item.exists is False
    else:
        if item_type == 'file':
            assert current_item.is_file
        elif item_type == 'directory':
            assert current_item.is_directory
        elif item_type == 'symlink':
            assert current_item.is_symlink
            assert current_item.linked_to == target

        assert current_item.exists
        assert current_item.user == user
        assert current_item.group == group
        assert current_item.mode == mode


def test_skel_template_content(host):
    """
    Ensure template has worked
    """

    assert host.file('/home/bar/bar/bar.txt').contains('Ansible managed')
