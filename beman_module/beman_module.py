#!/usr/bin/env python3

import argparse
import filecmp
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

def directory_compare(dir1, dir2, ignore):
    compared = filecmp.dircmp(dir1, dir2, ignore=ignore)
    if compared.left_only or compared.right_only or compared.diff_files:
        return False
    for common_dir in compared.common_dirs:
        path1 = os.path.join(dir1, common_dir)
        path2 = os.path.join(dir2, common_dir)
        if not directory_compare(path1, path2, ignore):
            return False
    return True

class BemanModule:
    def __init__(self, dirpath, url, commit_hash):
        self.dirpath = dirpath
        self.url = url
        self.commit_hash = commit_hash

def get_beman_module(dir):
    with open(os.path.join(dir, '.beman_module'), 'r') as f:
        return BemanModule(dir, f.readline().strip(), f.readline().strip())

def find_beman_module_dirs_in(dir):
    assert os.path.isdir(dir)
    result = []
    for dirpath, _, filenames in os.walk(dir):
        if '.beman_module' in filenames:
            result.append(dirpath)
    return result

def pull_beman_module_into_tmpdir(beman_module):
    tmpdir = tempfile.TemporaryDirectory()
    subprocess.run(
        ['git', 'clone', beman_module.url, tmpdir.name], capture_output=True, check=True)
    subprocess.run(
        ['git', '-C', tmpdir.name, 'reset', '--hard', beman_module.commit_hash],
        capture_output=True, check=True)
    return tmpdir

def beman_module_pull(beman_module):
    print(
        'Pulling', beman_module.url, 'at commit', beman_module.commit_hash, 'to',
        beman_module.dirpath)
    tmpdir = pull_beman_module_into_tmpdir(beman_module)
    shutil.rmtree(os.path.join(tmpdir.name, '.git'))
    shutil.copytree(tmpdir.name, beman_module.dirpath, dirs_exist_ok=True)

def beman_module_check(beman_module):
    print(
        'Checking', beman_module.dirpath, 'equivalence with', beman_module.url, 'at commit',
        beman_module.commit_hash)
    tmpdir = pull_beman_module_into_tmpdir(beman_module)
    if not directory_compare(tmpdir.name, beman_module.dirpath, ['.beman_module', '.git']):
        print(
            'Mismatch between', beman_module.dirpath, 'and', beman_module.url, 'at commit',
            beman_module.commit_hash, file=sys.stderr)
        sys.exit(1)

def update_command(remote, beman_module_path):
    pass

def add_command(repository, path):
    pass

def status_command(paths):
    pass

def get_parser():
    parser = argparse.ArgumentParser(description='Beman pseudo-submodule tool')
    subparsers = parser.add_subparsers(dest='command', help='available commands')
    parser_update = subparsers.add_parser('update', help='update beman_modules')
    parser_update.add_argument(
        '--remote', action='store_true',
        help='update a beman_module to its latest from upstream')
    parser_update.add_argument(
        'beman_module_path', nargs='?', help='relative path to the beman_module to update')
    parser_add = subparsers.add_parser('add', help='add a new beman_module')
    parser_add.add_argument('repository', help='git repository to add')
    parser_add.add_argument(
        'path', nargs='?', help='path where the repository will be added')
    parser_status = subparsers.add_parser(
        'status', help='show the status of beman_modules')
    parser_status.add_argument('paths', nargs='*')
    return parser

def parse_args(args):
    return get_parser().parse_args(args);

def usage():
    return get_parser().format_help()

def run_command(args):
    if args.command == 'update':
        update_command(args.remote, args.beman_module_path)
    elif args.command == 'add':
        add_command(args.repository, args.path)
    elif args.command == 'status':
        status_command(args.paths)
    else:
        print(usage(), file=sys.stderr)
        sys.exit(1)

def main():
    args = parse_args(sys.argv[1:])
    run_command(args)
    # script_path = pathlib.Path(__file__).resolve().parent
    # beman_module_directory = script_path.parent
    # infra_parent = beman_module_directory.parent
    # beman_module_dirs = find_beman_module_dirs_in(infra_parent)
    # print('Found beman_modules at: ', beman_module_dirs)
    # beman_modules = [get_beman_module(dir) for dir in beman_module_dirs]
    # for beman_module in beman_modules:
    #     if args.pull:
    #         beman_module_pull(beman_module)
    #     elif args.check:
    #         beman_module_check(beman_module)
    #     else:
    #         raise Exception('Specify either --pull or --check')

if __name__ == '__main__':
    main()
