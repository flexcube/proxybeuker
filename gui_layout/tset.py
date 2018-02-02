import wx

from wx.lib.pubsub import pub

# This message requires the argument "text"
MSG_CHANGE_TEXT = "change.text"


class Page(wx.Panel):
    def __init__(self, parent):
        self.textCtrl = wx.TextCtrl(self, -1, "THIS IS A PAGE OBJECT ",
                                    style=wx.TE_MULTILINE | wx.BORDER_NONE)
        ...

        pub.subscribe(self.onChangeText, MSG_CHANGE_TEXT)

    def onChangeText(self, text):
        self.textCtrl.AppendText(text)


class MainFrame(wx.Frame):
    ...

    def onButtonMessage(self, event):
        pub.sendMessage(MSG_CHANGE_TEXT, text="Yeah this works ")


if __name__ == "__main__":
    app = wx.App()
    MainFrame().Show()
    app.MainLoop()
