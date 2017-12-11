import glob
import subprocess
import argparse
import logging
import re
import os

# v0.6
# TODO Clean up logging, don't require slashes for directories, improve regex check if file exists, 
# TODO, Improve logging to only output ERRORS and general stats, mute output RED tool, (Export metadata all shots?)
# Clean-up code

# Accept commandline arguments for input
"""
parser = argparse.ArgumentParser(description='Collect input and output directory')
parser.add_argument('-i', action="store", dest="input_directory")
parser.add_argument('-o', action="store", dest="output_directory")
"""

#Hardcoded directory
#ALWAYS ADD SLASH BEFORE AND AFTER PATH
output_directory = "/Volumes/2017_UMF_SHANGHAI_BACKUP_01/2017 - UMF - SHANGHAI/09_Proxies/"
input_directory = "/Volumes/2017_UMF_SHANGHAI_BACKUP_01/2017 - UMF - SHANGHAI/02_Footage/"


# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s : %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename= output_directory + '/render_tool_log.txt',
                    filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%d-%m %H:%M:%S')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)



def scan_folder(input_directory):
	logging.info("Scanning input directory...")
	file_list = []
	for name in glob.iglob(input_directory + '/**/*.R3D', recursive = True):
	    file_list.append(name)
	    logging.info(name)
	return file_list

def check_if_file_exists(file):
	filename_from_path = re.findall("C\/(.*).R3D", file)[0]
	if os.path.isfile(output_directory + filename_from_path + "_Proxy.mov"):
		return True
	else:
		return False

def proxymaker(files_to_convert):
	converted_count = 0
	duplicate_count = 0
	error_count = 0
	for file in files_to_convert:
		# Try encoding, skip when error found.
		try:
			# Check if file exists
			if not check_if_file_exists(file):
				logging.info("Converting file: " + file)
				print(file)
				#Output file metadata to string
				x=subprocess.Popen(['REDline', '--i', file , '--printMeta', '1'],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
				output=x.communicate()[0].decode('utf-8')
				#Print the Metadata
				#print(output)
				# Find Frame Height and Width in Metadata
				search = re.findall("Frame Width:\s(\d*)\nFrame Height:\s(\d*)",output)
				#print(search[0])
				file_width = int(search[0][0])
				file_height = int(search[0][1])

				# Find filename
				search = re.findall("File Name:\s(.*?)\.R3D",output)
				file_name = search[0] 

				# Calculate new frame size
				#width is predetermined
				proxy_width = 1280
				proxy_height = int (proxy_width/(file_width/file_height))

				print ("Width" + str(file_width) + " Height " + str(file_height))

				print ("Proxy width " + str(proxy_width) + "Proxy Height " + str(proxy_height))	

				# Encode the proxy
				print("test")
				subprocess.run(["REDline" , "--useRMD", "1", "--i", file , "--outDir", output_directory , "--o", file_name + "_Proxy", "--format", "201", "--PRcodec", "2" ,"--res", "4", "--resizeX", str(proxy_width), "--resizeY", str(proxy_height)], shell=False)
				converted_count += 1
				logging.info (str(converted_count) + " of " + str(len(files_to_convert)) + " have been converted!")
			else:
				logging.info(str(file) + " already processed, skipping file.")
				duplicate_count += 1 

		except:
			logging.info ("Could not convert: " + str(file) + " skipping file")
			error_count += 1			

	logging.info("Conversion done! \n Converted files: " + str(converted_count) + "\n Duplicate files skipped: " + str(duplicate_count) + "\n Files with encoding error's: " + str(error_count) )


def main():
	subprocess.run("clear")

	print("\n\n\n FK R3D to ProRess Proxy Beuker v0.5 \n ________________ \n ")
	print("Input folder: " + input_directory)
	print ("Output folder: " + output_directory)
	input("Press enter to continue and start scanning \n\n")
	
	files_to_convert = scan_folder(input_directory)
	input(str(len(files_to_convert)) + " items found, press enter to start transcoding \n\n")

	proxymaker(files_to_convert)



main()
