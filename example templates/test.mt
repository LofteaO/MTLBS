import tkinter as tk

def gui():
    global window
    window = tk.Tk()

    #main window
    window.geometry('400x400')
    window.title()
    window.resizable(False, False)

    def loginSuccsess(username):
        showPasswordCheck.place_forget()

        passwdLabel.place_forget()
        userLabel.place_forget()

        passwd_entry.place_forget()
        username_entry.place_forget()

        logButton.place_forget()
        registerButton.place_forget()
        
          
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
        command=lambda: [build.login(password=userPasswd_var.get(), username=userName_var.get())]
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
        command=lambda: [build.register(password=userPasswd_var.get(), username=userName_var.get())]
    )


    userLabel = tk.Label(window, text="Username:")
    passwdLabel = tk.Label(window, text="Password:")

    showPasswordCheck.place(x=270, y=170)

    passwdLabel.place(x=80, y=170)
    userLabel.place(x=77, y=150)

    passwd_entry.place(x=140, y=170)
    username_entry.place(x=140, y=150)

    logButton.place(x=140, y=200)
    registerButton.place(x=140, y=245)
    
    window.mainloop()


gui()