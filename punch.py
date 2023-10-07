import wx
from lib import game


def main():
    app = wx.App()
    g = game.Game()
    g.Show()
    g.start()
    app.MainLoop()


if __name__ == "__main__":
    main()
