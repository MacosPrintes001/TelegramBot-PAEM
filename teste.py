import datetime

a = input("")

if "/" in a:
    print("tem")
else:
    print("Não tem")










def tempo():
    tstart = datetime.datetime.now().time
    tlimit = tstart + datetime.timedelta(seconds=5)
    tnow = tstart

    while True:
        tnow = datetime.datetime.now().time
        if tnow == tlimit or tnow > tlimit:
            #ocioso
            pass
            
def ocioso():
    print("Ususario Ocioso")