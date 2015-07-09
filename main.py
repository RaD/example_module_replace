from __future__ import print_function

"""Demo of dynamic module replacing.

Each module consists of a Thread-like class. To control the execution
this thread we use Event object. Also we keep MTIME value of a module
file because it help us to make decision of reloading module.

"""

import threading
import pkgutil
import os
import time
import sys


PREFIX_CLASS = 'Thread'
RELOAD_TIMEOUT = 10


class AttrDict(dict):
    """http://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute-in-python"""
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


last_info = AttrDict()  # here we keep an information about each thread
path = os.path.join(os.path.dirname(__file__), 'tasks')


def get_class(module):
    """Returns the class name. Each class has to begin with PREFIX."""
    try:
        class_name = [i for i in dir(module) if i.startswith(PREFIX_CLASS)][0]
    except IndexError:
        return None
    else:
        return getattr(module, class_name)


class ReloadException(Exception):
    pass


def reload_module(module_name):
    """Reloads and returns the module by its name."""
    full_name = '{}.{}'.format(path, module_name)

    # try to import the module
    try:
        module = __import__(full_name, fromlist=[module_name])
    except ImportError:
        msg = 'Could not import {} module.'.format(module_name)
        raise ReloadException(msg)

    # get original name
    pycfile = module.__file__
    pyfile = pycfile.replace('.pyc', '.py')

    # check the module existence and readability
    try:
        with open (pyfile, 'rU') as f:
            code = f.read()
    except:
        msg = 'Error opening file: {}.  Does it exist?'.format(pyfile)
        raise ReloadException(msg)

    # compile loaded source code
    try:
        compile(code, module_name, 'exec')
    except:
        msg = 'Error in compilation: {}'.format(str(sys.exc_info()[0]))
        raise ReloadException(msg)

    # check the consistence of source code
    try:
        execfile(pyfile)
    except:
        msg = 'Error in execution: {}'.format(str(sys.exc_info()[0]))
        raise ReloadException(msg)

    # and finally reload the module
    return reload(sys.modules[full_name])


def main_loop():
    while True:
        modules = pkgutil.iter_modules(path=[path])
        for loader, module_name, is_package in modules:
            info = last_info.get(module_name)
            mtime = os.path.getmtime(os.path.join('.', 'tasks', module_name+'.py'))

            if not info:
                # initial import
                module = __import__('{}.{}'.format(path, module_name),
                                    fromlist=[module_name])
            else:
                # repeat importing
                if info.mtime == mtime:
                    continue
                else:
                    info.event.set()
                module = reload_module(module_name)

            # restart thread
            klass = get_class(module)
            event = threading.Event()
            thread = klass(event)
            thread.start()
            last_info[module_name] = AttrDict(mtime=mtime, thread=thread, event=event)

        time.sleep(RELOAD_TIMEOUT)

if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        for info in last_info.values():
            info.event.set()

sys.exit(0)
