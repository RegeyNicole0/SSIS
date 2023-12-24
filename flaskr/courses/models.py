from flaskr import mysql
import mysql.connector as mcr


class Courses():
    def __init__(self, course_code=None,course_name=None, college_code=None):
        self.college_code = college_code
        self.course_name = course_name
        self.course_code = course_code


    def add(self):
        cursor = mysql.connection.cursor()
        sql = f"INSERT INTO courses(course_code,course_name, college_code) \
                VALUES('{self.course_code}','{self.course_name}','{self.college_code}')" 
        cursor.execute(sql)

    @classmethod
    def update(cls, old_code, new_name, new_code, new_college):
        cursor = mysql.connection.cursor()
        sql = f"UPDATE courses SET course_name ='{new_name}', course_code='{new_code}', \
                college_code='{new_college}' where course_code='{old_code}'" 
        cursor.execute(sql)

    @classmethod
    def query_get(cls,course_code):
        cursor = mysql.connection.cursor()
        sql = f"SELECT courses.course_code, courses.course_name, courses.college_code, \
                colleges.college_name FROM courses LEFT JOIN colleges ON courses.college_code = '{course_code}'\
                where courses.course_code='{course_code}'"
        cursor.execute(sql)
        result = Courses.result_zip(cursor.description,cursor.fetchall())
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
    def query_filter(cls, course_code=None, course_name=None, 
                college_code=None, all=None, search_exact=False):
        cursor = mysql.connection.cursor()
        base_sql = 'SELECT courses.course_code, courses.course_name, courses.college_code, \
                colleges.college_name FROM courses LEFT JOIN colleges ON courses.college_code = colleges.college_code'
        sql = ''
        if search_exact:
            if course_name:
                sql = base_sql+f" where courses.course_name='{course_name}'"
            if course_code:
                sql = base_sql+f" where courses.course_code='{course_code}'"
        else:
            if college_code:
                sql = base_sql+ f" where courses.college_code = '{college_code}'"
            if course_name:
                sql = base_sql + f" where courses.course_name LIKE '%{course_name}%'"
            if course_code:
                sql = base_sql + f" where courses.course_code LIKE '%{course_code}%'"
            if all:
                sql = base_sql + f" where courses.course_code LIKE '%{all}%' or courses.course_name LIKE '%{all}%'"
            if all and college_code:
                sql = base_sql + f" where (courses.course_code LIKE '%{all}%' or courses.course_name LIKE '%{all}%') AND courses.college_code = '{college_code}'"

        cursor.execute(sql)
        try:
            rows = cursor.fetchall()
        except mcr.InterfaceError:
            return []
        result = Courses.result_zip(cursor.description,rows)
        return result

    @classmethod
    def query_all(cls):
        cursor = mysql.connection.cursor()
        sql = 'SELECT courses.course_code, courses.course_name, courses.college_code, \
            colleges.college_name FROM courses LEFT JOIN colleges ON courses.college_code = colleges.college_code'
        cursor.execute(sql)
        try:
            rows = cursor.fetchall()
        except mcr.InterfaceError:
            return []
        result = Courses.result_zip(cursor.description,rows)
        return result

    
    @classmethod
    def delete_course(cls, course_code):
        cursor = mysql.connection.cursor()
        sql = f'DELETE FROM courses WHERE course_code="{course_code}"'
        cursor.execute(sql)