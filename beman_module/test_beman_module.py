import beman_module

def test_parse_args():
    def plain_update():
        args = beman_module.parse_args(['update'])
        assert args.command == 'update'
        assert not args.remote
        assert not args.beman_module
    plain_update()
    def update_remote():
        args = beman_module.parse_args(['update', '--remote'])
        assert args.command == 'update'
        assert args.remote
        assert not args.beman_module
    update_remote()
    def update_path():
        args = beman_module.parse_args(['update', 'my_beman_module'])
        assert args.command == 'update'
        assert not args.remote
        assert args.beman_module == 'my_beman_module'
    update_path()
    def update_path_remote():
        args = beman_module.parse_args(['update', '--remote', 'my_beman_module'])
        assert args.command == 'update'
        assert args.remote
        assert args.beman_module == 'my_beman_module'
    update_path_remote()
