import wx


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = kwds.get(
            "style", 0) | wx.CAPTION | wx.CLIP_CHILDREN | wx.CLOSE_BOX | wx.FRAME_NO_TASKBAR | wx.ICONIZE | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((611, 497))
        self.panel_1 = wx.Panel(self, wx.ID_ANY)
        self.input_folder_button = wx.Button(
            self.panel_1, wx.ID_ANY, "Input Folder")
        self.text_ctrl_1 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "None")
        self.button_2 = wx.Button(self.panel_1, wx.ID_ANY, "Output Folder")
        self.text_ctrl_2 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "None")
        self.button_3 = wx.Button(self.panel_1, wx.ID_ANY, "Start")
        self.Bind(wx.EVT_BUTTON, self.input_button_click,
                  self.input_folder_button)
        self.text_ctrl_3 = wx.TextCtrl(
            self.panel_1, wx.ID_ANY, "Progress...", style=wx.TE_MULTILINE)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("Proxy Tool")
        self.SetBackgroundColour(wx.Colour(0, 0, 0))
        self.input_folder_button.SetMinSize((111, 20))
        self.input_folder_button.SetFont(
            wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.text_ctrl_1.SetMinSize((200, 22))
        self.button_2.SetFont(
            wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.text_ctrl_2.SetMinSize((200, 22))
        self.input_folder_button.SetFont(
            wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.text_ctrl_3.SetMinSize((400, 100))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        fklogo = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(
            "/Users/Kevin/Desktop/Screen Shot 2018-02-01 at 20.36.56.png", wx.BITMAP_TYPE_ANY))
        sizer_1.Add(fklogo, 0, wx.ALIGN_CENTER, 0)
        sizer_3.Add(self.input_folder_button, 0, 0, 0)
        sizer_3.Add(self.text_ctrl_1, 0, wx.LEFT, 10)
        sizer_2.Add(sizer_3, 1, wx.ALIGN_CENTER, 0)
        sizer_4.Add(self.button_2, 0, 0, 0)
        sizer_4.Add(self.text_ctrl_2, 0, wx.LEFT, 10)
        sizer_2.Add(sizer_4, 1, wx.ALIGN_CENTER, 0)
        sizer_2.Add(self.input_folder_button, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        sizer_2.Add(self.text_ctrl_3, 0, wx.ALIGN_CENTER, 0)
        sizer_2.Add((0, 0), 0, 0, 0)
        self.panel_1.SetSizer(sizer_2)
        sizer_1.Add(self.panel_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        self.Centre()
        # end wxGlade

# end of class MyFrame


class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class MyApp


if __name__ == "__main__":
    rendertool = MyApp(0)
    while True:
        rendertool.MainLoop()
