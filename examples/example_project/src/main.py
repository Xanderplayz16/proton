import sys
sys.path.append("../../")
import proton as pt
win = pt.Window('A Proton webapp', '../web', frameless=False, easy_drag=False)
win.start(debug=True, gui="qt")
document=pt.Document(win)