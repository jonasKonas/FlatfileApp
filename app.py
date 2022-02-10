import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import random
import string






def get_random_password():
    random_source = string.ascii_letters + string.digits
    # select 1 lowercase
    password = random.choice(string.ascii_lowercase)
    # select 1 uppercase
    password += random.choice(string.ascii_uppercase)
    # select 1 digit
    password += random.choice(string.digits)
    # generate other characters
    for i in range(5):
        password += random.choice(random_source)
    password_list = list(password)
    # shuffle all characters
    random.SystemRandom().shuffle(password_list)
    password = ''.join(password_list)
    return password

def config_function():
    all_configs = []

    lan_mask = "255.255.255.248"
    vrrp_id = 1
    dhcp = "Disable"
    notes = "Notes"
    device_type = "RUT240"

    get_random_password()

    print("Button pressed")
    #reading GUI input
    text = txt_edit.get(1.0, tk.END).splitlines()    
    for i in text:
        ###CI NAME
        ###Get CI in the string ###
        ci_name = (i.split()[0])
        ###MANAGMENT IP ADDRESS
        ##gets managment IP address from text file in string
        mngmt_ip = (i.split()[1])
        #splits into list mngmt ip address to 4 objects
        mngmt_ip_list = mngmt_ip.split(".")
        #mngtm ip first 3 octets
        mngmt_1st_oct = f"{mngmt_ip_list[0]}.{mngmt_ip_list[1]}.{mngmt_ip_list[2]}."
        ###LAN-IP needs adding +3 to MANAGMENT IP last octect
        #gets last octet add + 3 to it and converts it back to the string
        lan_last_octect = str(int(mngmt_ip.split(".")[3])+3)
        lan_ip = mngmt_1st_oct+lan_last_octect
        ###VRRP-IP address needs adding +1 to MANAGMENT IP last octet
        vrrp_octect = str(int(mngmt_ip.split(".")[3])+1)
        vrrp_ip = mngmt_1st_oct+vrrp_octect            
        ###GRE-Dest ip, adds +2 to MANAGMENT IP last octect
        gre_octect = str(int(mngmt_ip.split(".")[3])+2)
        gre_dest = mngmt_1st_oct+gre_octect
        ##########GRE-IP, gets Tunnel IP address, add +2 to the last octect
        tunnel_ip = (i.split()[2])
        tunnel_list = tunnel_ip.split(".")
        gre_tunnel_1st = f"{tunnel_list[0]}.{tunnel_list[1]}.{tunnel_list[2]}."
        gre_octect = str(int(tunnel_ip.split(".")[3])+2)
        gre_ip = gre_tunnel_1st+gre_octect    
        framed_ip = i.split()[3]
        loopback_ip = i.split()[4]
        config_files = (f"{ci_name}@cellman Password = {get_random_password()},\nLoopback-IP = {loopback_ip},\nFramed-IP = {framed_ip},\nLAN-IP = {lan_ip},\nLAN-Mask = {lan_mask},\nVRRP-IP = {vrrp_ip},\nVRRP-ID = {vrrp_id},\nGRE-IP = {gre_ip},\nGRE-Dest = {gre_dest},\nDHCP-{dhcp},\nNotes = {notes},\nDevice-Type = {device_type}, \r\n")
        all_configs.append(config_files)
        
        ##need to sort out how more code can be put through. as only last config gets shown
        txt_edit.delete(1.0, tk.END)
        for c in all_configs:
            txt_edit.insert(tk.END, c)
            txt_edit.insert(tk.END, "\n")
        

    
    

        

   
        
   


###App functionality below#####


def open_file():
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    txt_edit.delete(1.0, tk.END)
    with open(filepath, "r") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    window.title("Cellman Flat file tool v0.8                                               ci_name   lan_ip   gre_ip   loopback_ip   framed_ip")

def save_file():
    """Save the current file as a new file."""
    filepath = asksaveasfilename(
        defaultextension="txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text = txt_edit.get(1.0, tk.END)
        output_file.write(text)
    window.title("Cellman Flat file tool v0.8                                               ci_name   lan_ip   gre_ip   loopback_ip   framed_ip")


window = tk.Tk()
window.title("Cellmann Flat file tool v0.8                                               ci_name   lan_ip   gre_ip   loopback_ip   framed_ip")
window.rowconfigure(0, minsize=500, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

txt_edit = tk.Text(window)
fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=3)
btn_open = tk.Button(fr_buttons, text="Open", command=open_file)
btn_save = tk.Button(fr_buttons, text="Save As...", command=save_file)
btn_generate = tk.Button(fr_buttons, text="Generate", command=config_function, bg= "#991155", fg= "white")


btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5)
btn_generate.grid(row=2, column=0, sticky="ew", padx=5)

fr_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")

window.mainloop()
