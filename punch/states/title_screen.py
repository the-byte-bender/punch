import wx
from .state import State
from .gameplay import Gameplay
from ..ui_helpers.button import Button


class TitleScreen(wx.Dialog, State):
    def __init__(self, parent: wx.Window | None = None, title: str = "Title screen"):
        wx.Dialog.__init__(self, parent, title=title)
        State.__init__(self)

    def on_push(self):
        super().on_push()
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(wx.StaticText(panel, label="Welcome!"), wx.ALIGN_CENTER | wx.BOTTOM)
        item_flags = wx.EXPAND | wx.TOP | wx.BOTTOM | wx.ALIGN_LEFT
        vbox.Add(Button(panel, "&Play game", self.on_play), item_flags)
        vbox.Add(
            Button(panel, "&Exit", self.on_exit_button, id=wx.ID_CANCEL), item_flags
        )
        panel.SetSizerAndFit(vbox)

    def on_pop(self):
        super().on_pop()
        self.Destroy()

    def on_enter(self):
        super().on_enter()
        game = self.get_root_state()
        self.Show(True)
        game.Show(False)

    def on_exit(self):
        super().on_exit()
        game = self.get_root_state()
        game.Show(True)
        self.Show(False)

    def on_play(self, event):
        self.get_root_state().append(Gameplay())

    def on_exit_button(self, event):
        self.Destroy()
        self.get_root_state().Destroy()
