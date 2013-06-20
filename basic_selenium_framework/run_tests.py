#!/usr/bin/python

import os
import re
import nose
import logging
import sys
import argparse
from noseplugins import xunitmultiprocess, multiprocess, capture, ignoredoc

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--timeout', default='600')
parser.add_argument('-p','--processes', default='4')
parser.add_argument('-i','--invisible', action="store_true", default=False)
parser.add_argument('-s', '--select', dest='select', nargs='*', action='append')
opts = parser.parse_args()

multiprocess._instantiate_plugins = [capture.Capture, xunitmultiprocess.Xunitmp, ignoredoc.IgnoreDocstrings]
handler = logging.NullHandler()
multiprocess.log.addHandler(handler)

argv = ['nosetests', '-v', '--with-xunitmp','--with-ignore-docstrings','--xunit-file=nosetests.xml']

mp_plugins = [capture.Capture(), multiprocess.MultiProcess(), xunitmultiprocess.Xunitmp(), ignoredoc.IgnoreDocstrings()]
mp_argv = argv + ['--processes=%s' % opts.processes,'--process-timeout=%s' % opts.timeout]


if opts.invisible:
    print "Running in headless mode..."
    import pyvirtualdisplay
    display = pyvirtualdisplay.Display(visible=0, size=(800,600))
    display.start()

try:
    if opts.select:
        selected = []
        for s in opts.select:
            for t in s:
                if os.path.isfile(t):
                    selected.append(t)
                else:
                    top, sep, bottom = t.partition('.')
                    filename = '%s.py' % top
                    if not os.path.exists(filename):
                        print "ERROR: could not locate file %s" % filename
                        sys.exit(1)
                    else:
                        selected.append('%s:%s' % (filename, bottom))
        
        if len(selected) == 0:
            print "ERROR: --select used but no selections given"
        elif [ t for t in selected if not re.search(r'[A-Z]|(!?py)', t.split('.')[-1]) ]:
            print "WARNING: Individual test method(s) selected, disabling multiprocessing"
            nose.core.TestProgram(argv=argv+selected, plugins=mp_plugins, exit=False)
        else:
            nose.core.TestProgram(argv=mp_argv+selected, plugins=mp_plugins, exit=False)
    else:
        nose.core.TestProgram(argv=mp_argv, plugins=mp_plugins, exit=False)
finally:
    if opts.invisible:
        display.stop()
