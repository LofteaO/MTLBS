import tkinter as tk
from tkinter import filedialog
import os
from PIL import ImageTk, Image
import hashlib
import ntplib
from datetime import datetime
import uuid
from termcolor import colored
import time
import socket
import sys
import io

#enables the option to enable debuging/testing

debug_option = True 

#director paths and other import file path located below.

workingDir = os.getcwd()
x = "\/"
x = x[0]
y = '/'
workingDir = workingDir.replace(x, y)

#path to the images directory
imageDir = workingDir + "/data/images"
userDir = workingDir + "/data/user"

#path to users.list file
userList = userDir + "/users.list"

#path to the login page dependencies image
logImage = imageDir + "/login.png"
buttonImage = imageDir + "/loginButton.png"
userData_Path = workingDir + "/data/user"

def gui_app():
    window = tk.Tk()

    #main window
    window.geometry('400x400')
    window.title('Login')
    window.resizable(False, False)

    debug_hash_Var = tk.IntVar(None)
    debug_Var = tk.IntVar(None)
    debug_login_Var = tk.IntVar()
    temp_user_check_Var = tk.IntVar()

    backGround = ImageTk.PhotoImage(Image.open(logImage))
    loginButton = ImageTk.PhotoImage(Image.open(buttonImage))

    setBackground = tk.Label(
        window,
        image=backGround,
    )

    def loginSuccsess(username):
        print(colored(f"Debug: user {username} has logged in succsessfuly", 'green'))
        #after a user has logged in the loggin page will dissapear
        if debug_Var.get() == 1:
            debug.destroy()
            
        showPasswordCheck.place_forget()

        if debug_option == True:
            debug_check.place_forget()

        passwdLabel.place_forget()
        userLabel.place_forget()

        passwd_entry.place_forget()
        username_entry.place_forget()

        logButton.place_forget()
        registerButton.place_forget()
        
        def app():
            #edit tk window variables
            window.title(f"User: {username}")
            window.geometry('700x400')
            
            #tkinter widgets for new login
            logoutButton = tk.Button(window, text="Logout", command=lambda: [logout()])
            
            logoutButton.place(x=5, y=5)
        
            def logout():
                window.title('Login')
                window.geometry('400x400')
                #removes all widget when logged in
                logoutButton.place_forget()
                
                
                #returns all widgets from login page
                
                showPasswordCheck.place(x=270, y=170)

                if debug_option == True:
                    debug_check.place(x=5, y=5)

                passwdLabel.place(x=80, y=170)
                userLabel.place(x=77, y=150)

                passwd_entry.place(x=140, y=170)
                username_entry.place(x=140, y=150)

                logButton.place(x=140, y=200)
                registerButton.place(x=140, y=245)
                
        app()
        

    def userSearch(username, password):
        # Convert the username to lowercase
        username_lower = username.lower()

        # Read existing data from the user list file
        user_list_file = userList
        existing_data = []
        if os.path.exists(user_list_file):
            with open(user_list_file, "r") as file:
                existing_data = file.read().splitlines()
        else:
            print("Debug: Unable to Find File")

        # Temporarily convert all usernames in the user list to lowercase for comparison
        existing_data_lower = [line.lower() for line in existing_data]

        # Check if the lowercase username exists in the user list
        username_index = next((i for i, line in enumerate(existing_data_lower) if f"user = {username_lower}:" in line), None)

        if username_index is not None:
            # Get the UUID associated with the provided username
            uuid_line = existing_data[username_index].split(": UUID = ")[1]
            expected_uuid = uuid_line

            # Construct the expected file name based on the provided username
            file_name = f"{username}.udata"
            file_path = os.path.join(userData_Path, file_name)

            if not os.path.exists(file_path):
                print(f"User file '{file_name}' not found.")
                return False

            # Read the file and check the 3rd line for the expected value (password)
            with open(file_path, 'r') as file:
                lines = file.readlines()

            if len(lines) >= 3:
                third_line = lines[4].strip()
                _, value = third_line.split("=")
                value = value.strip()

                # Check if the value matches the provided password
                if value == password and expected_uuid == uuid_line:
                    print(colored(f"Debug: UUID {uuid_line} Is a Match", 'green'))
                    print(colored(f"Debug: Password {password} Is a Match", 'green'))
                    loginSuccsess(username=username)  # You can define the login success function
        else:
            print(colored("Debug: Login Failed. Username or Password incorrect.", 'green'))

    def loginPress():
        username = userName_var.get()
        
        global uID
        uID = username
        global uID_username
        uID_username = username
        global passwd

        passwd = userPasswd_var.get()
        
        if debug_hash_Var.get() == 1:
            # Password hashing is disabled, store the password as is
            passwd = passwd
        else:
            # Password hashing is enabled, so hash the password
            passwd = hashlib.sha256(passwd.encode()).hexdigest()
        
        userSearch(username, passwd)
        
        
    def registerPress():
        username = userName_var.get()
        passwd = userPasswd_var.get()

        if passwd == "":
            return None
        elif debug_hash_Var.get() == 1:
            # Password hashing is disabled, so store the password as is
            passwd = passwd
        else:
            # Password hashing is enabled, so hash the password
            passwd = hashlib.sha256(passwd.encode()).hexdigest()

        createUser(username, passwd)

    def get_current_time(server='pool.ntp.org'):
        try:
            ntp_client = ntplib.NTPClient()
            response = ntp_client.request(server)
            ntp_time = response.tx_time
            current_datetime = datetime.utcfromtimestamp(ntp_time)
            
            global current_date
            global current_time
            
            current_date = current_datetime.date()
            current_time = current_datetime.time()
            return current_datetime
        except socket.gaierror:
            print("Error: No connection to the internet.")
            return None

    def createUser(username, passwd):
        current_datetime = get_current_time()  # Get the current time
        if current_time is not None:
            # Generate a unique user ID based on the username and current time
            user_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, f"{username}{current_datetime}"))
            #adding the new user to the existing user list.
            user_list_file = userList
            new_username = username
            new_username_lower = new_username.lower()
            # Read existing data from the user list file, if it exists
            existing_data = []
            if os.path.exists(user_list_file):
                with open(user_list_file, "r") as file:
                    existing_data = file.read().splitlines()

            # Temporarily convert all usernames to lowercase for comparison
            existing_data_lower = [line.lower() for line in existing_data]

            # Check if the lowercase username already exists in the user list
            username_exists = any(line.find(f"user = {new_username_lower}:") >= 0 for line in existing_data_lower)

            if not username_exists:
                # Prints user id
                print(f"User ID for {username}: {user_id}")
                # Create a new user information string
                new_user_info = f"Date/Time (UTC) Created = {current_datetime}: User = {new_username}: UUID = {user_id}"

                # Append the new user information to the existing user list
                existing_data.append(new_user_info)

                # Write the updated data back to the user list file
                with open(user_list_file, "w") as file:
                    file.write("\n".join(existing_data))

                print(f"User information added to {user_list_file}")
            else:
                print("Debug: User alreay exist")

            # Revert the existing data to its original case
            existing_data_lower = [line.lower() for line in existing_data]
            for i in range(len(existing_data)):
                if existing_data_lower[i].find(f"user = {new_username_lower}:") >= 0:
                    existing_data[i] = existing_data[i].replace(new_username_lower, new_username)
            
            #user file format
            UUID = user_id
            uPassword = passwd
            uCreation_Date = current_datetime
            uCreation_Time = current_time
            uName = username
            
            #unasigned data
            uPermissions_Level = None
            uDeletable = None
            logins = None
            time_spent = None
            
            user_file_format = f'''
                        uData[
                            UUID = {UUID}
                            uPermissions_Level = {uPermissions_Level}
                            uPassword = {uPassword}
                            uCreation_Date = {uCreation_Date}
                            uCreation_Time = {uCreation_Time}
                            uName = {uName}
                            uDeletable = {uDeletable}
                            uCommands = [
                                debug
                            ]
                        ]

                        collected_info[
                            logins = {logins}
                            logedIP = []
                            time_spent = {time_spent}
                            commandLog = []
                        ]'''
                        
            
            username = username.lower()         
            with open(f"{userDir}/{username}.udata", "w") as file:
                file.write(user_file_format)

        else:
            print("Error: Failed to generate a unique user ID due to no internet connection.")
        



    userName_var = tk.StringVar()
    userPasswd_var = tk.StringVar()

    passwd_entry = tk.Entry(window, textvariable=userPasswd_var, show="*")

    username_entry = tk.Entry(window, textvariable=userName_var)

    showPasswd_Var = tk.IntVar()

    def toggle_password_visibility():
        if showPasswd_Var.get() == 1:
            passwd_entry.config(show="")
        else:
            passwd_entry.config(show="*")

    showPasswordCheck = tk.Checkbutton(window, text="Show Password", variable=showPasswd_Var, onvalue=1, offvalue=0, command=toggle_password_visibility)

    debug_Var = tk.IntVar()

    def debug_check_box():
        debug_on = False
        if debug_Var.get() == 1:
            debug_on = True
        else:
            debug_on = False
        
        if debug_on == True:
            print(colored("Debug On: True", 'green'))
            debug_menu()
        else:
            print(colored("Debug on: False", 'green'))
            debug.destroy()


    debug_check = tk.Checkbutton(window, text="Enable Debug", variable=debug_Var, onvalue=1, offvalue=0, command=lambda: [debug_check_box()])
        


    def buttonchange_reg():
        registerButton.place_forget()
        logButton.place_forget()
        
        registerButton2.place(x=140, y=200)
        logButton2.place(x=140, y=245)
        
        
    def buttonchange_log():
        registerButton2.place_forget()
        logButton2.place_forget()
        
        logButton.place(x=140, y=200)
        registerButton.place(x=140, y=245)


    logButton = tk.Button(
        window,
        #image=loginButton,
        text="Login",
        width=16,
        height=2,
        #when pressed...
        command=lambda: [loginPress()]
    )

    registerButton = tk.Button(
        window,
        #image=loginButton,
        text="Register",
        width=16,
        height=1,
        #when pressed...
        command=lambda: [buttonchange_reg()]
    )

    logButton2 = tk.Button(
        window,
        #image=loginButton,
        text="Login",
        width=16,
        height=1,
        #when pressed...
        command=lambda: [buttonchange_log()]
    )

    registerButton2 = tk.Button(
        window,
        #image=loginButton,
        text="Register",
        width=16,
        height=2,
        #when pressed...
        command=lambda: [registerPress()]
    )


    temp_user_check = tk.Checkbutton(window, text="Temp User", variable=temp_user_check_Var, onvalue=1, offvalue=0, command=lambda: [])

    userLabel = tk.Label(window, text="Username:")
    passwdLabel = tk.Label(window, text="Password:")

    showPasswordCheck.place(x=270, y=170)

    def temp_user_place():
        if debug_tempusers_Var.get() == 1:
            temp_user_check_Var.set(0)
            temp_user_check.place(x=270, y=150)
        else:
            temp_user_check.place_forget()
            temp_user_check_Var.set(0)

    if debug_option == True:
        debug_check.place(x=5, y=5)

    passwdLabel.place(x=80, y=170)
    userLabel.place(x=77, y=150)

    passwd_entry.place(x=140, y=170)
    username_entry.place(x=140, y=150)

    logButton.place(x=140, y=200)
    registerButton.place(x=140, y=245)
    
    def redirect_stdout_to_text_widget(text_widget):
        class ConsoleRedirector(io.TextIOBase):
            def __init__(self, text_widget):
                self.text_widget = text_widget
                self.text_widget.tag_configure("green", foreground="green")
                self.text_widget.tag_configure("blue", foreground="blue")

            def write(self, s):
                if self.text_widget is not None:
                    self.text_widget.config(state=tk.NORMAL)
                    
                    # Add a tag to set the font
                    self.text_widget.tag_configure("mono_lisa", font=("MonoLisa", 12))

                    if "debug" in s.lower():
                        s = colored(s, 'green')
                        self.text_widget.insert("end", s, "green")
                    elif "note" in s.lower():
                        s = colored(s, 'blue')
                        # Use the "mono_lisa" tag to set the font
                        self.text_widget.insert("end", s, "blue", "mono_lisa")
                    else:
                        self.text_widget.insert("end", s)

                    self.text_widget.see("end")
                    self.text_widget.config(state=tk.DISABLED)
                else:
                    print("Text widget not found. Unable to redirect output.")

        sys.stdout = ConsoleRedirector(text_widget)


    # Function to open the debug log window

    def open_debug_log():
        debug_log_window = tk.Toplevel()
        debug_log_window.title("Debug Log")
        debug_log_window.geometry("600x400")

        debug_log_text = tk.Text(debug_log_window, wrap=tk.WORD, font=("MonoLisa", 12))
        debug_log_text.pack(fill=tk.BOTH, expand=True)

        # Create a scroll bar for the Text widget
        scroll_bar = tk.Scrollbar(debug_log_window, command=debug_log_text.yview)
        scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        debug_log_text.config(yscrollcommand=scroll_bar.set)  # Configure the yscrollcommand

        redirect_stdout_to_text_widget(debug_log_text)

        # Create a menu bar
        menu_bar = tk.Menu(debug_log_window)
        debug_log_window.config(menu=menu_bar)

        # Create a "File" menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        menu_bar.add_command(label="Exit", command=debug_log_window.destroy)

        # Add an "Exit" option to the "File" menu
        file_menu.add_command(label="Save As...", command=lambda: save_debug_log_as(debug_log_text))

    def save_debug_log_as(debug_log_text):
        content = debug_log_text.get("1.0", "end-1c")  # Get the content from the Text widget
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(content)


    def debug_menu():
        global debug_hash    
        global debug_hash_Var
        global debug_tempusers_Var

        debug_hash_Var = tk.IntVar()
        debug_tempusers_Var = tk.IntVar()
        
        global debug
        debug = tk.Toplevel()
        debug.title('Debug')
        debug.wm_geometry("300x350")
        debug.resizable(False, False)
        
        exitbtn = tk.Button(debug, width=10, height=1, text="Exit", command=lambda: [debug.destroy(), debug_Var.set(0)])
        debug_log = tk.Button(debug, width=10, height=1, text="Log", command=lambda:[open_debug_log()])
        
        debug_hash = tk.Checkbutton(debug, text="Disable Hash", variable=debug_hash_Var, onvalue=1, offvalue=0, command=lambda: [console_log(mtype = "*1")])
        debug_tempusers = tk.Checkbutton(debug, text="Enable TempUsers", variable=debug_tempusers_Var, onvalue=1, offvalue=0, command=lambda: [console_log(mtype = "*2"), temp_user_place()])
        debug_login_check = tk.Checkbutton(debug, text="Debug Login", variable=debug_login_Var, onvalue=1, offvalue=0, command=lambda: [])
        
        debug_log.place(x=215, y=35)
        debug_tempusers.place(x=0, y=20)
        debug_hash.place(x=0, y=0)
        exitbtn.place(x=215, y=5)
        

    def console_log(mtype):
        if mtype == "*1":
            if debug_hash_Var.get() == 0:
                print(colored('Debug: Password hashing enabled.', 'green'))
            else:
                print(colored('Debug: Password hashing disabled.', 'green'))
        elif mtype == "*2":
            if debug_tempusers_Var.get() == 1:
                print(colored('Debug: Temporary users enabled.', 'green'))
            else:
                print(colored('Debug: Temporary users disabled.', 'green'))

    window.mainloop()
    

if __name__ == "__main__":
    gui_app()