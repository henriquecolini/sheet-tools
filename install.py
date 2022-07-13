import importlib
import importlib.util
import subprocess
import sys
import platform

dependencies = ["progress", "pdfkit", "pandas", "openpyxl", "detect_delimiter"]
yes = ['', 'y', 'yes', 's', 'sim']
no = ['n', 'no', 'nao', 'não']

def pkg_install(package):
	subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def pkg_check(package):
	pkg_spec = importlib.util.find_spec(package)
	return pkg_spec is not None

def winget_check():
	try:
		subprocess.check_call(["winget", "-v"], stdout=subprocess.DEVNULL)
		return True
	except:
		return False

def winget_wk_check():
	return subprocess.run(["winget", "show", "wkhtmltopdf"], stdout=subprocess.DEVNULL).returncode == 0

def wk_check():
	try:
		subprocess.check_call(["wkhtmltopdf", "-V"], stdout=subprocess.DEVNULL)
		return True
	except:
		return False

def confirm():
	choice = 'NONE'
	while choice.strip().lower() not in [*yes, *no]:
		choice = input("Continuar? [s]im, [n]ao (padrão: sim) ")
	if choice.strip().lower() in no:
		exit(2)

if __name__ == "__main__":

	print("\nBem vindo ao instalador do sheet-tools.")
	print("Esse script irá te ajudar a instalar todas as dependências necessárias.")
	confirm()

	print("\nVerificando dependências do pip...")

	missing = []
	for dep in dependencies:
		if not pkg_check(dep):
			missing.append(dep)

	if len(missing) > 0:
		print("Os seguintes pacotes estão faltando e devem ser instalados:")
		print(", ".join(missing))
		confirm()
		for dep in missing:
			try:
				pkg_install(dep)
			except Exception as ex:
				print(ex)
				exit(1)
	else:
		print("Todas as dependências já estão instaladas. Continuando.")

	print("\nO software 'wkhtmltopdf' é necessário para o funcionamento do sheet-to-pdf.")
	print("Sua instalação e configuração pode exigir alguns passos manuais.\n")

	print("Detectando plataforma...")

	if platform.system() == "Windows":
		if winget_check():
			print("Verificando sua instalação...")
			if winget_wk_check():
				print("wkhtmltopdf encontrado.")
			else:
				print("wkhtmltopdf não encontrado.")
				print("Podemos usar o winget para instalar ele.")
				confirm()
				try:
					subprocess.check_call(["winget", "install", "wkhtmltopdf"])
				except Exception as ex:
					print(ex)
			print("\nVerificando variável PATH...")
			if wk_check():
				print("wkhtmltopdf está no PATH.")
				print("\nTodos os componentes estão instalados com sucesso.")
			else:
				print("wkhtmltopdf não está no PATH.")
				print("Você deve adicionar o diretório de seu executável à esta variável de ambiente.")
				print("Este costuma ser:")
				print(r'C:\Program Files\wkhtmltopdf\bin')
				print("Depois disso, reabra seu terminal, e execute o comando 'wkhtmltopdf -V' para verificar a instalação.")
				print("\nTerminado.")
		else:
			print("Você está no Windows, e o sistema winget não foi encontrado.")
			print("Você terá que instalar manualmente o wkhtmltopdf, em:")
			print("https://wkhtmltopdf.org/downloads.html")
			print("Após sua instalação, você deve adicionar o diretório de seu executável à variável de ambiente PATH.")
			print("Este costuma ser:")
			print(r'C:\Program Files\wkhtmltopdf\bin')
			print("Depois disso, reabra seu terminal, e execute o comando 'wkhtmltopdf -V' para verificar a instalação.")
			print("\nTerminado.")
	else:
		print("Você está usando " + platform.system() + ".")
		print("Você terá que instalar manualmente o wkhtmltopdf, em:")
		print("https://wkhtmltopdf.org/downloads.html")
		print("Usuários de Ubuntu podem utilizar o apt-get:")
		print("sudo apt-get install wkhtmltopdf")
		print("\nTerminado.")


