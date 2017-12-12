import glob
import subprocess
import logging
import re
import os
import sys # Can be deleted if error handling in Except is improved
import traceback
import tkinter as tk
from tkinter import filedialog
root = tk.Tk()
root.withdraw()

# DEBUG "Output directory not found", duplicates not detected
# TODO, Improve logging to only output ERRORS and general stats, mute output RED tool, (Export metadata all shots?)
# Make output less verbose, improve logging, show progress, add argparse as option for file paths and resolution

# Add other file formats with FFMPEG?


def scan_folder(input_directory):
	logging.info("Scanning input directory...")
	file_list = []
	# Only convert the first file in a RED Clip folder "_001" because REDLINE automaticly stitches the clips together
	for name in glob.iglob(input_directory + '/**/*_001.R3D', recursive = True):
	    file_list.append(name)
	    print(name)
	return file_list

def check_if_file_exists(file):
	# Only converts the file if it is in the RDC folder, otherwise throws an Index Error
	filename_from_path = re.findall("C\/(.*).R3D", file)[0]
	if os.path.isfile(output_directory + filename_from_path + ".mov"):
		print("Filename from path: " + filename_from_path)
		print(os.path.isfile(output_directory + filename_from_path + ".mov"))
		return True
	else:
		print(os.path.isfile(output_directory + filename_from_path + ".mov"))
		return False

def proxymaker(files_to_convert):
	converted_count = 0
	duplicate_count = 0
	error_count = 0
	for file in files_to_convert:
		# Try encoding, skip when error found.
		print(file)
		try:
			# Check if file already exists
			if not check_if_file_exists(file):
				logging.info("Converting file: " + file)
				#Output file metadata to string
				x=subprocess.Popen(['REDline', '--i', file , '--printMeta', '1'],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
				output=x.communicate()[0].decode('utf-8')

				# Find Frame Height and Width in Metadata
				search = re.findall("Frame Width:\s(\d*)\nFrame Height:\s(\d*)",output)
				file_width = int(search[0][0])
				file_height = int(search[0][1])

				# Find filename in Metadata
				search = re.findall("File Name:\s(.*?)\.R3D",output)
				file_name = search[0] 

				# Calculate new frame size, width is predetermined
				proxy_width = 1920
				proxy_height = int (proxy_width/(file_width/file_height))

				print ("Original width " + str(file_width) + " Original Height " + str(file_height) + " Proxy width: " + str(proxy_width) + " Proxy Height: " + str(proxy_height))	

				# Encode the proxy
				subprocess.run(["REDline" , "--silent", "--useRMD", "1", "--i", file , "--outDir", main.output_directory , "--o", file_name, "--format", "201", "--PRcodec", "2" ,"--res", "4", "--resizeX", str(proxy_width), "--resizeY", str(proxy_height)], shell=False)
				converted_count += 1
				logging.info (str(converted_count + error_count + duplicate_count) + " of " + str(len(files_to_convert)) + " have been processed!")
			else:
				logging.info(str(file) + " already processed, skipping file.")
				duplicate_count += 1 

		except:
			logging.info ("Could not convert: " + str(file) + " skipping file")
			print("Error: " + str(sys.exc_info()[0]))
			print(traceback.format_exc())
			error_count += 1			

	logging.info("Conversion done! \n Converted files: " + str(converted_count) + "\n Duplicate files skipped: " + str(duplicate_count) + "\n Files with encoding errors: " + str(error_count) )



def main():
	# Clear screen
	subprocess.run("clear")

	# Opening message
	print("\n\n\n FK R3D to ProRess Proxy Beuker v0.9 \n ________________ \n To get started specify the input directory with the R3D files and the output directory for the Proxies, render log files and file metadata")
	input("\n Press enter to open up a dialog to set the input directory \n")
	input_directory = filedialog.askdirectory()
	if not input_directory.endswith('/'): # Add trailing slash if not already in there
		input_directory = input_directory + "/"
	print("\n Input folder: " + input_directory)
	input("\n Press enter to open up a dialog to set the output directory \n")
	output_directory = filedialog.askdirectory()
	if not main.output_directory.endswith('/'): # Add trailing slash if not already in there
		input_directory = input_directory + "/"
	print ("Output folder: " + main.output_directory)


	# set up logging to file - see previous section for more details
	logging.basicConfig(level=logging.INFO,
	                    format='%(asctime)s : %(message)s',
	                    datefmt='%m-%d %H:%M')
	# define a Handler which writes INFO messages or higher to the sys.stderr
	console = logging.FileHandler(main.output_directory + 'render_tool_log.txt', mode='w', encoding=None, delay=False)
	console.setLevel(logging.INFO)
	# set a format which is simpler for console use
	formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%d-%m %H:%M:%S')
	# tell the handler to use this format
	console.setFormatter(formatter)
	# add the handler to the root logger
	logging.getLogger('').addHandler(console)

	input("Press enter to continue and start scanning \n\n")	
	files_to_convert = scan_folder(input_directory)
 
	input(str(len(files_to_convert)) + " items found, press enter to start transcoding \n\n")

	proxymaker(files_to_convert)

main()
