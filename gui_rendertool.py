#!/usr/bin/python3

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

# TODO: Add check if RED Cine-X is installed
# TODO: Improve GUI Design
# TODO: Make the conversion  stop when closing the program


class converter(threading.Thread):
    gui_log = ""

    def __init__(self, arg1, arg2):
        self.input_directory = arg1
        self.output_directory = arg2
        threading.Thread.__init__(self)
        # This starts the thread running on creation, but you could
        # also make the GUI thread responsible for calling this
        self.start()

    def run(self):
        self.main()

    # Scan input folder for RED .R3D Files
    def scan_folder(self, input_directory):
        print("Scanning input directory...")
        file_list = []
        # Only convert the first .R3D file in a RED Clip folder "_001" because REDLINE automaticly stitches the clips together
        for name in glob.iglob(input_directory + '/**/*_001.R3D', recursive=True):
            file_list.append(name)
        return file_list

    def check_duplicate_file(self, file):
        # Only converts the file if it is in the originial RDC folder
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

                    # Capture the metadata from the .R3D file  in a string by using Redline
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

                    print("Converting file: " + file_name)
                    # Encode the proxy
                    subprocess.run(["/Applications/REDCINE-X Professional/REDCINE-X PRO.app/Contents/MacOS/REDline", "--silent", "--useRMD", "1", "--i", file, "--outDir", self.output_directory, "--o", file_name, "--format",
                                    "201", "--PRcodec", "2", "--res", "4", "--resizeX", str(proxy_width), "--resizeY", str(proxy_height)], shell=False)
                    converted_count += 1
                    subprocess.run("clear")
                    print(str(converted_count + error_count + duplicate_count) +
                          " of " + str(len(files_to_convert)) + " have been processed!")
                else:
                    print(str(
                        file) + " already processed or file not in orginial RDC folder, skipping file.")
                    duplicate_count += 1

            except:
                print("Could not convert: " +
                      str(file) + " skipping file")
                error_count += 1

        print("Conversion done! \nConverted files: " + str(converted_count) + "\nDuplicate files or wrong location: " +
              str(duplicate_count) + "\nFiles with encoding errors: " + str(error_count))

    def main(self):
        # Get all the .R3D files that need to be converted
        files_to_convert = self.scan_folder(self.input_directory)

        # Start the conversion
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
        self.SetSize((450, 350))
        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        global text_box
        self.text_box = wx.TextCtrl(
            self.panel_1, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_NO_VSCROLL | wx.TE_RICH2)
        self.text_box.SetDefaultStyle(
            wx.TextAttr(wx.Colour(96, 207, 48), wx.Colour(36, 36, 36)))
        self.text_box.SetBackgroundColour(wx.Colour(36, 36, 36))
        self.text_box.SetOwnForegroundColour(wx.WHITE)

        self.input_folder_button = wx.Button(
            self.panel_1, wx.ID_ANY, "Input Folder")
        self.Bind(wx.EVT_BUTTON, self.input_button_click,
                  self.input_folder_button)
        self.input_folder_label = wx.TextCtrl(
            self.panel_1, wx.ID_ANY, "", style=wx.TE_READONLY)

        self.output_folder_button = wx.Button(
            self.panel_1, wx.ID_ANY, "Output Folder")
        self.Bind(wx.EVT_BUTTON, self.output_button_click,
                  self.output_folder_button)

        self.output_folder_label = wx.TextCtrl(
            self.panel_1, wx.ID_ANY, "", style=wx.TE_READONLY)
        self.start_button = wx.Button(self.panel_1, wx.ID_ANY, "Start")
        self.Bind(wx.EVT_BUTTON, self.start_conversion, self.start_button)

        self.__set_properties()
        self.__do_layout()

        # Barebones license check. Check by polling webpage if the trial is activated.
        try:
            r = requests.get("https://proxybeuker.com/license2.html")

            if r.status_code == 200:
                self.text_box.AppendText("License Status: Trial Activated \n")
                # Intro Text
                self.text_box.AppendText(
                    "Welcome to ProxyBeuker! This tool batch converts RED .R3D files to Full HD ProRes LT.  \nMake sure to have the latest Redcine-X Pro version installed.\n\nSoftware provided as is, make a back-up before running. \nContact: info@proxybeuker.com \n\n")
            # end wxGlade
            else:
                self.text_box.AppendText(
                    "Trial license expired or license Server could not be reached.\nBuy a license at www.proxybeuker.com or contact us at info@proxybeuker.com")
                self.input_folder_button.Disable()
                self.output_folder_button.Disable()
                self.start_button.Disable()

        except requests.exceptions.RequestException as e:
            self.text_box.AppendText(
                "The license server could not be reached due to a connection error. Are you connected to the internet?\nFor help contact us at info@proxybeuker.com")
            self.input_folder_button.Disable()
            self.output_folder_button.Disable()
            self.start_button.Disable()

        # This is wat redirects terminal output to the text box?
        redir = RedirectText(self.text_box)
        sys.stdout = redir

    def write(self, string):
        wx.CallAfter(self.text_box.AppendText, string)

    def input_button_click(self, e):

        # Open OS window to chose input directory
        directory_dialog = wx.DirDialog(None, "Choose input directory", "",
                                        wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if directory_dialog.ShowModal() == wx.ID_OK:
            self.input_directory = directory_dialog.GetPath()
            self.input_folder_label.SetLabelText(str(self.input_directory))
        directory_dialog.Destroy()

    def output_button_click(self, e):

        # Open OS window to chose output directory
        directory_dialog = wx.DirDialog(None, "Choose output directory", "",
                                        wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if directory_dialog.ShowModal() == wx.ID_OK:
            self.output_directory = directory_dialog.GetPath()
            self.output_folder_label.SetLabelText(str(self.input_directory))
        directory_dialog.Destroy()

    def __set_properties(self):
        # Set the general properties for WX and styling
        self.SetTitle("Proxy Beuker")
        self.SetBackgroundColour(wx.Colour(36, 36, 36))
        self.input_folder_button.SetMinSize((111, 20))
        self.input_folder_button.SetFont(
            wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.input_folder_label.SetMinSize((200, 22))
        self.input_folder_label.SetBackgroundColour(wx.Colour(36, 36, 36))
        self.input_folder_label.SetForegroundColour(wx.Colour(253, 151, 31))
        self.output_folder_button.SetFont(
            wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.output_folder_label.SetMinSize((200, 22))
        self.output_folder_label.SetBackgroundColour(wx.Colour(36, 36, 36))
        self.output_folder_label.SetForegroundColour(wx.Colour(253, 151, 31))
        self.start_button.SetFont(
            wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.text_box.SetMinSize((500, 150))
        # end wxGlade

    def __do_layout(self):
        # Construct the lay-out
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3.Add(self.input_folder_button, 0, wx.ALIGN_CENTER, 10)
        sizer_3.Add(self.input_folder_label, 1, wx.ALIGN_CENTER, 10)
        sizer_2.Add(sizer_3, 1, wx.ALIGN_CENTER, 0)
        sizer_4.Add(self.output_folder_button, 0, 0, 0)
        sizer_4.Add(self.output_folder_label, 0,
                    wx.ALIGN_CENTER_HORIZONTAL, 10)
        sizer_2.Add(sizer_4, 1, wx.ALIGN_CENTER, 0)
        sizer_2.Add(self.start_button, 0, wx.ALIGN_CENTER | wx.ALL, 20)
        sizer_2.Add(self.text_box, 0, wx.ALIGN_CENTER, 0)
        sizer_2.Add((0, 0), 0, 0, 0)
        self.panel_1.SetSizer(sizer_2)
        sizer_1.Add(self.panel_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        self.Centre()
        # end wxGlade

    def start_conversion(self, e):
        converter(self.input_directory, self.output_directory)
        self.text_box.AppendText(str(converter.gui_log))

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
