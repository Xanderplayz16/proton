from .patches.p_bottle import __patch__ as bottle_patch
from .core.window import Window
bottle_patch()
__version__ = "0.1.1"
#wv.DRAG_REGION_SELECTOR = "drag-region"