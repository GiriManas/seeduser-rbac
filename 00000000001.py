import builtins
import os
import sys
import logging

# 1️⃣ Disable all print() calls globally (applies to imported modules too)
builtins.print = lambda *a, **k: None

# 2️⃣ Remove any old log handlers
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# 3️⃣ Limit all logging to CRITICAL only
logging.basicConfig(level=logging.CRITICAL)
logging.getLogger().setLevel(logging.CRITICAL)

# 4️⃣ Redirect OS-level stdout and stderr (silences C/C++ backend prints)
sys.stdout.flush()
sys.stderr.flush()
devnull = os.open(os.devnull, os.O_WRONLY)
os.dup2(devnull, 1)
os.dup2(devnull, 2)
os.close(devnull)