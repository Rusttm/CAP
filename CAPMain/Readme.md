! before Start the project you should run setup.py for build all dependencies in OS

module CAPMain is main module and runs from command prompt.
If you want it to run as a system daemon, please read (systemctl_instructions)

CAPMain:
1. Starts module SocSrv:
   1. SocketServer
   2. socket client <em>admin</em>
2. starts API_Tbot:
   1. api Telegrambot
   2. socket client <em>telegrambot</em>
3. Pgsql module:
   1. socket client <em>pgsql</em>
   2. initiator for new empty database. copy all current data from MoiSklad
   3. database updater that updates bases to actual conditions
4. SQLAlchemy module
5. Django module

