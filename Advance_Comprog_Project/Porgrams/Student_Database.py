from DatabadeConnectionProvider import BaseDatabaseConnection

class StudentDatabaseConnection(BaseDatabaseConnection):
    def __init__(self, host='localhost', user='root', password='', db='students_db'):
        super().__init__(host, user, password, db)

    # Stores Registered User information to database
    def register_user(self, user_information, password_information):
        try:
            query = "INSERT INTO student_password(Username, Password) VALUES (%s, %s)"
            params = (user_information, password_information)
            self.execute_query(query, params)

            return True
        except:
            return False
        
    # Check if username input already exist
    def check_user_existence(self, username):
        try:
            query = "SELECT * FROM student_password WHERE username = %s"
            params = (username,)
            result_cursor = self.execute_query(query, params)
            result = result_cursor.fetchone()
            return bool(result)
        except:
            return False