join us t.me/jupyter_python 
# DIGITAL CLOCK IN PYTHON
# clcoding
from datetime import datetime
from time import sleep
while 1:
    n=datetime.now()
    print(datetime.strftime(n,"%H:%M:%S"), end='\r')
    sleep(1)
