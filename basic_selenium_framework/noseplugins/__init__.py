import capture
import ignoredoc

try:
    import multiprocess
    import xunitmultiprocess
except ImportError:
    # fails for python 2.5
    pass
