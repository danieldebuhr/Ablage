# coding=ISO-8859-1
import os
import time
import re
import logging
from random import randint


def moveToAblage(quelle, ziel):

    donotmove = ["OneNote-Notizbücher", "Add-in Express", "My Kindle Content", "Benutzerdefinierte Office-Vorlagen", "Diablo III", "Snagit", "Citavi 5", "Visual Studio 2015",
                 "Adobe Acrobat XI", "Arduino", "MCS Electronics"]

    logging.basicConfig(filename=ziel + "ablage.log", level=logging.DEBUG)

    workingdir = os.listdir(quelle)
    for fileobject in workingdir:
        if not os.path.isdir(quelle + fileobject):
            if not fileobject[fileobject.rfind("."):] == ".lnk" and fileobject != "ablage.log":
                try:
                    if os.path.exists(ziel + "\\" + fileobject):
                        uniq = str(randint(1000, 9999)) + "_"
                    else:
                        uniq = ""

                    os.rename(quelle + fileobject, ziel + "\\" + uniq + fileobject)
                except FileExistsError as err:
                    logging.debug("error in moving file " + str(fileobject) + ", " + str(err))
                    pass
        else:
            if not (fileobject in donotmove or fileobject[0:1] == "."):
                try:
                    if os.path.exists(ziel + "\\" + fileobject):
                        uniq = str(randint(1000, 9999)) + "_"
                    else:
                        uniq = ""
                    os.rename(quelle + fileobject, ziel + "\\" + uniq + fileobject)
                except FileExistsError as err:
                    logging.debug("error in moving dir" + ", " + str(fileobject) + ", " + str(err))
                    pass


def ablageAufraeumen(path, testmode=False):
    logging.basicConfig(filename=path + "ablage.log", level=logging.DEBUG)
    logging.debug("starting script")

    # Dateien durchgehen
    workingdir = os.listdir(path)
    for fileobject in workingdir:

        # Dateien
        if not os.path.isdir(path + fileobject) and fileobject != "ablage.log":

            t = time.gmtime(os.path.getmtime(path + fileobject))
            year = str(t[0])
            month = str(t[1]) if (len(str(t[1])) > 1) else "0" + str(t[1])
            if not os.path.isdir(path + year + "-" + month):
                logging.debug("create dir" + ", " + str(path) + str(year) + "-" + str(month))
                if not testmode:
                    os.mkdir(path + year + "-" + month)

            if not testmode:
                try:
                    if os.path.exists(path + str(year) + "-" + str(month) + "\\" + fileobject):
                        uniq = str(randint(1000, 9999)) + "_"
                    else:
                        uniq = ""
                    os.rename(path + fileobject, path + str(year) + "-" + str(month) + "\\" + uniq + fileobject)
                except FileExistsError as err:
                    logging.debug("error in moving file" + ", " + str(fileobject) + ", " + str(err))
                    pass

            logging.debug("moved file to folder" + ", " + str(fileobject) + ", " + str(year) + "-" + str(month))

    # Ordner durchgehen
    workingdir = os.listdir(path)

    # Objekte durchgehen
    for fileobject in workingdir:
        # Ordner
        if os.path.isdir(path + fileobject):
            # Nur Ordner, die nicht Datumskonform sind
            if not re.search(r"^[0-9]{4}\-[0-9]{2}", str(fileobject)) and not re.search(r"^[0-9]{4}",
                                                                                        str(fileobject)) and not \
                            fileobject[0] == "!":
                t = time.gmtime(os.path.getmtime(path + fileobject))
                year = str(t[0])
                month = str(t[1]) if (len(str(t[1])) > 1) else "0" + str(t[1])
                if not os.path.isdir(path + year + "-" + month):
                    logging.debug("create dir" + ", " + str(path) + str(year) + "-" + str(month))
                    if not testmode:
                        os.mkdir(path + year + "-" + month)

                if not testmode:
                    try:
                        if os.path.exists(path + year + "-" + month + "\\" + fileobject):
                            uniq = str(randint(1000, 9999)) + "_"
                        else:
                            uniq = ""
                        os.rename(path + fileobject, path + year + "-" + month + "\\" + uniq + fileobject)
                    except FileExistsError as err:
                        logging.debug("error in moving folder" + ", " + str(fileobject) + ", " + str(err))
                        pass
                        logging.debug("moved folder to folder" + ", " + str(fileobject) + ", " + str(year) + "-" + str(month))

    # Gruppen bilden
    workingdir = os.listdir(path)

    # Objekte durchgehen
    for fileobject in workingdir:
        # Ordner
        if os.path.isdir(path + fileobject):

            # Nur Ordner, die Datumskonform sind
            if re.search(r"^[0-9]{4}\-[0-9]{2}", str(fileobject)) and fileobject[0:4] != time.strftime("%Y"):

                if not os.path.isdir(path + fileobject[0:4]):
                    logging.debug("create dir" + ", " + str(path) + str(fileobject)[0:4])
                    if not testmode:
                        os.mkdir(path + fileobject[0:4])

                # Zielordner wurde schon mal angelegt...
                if os.path.isdir(path + fileobject[0:4] + "\\" + fileobject):

                    logging.debug("moved files of folder to folder" + ", " + str(fileobject) + ", " + str(fileobject)[0:4])
                    workingsubdir = os.listdir(path + fileobject)
                    for fileObject2 in workingsubdir:
                        if not testmode:
                            try:
                                if os.path.exists(path + fileobject[0:4] + "\\" + fileobject + "\\" + fileObject2):
                                    uniq = str(randint(1000, 9999)) + "_"
                                else:
                                    uniq = ""
                                os.rename(path + fileobject + "\\" + fileObject2,
                                          path + fileobject[0:4] + "\\" + fileobject + "\\" + uniq + fileObject2)
                            except FileExistsError as err:
                                logging.debug("error in moving file" + ", " + str(fileobject), str(err))
                                pass
                    if not testmode:
                        os.removedirs(path + fileobject)

                else:
                    logging.debug("moved folder to folder" + ", " + str(fileobject) + ", " + str(fileobject)[0:4])
                    if not testmode:
                        try:
                            if os.path.exists(path + fileobject[0:4] + "\\" + fileobject):
                                uniq = str(randint(1000, 9999)) + "_"
                            else:
                                uniq = ""
                            os.rename(path + fileobject, path + fileobject[0:4] + "\\" + uniq + fileobject)
                        except FileExistsError as err:
                            logging.debug("error in moving folder" + ", " + str(fileobject) + ", " + str(err))
                            pass


moveToAblage("D:\\Eigene Dateien\\Desktop\\", "D:\\Ablage\\")
moveToAblage("D:\\Eigene Dateien\\Downloads\\", "D:\\Ablage\\")
moveToAblage("D:\\Eigene Dateien\\Eigene Dokumente\\", "D:\\Ablage\\")
ablageAufraeumen("D:\\Ablage\\")
