import sys
import os
import platform


sys_os = platform.platform()
APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(APP_PATH)
sys.path.append(MODULE_PATH)
print(f"Current project path: {APP_PATH}, module {MODULE_PATH} added to System: {sys_os}")


# or
# dir_path = os.path.dirname(os.path.realpath(__file__))
# os.environ['PATH'] += ':' + dir_path
# sys.path.insert(0, dir_path)
# print(os.path.realpath(__file__))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print(f"Current project path: {dir_path} added to System: {sys_os}")