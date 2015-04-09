import os
import time
import re
import logging


def desktop(path):

    logging.basicConfig(filename=path + "ablage.log", level=logging.DEBUG)
    #logging.debug("starting script")

    workingdir = os.listdir(path)
    for fileobject in workingdir:
        if not os.path.isdir(path + fileobject):
            if not fileobject[fileobject.rfind("."):] == ".lnk" and fileobject != "ablage.log":
                try:
                    print(fileobject)
                    os.rename(path + fileobject, path + "Desktop-Ablage\\" + fileobject)
                except FileExistsError as err:
                    #logging.debug("error in moving file", str(fileobject), str(err))
                    pass
        else:
            if not fileobject == "Desktop-Ablage":
                try:
                    os.rename(path + fileobject, path + "Desktop-Ablage\\" + fileobject)
                except FileExistsError as err:
                    #logging.debug("error in moving dir", str(fileobject), str(err))
                    pass


def ablage(path, testmode=False):

    logging.basicConfig(filename=path + "ablage.log", level=logging.DEBUG)
    #logging.debug("starting script")

    # Dateien durchgehen
    workingdir = os.listdir(path)
    for fileobject in workingdir:

        # Dateien
        if not os.path.isdir(path + fileobject) and fileobject != "ablage.log":

            t = time.gmtime(os.path.getmtime(path + fileobject))
            year = str(t[0])
            month = str(t[1]) if (len(str(t[1])) > 1) else "0" + str(t[1])
            if not os.path.isdir(path + year + "-" + month):
                #logging.debug("create dir", path + str(year) + "-" + str(month))
                if not testmode:
                    os.mkdir(path + year + "-" + month)

            if not testmode:
                try:
                    os.rename(path + fileobject, path + str(year) + "-" + str(month) + "\\" + fileobject)
                except FileExistsError as err:
                    #logging.debug("error in moving file", str(fileobject), str(err))
                    pass


            #logging.debug("moved file to folder", str(fileobject), str(year) + "-" + str(month))

    # Ordner durchgehen
    workingdir = os.listdir(path)

    # Objekte durchgehen
    for fileobject in workingdir:
        # Ordner
        if os.path.isdir(path + fileobject):
            # Nur Ordner, die nicht Datumskonform sind
            if not re.search(r"^[0-9]{4}\-[0-9]{2}", str(fileobject)) and not re.search(r"^[0-9]{4}", str(fileobject)) and not \
                            fileobject[0] == "!":
                t = time.gmtime(os.path.getmtime(path + fileobject))
                year = str(t[0])
                month = str(t[1]) if (len(str(t[1])) > 1) else "0" + str(t[1])
                if not os.path.isdir(path + year + "-" + month):
                    #logging.debug("create dir", path + str(year) + "-" + str(month))
                    if not testmode:
                        os.mkdir(path + year + "-" + month)

                if not testmode:
                    try:
                        os.rename(path + fileobject, path + year + "-" + month + "\\" + fileobject)
                    except FileExistsError as err:
                        #logging.debug("error in moving folder", str(fileobject), str(err))
                        pass
                #logging.debug("moved folder to folder", str(fileobject), str(year) + "-" + str(month))

    # Gruppen bilden
    workingdir = os.listdir(path)

    # Objekte durchgehen
    for fileobject in workingdir:
        # Ordner
        if os.path.isdir(path + fileobject):

            # Nur Ordner, die Datumskonform sind
            if re.search(r"^[0-9]{4}\-[0-9]{2}", str(fileobject)) and fileobject[0:4] != time.strftime("%Y"):

                if not os.path.isdir(path + fileobject[0:4]):
                    #logging.debug("create dir", path + fileobject[0:4])
                    if not testmode:
                        os.mkdir(path + fileobject[0:4])

                # Zielordner wurde schon mal angelegt...
                if os.path.isdir(path + fileobject[0:4] + "\\" + fileobject):

                    #logging.debug("moved files of folder to folder", str(fileobject), str(fileobject)[0:4])
                    workingsubdir = os.listdir(path + fileobject)
                    for fileObject2 in workingsubdir:
                        if not testmode:
                            try:
                                os.rename(path + fileobject + "\\" + fileObject2,
                                      path + fileobject[0:4] + "\\" + fileobject + "\\" + fileObject2)
                            except FileExistsError as err:
                                #logging.debug("error in moving file", str(fileobject), str(err))
                                pass
                    if not testmode:
                        os.removedirs(path + fileobject)

                else:
                    #logging.debug("moved folder to folder", str(fileobject), str(fileobject)[0:4])
                    if not testmode:
                        try:
                            os.rename(path + fileobject, path + fileobject[0:4] + "\\" + fileobject)
                        except FileExistsError as err:
                            #logging.debug("error in moving folder", str(fileobject), str(err))
                            pass


    #logging.debug("finishing script")


desktop("D:\\Daten\\Desktop\\")
ablage("D:\\Daten\\Desktop\\Desktop-Ablage\\")
