import subprocess as sp
import os

folder_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(folder_path)

sp.run(['python', 'setup.py', 'sdist', 'bdist_wheel'])
sp.run(['twine', 'upload', 'dist/*'])