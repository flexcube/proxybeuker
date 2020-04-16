import wx
import glob
import subprocess
import logging
import re
import requests
import os
import sys  # Can be deleted if error handling in Except is improved
import traceback
import threading

# Pyinstaller: pyinstaller --onefile -y --icon=ico.icns -windowed gui_rendertool.py
# Refractor/Clean-up code
# Better GUI Design

# BUG: Program crashes if there is no internet connection (no error handling of requests)


class converter(threading.Thread):
    gui_log = "guilog"

    def __init__(self, arg1, arg2):
        self.input_directory = arg1
        self.output_directory = arg2
        threading.Thread.__init__(self)
        # This starts the thread running on creation, but you could
        # also make the GUI thread responsible for calling this
        self.start()

        # WTF is the purpose of below lines?
        # file_metadata = subprocess.Popen(['REDline', '--i', "/Users/Kevin/Downloads/redapptest/input/A004_C014_01061E.RDC/A004_C014_01061E_001.R3D",
        #                                  '--printMeta', '1'], shell = False, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        # print(str(file_metadata.communicate()))

    def run(self):
        self.main()

    def scan_folder(self, input_directory):
        print("Scanning input directory...")
        file_list = []
        # Only convert the first file in a RED Clip folder "_001" because REDLINE automaticly stitches the clips together
        for name in glob.iglob(input_directory + '/**/*_001.R3D', recursive=True):
            file_list.append(name)
            print(name)
        return file_list

    def check_duplicate_file(self, file):
        # Only converts the file if it is in the RDC folder, otherwise throws an Index Error
        try:
            filename_from_path = re.findall("C\/(.*).R3D", file)[0]
        except:
            return False

        if os.path.isfile(self.output_directory + "/" + filename_from_path + ".mov"):
            return False
        else:
            return True

    def proxymaker(self, files_to_convert):
        converted_count = 0
        duplicate_count = 0
        error_count = 0
        for file in files_to_convert:
            # Try encoding, skip when error found.
            try:
                # Check if file already exists
                if self.check_duplicate_file(file):
                    print("Converting file: " + file)

                    # Output file metadata to string
                    file_metadata = subprocess.Popen(['/Applications/REDCINE-X Professional/REDCINE-X PRO.app/Contents/MacOS/REDline', '--i', file, '--printMeta', '1'],
                                                     shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    file_metadata = file_metadata.communicate()[
                        0].decode('utf-8')

                    # Find Frame Height and Width in Metadata
                    search = re.findall(
                        "Frame Width:\s(\d*)\nFrame Height:\s(\d*)", file_metadata)
                    file_width = int(search[0][0])
                    file_height = int(search[0][1])

                    # Find filename in Metadata
                    search = re.findall(
                        "File Name:\s(.*?)\.R3D", file_metadata)
                    file_name = search[0]

                    # Calculate new frame size, width is predetermined
                    proxy_width = 1920
                    proxy_height = int(proxy_width/(file_width/file_height))

                    print("Original width: " + str(file_width) + " Original Height: " + str(file_height) +
                          " Proxy width: " + str(proxy_width) + " Proxy Height: " + str(proxy_height))

                    # Encode the proxy
                    subprocess.run(["/Applications/REDCINE-X Professional/REDCINE-X PRO.app/Contents/MacOS/REDline", "--silent", "--useRMD", "1", "--i", file, "--outDir", self.output_directory, "--o", file_name, "--format",
                                    "201", "--PRcodec", "2", "--res", "4", "--resizeX", str(proxy_width), "--resizeY", str(proxy_height)], shell=False)
                    converted_count += 1
                    subprocess.run("clear")
                    print(str(converted_count + error_count + duplicate_count) +
                          " of " + str(len(files_to_convert)) + " have been processed!")
                else:
                    print(str(
                        file) + " already processed or not in the right format or folder, skipping file.")
                    duplicate_count += 1

            except:
                print("Could not convert: " +
                      str(file) + " skipping file")
                # print("Error: " + str(sys.exc_info()[0]))
                # print(traceback.format_exc())
                error_count += 1

        print("Conversion done! \n Converted files: " + str(converted_count) + "\n Duplicate files or wrong location: " +
              str(duplicate_count) + "\n Files with encoding errors: " + str(error_count))

    def main(self):

        files_to_convert = self.scan_folder(self.input_directory)

        # Not needed in GUI Version
        # print(str(len(files_to_convert)) +
        #      " item(s) found, press enter to start transcoding \n\n")

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
            "style", 0) | wx.CAPTION | wx.CLIP_CHILDREN | wx.CLOSE_BOX | wx.FRAME_NO_TASKBAR | wx.ICONIZE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((611, 497))
        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        global text_ctrl_3
        self.text_ctrl_3 = wx.TextCtrl(
            self.panel_1, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_NO_VSCROLL | wx.TE_RICH2)
        self.text_ctrl_3.SetDefaultStyle(wx.TextAttr(wx.GREEN, wx.BLACK))
        self.text_ctrl_3.SetBackgroundColour(wx.BLACK)
        self.text_ctrl_3.SetOwnForegroundColour(wx.WHITE)

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

        self.__set_properties()
        self.__do_layout()

        # Trial License Check
        try:
            r = requests.get("https://proxybeuker.com/license2.html")

            if r.status_code == 200:
                self.text_ctrl_3.AppendText("Trial Activated. \n")
                # Intro Text
                self.text_ctrl_3.AppendText(
                    "Batch convert RED .R3D files to Full HD ProRes LT. Select a folder to start. \nThe latest Redcine-x Pro version needs to be installed.\n\nSoftware provided as is, make a back-up before running this. \nAuthor: info@pieterboerboom.nl \n\n")
            # end wxGlade
            else:
                self.text_ctrl_3.AppendText(
                    "Trial License Expired or License Server could not be reached.\nBuy a license at www.proxybeuker.com or contact us at info@proxybeuker.com")
                self.button_1.Disable()
                self.button_2.Disable()
                self.button_3.Disable()

        except requests.exceptions.RequestException as e:
            self.text_ctrl_3.AppendText(
                "The License Server could not be reached due to a connection error. Are you connected to the internet?\nFor help contact us at info@proxybeuker.com")
            self.button_1.Disable()
            self.button_2.Disable()
            self.button_3.Disable()

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
        self.SetTitle("Proxy Beuker")
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
        self.text_ctrl_3.SetMinSize((600, 200))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        # fklogo = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(
        #    "/Users/Kevin/Downloads/minilogo.png", wx.BITMAP_TYPE_ANY))
        # sizer_1.Add(fklogo, 0, wx.ALIGN_CENTER, 0)
        sizer_3.Add(self.button_1, 0, wx.ALIGN_CENTER, 10)
        sizer_3.Add(self.text_ctrl_1, 1, wx.ALIGN_CENTER, 10)
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
    rendertool.MainLoop()
