import mls

template = "C:/Users/current_user/Desktop/template_folder/default.mt"
mls.link.local(path=None)
mls.build(template)
print("build finished")


username = mls.credentials.pull.username()
password = mls.credentials.pull.password()
uuid = mls.credentials.pull.uuid()
print(f"The username is: {username}\nThe password is {password}\nThe UUID is: {uuid}")
