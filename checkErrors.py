def checkErrors(testsAndMessages):
    for test in testsAndMessages.keys():
        if (not test):
            raise Excpetion(testsAndMessages(test))

def isType(obj, *types):
    for type in types:
        if (isinstance(obj, type)):
            return True
    return False