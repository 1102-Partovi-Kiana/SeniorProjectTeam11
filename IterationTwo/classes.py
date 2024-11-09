class User:
    #Default Constructor
    def __init__(self):
        self.username = "defaultUsername"
        self.email = "defaultEmail"
        self.firstname = "defaultFirst"
        self.lastname = "defaultLast"
        self.password = "defaultUsername"
        self.secret_key = "defaultSecretKey"
        self.user_type = "defaultUserType"

    #Parameterized Constructor
    @classmethod
    def create_user(cls, username, email, password, firstname, lastname):
        user = cls() 
        user.username = username
        user.email = email
        user.password = password
        user.firstname = firstname
        user.lastname = lastname
        return user
    
    def display_all(self):
        print(self.username)
        print(self.firstname)
        print(self.lastname)
        print(self.email)
        print(self.password)