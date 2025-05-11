import beman_module

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
