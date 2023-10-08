import wx
from typing import Callable


class Button(wx.Button):
    """A wx.button that allows you to set a callback for the button clicked in the initializer."""

    def __init__(
        self,
        parent: wx.Window,
        label: str,
        callback: Callable[[wx.CommandEvent], None],
        **kwargs
    ):
        super().__init__(parent, label=label, **kwargs)
        self.Bind(wx.EVT_BUTTON, callback)
        self.callback = callback
