py-cmpe
=======

Python convenience functions for computer engineering

These functions are intended to be used in an interactive Python
shell (i.e., like a calculator).  To automatically include these
functions for all Python shells, add the following to ~/.python.start.py:

    import os, sys
    # Append home directory to PYTHONPATH
    sys.path.append(os.path.expanduser("~"))
    from cmpe import *

Alternatively, you can also simply invoke this script and it will
launch a basic Python interactive shell with these functions available
in the global namespace.

To update to the latest version of this script, simply run:

    $ curl -O https://raw.github.com/nacase/py-cmpe/master/cmpe.py

Author: Nate Case <nacase@gmail.com>
