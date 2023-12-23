from flaskr import mysql
import mysql.connector as mcr


class Colleges():
    def __init__(self, college_code=None, college_name=None):
        self.college_code = college_code
        self.college_name = college_name


    def add(self):
        cursor = mysql.connection.cursor()
        sql = f"INSERT INTO colleges(college_code, college_name) \
                VALUES('{self.college_code}','{self.college_name}')" 

        cursor.execute(sql)

    @classmethod
    def update(cls, old_code, new_name, new_code):
        cursor = mysql.connection.cursor()
        sql = f"UPDATE colleges SET college_name ='{new_name}', college_code='{new_code}' \
                where college_code='{old_code}'" 
        cursor.execute(sql)

    @classmethod
    def query_get(cls,college_code):
        cursor = mysql.connection.cursor()
        sql = f"SELECT * FROM colleges where college_code='{college_code}'"
        cursor.execute(sql)
        result = Colleges.result_zip(cursor.description,cursor.fetchall())
        if result:
            return result[0]
        return result

    @classmethod
    def result_zip(cls, cursor_desc, rows):
        columns = [desc[0] for desc in cursor_desc]
        result = []
        for row in rows:
            row = dict(zip(columns,row))
            result.append(row)
        if result:
            return result
        return []


    @classmethod
    def query_filter(cls, college_code=None, college_name=None, all=None, search_exact=False):
        cursor = mysql.connection.cursor()
        sql =''
        if search_exact:
            if college_name:
                sql = f"SELECT * FROM colleges where college_name='{college_name}'"
            if college_code:
                sql = f"SELECT * FROM colleges where college_code='{college_code}'"

        else:
            if college_name:
                sql = f"SELECT * FROM colleges where college_name LIKE '%{college_name}%'"
            if college_code:
                sql = f"SELECT * FROM colleges where college_code LIKE '%{college_code}%'"
            if all:
                sql = f"SELECT * FROM colleges where college_code LIKE '%{all}%' or college_name LIKE '%{all}%'"

        cursor.execute(sql)
        try:
            rows = cursor.fetchall()
        except mcr.InterfaceError:
            return []
        result = Colleges.result_zip(cursor.description,rows)
        return result

    @classmethod
    def query_all(cls):
        cursor = mysql.connection.cursor()
        sql = 'SELECT * FROM colleges'
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = Colleges.result_zip(cursor.description, rows)
        return result
    
    @classmethod
    def delete_college(cls, college_code):
        cursor = mysql.connection.cursor()
        sql = f'DELETE FROM colleges WHERE college_code="{college_code}"'
        cursor.execute(sql)