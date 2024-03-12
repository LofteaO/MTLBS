import mls

template = "C:/Users/joshu/Desktop/Modular Login Sysmtem -Kivy/Betas/beta 1.0/test.mt"
mls.link.local(path=None)
mls.build(template)
print("build finished")


username = mls.credentials.pull.username()
password = mls.credentials.pull.password()
uuid = mls.credentials.pull.uuid()
print(f"The username is: {username}\nThe password is {password}\nThe UUID is: {uuid}")
