#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import glob
import inspect
import argparse
import importlib

class NoDefault():
    """This is a virtual class to represent function args with no
    default value"""
    pass

def get_salt_version():
    import salt as _salt
    return _salt.__version__

def list_states_modules():
    """ Scan for all states modules, load them and return.

    Returns a list of states modules (imported)
    """
    import salt.states as _states
    states_path = os.path.dirname(_states.__file__)
    for module_file in glob.glob(states_path + "/*.py"):
        module_name = os.path.basename(module_file).replace(".py", "")
        module = importlib.import_module("salt.states." + module_name)
        yield module

def list_module_funcs(module):
    """ Scan for all states functions in a module.

    Returns a list of tupple:
        (module_name, function_name, [(arg1, default), (arg2, default) ...])
    """
    module_name = module.__name__.replace("salt.states.", "")
    for (name, member) in inspect.getmembers(module):
        if inspect.isfunction(member) and not name.startswith("_"):
            args, _, _, defaults = inspect.getargspec(member)

            if defaults is None:
                defaults = []

            if len(args) != len(defaults):
                defaults = [NoDefault()] * (len(defaults) - len(args)) + list(defaults)

            yield (module_name, name, zip(args, defaults))

def gen_snippet(module_name, function_name, argspec, ignore_args):
    """ Generate snippet for given function.
    """
    lines = []
    lines.append("snippet %s.%s" % (module_name, function_name))
    lines.append("  %s:" % module_name)
    lines.append("    - %s" % function_name)
    idx = 0
    for arg, default in argspec:
        if arg in ignore_args:
            continue
        idx += 1
        if default == '':
            default = "''"
        if isinstance(default, NoDefault):
            default = ''
        lines.append("    - %s: ${%s:%s}" % (arg, idx, default))
    lines.append("")

    return "\n".join(lines)

def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--engine", default="neosnippet",
            help="snippet engine: neosnippet, ultisnips")
    parser.add_argument("-i", "--ignore-args", default=[],
            action="append", help="ignore args, may be repeated")
    parser.add_argument("-p", "--salt-path", default=None,
            help="salt source path")

    return parser.parse_args(sys.argv[1:])

def main():
    args = parseargs()

    if args.engine != "neosnippet":
        print "Only 'neosnippet' is supported currently."
        sys.exit(0)

    if args.salt_path is not None:
        sys.path.insert(0, args.salt_path)

    salt_version = get_salt_version()
    output_path = os.path.join(os.path.dirname(__file__), "snippets")
    output_file = os.path.join(output_path, "sls-%s.snippets" % salt_version)

    with open(output_file, "w+") as fp:
        for module in list_states_modules():
            for module_name, function_name, argspec in list_module_funcs(module):
                fp.write(gen_snippet(module_name, function_name, argspec, args.ignore_args))

if __name__ == '__main__':
    main()
