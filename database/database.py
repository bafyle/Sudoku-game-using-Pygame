import sqlite3

class Database:
    """
    Connects to sqlite database in read-only mode by passing
    the database path in string
    """
    def __init__(self, dbpath: str):
        self.database_path = dbpath

        # connect to the database using sqlite3 library
        # And open the database in read-only mode because we will not insert anything
        # to the database
        connection_query = rf"file:{self.database_path}?mode=ro"
        Database.connection = sqlite3.connect(connection_query, uri = True)

        # initialize the query executioner
        self.cursor = Database.connection.cursor()
    
    def get_puzzle_string(self, id: int) -> str:
        """
        This function reads a puzzle from the database and returns 
        it in string foramt
        """
        # get the puzzle which its q_id equal to id
        puzzle_text = self.cursor.execute("SELECT quiz FROM Quizzes WHERE q_id = ?", [id])

        # since the q_id is a primary key in the database,
        # there will be only one object in 'puzzleText'
        # we get that object and reassign 'puzzleText' with it
        # for i in puzzle_text:
        #     puzzle_text = i
        # puzzle_text = puzzle_text[0]

        for row in puzzle_text:
            return row[0]
        
        # return puzzle_text
    
    def get_answer_string(self, id: int) -> str:
        """
        This functions reads the answer of a certain puzzle and
        returns it in string format
        """
        answer_text = self.cursor.execute("SELECT quiz FROM Answers WHERE a_id = ?", [id])

        for i in answer_text:
            answer_text = i
        answer_text = answer_text[0]

        return answer_text
    
    @classmethod
    def close_connection(cls):
        """Closes the connection of the database without commiting any changes"""
        Database.connection.close()
    
    @classmethod
    def close_connection_commit(cls):
        """Closes the connection of the database and commits any changes"""
        Database.connection.commit()
        Database.close_connection()
        # we didn't use this function since we only read from the database
