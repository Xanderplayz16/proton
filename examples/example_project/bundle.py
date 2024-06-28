#!/usr/bin/env python
import os,sys
print("Bundlr-zstd 1.0")
print("Argv = "+str(sys.argv))
os.system(f"cd {sys.argv[1]} && tar cf - * | zstd -19 | base64 --wrap=0 > /tmp/compressed.t64")
os.system("cd ..")
with open("/tmp/compressed.t64") as f:
    compressed = f.read()
with open("a.out", "w") as f:
    f.write(f"#!/bin/sh\nexport TMP_DIR=$(mktemp -d) \necho '{compressed}' | base64 -d | zstd -d | tar xf - -C $TMP_DIR\ncd $TMP_DIR\nchmod +x $TMP_DIR/{sys.argv[2]}\n$TMP_DIR/{sys.argv[2]} $@\nrm -rf $TMP_DIR")
