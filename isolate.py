import wx
import glob
import subprocess
import logging
import re
import os
import sys  # Can be deleted if error handling in Except is improved
import traceback
import threading


file_metadata = subprocess.Popen(['REDline', '--i', "/Users/Kevin/Downloads/redapptest/input/A004_C014_01061E.RDC/A004_C014_01061E_001.R3D",
                                  '--printMeta', '1'], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


print(str(file_metadata.communicate()))


def main(self):

    files_to_convert = self.scan_folder(self.input_directory)
    print(str(len(files_to_convert)) +
          " item(s) found, press enter to start transcoding \n\n")
    # Start Conversion
    self.proxymaker(files_to_convert)


class RedirectText(object):
    def __init__(self, aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self, string):
        wx.CallAfter(self.out.WriteText, string)


class MyFrame(wx.Frame):

    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = kwds.get(
            "style", 0) | wx.CAPTION | wx.CLIP_CHILDREN | wx.CLOSE_BOX | wx.FRAME_NO_TASKBAR | wx.ICONIZE | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((611, 497))
        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        self.button_1 = wx.Button(self.panel_1, wx.ID_ANY, "Input Folder")
        self.Bind(wx.EVT_BUTTON, self.input_button_click,
                  self.button_1)
        self.text_ctrl_1 = wx.TextCtrl(
            self.panel_1, wx.ID_ANY, "", style=wx.TE_READONLY)

        self.button_2 = wx.Button(self.panel_1, wx.ID_ANY, "Output Folder")
        self.Bind(wx.EVT_BUTTON, self.output_button_click,
                  self.button_2)

        self.text_ctrl_2 = wx.TextCtrl(
            self.panel_1, wx.ID_ANY, "", style=wx.TE_READONLY)
        self.button_3 = wx.Button(self.panel_1, wx.ID_ANY, "Start")
        self.Bind(wx.EVT_BUTTON, self.start_conversion, self.button_3)
        global text_ctrl_3
        self.text_ctrl_3 = wx.TextCtrl(
            self.panel_1, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_NO_VSCROLL | wx.TE_RICH2)
        self.text_ctrl_3.SetDefaultStyle(wx.TextAttr(wx.GREEN, wx.BLACK))
        self.text_ctrl_3.SetBackgroundColour(wx.BLACK)
        self.text_ctrl_3.SetOwnForegroundColour(wx.WHITE)
        self.__set_properties()
        self.__do_layout()
        # end wxGlade

        redir = RedirectText(self.text_ctrl_3)
        sys.stdout = redir

    def write(self, string):
        wx.CallAfter(self.text_ctrl_3.AppendText, string)

    def input_button_click(self, e):
        """ Open a file"""
        # dlg = wx.FileDialog(self, "Choose a file",
        # self.dirname, "", "*.*", wx.FD_OPEN)
        directory_dialog = wx.DirDialog(None, "Choose input directory", "",
                                        wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if directory_dialog.ShowModal() == wx.ID_OK:
            self.input_directory = directory_dialog.GetPath()
            self.text_ctrl_1.SetLabelText(str(self.input_directory))
            print(str(self.input_directory))
        directory_dialog.Destroy()

    def output_button_click(self, e):
        """ Open a file"""
        # dlg = wx.FileDialog(self, "Choose a file",
        # self.dirname, "", "*.*", wx.FD_OPEN)
        directory_dialog = wx.DirDialog(None, "Choose output directory", "",
                                        wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if directory_dialog.ShowModal() == wx.ID_OK:
            self.output_directory = directory_dialog.GetPath()
            self.text_ctrl_2.SetLabelText(str(self.input_directory))
            print(str(self.output_directory))
        directory_dialog.Destroy()

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle(".R3D Proxy Maker")
        self.SetBackgroundColour(wx.Colour(0, 0, 0))
        self.button_1.SetMinSize((111, 20))
        self.button_1.SetFont(
            wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.text_ctrl_1.SetMinSize((200, 22))
        self.button_2.SetFont(
            wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.text_ctrl_2.SetMinSize((200, 22))
        self.button_3.SetFont(
            wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.text_ctrl_3.SetMinSize((600, 100))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        fklogo = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(
            "/Users/Kevin/Downloads/minilogo.png", wx.BITMAP_TYPE_ANY))
        sizer_1.Add(fklogo, 0, wx.ALIGN_CENTER, 0)
        sizer_3.Add(self.button_1, 0, 0, 0)
        sizer_3.Add(self.text_ctrl_1, 0, wx.LEFT, 10)
        sizer_2.Add(sizer_3, 1, wx.ALIGN_CENTER, 0)
        sizer_4.Add(self.button_2, 0, 0, 0)
        sizer_4.Add(self.text_ctrl_2, 0, wx.LEFT, 10)
        sizer_2.Add(sizer_4, 1, wx.ALIGN_CENTER, 0)
        sizer_2.Add(self.button_3, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        sizer_2.Add(self.text_ctrl_3, 0, wx.ALIGN_CENTER, 0)
        sizer_2.Add((0, 0), 0, 0, 0)
        self.panel_1.SetSizer(sizer_2)
        sizer_1.Add(self.panel_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        self.Centre()
        # end wxGlade

    def start_conversion(self, e):
        converter(self.input_directory, self.output_directory)
        self.text_ctrl_3.AppendText(str(converter.gui_log))

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
