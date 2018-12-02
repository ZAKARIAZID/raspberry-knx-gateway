'''
'''
import copy
import ip
import timeupdater 
import core

#Connection
tun = ip.KNXIPTunnel()
if tun.connected or tun.connect():
    print("Connected!... [{}:{}]".format(tun.remote_ip,remote_port))
    tun.keepalive()
    print("Checking KNX...")
    if tun.check_connection_state():
        print("KNX OK!")
else:
    print("ERROR:Enable to Connect to KNX !")
#Read addresses
if tun.connected == False:
    with open("config.txt","r") as fic:
        data = fic.readlines()
        actr_list = copy.deepcopy(data)
        temp = []
        for i in range(0,len(data)):
            temp = data[i].split(":")
            data[i] = temp[0]
            actr_list[i] = temp[1].replace("\n","")
            del temp[:]

#defin functions

'''Extract data from inputs & WRITE'''
def WriteTo(add = "", actor = "", value = 0):
    act = "" 
    resAdd = ""
    pareadd = 0
    valuetosend = [value]
    if not actor == "":
        try:
            resAdd = data[actr_list.index(actor)]
            act = actor
        except:
            print("ERROR:Actor not found !")
            return
    elif not add == "":
        try:
            resAdd = add
            act = actr_list[data.index(add)]
        except:
            print("ERROR:Address not found !")
            return 
    print("Sending {} => {} :: {} ...".format(value, act, resAdd)) 
    pareadd = core.parse_group_address(resAdd)
    tun.group_write(addr=pareadd, data=valuetosend)
    time.sleep(3)


'''Extract data from inputs & READ'''
def ReadFrom(add = "", actor = ""):
    act = "" 
    resAdd = ""
    pareadd = 0
    if not actor == "":
        try:
            resAdd = data[actr_list.index(actor)]
            act = actor
        except:
            print("ERROR:Actor not found !")
            return
    elif not add == "":
        try:
            resAdd = add
            act = actr_list[data.index(add)]
        except:
            print("ERROR:Address not found !")
            return 
    print("Asking: {} :: {}...".format(act, resAdd)) 
    pareadd = core.parse_group_address(resAdd)
    ValG = tun.group_read(addr=pareadd, use_cache=True, timeout=1)
    if ValG != None:
        print("State of {} : {} ".format(act, ValG)) 
    else:
        print("ERROR:Value not received !")
    
'''Extract data from inputs & TOGGLE'''
def Togg(add = "", actor = ""):
    act = "" 
    resAdd = ""
    pareadd = 0
    if not actor == "":
        try:
            resAdd = data[actr_list.index(actor)]
            act = actor
        except:
            print("ERROR:Actor not found !")
            return
    elif not add == "":
        try:
            resAdd = add
            act = actr_list[data.index(add)]
        except:
            print("ERROR:Address not found !")
            return    
    print("Toggling {} :: {}".format(act, resAdd))                
    pareadd = core.parse_group_address(resAdd)             
    tun.group_toggle(addr=pareadd)     
         
'''LOGGER'''              
def logger():
    cmd_user = {
        "w":0,
        "r":1,
        "t":2,
        "q":3,
        "d":4,
        "c":5,
        "h":6,
        "s":7,
    }
    User = []
    CommExt = []
    adds = ""
    actr = ""
    valu = 0
    print("Welcom... for Help tap h /:1")
    while(True):
        verified = True
        AddVer = False
        UserTap = input(":>") 
        if ":" in UserTap:
            User = UserTap.split(":")                  
            if "/" in User[0]:
                AddVer = True
            if not User[1].isnumeric():
                print("ERROR:Invalide value !")
                verified = False  
        else:
            print("ERROR: Invalid command !")
            verified = False 
        if verified == True and " " in User[0]: #r,w,t
            CommExt = User[0].split(" ")
            cmdType = cmd_user.get(CommExt[0],"Command not found !")
            if AddVer and cmdType != "Command not found !":
                adds = CommExt[1]
            elif cmdType != "Command not found !":
                act = " ".join(CommExt[1:]) 
            else:
                print(cmdType)
                verified = False

            if verified and AddVer:
                if int(cmdType) == 0:
                    WriteTo(add=adds, value=int(User[1]))
                if int(cmdType) == 1:
                    ReadFrom(add = adds)
                if int(cmdType) == 2:
                    Togg(add = adds)
            if verified and not AddVer:
                if int(cmdType) == 0:
                    WriteTo(actor = act, value=int(User[1]))
                if int(cmdType) == 1:
                    ReadFrom(actor = act)
                if int(cmdType) == 2:
                    Togg(actor = act)    
            if verified:
                if int(cmdType) == 6:
                    print("*** Form: Command address/name:Value ***".center(50))
                    print("\tCommand: \n \tr : Read | w : Write | t : Toggle | d : Disconnect | c : Connect | q : Quit")
                if int(cmdType) == 4:
                    tun.disconnect()
                if int(cmdType) == 5:
                    tun.connect()        
                if int(cmdType) == 3:
                    break
                if int(cmdType) == 7:
                    if tun.check_connection_state():
                        print("KNX OK !")
                    else:
                        print("KNX not available !")


logger()
