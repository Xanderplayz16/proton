import importlib

def patch(name):
    ptch = importlib.import_module("proton.patches." + name)

    ptch.__patch__()