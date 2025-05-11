import beman_module
import pathlib
import tempfile

def test_parse_args():
    def plain_update():
        args = beman_module.parse_args(['update'])
        assert args.command == 'update'
        assert not args.remote
        assert not args.beman_module_path
    plain_update()
    def update_remote():
        args = beman_module.parse_args(['update', '--remote'])
        assert args.command == 'update'
        assert args.remote
        assert not args.beman_module_path
    update_remote()
    def update_path():
        args = beman_module.parse_args(['update', 'infra/'])
        assert args.command == 'update'
        assert not args.remote
        assert args.beman_module_path == 'infra/'
    update_path()
    def update_path_remote():
        args = beman_module.parse_args(['update', '--remote', 'infra/'])
        assert args.command == 'update'
        assert args.remote
        assert args.beman_module_path == 'infra/'
    update_path_remote()
    def plain_add():
        args = beman_module.parse_args(['add', 'git@github.com:bemanproject/infra.git'])
        assert args.command == 'add'
        assert args.repository == 'git@github.com:bemanproject/infra.git'
        assert not args.path
    plain_add()
    def add_path():
        args = beman_module.parse_args(
            ['add', 'git@github.com:bemanproject/infra.git', 'infra/'])
        assert args.command == 'add'
        assert args.repository == 'git@github.com:bemanproject/infra.git'
        assert args.path == 'infra/'
    add_path()
    def plain_status():
        args = beman_module.parse_args(['status'])
        assert args.command == 'status'
        assert args.paths == []
    plain_status()
    def status_one_module():
        args = beman_module.parse_args(['status', 'infra/'])
        assert args.command == 'status'
        assert args.paths == ['infra/']
    status_one_module()
    def status_multiple_modules():
        args = beman_module.parse_args(['status', 'infra/', 'foobar/'])
        assert args.command == 'status'
        assert args.paths == ['infra/', 'foobar/']
    status_multiple_modules()

def test_parse_beman_module_file():
    def valid_file():
        tmpfile = tempfile.NamedTemporaryFile()
        tmpfile.write('[beman_module]\n'.encode('utf-8'))
        tmpfile.write(
            'remote=git@github.com:bemanproject/infra.git\n'.encode('utf-8'))
        tmpfile.write(
            'commit_hash=9b88395a86c4290794e503e94d8213b6c442ae77\n'.encode('utf-8'))
        tmpfile.flush()
        module = beman_module.parse_beman_module_file(tmpfile.name)
        assert module.dirpath == pathlib.Path(tmpfile.name).resolve().parent
        assert module.remote == 'git@github.com:bemanproject/infra.git'
        assert module.commit_hash == '9b88395a86c4290794e503e94d8213b6c442ae77'
    valid_file()
    def invalid_file_missing_remote():
        threw = False
        try:
            tmpfile = tempfile.NamedTemporaryFile()
            tmpfile.write('[beman_module]\n'.encode('utf-8'))
            tmpfile.write(
                'commit_hash=9b88395a86c4290794e503e94d8213b6c442ae77\n'.encode('utf-8'))
            tmpfile.flush()
            module = beman_module.parse_beman_module_file(tmpfile.name)
        except:
            threw = True
        assert threw
    invalid_file_missing_remote()
    def invalid_file_missing_commit_hash():
        threw = False
        try:
            tmpfile = tempfile.NamedTemporaryFile()
            tmpfile.write('[beman_module]\n'.encode('utf-8'))
            tmpfile.write(
                'remote=git@github.com:bemanproject/infra.git\n'.encode('utf-8'))
            tmpfile.flush()
            module = beman_module.parse_beman_module_file(tmpfile.name)
        except:
            threw = True
        assert threw
    invalid_file_missing_commit_hash()
    def invalid_file_wrong_section():
        threw = False
        try:
            tmpfile = tempfile.NamedTemporaryFile()
            tmpfile.write('[invalid]\n'.encode('utf-8'))
            tmpfile.write(
                'remote=git@github.com:bemanproject/infra.git\n'.encode('utf-8'))
            tmpfile.write(
                'commit_hash=9b88395a86c4290794e503e94d8213b6c442ae77\n'.encode('utf-8'))
            tmpfile.flush()
            module = beman_module.parse_beman_module_file(tmpfile.name)
        except:
            threw = True
        assert threw
    invalid_file_wrong_section()
