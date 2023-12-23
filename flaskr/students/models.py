from flaskr import mysql


class Students():
    base_select = 'SELECT students.first_name, students.last_name,\
            students.gender, students.year_level, students.profile_pic,\
            students.id, students.course_code, courses.course_name \
            FROM students LEFT JOIN courses ON students.course_code=courses.course_code'

    def __init__(self, id=None,last_name=None, first_name=None, year=None,gender=None, profile_pic=None, course_code=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.year_level = year
        self.gender =  gender
        self.profile_pic = profile_pic
        self.course_code = course_code

    def add(self):
        cursor = mysql.connection.cursor()
        sql = f"INSERT INTO students(id, last_name,first_name,year_level, gender, \
                course_code) VALUES('{self.id}','{self.last_name}', \
                '{self.first_name}','{self.year_level}','{self.gender}','{self.course_code}')" 
        cursor.execute(sql)

    @classmethod
    def update(cls, old_id, new_fname, new_lname, new_id, new_gender, new_year_level, new_course):
        cursor = mysql.connection.cursor()
        sql = f"UPDATE students SET first_name ='{new_fname}', last_name='{new_lname}', id='{new_id}',\
             gender='{new_gender}', year_level='{new_year_level}', course_code='{new_course}' WHERE id='{old_id}'" 
        cursor.execute(sql)

    @classmethod
    def query_get(cls,id):
        cursor = mysql.connection.cursor()
        sql = cls.base_select + f" WHERE id='{id}'"
        cursor.execute(sql)
        result = Students.result_zip(cursor.description,cursor.fetchall())
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
    def query_filter(cls, gender=None, id=None, name=None, course=None, all=None, exact_match=False):
        cursor = mysql.connection.cursor()
        sql = ''
        # if not gender:
        if exact_match:
            if name:
                sql = cls.base_select+f" WHERE MATCH (students.last_name, students.first_name) AGAINST('{name}') \
                                        or students.last_name LIKE '%{name}%' or students.first_name LIKE '%{name}%'"
            if id:
                sql = cls.base_select+f" WHERE students.id='{id}'"
        else:
            if course:
                sql = cls.base_select+ f" WHERE students.course_code LIKE '%{course}%'"
            if name:
                sep = name.split(' ')
                if len(sep) > 1:
                    sql = cls.base_select+f" WHERE MATCH (students.last_name, students.first_name) AGAINST('{name}')"
                else:
                    sql = cls.base_select+f" WHERE students.last_name LIKE '%{name}%'\
                                             or students.first_name LIKE '%{name}%'"

            if id:
                sql = cls.base_select+f" WHERE students.id LIKE '%{id}%'"
            if all:
                sep = all.split(' ')
                if len(sep) > 1:
                    sql = cls.base_select + f" WHERE students.course_code LIKE '%{all}%'\
                                            or courses.course_name LIKE '%{all}%'\
                                            or students.id LIKE '%{all}%'or MATCH\
                                            (students.last_name, students.first_name) AGAINST('{all}')"
                else:
                    sql = cls.base_select + f" WHERE students.course_code LIKE '%{all}%'\
                                            or courses.course_name LIKE '%{all}%'\
                                            or students.id LIKE '%{all}%' or students.last_name\
                                             LIKE '%{all}%' or students.first_name LIKE '%{all}%'"

        cursor.execute(sql)
        result = Students.result_zip(cursor.description,cursor.fetchall())
        filtered_result = []
        if gender != 'all':
            for row in result:
                if row['gender'].lower() == gender:
                    filtered_result.append(row)
            return filtered_result
        return result

    @classmethod
    def query_all(cls, gender='all'):
        cursor = mysql.connection.cursor()
        cursor.execute(cls.base_select)
        result = Students.result_zip(cursor.description, cursor.fetchall())
        if gender != 'all':
            filtered_result = []
            for row in result:
                if row['gender'].lower() == gender:
                    filtered_result.append(row)
            return filtered_result
        return result
    
    @classmethod
    def delete_student(cls, id):
        cursor = mysql.connection.cursor()
        sql = f'DELETE FROM students WHERE id="{id}"'
        cursor.execute(sql)

    @classmethod
    def update_pfp(cls, id, url):
        cursor = mysql.connection.cursor()
        sql = f"UPDATE students SET profile_pic ='{url}' WHERE id='{id}'"
        cursor.execute(sql)