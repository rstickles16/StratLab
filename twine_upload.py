import subprocess as sp
import os

version = '1.0.24'

folder_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(folder_path)

# Send version to the package
with open(f'{folder_path}/StratLab/__vrsn__.txt', 'w') as file:
    file.write(version)

sp.run(['python', 'setup.py', 'sdist', 'bdist_wheel'])
sp.run(['twine', 'upload', 'dist/*'])

