# beman_module.py

## What is this script?

beman_module.py provides some of the features of `git submodule`, adding child git repositories to a parent git repository, but unlike with `git submodule`, the entire child repo is directly checked in, so only maintainers, not users, need to run this script. The command line interface mimics `git submodule`'s.

## How do I add a beman_module to my repository?

The first `beman_module` you should add is this repository, `infra/`, which you can bootstrap by running:

```
curl -s https://raw.githubusercontent.com/bemanproject/infra/refs/heads/main/beman_module/beman_module.py | python3 - add https://github.com/bemanproject/infra.git
```

Once that's added, you can run the script from `infra/beman_module/beman_module.py`.

## How do I update a beman_module to the latest trunk?

Simply run `beman_module.py update --remote` to update all beman_modules to latest trunk, or e.g. `beman_module.py update --remote infra` to update only a specific one.

## How does it work under the hood?

Along with the files from the child repository, it creates a dotfile called `.beman_module`, which looks like this:

```
[beman_module]
remote=https://github.com/bemanproject/infra.git
commit_hash=9b88395a86c4290794e503e94d8213b6c442ae77
```

## How can I make CI ensure that my beman_modules are in a valid state?

Add a test to CI that ensures that the following succeeds:

```
! beman_module.py status | grep -F '+'
```

This will fail if the contents of the directory don't match what's specified in the `.beman_module` file.
