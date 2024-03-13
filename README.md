# MTLBS
![](https://img.shields.io/github/stars/LofteaO/mtlbs)![](https://img.shields.io/github/forks/LofteaO/mtlbs) ![](https://img.shields.io/github/tag/LofteaO/mtlbs) ![](https://img.shields.io/github/release/LofteaO/mtlbs) ![](https://img.shields.io/github/issues/LofteaO/mtlbs) 

> ![N|Solid](https://i.ibb.co/sFdhN3f/Add-a-heading-1.png)
> 
> Modular Template Login System

# Getting Started
## How to install?

To install the module using pip use the following command.

    pip install mtlbs

Alternatively download the latest release of mtlbs on github

`<Latest Release>` : https://github.com/LofteaO/MTLBS/releases

## How to use?

**Import the module into your main application file**

    app.py
    
    1. #imports
    2. import mtlbs as mtl

**Specifiy the template file location**

> .mt or .amt files are the only supported file format

    1. #value of the template variable should be the path to the template file
    2. template  =  "C:/Users/joshu/Desktop/Modular Login Sysmtem -Kivy/Betas/beta 1.0/test.mt"

***Refrence Code***

    1. #imports
    2. import mtlbs as mtl
    3.
    4. #value of the template variable should be the path to the template file
    5. template  =  "C:/Users/joshu/Desktop/Modular Login Sysmtem -Kivy/Betas/beta 1.0/test.mt"

**Create variables for build, link & pull**

> Assign the link, build & pull variables for ease of use

    1. link  =  mtlbs.link
    2. build  =  mtlbs.build
    3. pull  =  mtlbs.credentials.pull

***Refrence Code***

    1. #imports
    2. import mtlbs as mtl
    3. 
    4. #value of the template variable should be the path to the template file
    5. template  =  "C:/Users/joshu/Desktop/Modular Login Sysmtem -Kivy/Betas/beta 1.0/test.mt"
    6. 
    7. link  =  mtl.link
    8. build  =  mtl.build
    9. pull  =  mtl.credentials.pull
*this step is **not** required** 

**Specify the where the data will be stored/retrieved from locally or from a database**

***Locally:***

> The code required to locally store/retrieve data is the following.

    link.local(path=None)

> The link.local represents the choice of storing/retrieving the data locally and if the path is set to **None**
> The data will be stored and retrieved by default from the AppData directory of the current User
> *Disclaimer** *IT IS **ADVISED** TO SET A PATH AS BY DEFAULT IT WILL ONLY WORK ON WINDOWS AND WILL BREAK ON NON-WINDOWS OPERATING SYSTEMS*

***Refrence Code***

    1.  #imports
    2.  import mtlbs as mtl
    3. 
    4.  #value of the template variable should be the path to the template file
    5.  template  =  "C:/Users/joshu/Desktop/Modular Login Sysmtem -Kivy/Betas/beta 1.0/test.mt"
    6. 
    7.  link  =  mtl.link
    8.  build  =  mtl.build
    9.  pull  =  mtl.credentials.pull
    10.
    11. link.local(path=None)   

***With MDL-Api (Not Yet Working):***

> MDL api is a api made for mtlbs to link mtlbs to a database of your choice.
> MDL api is the only ***officially*** supported way to link mtlbs to a database without directly changing
> the code of mtlbs.

***Refrence Code***
    
    1.  #imports
    2.  import mtlbs as mtl
    3. 
    4.  #value of the template variable should be the path to the template file
    5.  template  =  "C:/Users/joshu/Desktop/Modular Login Sysmtem -Kivy/Betas/beta 1.0/test.mt"
    6. 
    7.  link  =  mtl.link
    8.  build  =  mtl.build
    9.  pull  =  mtl.credentials.pull 
    10. 
    11. link.local(path=None) 

**Build the template** 

> Code to build the template
> *Note** *the template var in the build call is the path to the template file*

    build(template)

***Refrence Code***

> The build class **must** be called after the link class

    1.  #imports
    2.  import mtlbs as mtl
    3. 
    4.  #value of the template variable should be the path to the template file
    5.  template  =  "C:/Users/joshu/Desktop/Modular Login Sysmtem -Kivy/Betas/beta 1.0/test.mt"
    6. 
    7.  link  =  mtl.link
    8.  build  =  mtl.build
    9.  pull  =  mtl.credentials.pull 
    10.
    10. link.local(path=None)
    11. build(template) 

**How to retrieve user data**

> Use the assigned pull class to retreive user data after the login process is complete

    1. username  =  pull.username()
    2. password  =  pull.password()
    3. uuid  =  pull.uuid()
    4.
	5. #The print is only for debug purposed and is not needed
    6. print(f"The username is: {username}\nThe password is {password}\nThe UUID is: {uuid}")

***Refrence Code***

    1.  #imports
    2.  import mtlbs as mtl
    3. 
    4.  #value of the template variable should be the path to the template file
    5.  template  =  "C:/Users/joshu/Desktop/Modular Login Sysmtem -Kivy/Betas/beta 1.0/test.mt"
    6. 
    7.  link  =  mtl.link
    8.  build  =  mtl.build
    9.  pull  =  mtl.credentials.pull 
    10.
    10. link.local(path=None)
    11. build(template) 
    12. 
    13. username  =  pull.username()
    14. password  =  pull.password()
    15. uuid  =  pull.uuid()
    16. 
    17. print(f"The username is: {username}\nThe password is {password}\nThe UUID is: {uuid}")


