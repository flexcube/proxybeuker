# TODO: Add check if RED Cine-X is installed (Multiplatform)
# TODO: Build license module (GR + Trial License)
# TODO: Stop and resume buttons
# TODO: Trial should limit to 5x files it can do 
# BUG: Kill the conversion process and all threads when closing the GUI
# Nice to have
# TODO: Check if the output settings are correct for RED color and if audio gets added
# TODO: Add estimated time remaining
# TODO: Create progressbar instead of textbox, have the start button display with text the status.
# TODO: Add Dropdown for multiple formats and output sizes
# TODO: Splash screen when you press the logo


import wx
import subprocess
import re
import os
import sys
import threading
from pathlib import Path
import platform
import license_check

class converter(threading.Thread):
    gui_log = ""

    def __init__(self, arg1, arg2):
        self.input_directory = Path(arg1)
        self.output_directory = Path(arg2)
        threading.Thread.__init__(self)
        self.start()

    # Function used to acces file bundled in PyInstaller
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def run(self):
        self.main()

    def scan_folder(self, input_directory, output_directory):
        print("Scanning input directory...")
        file_list = []
        for name in input_directory.glob("**/*_001.R3D"):
            if not Path.exists(output_directory / (name.stem + ".mov")):
                file_list.append(name)
        return file_list


    def convert_files(self, files_to_convert):
        converted_count = 0
        error_count = 0

        print(str(converted_count + error_count) +
        " of " + str(len(files_to_convert)) + " have been processed!")

        for file in files_to_convert:
            try:
                file_metadata = ""
                if platform.system() == "Darwin":
                    file_metadata = subprocess.Popen(['/Applications/REDCINE-X Professional/REDCINE-X PRO.app/Contents/MacOS/REDline', '--i', file, '--printMeta', '1'],
                                                    shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                elif platform.sysyem() == "Windows":
                    file_metadata = subprocess.Popen(['WINDOWSPATH', '--i', file, '--printMeta', '1'],
                                                    shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                                    
                file_metadata = file_metadata.communicate()[0].decode('utf-8')

                search = re.findall("Frame Width:\s(\d*)\nFrame Height:\s(\d*)", file_metadata)
                file_width = int(search[0][0])
                file_height = int(search[0][1])

                # Find filename in Metadata, can be replaced with Pathlib
                search = re.findall(
                    "File Name:\s(.*?)\.R3D", file_metadata)
                file_name = search[0]

                # Calculate new frame size, width is predetermined
                proxy_width = 1920
                proxy_height = int(proxy_width/(file_width/file_height))

                print("Converting file: " + file_name)

                if platform.system() == "Darwin":
                    subprocess.run(["/Applications/REDCINE-X Professional/REDCINE-X PRO.app/Contents/MacOS/REDline", "--silent", "--useRMD", "1", "--i", file, "--outDir", self.output_directory, "--o", file_name, "--format",
                                "201", "--PRcodec", "2", "--res", "4", "--resizeX", str(proxy_width), "--resizeY", str(proxy_height)], shell=False)
                if platform.system() == "Windows":
                    subprocess.run(["WINDWOWS REDLINE PATH", "--silent", "--useRMD", "1", "--i", file, "--outDir", self.output_directory, "--o", file_name, "--format",
                                "201", "--PRcodec", "2", "--res", "4", "--resizeX", str(proxy_width), "--resizeY", str(proxy_height)], shell=False)
                    
                converted_count += 1
                print(str(converted_count + error_count) +
                        " of " + str(len(files_to_convert)) + " have been processed!")

            except:
                print("Could not convert: " +
                      str(file) + " skipping file")
                error_count += 1

        print("Conversion done! \nConverted files: " + str(converted_count) + "\nFiles with encoding errors: " + str(error_count))

    def main(self):
        # Get all the .R3D files that need to be converted
        files_to_convert = self.scan_folder(self.input_directory, self.output_directory)

        # Start the conversion
        self.convert_files(files_to_convert)


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
        self.SetSize((450, 400))
        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        self.text_box = wx.TextCtrl(
            self.panel_1, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_NO_VSCROLL | wx.TE_RICH2)
        self.text_box.SetDefaultStyle(
            wx.TextAttr(wx.Colour(96, 207, 48), wx.Colour(36, 36, 36)))
        self.text_box.SetBackgroundColour(wx.Colour(36, 36, 36))
        self.text_box.SetOwnForegroundColour(wx.WHITE)

        self.bitmap_1 = wx.StaticBitmap(self.panel_1, wx.ID_ANY, wx.Bitmap(converter.resource_path("ico.ico"), wx.BITMAP_TYPE_ANY))

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

        self.SetIcon(wx.Icon(converter.resource_path("ico.ico")))

        self.__set_properties()
        self.__do_layout()

        # Comment out to skip the license checking
        if license_check.get_license_status():
            # Intro Text
            self.text_box.AppendText(
                "Welcome to ProxyBeuker V1.2! Contact: info@proxybeuker.com\nThis tool batch converts RED .R3D files to Full HD ProRes LT \n\n")
            self.text_box.AppendText("License Status: Trial Activated\n\n")
        else:
            self.text_box.AppendText(
                "Trial license expired or license server could not be reached.\nBuy a license at www.proxybeuker.com or contact us at \ninfo@proxybeuker.com")
            self.input_folder_button.Disable()
            self.output_folder_button.Disable()
            self.start_button.Disable()

        # This is wat redirects terminal output to the text box
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
        self.bitmap_1.SetMinSize((96, 96))

    def __do_layout(self):
        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5.Add(self.bitmap_1, 0, wx.ALIGN_CENTER, 10)
        sizer_3.Add(self.input_folder_button, 0, wx.ALIGN_CENTER, 10)
        sizer_3.Add(self.input_folder_label, 1, wx.ALIGN_CENTER, 10)
        sizer_4.Add(self.output_folder_button, 0, wx.ALIGN_CENTER, 10)
        sizer_4.Add(self.output_folder_label, 1, wx.ALIGN_CENTER, 10)
        sizer_2.Add(sizer_5, 1, wx.ALIGN_CENTER, 0)
        sizer_2.Add(sizer_3, 1, wx.ALIGN_CENTER, 0)
        sizer_2.Add(sizer_4, 1, wx.ALIGN_CENTER, 0)
        sizer_2.Add(self.start_button, 0, wx.ALIGN_CENTER | wx.ALL, 20)
        sizer_2.Add(self.text_box, 0, wx.ALIGN_CENTER, 0)
        sizer_2.Add((0, 0), 0, 0, 0)
        sizer_1.Add(self.panel_1, 1, wx.EXPAND, 0)
        self.panel_1.SetSizer(sizer_2)
        self.SetSizer(sizer_1)
        self.Layout()
        self.Centre()

    def start_conversion(self, e):
        converter(self.input_directory, self.output_directory)
        self.text_box.AppendText(str(converter.gui_log))
    
class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

if __name__ == "__main__":
    rendertool = MyApp(0)
    rendertool.MainLoop()