import sys
import os
import platform


sys_os = platform.platform()
APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(APP_PATH)
sys.path.append(MODULE_PATH)
sys.path.insert(0, os.path.dirname("/home/rusttm/PycharmProjects/CAP/"))
print(f"Current project path: {APP_PATH}, module {MODULE_PATH} added to System: {sys_os}")
