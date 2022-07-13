import argparse
import re
import pandas as pd
from core.utils import read_sheet, write_sheet

def read_col (path: str, col_name: str, engine: str = None):
	sheet = read_sheet(path, engine, str)
	if col_name not in sheet:
		raise Exception("Sheet does not contain the '" + col_name + "' column")
	return sheet[col_name]

def parse_form (entry: str):
	form = {}
	last_question = None
	for i, line in enumerate(entry.split('\n')):
		if i == 0:
			m = re.match(r"(\d\d\/\d\d\/\d\d\d\d) (\d\d:\d\d) \[.+\] (.+):", line)
			if m != None:
				form["Date"] = m.group(1)
				form["Time"] = m.group(2)
				form["Name"] = m.group(3)
		else:
			if len(line.strip()) <= 0:
				continue
			if last_question == None:
				last_question = line
			else:
				form[last_question] = line.lstrip("- ").strip()
				last_question = None
	return pd.Series(form)

def parse_forms (col: pd.Series):
	forms = []
	for entry in col:
		forms.append(parse_form(entry))
	return pd.DataFrame(forms)

def form_to_sheet(data_path: str, col_name: str, output_path: str, input_engine: str, output_engine: str):
	col = read_col(data_path, col_name, input_engine)
	df = parse_forms(col)
	write_sheet(df, output_path, output_engine)


if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument(
		"-d",
		"--data",
		dest="data_path",
		required=True
	)
	parser.add_argument(
		"-c",
		"--column",
		dest="col",
		required=True
	)
	parser.add_argument(
		"-o",
		"--output",
		dest="output_path",
		required=True
	)
	parser.add_argument(
		"--input-engine",
		dest="input_engine",
	)
	parser.add_argument(
		"--output-engine",
		dest="output_engine",
	)
	parser.add_argument(
		"--debug",
		dest="is_debug",
		action=argparse.BooleanOptionalAction
	)
	args = parser.parse_args()

	try:
		form_to_sheet(args.data_path, args.col, args.output_path, args.input_engine, args.output_engine)
	except Exception as ex:
		if args.is_debug:
			raise ex
		else:
			print("Error:", ex)