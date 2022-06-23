import pdfkit
import argparse
import pandas as pd
import datetime as dt
import locale
import re
import os
from progress.bar import Bar
from core.utils import read_sheet

def populate_field (match, entry, entries, keywords):
	tokens = match.group(1).split(';')
	if len(tokens) == 0:
		return ''
	name = tokens[0]
	key = name.strip().lower()
	output = ''
	if key.startswith('!'):
		if key not in keywords:
			print("Keyword '" + key + "' does not exist");
			return key
		output = str(keywords[key])
	elif key not in entry:
		value = input(name + ": ")
		for other in entries:
			other[key] = value
		output = value
	else:
		output = entry[key]
	output = str(output)
	if len(tokens) > 1:
		if 'd' in tokens[1] and len(tokens) > 2:
			output = dt.datetime.strptime(output, "%Y-%m-%d").strftime(tokens[2])
		if 'u' in tokens[1]:
			output = output.upper()
		if 'l' in tokens[1]:
			output = output.lower()
		if 'c' in tokens[1]:
			output = output.capitalize()
		if 's' in tokens[1]:
			output = output.replace(' ', '_')
	return output

PATTERN_DATA = "(?<!\\$)\\${([^}]*)}"
PATTERN_DATA_NO_KEYWORDS  = "(?<!\\$)\\${(?!!)([^}]*)}"
PDF_SETTINGS = {
	"enable-local-file-access": True,
	"page-size": "A4",
	"margin-top": "15mm",
	"margin-bottom": "25mm",
	"margin-left": "30mm",
	"margin-right": "30mm"
}

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"-t",
		"--template",
		default="template.html",
		dest="template_path"
	)
	parser.add_argument(
		"-d",
		"--data",
		dest="data_path"
	)
	parser.add_argument(
		"-o",
		"--output",
		default="${!i}_out.pdf",
		dest="output_path",
		required=True
	)
	parser.add_argument(
		"-l",
		"--locale",
		default="pt_BR.UTF-8",
		dest="locale_str"
	)
	parser.add_argument(
		"--input-engine",
		dest="input_engine",
	)

	args = parser.parse_args()

	locale.setlocale(locale.LC_TIME, args.locale_str)

	data_entries = pd.DataFrame()

	if args.data_path == None:
		with open(args.template_path, encoding='utf8') as template_f:
			matches = re.findall(PATTERN_DATA_NO_KEYWORDS, template_f.read())
			entry = {}
			for match in matches:
				match = match.split(';')[0]
				entry[match.strip().lower()] = input(match + ": ")
			data_entries.append(entry)
	else:
		data_entries = read_sheet(args.data_path, args.input_engine, str)

	data_entries.rename(columns=lambda c: c.strip().lower(), inplace=True)
	data_entries = data_entries.to_dict('records')

	with open(args.template_path, encoding='utf8') as template_f:
		template_str = template_f.read()
		keywords = {"!date": dt.datetime.now().strftime("%Y-%m-%d"), "!i": 0}
		bar = Bar('Generating', max=len(data_entries))
		for entry in data_entries:
			result_html = re.sub(PATTERN_DATA, lambda x: populate_field(x, entry, data_entries, keywords), template_str)
			filename_pdf = re.sub(PATTERN_DATA, lambda x: populate_field(x, entry, data_entries, keywords), args.output_path)
			#filename_tmp = filename_pdf+"_TEMP_" + str(dt.datetime.now().microsecond) + ".html"
			#with open(filename_tmp, 'w', encoding="utf8") as tmp:
			#	tmp.write(result_html)
			#pdfkit.from_file(filename_tmp, filename_pdf, PDF_SETTINGS)
			#os.remove(filename_tmp)
			pdfkit.from_string(result_html, filename_pdf, PDF_SETTINGS)
			keywords["!i"] += 1
			bar.next()
		bar.finish()