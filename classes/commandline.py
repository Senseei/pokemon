import os

class CommandLine:
    @classmethod
    def check(cls, argv):
        if len(argv) < 3:
            print("Insufficient arguments")
            return False
        elif len(argv) > 3:
            print("Too many arguments")
            return False

        player1 = os.path.splitext(argv[1])
        player2 = os.path.splitext(argv[2])
        if player1[1] != ".profile" or player2[1] != ".profile":
            print("Not a .profile file")
            return False
        return True

    @classmethod
    def getFileProperty(cls, arg, property="name"):
        if property == "name":
            file = os.path.splitext(arg)
            return file[0]
        elif property == "ext":
            return file[1]

    @classmethod
    def file_exists(cls, file_path):
        try:
            file = open(file_path, "rb")
            file.close()
            return True
        except FileNotFoundError:
            return False