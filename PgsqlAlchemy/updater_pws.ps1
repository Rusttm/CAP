$path = 'C:\Users\User\Desktop\CAP\CAP\PgsqlAlchemy\ModALUpdaters'
$file = 'ModALUpdater.py'
Write-Output $1
$cmd = $path+'\\'+$file  # This line of code will create the concatenate the path and file
Start-Process $cmd  # This line will execute the cmd 