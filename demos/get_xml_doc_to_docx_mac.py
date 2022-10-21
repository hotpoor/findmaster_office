import os
import subprocess
# source = "a.doc"
dest = "./dest"
# g = os.listdir(source)
# file_path = [f for f in g if f.endswith(('.doc'))]
file = "./dest/a.doc"
print (file)
output = subprocess.check_output(["/Applications/LibreOffice.app/Contents/MacOS/soffice","--headless","--convert-to","docx",file,"--outdir",dest])
print('success!')