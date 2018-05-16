import wx.adv
import wx

TRAY_TOOLTIP = 'Scanner Web-Agent'
TRAY_ICON = 'img/24x24.png'

class App(wx.App):
    def OnInit(self):
        frame = wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)
        return True

class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        icon = wx.Icon(wx.Bitmap(TRAY_ICON))
        self.SetIcon(icon, TRAY_TOOLTIP)
        self.Bind(wx.adv.EVT_TASKBAR_RIGHT_DOWN, self.BuildPopupMenu)

    def BuildPopupMenu(self, event):
        self.CreatePopupMenu()

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()
        raise exitingApplication

class exitingApplication(BaseException):
    pass

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item