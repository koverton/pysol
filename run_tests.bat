
rem Executes test code against external addresses of demo-tr server

IF "%SOLCLIENT_DIR%"=="" (set SOLCLIENT_DIR=.)

set PYTHONHOME=c:\Python27
set PYTHONPATH=.;%SOLCLIENT_DIR%\lib;%PYTHONHOME%\Lib
set PATH=%SOLCLIENT_DIR%\lib;%PYTHONHOME%;%PATH%

python tests\data_test.py
python tests\callback_test.py
python tests\direct_test.py ../properties/demotr-ext.properties
python tests\persistent_test.py ../properties/demotr-ext.properties
python tests\persistent_ack_test.py ../properties/demotr-ext.properties
python tests\persistent_streaming_test.py ../properties/demotr-ext.properties
rem python tests\cache_test.py ../properties/demotr-ext.properties
