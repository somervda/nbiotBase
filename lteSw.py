import sqnsupgrade

#  see https://docs.pycom.io/updatefirmware/ltemodem/


def upgradeLteModemSw()


sqnsupgrade.run('/sd/upgdiff_old-to-new.dup')
# if no upgdiff is available, run the following instead
# sqnsupgrade.run('/sd/name.dup')
# WARNING! If you are updating from version 33080, use the updater.elf file as well, this is not needed for the upgdiff file.
# sqnsupgrade.run('/sd/name.dup', '/sd/updater.elf')


def getLteModemVersion()


sqnsupgrade.info()
