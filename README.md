Snippets for SaltStack
========================================

This repository contains snippets files for [SaltStack](http://www.saltstack.com/) state files.

Contents
---------

- `gen-snippets.py`: script used for generating snippets from salt source
- `snippets/*`: generated snippets go here

Installation
--------------

You need to install a snippet engine first. Currently [neosnippet](https://github.com/Shougo/neosnippet.vim)
is supported, and thanks to neosnippet's compatibility to [vim-snipmate](https://github.com/garbas/vim-snipmate),
it is also supported.

I will only cover configuration for neosnippet, since I only use this.
You are welcome to help me complete this instruction.

1. Save the ``snippets/`` directory somewhere vim can find, like:

   ```sh
   cd ~/.vim/
   git clone https://github.com/StephenPCG/vim-snippets-salt/
   # you may also only copy the snippets/ directory here
   ```

2. Add the ``snippets/`` directory to ``g:neosnippet#snippets_directory``:

   ```vim
   " g:neosnippet#snippets_directory is a comma-seperated string or list,
   " I prefer using list.
   let g:neosnippet#snippets_directory = [$HOME . "/.vim/vim-snippets-salt/snippets/"]
   ```

3. Since different versions of salt have different amount of states functions,
   you can generate snippets for each version you need. Snippets are named as
   ``sls-$version.sls``, so you need to set ``g:neosnippet#scope_alias`` to tell
   neosnippet which file to use. e.g.

   ```vim
   " g:neosnippet#scope_aliases is a dictionary, initialize it if you haven't done it
   let g:neosnippet#scope_aliases = {}
   let g:neosnippet#scope_aliases['sls'] = 'sls-0.17.2'
   ```

   ``scope_aliases[filetype]`` is a comma-seperated string, all listed variant
   snippets will be loaded, so make sure you only list one here, or multiple versions
   if you realy need.

   For vim-snipmate, there is also a ``g:snipMate.scope_aliases`` which does the same thing.

Generating Snippets
----------------------

You can generate snippets by yourself. You have to get [saltstack source code](https://github.com/saltstack/salt.git)
and make sure ``salt`` is importable. The ``gen-snippets.py`` will ``import salt.states.*``
and find functions for each module, if any required library is missing, the generation will fail.

```
# This will try to import salt from system, detect its version, and save output to snippets/sls-$version.snippets
./gen-snippets.py
```
If you have salt source stored elsewhere, or want to generate for a specific version, you can do like this:

```
cd ~/salt/
git checkout v0.17.2
/path/to/gen-snippets.py -p ~/salt/
```
Sometimes, we would like to ignore function argument ``name``, since in most cases we don't need it,
you can ignore it:

```
./gen-snippets.py -i name
```

``-i`` may be specified multiple times to ignore multiple args.

I have added two pre-generated snippets for version ``0.17.2`` and ``2014.1.5`` with ``name`` ignored.

Screenshot
--------------

![ScreenShot](https://onebitbug.me/images/uploads/vim-snippets-salt.gif)
