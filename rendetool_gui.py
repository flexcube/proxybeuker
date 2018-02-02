
import wx


class MyDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyDialog.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetSize((567, 264))
        self.button_6 = wx.Button(self, wx.ID_ANY, "Input Folder")
        self.text_ctrl_4 = wx.TextCtrl(
            self, wx.ID_ANY, "None", style=wx.TE_READONLY)
        self.button_4 = wx.Button(self, wx.ID_ANY, "Output Folder")
        self.text_ctrl_3 = wx.TextCtrl(
            self, wx.ID_ANY, "None", style=wx.TE_READONLY)
        self.button_7 = wx.Button(self, wx.ID_ANY, "Start conversion")
        self.gauge_1 = wx.Gauge(self, wx.ID_ANY, 10)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyDialog.__set_properties
        self.SetTitle("FK Render Tool")
        self.SetSize((567, 264))
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.button_6.SetMinSize((110, 21))
        self.text_ctrl_4.SetMinSize((200, 22))
        self.button_4.SetMinSize((110, 21))
        self.text_ctrl_3.SetMinSize((200, 22))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyDialog.__do_layout
        sizer_3 = wx.StaticBoxSizer(wx.StaticBox(
            self, wx.ID_ANY, "sizer_3"), wx.VERTICAL)
        sizer_7 = wx.BoxSizer(wx.VERTICAL)
        sizer_6 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5.Add(self.button_6, 0, 0, 0)
        sizer_5.Add(self.text_ctrl_4, 0, 0, 0)
        sizer_3.Add(sizer_5, 5, wx.ALL | wx.SHAPED, 0)
        sizer_4.Add(self.button_4, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 0)
        sizer_4.Add(self.text_ctrl_3, 1, 0, 0)
        sizer_3.Add(sizer_4, 23, wx.ALL | wx.SHAPED, 0)
        label_1 = wx.StaticText(
            self, wx.ID_ANY, "Progress: 1/10 Errors: Weolr: 10")
        sizer_6.Add(label_1, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_3.Add(sizer_6, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        sizer_7.Add(self.button_7, 0, wx.ALIGN_CENTER, 0)
        sizer_7.Add(self.gauge_1, 0, wx.ALIGN_CENTER | wx.SHAPED, 0)
        sizer_3.Add(sizer_7, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_3)
        self.Layout()
        # end wxGlade

# end of class MyDialog


class MyApp(wx.App):
    def OnInit(self):
        self.dialog = MyDialog(None, wx.ID_ANY, "")
        self.SetTopWindow(self.dialog)
        self.dialog.ShowModal()
        self.dialog.Destroy()
        return True

# end of class MyApp


if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
