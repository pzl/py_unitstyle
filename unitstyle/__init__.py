try:
    from unitstyle.unitstyle import TestRunner
except ImportError:
    from unitstyle import TestRunner # this worked better for python 2.7 venv
