import os
import ntplib
from datetime import datetime
import uuid
import socket
import ast
import importlib.util
import hashlib

class error:
    error_codes = {
                    '001': "Error: Username or Password is icorect",
                    '002': "Error: Does not exist",
                    '003': "Error: File does not exist",
                    '021': "Error: No internet connection",
                    '022': "Error: User already exist",
                    }
    
    def handle(error_code):
        # error codes 001-020 are login related
        # error codes 021-049 are register related
        buildError = error.error_codes[error_code]
        print(buildError)


class local:
    class backend:
        def search(username, password):
            # Convert the username to lowercase
            username_lower = username.lower()

            # Read existing data from the user list file
            user_list_file = userList
            existing_data = []
            if os.path.exists(user_list_file):
                with open(user_list_file, "r") as file:
                    existing_data = file.read().splitlines()
            else:
                return '003'

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
                file_path = os.path.join(userDir, file_name)

                if not os.path.exists(file_path):
                    return '003'

                password_string_data = None
                uuid_string_data = None

                with open(file_path, "r") as file:
                    for line in file:
                        # Check if the line contains the desired string
                        if "Password" in line:
                            # Split the line by ':' to extract the value
                            key, value = line.split('=')
                            # Remove leading and trailing whitespace from the value
                            password_string_data = value.strip()

                        if "UUID" in line:
                            # Split the line by ':' to extract the value
                            key, value = line.split('=')
                            # Remove leading and trailing whitespace from the value
                            uuid_string_data = value.strip()

                #asign the uuid to the global var pulluuid
                global pulluuid
                pulluuid = uuid_line

                # Check if the value matches the provided password
                if password_string_data == password and uuid_string_data == uuid_line:
                    #print("Logged In")
                    return '101'
                else:
                    return '001'
            else:
                return '002'
            

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

        def create(username, password):
            current_datetime = local.backend.get_current_time()  # Get the current time
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

                                    # Revert the existing data to its original case
                    existing_data_lower = [line.lower() for line in existing_data]
                    for i in range(len(existing_data)):
                        if existing_data_lower[i].find(f"user = {new_username_lower}:") >= 0:
                            existing_data[i] = existing_data[i].replace(new_username_lower, new_username)
                    
                    #unasigned data
                    logins = None
                    time_spent = None

                    user_file_format = f'''
Data[
    UUID = {user_id}
    Password = {password}
    Creation_Date = {current_date}
    Creation_Time = {current_time}
    Username = {username}
],

Collected_info[
    logins = {logins}
    logedIP = []
    time_spent = {time_spent}
    commandLog = []
]'''
            
                    username = username.lower()        
                    with open(f"{userDir}/{username}.udata", "w") as file:
                        file.write(user_file_format)
                    
                    return '102' # User Created
                else:
                    return '022' # User already exist
            else:
                return '021' # No internet

class sql:
    def __init__(self, ip, port, name, username, password):
        self.ip = ip
        self.port = port
        self.name = name
        self.username = username 
        self.password = password        

class directorys:
    def __init__(self, path):
        self.path = path
        self.setup(path=self.path)

    def setup(self, path):
        if path == None or "":
            # creates the working directory
            dir_name = "mls-local"
            # Get the path to the AppData directory
            appdata_path = os.getenv('APPDATA')
            if appdata_path is None:
                raise EnvironmentError("Couldn't find the APPDATA environment variable.")

            # Create the full path for the new directory
            self.workingDir = os.path.join(appdata_path, dir_name)
            global workingDir
            workingDir = self.workingDir

            # Check if the directory already exists
            if os.path.exists(self.workingDir):
                print(f"Directory '{dir_name}' already exists in AppData.")
            else:
                # Create the directory
                os.makedirs(self.workingDir)
                print(f"Directory '{dir_name}' created successfully in AppData.")

            self.dataDir = os.path.join(self.workingDir, "data")
            global dataDir
            dataDir = self.dataDir

            if os.path.exists(self.dataDir):
                print(f"Directory data already exists in AppData.")
            else:
                # Create the directory
                os.makedirs(self.dataDir)
                print(f"Directory data created successfully in AppData.")

            self.userDir = os.path.join(self.dataDir, "user")
            self.userList = os.path.join(self.userDir, "user.list")

            global userDir
            global userList
            userDir = self.userDir         
            userList = self.userList

            if os.path.exists(self.userDir):
                #print(f"Directory user already exists in AppData.")
                pass
            else:
                # Create the directory
                os.makedirs(self.userDir)
                #print(f"Directory user created successfully in AppData.")                    

class link:
    choose = []
    class local:
        def __init__(self, path):
            link.choose.append("local")
            self.path = path
            directorys(path=self.path)

    class mdl: # modular database link
        pass

class credentials:
    def __init__(self, type, username, password):
        self.username = username
        self.password = password
        self.type = type
        self.credential_passer()

    def credential_passer(self):
        global pullusername
        global pullpassword
        pullusername = self.username
        pullpassword = self.password

        username = self.username
        password = self.password
        if link.choose[0] == "local":
            if self.type == "login":
                result = local.backend.search(username, password)
                intResult = int(result)
                if intResult > 100:
                    print("Debug: User credentials match")
                    window.destroy()
                elif intResult < 100:
                    error.handle(error_code=result)
            elif self.type == "register":
                result = local.backend.create(username, password)
                intResult = int(result)
                if intResult > 100:
                    print("Debug: User Data File Created")
                elif intResult < 100:
                    error.handle(error_code=result)

    class pull:
        def username():
            username = pullusername
            return username
        
        def password():
            password = pullpassword
            return password
        
        def uuid():
            uuid = pulluuid
            return uuid

class build():
    def __init__(self, template):
        self.template = template
        self.buildTemplate() 

    def register(username, password):
        type = "register"

        string_bytes = password.encode('utf-8')
        hash_object = hashlib.new('sha256')
        hash_object.update(string_bytes)
        hashed_password = hash_object.hexdigest()
        credentials(type, username, password=hashed_password)


    def login(username, password):
        type = "login"

        string_bytes = password.encode('utf-8')
        hash_object = hashlib.new('sha256')
        hash_object.update(string_bytes)
        hashed_password = hash_object.hexdigest()
        credentials(type, username, password=hashed_password)


    def buildTemplate(self):

        # The extension must be .mt for security reasons and that other unkown file types are not run

        # get the extension of the file e.g. .mt

        extension = self.template.split(".")[-1]
        extension = f".{extension}"
        
        # determine wether to execute the code based on the file type

        if extension != ".mt":
            print(f"File type: {extension} is not suported")
        else:
            with open(self.template, "r") as file:
                templateContents = file.read()  # Read the .mt file

            # Parse the code to find import statements
            tree = ast.parse(templateContents)
            import_statements = [node for node in tree.body if isinstance(node, ast.Import)]
            import_from_statements = [node for node in tree.body if isinstance(node, ast.ImportFrom)]

            imports = {}
            for imp in import_statements:
                for alias in imp.names:
                    imports[alias.name] = alias.asname
            for imp in import_from_statements:
                module_name = imp.module
                for alias in imp.names:
                    imports[module_name] = alias.asname

            # Dynamically import the required modules with their abbreviations or without abbreviations
            for module_name, abbreviation in imports.items():
                if abbreviation:
                    imported_module = importlib.import_module(module_name)
                    globals()[abbreviation] = imported_module
                else:
                    globals()[module_name] = importlib.import_module(module_name)


            # Execute the code from the .mt file
            exec(templateContents)

            