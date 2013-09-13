import subprocess
subprocess.call(r'mysql -u root -p -h localhost djangodb < djangodb.sql', shell=True)