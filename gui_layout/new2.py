import wx
import glob
import subprocess
import logging
import re
import os
import sys  # Can be deleted if error handling in Except is improved
import traceback


class converter(object):

    def __init__(self, arg1, arg2):
        self.input_directory = arg1
        self.output_directory = arg2
        self.main()

    def scan_folder(self, input_directory):
        logging.info("Scanning input directory...")
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
            if os.path.isfile(self.output_directory + filename_from_path + ".mov"):
                return False
            else:
                return True
        except:
            return False

    def proxymaker(self, files_to_convert):
        converted_count = 0
        duplicate_count = 0
        error_count = 0
        for file in files_to_convert:
            # Try encoding, skip when error found.
            try:
                # Check if file already exists
                if self.check_duplicate_file(file):
                    logging.info("Converting file: " + file)
                    # Output file metadata to string
                    file_metadata = subprocess.Popen(['REDline', '--i', file, '--printMeta', '1'],
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
                    subprocess.run(["REDline", "--silent", "--useRMD", "1", "--i", file, "--outDir", self.output_directory, "--o", file_name, "--format",
                                    "201", "--PRcodec", "2", "--res", "4", "--resizeX", str(proxy_width), "--resizeY", str(proxy_height)], shell=False)
                    converted_count += 1
                    subprocess.run("clear")
                    logging.info(str(converted_count + error_count + duplicate_count) +
                                 " of " + str(len(self.files_to_convert)) + " have been processed!")
                else:
                    logging.info(str(
                        file) + " already processed or not in the right format or folder, skipping file.")
                    duplicate_count += 1

            except:
                logging.info("Could not convert: " +
                             str(file) + " skipping file")
                print("Error: " + str(sys.exc_info()[0]))
                print(traceback.format_exc())
                error_count += 1

        logging.info("Conversion done! \n Converted files: " + str(converted_count) + "\n Duplicate files or wrong location: " +
                     str(duplicate_count) + "\n Files with encoding errors: " + str(error_count))

    def main(self):
        # set up logging to file - see previous section for more details
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s : %(message)s',
                            datefmt='%m-%d %H:%M')
        # define a Handler which writes INFO messages or higher to the sys.stderr
        console = logging.FileHandler(
            self.output_directory + 'render_tool_log.txt', mode='w', encoding=None, delay=False)
        console.setLevel(logging.INFO)
        # set a format which is simpler for console use
        formatter = logging.Formatter(
            '%(asctime)s - %(message)s', datefmt='%d-%m %H:%M:%S')
        # tell the handler to use this format
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger('').addHandler(console)

        files_to_convert = self.scan_folder(self.input_directory)
        print(str(len(files_to_convert)) +
              " item(s) found, press enter to start transcoding \n\n")
        # Start Conversion
        self.proxymaker(files_to_convert)


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = kwds.get(
            "style", 0) | wx.CAPTION | wx.CLIP_CHILDREN | wx.CLOSE_BOX | wx.FRAME_NO_TASKBAR | wx.ICONIZE | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER
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

        self.text_ctrl_3 = wx.TextCtrl(
            self.panel_1, wx.ID_ANY, "", style=wx.TE_MULTILINE)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

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
        self.SetTitle("frame")
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
