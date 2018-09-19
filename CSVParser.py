#!/usr/bin/env python

import os, sys, csv, re
from optparse import OptionParser
from optparse import Option, OptionValueError

VERSION = '1.0'
DATA_TYPES = ["STRING", "INT", "DECIMAL"]

class MultipleOption(Option):
	ACTIONS = Option.ACTIONS + ("extend",)
	STORE_ACTIONS = Option.STORE_ACTIONS + ("extend",)
	TYPED_ACTIONS = Option.TYPED_ACTIONS + ("extend",)
	ALWAYS_TYPED_ACTIONS = Option.ALWAYS_TYPED_ACTIONS + ("extend",)

	def take_action(self, action, dest, opt, value, values, parser):
		if action == "extend":
			values.ensure_value(dest, []).append(value)
		else:
			Option.take_action(self, action, dest, opt, value, values, parser)

def validate_arguments(options):

	# verify input file exists
	if os.path.isfile(options.file[0]) == False:
		print "ERROR: FILE PATH INVALID."
		return False;

	# verify the data types are valid
	dataTypeList = options.datatypes[0].split(",")
	for dataType in dataTypeList:
		if dataType not in DATA_TYPES:
			print "ERROR: INVAID DATA TYPE: " + dataType
			return False;

	return True

def getOutputFile(outputLocation, inputFile):
	
	# get path to output file
	outputPath, outputFilename = os.path.split(outputLocation)

	# make sure the output directory exists
	if os.path.isdir(outputPath):

		# check if specified output location is a file or directory
		name, ext = os.path.splitext(outputLocation)
		if ext == "":

			# check if the input file name already exists
			#if os.path.exists(outputLocation + inputFile):
			#	print "ERROR: File will be overwritten. Change output file name."
			#	sys.exit(2)
			#else:
			return outputLocation + inputFile
		else:
			return outputLocation
	else:
		print "ERROR: Output directory does not exist"
		sys.exit(2)

def main():
	PROG = os.path.basename(os.path.splitext(__file__)[0])
    
	# create the parser
	description = """Input Parser"""
	parser = OptionParser(option_class=MultipleOption,
		usage='usage: %prog -f <file> -d <datatypes> -o <outputlocation>',
		version='%s %s' % (PROG, VERSION),
		description=description)

	# add option for specifying file name
	parser.add_option("-f", "--file", 
		action="extend", type="string",
		dest='file',
		metavar='FILE',
		help='path to input file')

	# add option for specifying data types for file
	parser.add_option("-d", "--datatypes", 
		action="extend", type="string",
		dest='datatypes',
		metavar='DATATYPES',
		help='comma separated list of data types')

	# add option for specifying output directory
	parser.add_option("-o", "--outputlocation", 
		action="extend", type="string",
		dest='outputlocation',
		metavar='OUTPUTLOCATION',
		help='output location for generated file')

	# add option for specifying that the first line (headers) should be skipped
	parser.add_option("-s",  "--skip header", 
		action="store_true", 
		dest="skipheader",
		metavar='SKIPHEADER',
		help='flag skip first line of file')

	# help requested
	if len(sys.argv) == 1:
		parser.parse_args(['--help'])

	# make sure the arguments are valid
	options, args = parser.parse_args()
	if not validate_arguments(options):
		sys.exit(2)

	# get the path to the output file
	inputPath, inputFilename = os.path.split(options.file[0])
	outputFile = getOutputFile(options.outputlocation[0], inputFilename)

	# get data types specified for the file
	dataTypeList = options.datatypes[0].split(",")

	# store skip header flag value
	skipheader = options.skipheader

	with open(options.file[0], 'rb') as inputFile:

		# open file for writing
		with open(outputFile, 'wb') as outputFile:
			csvWriter = csv.writer(outputFile, delimiter=',')

			csvReader = csv.reader(inputFile, delimiter=',')
			for row in csvReader:
				count = 0

				# store values to be writtrn to row
				writeRow = []

				if (skipheader):
					skipheader = False
				else:

					# process each data type passed in for each row
					for dataType in dataTypeList:


						# get current row
						item = row[count]

						if dataType == 'INT':

							# remove any non-integer characters
							pattern = re.compile(r'^[0-9]+$')
							if not pattern.findall(item):
								print('Output: INT \"'+ item + '\" contains non numeric characters. These will be removed.')
								item = re.sub('[^0-9]','', item)
							writeRow.append(item)    

						elif dataType == 'DECIMAL':

							# change any instances of commas to decimals
							pattern = re.compile(r'^[0-9 ,]+$')
							if ',' in item:
								print('Output: DECIMAL \"'+ item + '\" contains commas. They will be replaced with decimal points.')
								item = re.sub(',','.', item)
							
							# remove any non-integer or decimal characters
							pattern = re.compile(r'^[0-9 \.]+$')
							if not pattern.findall(item):
								print('Output: DECIMAL \"'+ item + '\" contains invalid characters. These will be removed.')
								item = re.sub('[^0-9 \.]','', item)
							writeRow.append(item)

						else:

							# leave strings as they are
							writeRow.append(item)

						# move to the next data type
						count = count + 1

					# write the data to the output file
					csvWriter.writerow(writeRow)

if __name__ == '__main__':
	main()
