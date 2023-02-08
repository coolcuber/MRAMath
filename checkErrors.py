def checkErrors(testsAndMessages):
    for test in testsAndMessages.keys():
        if (not test):
            raise Exception(testsAndMessages(test))

# Seemed like a better idea at the time
def isType(obj, *types):
    for type in types:
        if (isinstance(obj, type)):
            return True
    return False
