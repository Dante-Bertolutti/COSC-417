import os
print(os.popen("tracert 8.8.8.8").read())
