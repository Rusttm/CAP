import sys
import os
import platform

sys_os = platform.platform()
dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
os.environ['PATH'] += ':' + dir_path
sys.path.insert(0, dir_path)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
print(f"Current project path: {dir_path} added to System: {sys_os}")
print(os.path.realpath(__file__))
from Pgsql.PgsqlUpdaterAir import PgsqlUpdaterAir

runner = PgsqlUpdaterAir()
runner.update_all_report_tables()
print("script runed all is ok!!!")