

# Please
If you have time help me out with my architectural research by filling out the survey [here.](https://docs.google.com/forms/d/e/1FAIpQLSdZtdf6eobLYJHM9Jrjs8mUJWDF1eSGMAo6GEEwMjzf-yTDpA/viewform?usp=sf_link)

---

(built on 3.7.7)

This .exe allows the user to input the camera angles x,y,z from a DCC and return -vd and -vu values that can be used in radiance. For information at [https://latimerias.github.io/using-radiance](https://latimerias.github.io/using-radiance). Note that the .exe expects values from a program thats Z-up.

If you don't want to download an .exe the script below script can also be run on an online compiler like [this](https://www.online-python.com/online_python_compiler).

                import numpy as np
                
                print("Expects angles coming from a Z-up DCC")
                
                # user inputs euler angles
                # float() converts the input into a float, without this the values would be read as strings even if they were numbers, all values read by input() are read as strings.
                e1 = float(input("x angle = "))
                e2 = float(input("y angle = "))
                e3 = float(input("z angle = "))

                # convert euler to quaternion
                w = np.sqrt(np.cos(e2*np.pi/180)*np.cos(e1*np.pi/180)+np.cos(e2*np.pi/180)*np.cos(e3*np.pi/180)-np.sin(e2*np.pi/180)*np.sin(e1*np.pi/180)*np.sin(e3*np.pi/180)+np.cos(e1*np.pi/180)* np.cos(e3*np.pi/180)+1)/2
                x = ((np.sin(e2*np.pi/180)*np.sin(e3*np.pi/180)-np.cos(e2*np.pi/180)*np.sin(e1*np.pi/180)*np.cos(e3*np.pi/180)-np.sin(e1*np.pi/180))/np.sqrt(np.cos(e2*np.pi/180)*np.cos(e1*np.pi/180)+ np.cos(e2*np.pi/180)*np.cos(e3*np.pi/180)-np.sin(e2*np.pi/180)*np.sin(e1*np.pi/180)*np.sin(e3*np.pi/180)+np.cos(e1*np.pi/180)*np.cos(e3*np.pi/180)+1)/2)*-1
                y = (np.sin(e2*np.pi/180)*np.cos(e1*np.pi/180)+np.sin(e2*np.pi/180)*np.cos(e3*np.pi/180)+np.cos(e2*np.pi/180)*np.sin(e1*np.pi/180)*np.sin(e3*np.pi/180))/np.sqrt(np.cos(e2*np.pi/180)* np.cos(e1*np.pi/180)+np.cos(e2*np.pi/180)*np.cos(e3*np.pi/180)-np.sin(e2*np.pi/180)*np.sin(e1*np.pi/180)*np.sin(e3*np.pi/180)+np.cos(e1*np.pi/180)*np.cos(e3*np.pi/180)+1)/2
                z = (np.cos(e1*np.pi/180)*np.sin(e3*np.pi/180)+np.cos(e2*np.pi/180)*np.sin(e3*np.pi/180)+np.sin(e2*np.pi/180)*np.sin(e1*np.pi/180)*np.cos(e3*np.pi/180))/np.sqrt(np.cos(e2*np.pi/180)* np.cos(e1*np.pi/180)+np.cos(e2*np.pi/180)*np.cos(e3*np.pi/180)-np.sin(e2*np.pi/180)*np.sin(e1*np.pi/180)*np.sin(e3*np.pi/180)+np.cos(e1*np.pi/180)*np.cos(e3*np.pi/180)+1)/2

                # multiply quaternion by vector, this is a simplification of quaternion matrix multiplication 
                vd = (2*x*z+2*w*y)*-1, (2*y*z-2*w*x)*-1, (w**2-x**2-y**2+z**2)*-1
                vu = (2*x*y-2*w*z), (w**2-x**2+y**2-z**2), (2*y*z+2*w*x)

                print("-vd = ",vd)
                print("-vu = ",vu)
                u)

                dummy = input("press enter to exit")
