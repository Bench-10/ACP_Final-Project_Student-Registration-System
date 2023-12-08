import pymysql

# Allows Connection to Database
class BaseDatabaseConnection:
    def __init__(self, host='localhost', user='root', password='', db='students_db'):

        # Connection parameters
        self.host = host
        self.user = user
        self.password = password
        self.db = db

    def connect(self):

        # Establish a connection to the database
        try:
            conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                db=self.db,
            )
            return conn
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return None

    def execute_query(self, query, params=None):
        try:
            # Connect to the database
            conn = self.connect()
            if conn:
                # Create a cursor to execute the query
                cursor = conn.cursor()
                if params:
                    # Execute the query with parameters
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                # Commit changes to the database
                conn.commit()
                return cursor
            
        finally:
            # Close the connection
            if conn:
                conn.close()