import pandas as pd
from detect_delimiter import detect

def find_engine(path: str, engine: str):
	if path == None:
		return None
	if engine == None:
		tokens = path.split('/')[-1].split('\\')[-1].split('.')
		if len(tokens) >= 2:
			engine = tokens[-1]
	if engine in [None, "csv"]:
		return "csv"
	if engine in ["excel", "xls", "xlsx", "xlsm", "xlsb", "odf", "ods", "odt"]:
		return "excel"
	return None

def read_sheet(path: str, engine: str, dtype: type):
	engine = find_engine(path, engine)
	if engine == None:
		raise Exception("Unknown file type")
	if engine == "csv":
		delimiter = ';'
		with open(path) as myfile:
			firstline = myfile.readline()
			delimiter = detect(firstline, ';')
			myfile.close()
		return pd.read_csv(path, sep=delimiter, dtype=dtype)
	if engine == "excel":
		return pd.read_excel(path, dtype=dtype)

def write_sheet(df: pd.DataFrame, path: str, engine: str):
	engine = find_engine(path, engine)
	if engine == None:
		raise Exception("Unknown file type")
	if engine == "csv":
		df.to_csv(path, sep=';')
	if engine == "excel":
		df.to_excel(path)