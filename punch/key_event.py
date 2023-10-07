import wx
class KeyEvent:
    """A key event."""
    def __init__(self, type: int, key_code: int, modifiers: int):
        self.type = type
        self.key_code = key_code
        self.modifiers = modifiers
    @classmethod
    def from_wx_event(cls, type: int, event: wx.KeyEvent):
        return cls(type, event.GetKeyCode(), event.GetModifiers())
    @property
    def is_ctrl_pressed(self):
        return self.modifiers & wx.MOD_CONTROL
    @property
    def is_alt_pressed(self):
        return self.modifiers & wx.MOD_ALT
    @property
    def is_shift_pressed(self):
        return self.modifiers & wx.MOD_SHIFT