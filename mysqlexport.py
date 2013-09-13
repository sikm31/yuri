import subprocess
subprocess.call(r'mysqldump -u root -p -h localhost djangodb > djangodb.sql', shell=True)