import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import telnetlib
import time
import threading

#windows properties
win = tk.Tk()
win.title("OLT AUTO REGISTER & REMOVE ONT")
win.resizable(False,False)


#threading Function
def checkprogress(t):
    if not t.is_alive():
        l3["text"] = "Ready"
        l3["fg"] = "green"
        b1["state"] = "normal"
        b2["state"] = "normal"
        b3["state"] = "normal"
        b4["state"] = "normal"
        b5["state"] = "normal"
        b6["state"] = "normal"
        b7["state"] = "normal"
        b8["state"] = "normal"
    else:
        win.after(1000,checkprogress,t)

def regall_btn():
    b1["state"] = "disabled"
    b2["state"] = "disabled"
    b3["state"] = "disabled"
    b4["state"] = "disabled"
    b5["state"] = "disabled"
    b6["state"] = "disabled"
    b7["state"] = "disabled"
    b8["state"] = "disabled"
    l3["text"] = "Processing - Register All"
    l3["fg"] = "orange"
    t = threading.Thread(target=register_all)
    t.start()
    checkprogress(t)

def remall_btn():
    b1["state"] = "disabled"
    b2["state"] = "disabled"
    b3["state"] = "disabled"
    b4["state"] = "disabled"
    b5["state"] = "disabled"
    b6["state"] = "disabled"
    b7["state"] = "disabled"
    b8["state"] = "disabled"
    l3["text"] = "Processing - Remove All"
    l3["fg"] = "orange"
    t = threading.Thread(target=remove_all)
    t.start()
    checkprogress(t)

def check_ont_btn():
    b1["state"] = "disabled"
    b2["state"] = "disabled"
    b3["state"] = "disabled"
    b4["state"] = "disabled"
    b5["state"] = "disabled"
    b6["state"] = "disabled"
    b7["state"] = "disabled"
    b8["state"] = "disabled"
    l3["text"] = "Processing - Check Registered ONU"
    l3["fg"] = "orange"
    t = threading.Thread(target=check_onu_reg)
    t.start()
    checkprogress(t)

def check_noont_btn():
    b1["state"] = "disabled"
    b2["state"] = "disabled"
    b3["state"] = "disabled"
    b4["state"] = "disabled"
    b5["state"] = "disabled"
    b6["state"] = "disabled"
    b7["state"] = "disabled"
    b8["state"] = "disabled"
    l3["text"] = "Processing - Check Unregistered ONU"
    l3["fg"] = "orange"
    t = threading.Thread(target=check_onu_unreg)
    t.start()
    checkprogress(t)

def reg1_btn():
    b1["state"] = "disabled"
    b2["state"] = "disabled"
    b3["state"] = "disabled"
    b4["state"] = "disabled"
    b5["state"] = "disabled"
    b6["state"] = "disabled"
    b7["state"] = "disabled"
    b8["state"] = "disabled"
    l3["text"] = "Processing - Register 1 ONU"
    l3["fg"] = "orange"
    t = threading.Thread(target=regist1)
    t.start()
    checkprogress(t)

def rem1_btn():
    b1["state"] = "disabled"
    b2["state"] = "disabled"
    b3["state"] = "disabled"
    b4["state"] = "disabled"
    b5["state"] = "disabled"
    b6["state"] = "disabled"
    b7["state"] = "disabled"
    b8["state"] = "disabled"
    l3["text"] = "Processing - Remove 1 ONU"
    l3["fg"] = "orange"
    t = threading.Thread(target=remove1)
    t.start()
    checkprogress(t)

def checksn_btn():
    b1["state"] = "disabled"
    b2["state"] = "disabled"
    b3["state"] = "disabled"
    b4["state"] = "disabled"
    b5["state"] = "disabled"
    b6["state"] = "disabled"
    b7["state"] = "disabled"
    b8["state"] = "disabled"
    l3["text"] = "Processing - Checking Selected Serial Number"
    l3["fg"] = "orange"
    t = threading.Thread(target=checkonusn)
    t.start()
    checkprogress(t)

def regp3oe_btn():
    b1["state"] = "disabled"
    b2["state"] = "disabled"
    b3["state"] = "disabled"
    b4["state"] = "disabled"
    b5["state"] = "disabled"
    b6["state"] = "disabled"
    b7["state"] = "disabled"
    b8["state"] = "disabled"
    l3["text"] = "Processing - Register 1 ONU Mode PPPOE"
    l3["fg"] = "orange"
    t = threading.Thread(target=registpppoe)
    t.start()
    checkprogress(t)

#main funtion
def register_all():
    #verify if entry is filled
    host = str(e1.get())
    usr = str(e2.get())
    pwd = str(e3.get())
    port = str(e4.get())
    if port == "":
        port = 23
    if host == "":
        return messagebox.showerror("Error","Host IP is empty!")
    if usr == "":
        return messagebox.showerror("Error","Username is empty!")
    if pwd == "":
        return messagebox.showerror("Error","Password is empty!")
    print(f"{host},{usr},{pwd},{port}")

    tn = telnetlib.Telnet(host,port,3)
    tn.write(bytes(f"{usr}\n",'ascii'))  # username
    tn.write(bytes(f"{pwd}\n",'ascii'))  # password
    time.sleep(0.7)
    fin = tn.read_very_eager().decode('utf-8')
    tb1.insert(tk.INSERT, f"{fin}\n")
    print(fin)
    tn.write(b'show pon onu uncfg\n')  # cek Unregistered onu
    time.sleep(1)
    fin = tn.read_very_eager().decode('utf-8')
    tb1.insert(tk.INSERT, f"{fin}\n")
    print(fin)

    ####unregistered onu
    onu_uncfg = []
    onu_uncfg2 = fin.splitlines()[3:-1]
    # print(f"hasil {onu_uncfg2}")
    for x in onu_uncfg2:
        result = " ".join(x.split())
        onu_uncfg.append(result)

    onu_uncfg_lst = []

    for x in onu_uncfg:
        f = x.split(" ")
        # print(f)
        onu_uncfg_lst.append([f[0], f[2]])

    print(onu_uncfg_lst)

    ######maincode

    if onu_uncfg_lst == []:
        print("\nSUMMARY INFO : Nothing to register\n")
        tb1.insert(tk.INSERT, "\nSUMMARY INFO : Nothing to register\n")

    for gpon in onu_uncfg_lst:
        tn.write(bytes(f"show gpon onu state {gpon[0]}\n", 'ascii'))  # check used index onu
        time.sleep(1)
        data_onu_index = tn.read_very_eager().decode('utf-8')
        print(data_onu_index)

        # get registered and unregistered onu index
        onu_cfg = []
        onu_cfg2 = data_onu_index.splitlines()[3:-2]
        onu_cfg_lst = []
        # print(onu_cfg2)

        for x in onu_cfg2:
            result = " ".join(x.split())
            onu_cfg.append(result)

        for x in onu_cfg:
            f = x.split(" ")
            # print(f)
            onu_cfg_lst.append(f[0])
        print(onu_cfg_lst)

        ffind = False
        i = 0
        count = 1
        while count > 0:
            i += 1
            temp_index = (f"{gpon[0][9:]}:{i}")
            count = onu_cfg_lst.count(temp_index)
            if count == 0:
                onu_index = temp_index
                onu_cfg_lst.append(onu_index)

        print(onu_index)

        # register SN on specific interface
        tn.write(b'conf t\n')  # goto configure state
        tn.write(bytes(f"interface {gpon[0]}\n", 'ascii'))  # go to interface gpon olt
        # get data registered & unregistered onu index
        tn.write(bytes(f"onu {i} type ALL sn {gpon[1]}\n", 'ascii'))  # register onu sn on specific index (10)
        tn.write(b'exit\n')
        print(gpon[1])
        time.sleep(1)
        fiz = tn.read_very_eager().decode('utf-8')
        tb1.insert(tk.INSERT, f"{fiz}\n")
        print(fiz)

        # configure onu profile
        # tn.write(b'interface gpon-onu_1/1/8:10\n')  # goto interface gpon onu
        tn.write(bytes(f"interface gpon-onu_{onu_index}\n", "ascii"))
        tn.write(b'tcont 1 profile default\n')  # add profile
        tn.write(b'gemport 1 tcont 1\n')
        tn.write(b'service-port 1 vport 1 user-vlan 147 vlan 147\n')  # insert to vlan 147
        tn.write(b'exit\n')
        time.sleep(1)
        fiz = tn.read_very_eager().decode('utf-8')
        tb1.insert(tk.INSERT, f"{fiz}\n")
        print(fiz)

        # onu management
        # tn.write(b'pon-onu-mng gpon-onu_1/1/8:10\n')  # go to onu management
        tn.write(bytes(f"pon-onu-mng gpon-onu_{onu_index}\n", 'ascii'))
        tn.write(b'service 1 gemport 1 vlan 147\n')  # add vlan
        tn.write(b'wan-ip 1 mode dhcp vlan-profile labtjat147 host 1\n')  # add dhcp ip & vlan profile
        tn.write(b'end\n')
        print(f"success register {gpon[1]} on {onu_index}")
        time.sleep(1)
        fiz = tn.read_very_eager().decode('utf-8')
        tb1.insert(tk.INSERT, f"{fiz}\n")
        print(fiz)
    return messagebox.showinfo("Success","Register Completed")

def remove_all():
    #verify if entry is filled
    host = str(e1.get())
    usr = str(e2.get())
    pwd = str(e3.get())
    port = str(e4.get())
    if port == "":
        port = 23
    if host == "":
        return messagebox.showerror("Error","Host IP is empty!")
    if usr == "":
        return messagebox.showerror("Error","Username is empty!")
    if pwd == "":
        return messagebox.showerror("Error","Password is empty!")
    print(f"{host},{usr},{pwd},{port}")

    tn = telnetlib.Telnet(host,port,3)
    tn.write(bytes(f"{usr}\n",'ascii'))  # username
    tn.write(bytes(f"{pwd}\n",'ascii'))  # password
    time.sleep(0.5)
    fin = tn.read_very_eager().decode('utf-8')
    tb1.insert(tk.INSERT, f"{fin}\n")
    tn.write(b'show gpon onu state\n')
    time.sleep(0.5)
    fin = tn.read_very_eager().decode('utf-8')
    tb1.insert(tk.INSERT, f"{fin}\n")
    print(fin)
    onu_reg = []
    onu_reg2 = fin.splitlines()[3:-2]
    for x in onu_reg2:
        result = " ".join(x.split())
        onu_reg.append(result)

    onu_reglst = []

    for x in onu_reg:
        f = x.split(" ")
        # print(f)
        onu_reglst.append(f[0])
    onu_reg = []

    # print(onu_reglst)
    # ubah jadi data = [[port,index],[port,index],[],....]
    for x in onu_reglst:
        f = x.split(":")
        onu_reg.append(f)

    print(onu_reg)

    # maincode (remove onu)
    for onu in onu_reg:
        tn.write(b"conf t\n")
        tn.write(bytes(f"interface gpon-olt_{onu[0]}\n", "ascii"))
        tn.write(bytes(f"no onu {onu[1]}\n", "ascii"))
        tn.write(b"end\n")
        time.sleep(0.5)
        status = tn.read_very_eager().decode('utf-8')
        tb1.insert(tk.INSERT, f"{status}\n")
        print(status)
    return messagebox.showinfo("Success","Remove Completed")

def check_onu_reg():
    #verify if entry is filled
    host = str(e1.get())
    usr = str(e2.get())
    pwd = str(e3.get())
    port = str(e4.get())
    if port == "":
        port = 23
    if host == "":
        return messagebox.showerror("Error","Host IP is empty!")
    if usr == "":
        return messagebox.showerror("Error","Username is empty!")
    if pwd == "":
        return messagebox.showerror("Error","Password is empty!")
    print(f"{host},{usr},{pwd},{port}")

    try:
        tn = telnetlib.Telnet(host,port,3)
    except:
        return "error. Wrong IP or Port"

    tn.write(bytes(f"{usr}\n","ascii"))  # username
    tn.write(bytes(f"{pwd}\n","ascii"))  # password
    time.sleep(0.5)
    tn.write(b'show gpon onu state\n')
    time.sleep(2)
    fin = tn.read_very_eager().decode('utf-8')
    tb1.insert(tk.INSERT,f"{fin}\n")
    print(fin)

def check_onu_unreg():
    #verify if entry is filled
    host = str(e1.get())
    usr = str(e2.get())
    pwd = str(e3.get())
    port = str(e4.get())
    if port == "":
        port = 23
    if host == "":
        return messagebox.showerror("Error","Host IP is empty!")
    if usr == "":
        return messagebox.showerror("Error","Username is empty!")
    if pwd == "":
        return messagebox.showerror("Error","Password is empty!")
    print(f"{host},{usr},{pwd},{port}")

    tn = telnetlib.Telnet(host,port,3)
    tn.write(bytes(f"{usr}\n","ascii"))  # username
    tn.write(bytes(f"{pwd}\n","ascii"))  # password
    time.sleep(1)
    fin = tn.read_very_eager().decode('utf-8')
    tb1.insert(tk.INSERT, f"{fin}\n")
    print(fin)
    tn.write(b'show pon onu uncfg\n')  # cek Unregistered onu
    time.sleep(1)
    fin = tn.read_very_eager().decode('utf-8')
    tb1.insert(tk.INSERT, f"{fin}\n")
    print(fin)

def regist1():
    #verify if entry is filled
    host = str(e1.get())
    usr = str(e2.get())
    pwd = str(e3.get())
    port = str(e4.get())
    if port == "":
        port = 23
    if host == "":
        return messagebox.showerror("Error","Host IP is empty!")
    if usr == "":
        return messagebox.showerror("Error","Username is empty!")
    if pwd == "":
        return messagebox.showerror("Error","Password is empty!")
    print(f"{host},{usr},{pwd},{port}")
    #get unregister ONU data
    tn = telnetlib.Telnet(host,port,3)
    tn.write(bytes(f"{usr}\n",'ascii'))  # username
    tn.write(bytes(f"{pwd}\n",'ascii'))  # password
    time.sleep(1)
    fin = tn.read_very_eager().decode('utf-8')
    tb1.insert(tk.INSERT, f"{fin}\n")
    print(fin)
    tn.write(b'show pon onu uncfg\n')  # cek Unregistered onu
    time.sleep(1)
    fin = tn.read_very_eager().decode('utf-8')
    tb1.insert(tk.INSERT, f"{fin}\n")
    print(fin)

    ####unregistered onu
    onu_uncfg = []
    onu_uncfg2 = fin.splitlines()[3:-1]
    # print(f"hasil {onu_uncfg2}")
    for x in onu_uncfg2:
        result = " ".join(x.split())
        onu_uncfg.append(result)

    onu_uncfg_lst = []

    for x in onu_uncfg:
        f = x.split(" ")
        # print(f)
        onu_uncfg_lst.append([f[0], f[2]])

    print(onu_uncfg_lst)

    ######maincode

    if onu_uncfg_lst == []:
        print("\nSUMMARY INFO : Nothing to register\n")
        tb1.insert(tk.INSERT, "\nSUMMARY INFO : Nothing to register\n")
        return messagebox.showwarning("Nothing to Register", "Nothing to Register")



    def selection_changed(event):
        selection = combo.get()
        v = messagebox.askyesno(
            title="Confirmation",
            message=f"Selected option: {selection}. Want to Register this ONU?"
        )
        print(v)
        if v == True:
            selection = selection.split()
            gpon = [selection[0],selection[1]]
            print(f"Process to Register : interface : {gpon[0]},{gpon[1]}")
            #return main_window.destroy()
            #execute register selected ONU
            tn.write(bytes(f"show gpon onu state {gpon[0]}\n", 'ascii'))  # check used index onu
            time.sleep(1)
            data_onu_index = tn.read_very_eager().decode('utf-8')
            print(data_onu_index)

            # get registered and unregistered onu index
            onu_cfg = []
            onu_cfg2 = data_onu_index.splitlines()[3:-2]
            onu_cfg_lst = []
            # print(onu_cfg2)

            for x in onu_cfg2:
                result = " ".join(x.split())
                onu_cfg.append(result)

            for x in onu_cfg:
                f = x.split(" ")
                # print(f)
                onu_cfg_lst.append(f[0])
            print(onu_cfg_lst)

            ffind = False
            i = 0
            count = 1
            while count > 0:
                i += 1
                temp_index = (f"{gpon[0][9:]}:{i}")
                count = onu_cfg_lst.count(temp_index)
                if count == 0:
                    onu_index = temp_index
                    onu_cfg_lst.append(onu_index)

            print(onu_index)

            # register SN on specific interface
            tn.write(b'conf t\n')  # goto configure state
            tn.write(bytes(f"interface {gpon[0]}\n", 'ascii'))  # go to interface gpon olt
            # get data registered & unregistered onu index
            tn.write(bytes(f"onu {i} type ALL sn {gpon[1]}\n", 'ascii'))  # register onu sn on specific index (10)
            tn.write(b'exit\n')
            print(gpon[1])
            time.sleep(1)
            fiz = tn.read_very_eager().decode('utf-8')
            tb1.insert(tk.INSERT, f"{fiz}\n")
            print(fiz)

            # configure onu profile
            # tn.write(b'interface gpon-onu_1/1/8:10\n')  # goto interface gpon onu
            tn.write(bytes(f"interface gpon-onu_{onu_index}\n", "ascii"))
            tn.write(b'tcont 1 profile default\n')  # add profile
            tn.write(b'gemport 1 tcont 1\n')
            tn.write(b'service-port 1 vport 1 user-vlan 147 vlan 147\n')  # insert to vlan 147
            tn.write(b'exit\n')
            time.sleep(1)
            fiz = tn.read_very_eager().decode('utf-8')
            tb1.insert(tk.INSERT, f"{fiz}\n")
            print(fiz)

            # onu management
            # tn.write(b'pon-onu-mng gpon-onu_1/1/8:10\n')  # go to onu management
            tn.write(bytes(f"pon-onu-mng gpon-onu_{onu_index}\n", 'ascii'))
            tn.write(b'service 1 gemport 1 vlan 147\n')  # add vlan
            tn.write(b'wan-ip 1 mode dhcp vlan-profile labtjat147 host 1\n')  # add dhcp ip & vlan profile
            tn.write(b'end\n')
            print(f"success register {gpon[1]} on {onu_index}")
            time.sleep(1)
            fiz = tn.read_very_eager().decode('utf-8')
            tb1.insert(tk.INSERT, f"{fiz}\n")
            print(fiz)
            main_window.destroy()
            return messagebox.showinfo("Registered")

    main_window = tk.Tk()
    main_window.geometry("200x50+0+0")
    main_window.title("Register 1 ONU")
    lbl_reg = tk.Label(main_window,text="Select Serial Number to Register")
    combo = ttk.Combobox(main_window,values=onu_uncfg_lst,width=25) #value is unregister ONU data
    combo.bind("<<ComboboxSelected>>", selection_changed)
    lbl_reg.pack()
    combo.pack()
    main_window.mainloop()

def remove1():
    #verify if entry is filled
    host = str(e1.get())
    usr = str(e2.get())
    pwd = str(e3.get())
    port = str(e4.get())
    if port == "":
        port = 23
    if host == "":
        return messagebox.showerror("Error","Host IP is empty!")
    if usr == "":
        return messagebox.showerror("Error","Username is empty!")
    if pwd == "":
        return messagebox.showerror("Error","Password is empty!")
    print(f"{host},{usr},{pwd},{port}")

    #check registered ONT
    tn = telnetlib.Telnet(host,port,3)
    tn.write(bytes(f"{usr}\n",'ascii'))  # username
    tn.write(bytes(f"{pwd}\n",'ascii'))  # password
    time.sleep(1)
    fin = tn.read_very_eager().decode('utf-8')
    tb1.insert(tk.INSERT, f"{fin}\n")
    tn.write(b'show gpon onu state\n')
    time.sleep(1)
    fin = tn.read_very_eager().decode('utf-8')
    tb1.insert(tk.INSERT, f"{fin}\n")
    print(fin)
    onu_reg = []
    onu_reg2 = fin.splitlines()[3:-2]
    for x in onu_reg2:
        result = " ".join(x.split())
        onu_reg.append(result)

    onu_reglst = []
    print(onu_reglst)

    for x in onu_reg:
        f = x.split(" ")
        # print(f)
        onu_reglst.append(f[0])
    onu_reg = []

    # print(onu_reglst)
    # ubah jadi data = [[port,index],[port,index],[],....]
    for x in onu_reglst:
        f = x.split(":")
        onu_reg.append(f)

    print(onu_reg)
    time.sleep(0.5)
    indexsn = []
    #check sn each index
    for index in onu_reg:
        tn.write(bytes(f'show gpon remote-onu equip gpon-onu_{index[0]}:{index[1]}\n',"ascii"))
        time.sleep(0.75)
        status = tn.read_very_eager().decode('utf-8')
        #print(status)
        status = status.splitlines()[3]
        sernum = status.replace(" ","")[3:]
        print(sernum)
        indexsn.append([index[0],index[1],sernum])
    print(indexsn)




    def selection_changed(event):
        selection = combo.get()
        v = messagebox.askyesno(
            title="Confirmation",
            message=f"Selected option: {selection}. Want to Remove this ONU?"
        )
        print(v)
        if v == True:
            selection = selection.split()
            print(selection)
            print("Process to Remove")
            #execute remove selected ONU
            tn.write(b"conf t\n")
            tn.write(bytes(f"interface gpon-olt_{selection[0]}\n", "ascii"))
            tn.write(bytes(f"no onu {selection[1]}\n", "ascii"))
            tn.write(b"end\n")
            time.sleep(1)
            status = tn.read_very_eager().decode('utf-8')
            tb1.insert(tk.INSERT, f"{status}\n")
            print(status)
            main_window.destroy()
            return messagebox.showinfo("Removed")


    main_window = tk.Tk()
    main_window.geometry("200x50")
    main_window.title("Remove ONU")
    lbl_reg = tk.Label(main_window,text="Select Port and Index to Remove")
    combo = ttk.Combobox(main_window,values=indexsn,width=30) #value is unregister ONU data
    combo.bind("<<ComboboxSelected>>", selection_changed)
    lbl_reg.pack()
    combo.pack()
    main_window.mainloop()

def checkonusn():
    #verify if entry is filled
    host = str(e1.get())
    usr = str(e2.get())
    pwd = str(e3.get())
    port = str(e4.get())
    if port == "":
        port = 23
    if host == "":
        return messagebox.showerror("Error","Host IP is empty!")
    if usr == "":
        return messagebox.showerror("Error","Username is empty!")
    if pwd == "":
        return messagebox.showerror("Error","Password is empty!")
    print(f"{host},{usr},{pwd},{port}")

    def check():
        sernum = entryy.get()
        tn = telnetlib.Telnet(host, port, 3)
        tn.write(bytes(f"{usr}\n", 'ascii'))  # username
        tn.write(bytes(f"{pwd}\n", 'ascii'))  # password
        time.sleep(1)
        fin = tn.read_very_eager().decode('utf-8')
        tb1.insert(tk.INSERT, f"{fin}\n")
        tn.write(bytes(f'show gpon onu by sn {sernum}\n','ascii'))
        time.sleep(1)
        fin = tn.read_very_eager().decode('utf-8')
        tb1.insert(tk.INSERT, f"{fin}\n")
        #print(fin)
        res = fin.splitlines()[3]
        print(res)
        print(res.find("gpon"))
        if res.find("gpon") == 1:
            print("Serial Number Exist")


    main_window = tk.Tk()
    main_window.geometry("200x75")
    main_window.title("Check SN")
    entryy = tk.Entry(main_window)
    btnn = tk.Button(main_window,text="Check SN",command=check)
    snresult = tk.Label(main_window,text="Klik Check SN untuk mengecek")
    entryy.pack()
    btnn.pack()
    snresult.pack()

def registpppoe():
    #verify if entry is filled
    host = str(e1.get())
    usr = str(e2.get())
    pwd = str(e3.get())
    port = str(e4.get())
    if port == "":
        port = 23
    if host == "":
        return messagebox.showerror("Error","Host IP is empty!")
    if usr == "":
        return messagebox.showerror("Error","Username is empty!")
    if pwd == "":
        return messagebox.showerror("Error","Password is empty!")
    print(f"{host},{usr},{pwd},{port}")
    #get unregister ONU data
    tn = telnetlib.Telnet(host,port,3)
    tn.write(bytes(f"{usr}\n",'ascii'))  # username
    tn.write(bytes(f"{pwd}\n",'ascii'))  # password
    time.sleep(1)
    fin = tn.read_very_eager().decode('utf-8')
    tb1.insert(tk.INSERT, f"{fin}\n")
    print(fin)
    tn.write(b'show pon onu uncfg\n')  # cek Unregistered onu
    time.sleep(1)
    fin = tn.read_very_eager().decode('utf-8')
    tb1.insert(tk.INSERT, f"{fin}\n")
    print(fin)

    ####unregistered onu
    onu_uncfg = []
    onu_uncfg2 = fin.splitlines()[3:-1]
    # print(f"hasil {onu_uncfg2}")
    for x in onu_uncfg2:
        result = " ".join(x.split())
        onu_uncfg.append(result)

    onu_uncfg_lst = []

    for x in onu_uncfg:
        f = x.split(" ")
        # print(f)
        onu_uncfg_lst.append([f[0], f[2]])

    print(onu_uncfg_lst)

    ######maincode

    if onu_uncfg_lst == []:
        print("\nSUMMARY INFO : Nothing to register\n")
        tb1.insert(tk.INSERT, "\nSUMMARY INFO : Nothing to register\n")
        return messagebox.showwarning("Nothing to Register", "Nothing to Register")



    def registp3oe():
        sn = combo.get()
        p3oeusr = ent2.get()
        p3oepwd = ent3.get()
        print(sn, p3oeusr, p3oepwd)
        v = messagebox.askyesno(
            title="Confirmation",
            message=f"Selected option: {sn}. Want to Register this ONU?"
        )
        if v == True:
            sn = sn.split()
            gpon = [sn[0],sn[1]]
            print(f"Process to Register : interface : {gpon[0]},{gpon[1]}")
            #return main_window.destroy()
            #execute register selected ONU
            tn.write(bytes(f"show gpon onu state {gpon[0]}\n", 'ascii'))  # check used index onu
            time.sleep(1)
            data_onu_index = tn.read_very_eager().decode('utf-8')
            print(data_onu_index)

            # get registered and unregistered onu index
            onu_cfg = []
            onu_cfg2 = data_onu_index.splitlines()[3:-2]
            onu_cfg_lst = []
            # print(onu_cfg2)

            for x in onu_cfg2:
                result = " ".join(x.split())
                onu_cfg.append(result)

            for x in onu_cfg:
                f = x.split(" ")
                # print(f)
                onu_cfg_lst.append(f[0])
            print(onu_cfg_lst)

            ffind = False
            i = 0
            count = 1
            while count > 0:
                i += 1
                temp_index = (f"{gpon[0][9:]}:{i}")
                count = onu_cfg_lst.count(temp_index)
                if count == 0:
                    onu_index = temp_index
                    onu_cfg_lst.append(onu_index)

            print(onu_index)

            # register SN on specific interface
            tn.write(b'conf t\n')  # goto configure state
            tn.write(bytes(f"interface {gpon[0]}\n", 'ascii'))  # go to interface gpon olt
            # get data registered & unregistered onu index
            tn.write(bytes(f"onu {i} type ALL sn {gpon[1]}\n", 'ascii'))  # register onu sn on specific index (10)
            tn.write(b'exit\n')
            print(gpon[1])
            time.sleep(1)
            fiz = tn.read_very_eager().decode('utf-8')
            tb1.insert(tk.INSERT, f"{fiz}\n")
            print(fiz)

            # configure onu profile
            # tn.write(b'interface gpon-onu_1/1/8:10\n')  # goto interface gpon onu
            tn.write(bytes(f"interface gpon-onu_{onu_index}\n", "ascii"))
            tn.write(b'tcont 1 profile default\n')  # add profile
            tn.write(b'gemport 1 tcont 1\n')
            tn.write(b'service-port 1 vport 1 user-vlan 147 vlan 147\n')  # insert to vlan 147
            tn.write(b'exit\n')
            time.sleep(1)
            fiz = tn.read_very_eager().decode('utf-8')
            tb1.insert(tk.INSERT, f"{fiz}\n")
            print(fiz)

            # onu management
            # tn.write(b'pon-onu-mng gpon-onu_1/1/8:10\n')  # go to onu management
            tn.write(bytes(f"pon-onu-mng gpon-onu_{onu_index}\n", 'ascii'))
            tn.write(b'service 1 gemport 1 vlan 147\n')  # add vlan
            tn.write(bytes(f'wan-ip 1 mode pppoe username {p3oeusr} password {p3oepwd} vlan-profile labtjat147 host 1\n','ascii')) # add pppoe username password ip & vlan profile
            tn.write(b'end\n')
            print(f"success register {gpon[1]} on {onu_index}")
            time.sleep(1)
            fiz = tn.read_very_eager().decode('utf-8')
            tb1.insert(tk.INSERT, f"{fiz}\n")
            print(fiz)
            messagebox.showinfo("Success","Register Success")
            win.destroy()


    win = tk.Tk()
    win.geometry("300x200+0+0")
    win.title("Register PPPoE")

    lbl1 = tk.Label(win, text="Serial Number")
    lbl2 = tk.Label(win, text="PPPoE Username")
    lbl3 = tk.Label(win, text="PPPoE Password")

    combo = ttk.Combobox(win, values=onu_uncfg_lst, width=25)  # value is unregister ONU data
    ent2 = tk.Entry(win, width=28)
    ent3 = tk.Entry(win, width=28, show="*")

    confbtn = tk.Button(win, text="Register", command=registp3oe)

    lbl1.grid(row=0, column=0)
    lbl2.grid(row=1, column=0)
    lbl3.grid(row=2, column=0)
    combo.grid(row=0, column=1)
    ent2.grid(row=1, column=1)
    ent3.grid(row=2, column=1)
    confbtn.grid(row=3, column=0, columnspan=2)

    win.mainloop()

#widget
f1 = tk.LabelFrame(win,text="Configure")
f2 = tk.LabelFrame(win,text="Logs")
f3 = tk.LabelFrame(f1,text="Action")
f4 = tk.LabelFrame(f1,text="Other Information")
f5 = tk.LabelFrame(f1,text="Status")
t1 = tk.Label(f1,text="Host IP")
t2 = tk.Label(f1,text="Username")
t3 = tk.Label(f1,text="Password")
t4 = tk.Label(f1,text="Port (blank = 23)")
e1 = tk.Entry(f1)
e2 = tk.Entry(f1)
e3 = tk.Entry(f1,show="*")
e4 = tk.Entry(f1)
b1 = tk.Button(f3,text="REGISTER ALL", command=regall_btn,padx=2,pady=2)
b2 = tk.Button(f3,text="REMOVE ALL", command=remall_btn,padx=2,pady=2)
b3 = tk.Button(f3,text="SHOW REGISTERED ONU", command=check_ont_btn,padx=2,pady=2)
b4 = tk.Button(f3,text="SHOW UNREGISTER ONU", command=check_noont_btn,padx=2,pady=2)
b5 = tk.Button(f3,text="Register 1 ONU", command=reg1_btn, padx=2, pady=2)
b6 = tk.Button(f3,text="Remove 1 ONU", command=rem1_btn, padx=2, pady=2)
b7 = tk.Button(f3,text="Check ONU by SN", command=checkonusn, padx=2, pady=2)
b8 = tk.Button(f3,text="Register 1 ONU (PPPoE)",command=regp3oe_btn,padx=2, pady=2)
l1 = tk.Label(f3,text="\n")
l2 = tk.Label(f4,text="Created by Taufik Hidayat for SMK Telkom Bandung\nOLT. email : taufik1118a@gmail.com")
l3 = tk.Label(f5,text="Ready",width=40,fg="green")

v=ttk.Scrollbar(f2, orient='vertical')
v.pack(side=tk.RIGHT, fill='y')
tb1 = tk.Text(f2,height=30,width=80,yscrollcommand=v.set)

#widget placing
f1.pack(fill=tk.BOTH,expand=tk.YES,side=tk.LEFT)
f2.pack(fill=tk.BOTH,expand=tk.YES,side=tk.RIGHT)
t1.grid(sticky="W",row=0,column=0)
e1.grid(sticky="W",row=0,column=1)
t2.grid(sticky="W",row=1,column=0)
e2.grid(sticky="W",row=1,column=1)
t3.grid(sticky="W",row=2,column=0)
e3.grid(sticky="W",row=2,column=1)
t4.grid(sticky="W",row=3,column=0)
e4.grid(sticky="W",row=3,column=1)
f3.grid(sticky="W",row=4,column=0,columnspan=2)
b1.grid(row=0,column=0)
b2.grid(row=0,column=1)
b3.grid(row=1,column=0)
b4.grid(row=1,column=1)
b5.grid(row=2,column=0)
b6.grid(row=2,column=1)
b7.grid(row=3,column=0)
b8.grid(row=3,column=1)
l1.grid(row=4,columnspan=2,column=0)
tb1.pack()
v.config(command=tb1.yview)
f4.grid(sticky="W",row=5,column=0,columnspan=2)
l2.pack()
f5.grid(sticky="W",row=6,column=0,columnspan=2)
l3.pack()


win.mainloop()