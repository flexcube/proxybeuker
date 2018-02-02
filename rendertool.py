import glob
import subprocess
import logging
import re
import os
import sys  # Can be deleted if error handling in Except is improved
import traceback
# TODO improve/disable logging
# Build command: pyinstaller --onefile -y rendertool.py
# Improve file path parsing


def scan_folder(input_directory):
    logging.info("Scanning input directory...")
    file_list = []
    # Only convert the first file in a RED Clip folder "_001" because REDLINE automaticly stitches the clips together
    for name in glob.iglob(input_directory + '/**/*_001.R3D', recursive=True):
        file_list.append(name)
        print(name)
    return file_list


def check_if_file_exists(file):
    # Only converts the file if it is in the RDC folder, otherwise throws an Index Error
    try:
        filename_from_path = re.findall("C\/(.*).R3D", file)[0]
        if os.path.isfile(main.output_directory + filename_from_path + ".mov"):
            return False
        else:
            return True
    except:
        return False


def proxymaker(files_to_convert):
    converted_count = 0
    duplicate_count = 0
    error_count = 0
    for file in files_to_convert:
        # Try encoding, skip when error found.
        try:
            # Check if file already exists
            if check_if_file_exists(file):
                logging.info("Converting file: " + file)
                # Output file metadata to string
                file_metadata = subprocess.Popen(['REDline', '--i', file, '--printMeta', '1'],
                                                 shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                file_metadata = file_metadata.communicate()[0].decode('utf-8')

                # Find Frame Height and Width in Metadata
                search = re.findall(
                    "Frame Width:\s(\d*)\nFrame Height:\s(\d*)", file_metadata)
                file_width = int(search[0][0])
                file_height = int(search[0][1])

                # Find filename in Metadata
                search = re.findall("File Name:\s(.*?)\.R3D", file_metadata)
                file_name = search[0]

                # Calculate new frame size, width is predetermined
                proxy_width = 1920
                proxy_height = int(proxy_width/(file_width/file_height))

                print("Original width: " + str(file_width) + " Original Height: " + str(file_height) +
                      " Proxy width: " + str(proxy_width) + " Proxy Height: " + str(proxy_height))

                # Encode the proxy
                subprocess.run(["REDline", "--silent", "--useRMD", "1", "--i", file, "--outDir", main.output_directory, "--o", file_name,
                                "--format", "201", "--PRcodec", "2", "--res", "4", "--resizeX", str(proxy_width), "--resizeY", str(proxy_height)], shell=False)
                converted_count += 1
                subprocess.run("clear")
                logging.info(str(converted_count + error_count + duplicate_count) +
                             " of " + str(len(files_to_convert)) + " have been processed!")
            else:
                logging.info(str(
                    file) + " already processed or not in the right format or folder, skipping file.")
                duplicate_count += 1

        except:
            logging.info("Could not convert: " + str(file) + " skipping file")
            print("Error: " + str(sys.exc_info()[0]))
            print(traceback.format_exc())
            error_count += 1
    logging.info("Conversion done! \n Converted files: " + str(converted_count) + "\n Duplicate files or wrong location: " +
                 str(duplicate_count) + "\n Files with encoding errors: " + str(error_count))


def main():
    # Clear screen
    subprocess.run("clear")
    # Opening message
    print("\n\n\n R3D to ProRess Proxy Tool V1 || pieter@finalkid.com \n ________________ \n This app batch converts .R3D files to 1080P ProRess LT.\n It is designed to convert 1000+ files fast without freezing.")
    print("\n NOTE: REDCINE-X NEEDS TO BE INSTALLED ON YOUR SYSTEM FOR THIS PROGRAM TO WORK. \n NOTE: It only works if the R3D files are in the original '.RDC' folders.\n")
    input_directory = input(
        "\n Drag the input directory in here and press enter... \n")
    # Remove space at the end when dragging in folder
    input_directory = input_directory.rstrip()
    # Add trailing slash if not already in there
    if input_directory:
        if not input_directory.endswith('/'):
            input_directory = input_directory + "/"

    main.output_directory = input(
        "\n Drag the output directory in here and press enter... \n")
    main.output_directory = main.output_directory.rstrip()
    # Add trailing slash if not already in there
    if not main.output_directory.endswith('/'):
        main.output_directory = main.output_directory + "/"

    subprocess.run("clear")
    print("Selected input folder: " + input_directory)
    print("Selected output folder: " + main.output_directory)

    # set up logging to file - see previous section for more details
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s : %(message)s',
                        datefmt='%m-%d %H:%M')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.FileHandler(
        main.output_directory + 'render_tool_log.txt', mode='w', encoding=None, delay=False)
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter(
        '%(asctime)s - %(message)s', datefmt='%d-%m %H:%M:%S')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

    input("\n\nPress enter to continue and start scanning \n\n")
    subprocess.run("clear")
    files_to_convert = scan_folder(input_directory)
    input(str(len(files_to_convert)) +
          " item(s) found, press enter to start transcoding \n\n")
    # Clear screen
    subprocess.run("clear")
    # Start Conversion
    proxymaker(files_to_convert)


main()
