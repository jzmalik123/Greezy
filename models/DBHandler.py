import pymysql, time


class DBHandler:
    def __init__(self, DATABASEIP, DB_USER, DB_PASSWORD, DATABASE):
        self.DATABASEIP = DATABASEIP
        self.DB_USER = DB_USER
        self.DB_PASSWORD = DB_PASSWORD
        self.DATABASE = DATABASE

    def __del__(self):
        print("Destructor")

    def getComments(self,courses):
        db = None
        cursor = None
        insert = False
        try:
            db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD, self.DATABASE)
            cur = db.cursor()
            sql = 'Select * from post where course = %s'
            x = 1
            while x in range(len(courses)):
                sql = sql + ' or course = %s'
                x = x + 1
            sql = sql + " order by owner_type desc"
            cur.execute(sql, tuple(courses))
            posts = cur.fetchall()

            #geting comments

            posts_ids = []
            for post in posts:
                posts_ids.append(post[0])
            print(posts_ids)
            sql = 'select * from comment where post_id = %s'
            x = 1
            while x in range(len(posts_ids)):
                sql = sql + ' or post_id = %s'
                x = x + 1
            print(sql)
            cur = db.cursor()
            cur.execute(sql, tuple(posts_ids))
            comments = cur.fetchall()
            print(comments)
            return comments

        except Exception as e:
            print("Error in getting posts: ")
            print(e)
        finally:
            print("finally bro")
        # if db is not None:
        #    db.commit()

    def get_Latest_Comment(self):
        db = None
        cursor = None
        insert = False
        try:
            db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD, self.DATABASE)
            cur = db.cursor()
            sql = 'Select * from comment order by comment_id desc'
            cur.execute(sql)
            new_comment = cur.fetchone()
            print(new_comment)
            return new_comment
        except Exception as e:
            print("Error in getting latest comment: ")
            print(e)
        finally:
            print("finally bro")
        # if db is not None:
        #    db.commit()

    def getPOSTS(self, courses):
        db = None
        cursor = None
        insert = False
        try:
            db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD, self.DATABASE)
            cur = db.cursor()
            sql = 'Select * from post where course = %s'
            x = 1
            while x in range(len(courses)):
                sql = sql + ' or course = %s'
                x = x + 1
            sql = sql + " order by owner_type desc"
            cur.execute(sql, tuple(courses))
            data = cur.fetchall()
            return data

        except Exception as e:
            print("Error in getting posts:")
            print(e)
        finally:
            print("finally bro")
        # if db is not None:
        #    db.commit()

    def login(self, id, password, type):
        db = None
        cursor = None
        insert = False
        try:
            db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD, self.DATABASE)
            cur = db.cursor()
            if type == "Student":
                sql = 'Select * from student where rollno = %s AND password = %s'
                args = (id, password)
                cur.execute(sql, args)
                # for row in cur.fetchall():
                data = cur.fetchall()
                return data
            else:
                sql = 'Select * from teacher where username = %s AND password = %s'
                args = (id, password)
                cur.execute(sql, args)
                data = cur.fetchall()
                return data
        except Exception as e:
            print(e)
            print("some error")
        finally:
            if db is not None:
                db.commit()
            if str(data) == '()':
                return ''
            else:
                return data

    def insertPost(self, type, description, owner, owner_key, owner_type, course):
        db = None
        cursor = None
        insert = False
        try:
            db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD, self.DATABASE)
            cur = db.cursor()
            sql = 'INSERT INTO post (type,description,owner,owner_key,owner_type,course) VALUES (%s,%s,%s,%s,%s,%s)'
            args = (type, description, owner, owner_key, owner_type, course)
            cur.execute(sql, args)
            insert = True

        except Exception as e:
            print(e)
            print("SQL Exception")
        finally:
            if db is not None:
                db.commit()
            return insert

    def get_post(self,post_id):
        db = None
        cursor = None
        insert = False
        try:
            db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD, self.DATABASE)
            cur = db.cursor()
            sql = 'Select * from post where id = %s'
            cur.execute(sql, post_id)
            data = cur.fetchall()
            return data
        except Exception as e:
            print(str(e))

    def insert_comment(self, comment_content,post_id,owner,owner_key,owner_type):
        db = None
        cursor = None
        insert = False
        try:
            db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD, self.DATABASE)
            cur = db.cursor()
            sql = 'INSERT INTO comment (post_id,content,owner,owner_key,owner_type) VALUES (%s,%s,%s,%s,%s)'
            args = (post_id,comment_content,owner,owner_key,owner_type)
            cur.execute(sql, args)
            insert = True

        except Exception as e:
            print(e)
            print("SQL Exception")
        finally:
            if db is not None:
                db.commit()
            return insert

    def get_names(self, course):
        db = None
        cur = None
        try:
            db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD, self.DATABASE)
            cur = db.cursor()
            sql_teach = 'SELECT username,name from teacher where course = %s'
            args = course
            cur.execute(sql_teach, args)
            list_names = list(cur.fetchone())
            dict = {list_names[1]: 'teacher'}
            dict_key = {list_names[0]: list_names[1]}
            sql = 'SELECT rollno,name from student where course = %s or course2 = %s or course3 = %s'
            argst=(course, course, course)
            cur.execute(sql, argst)
            for i in cur.fetchall():
                d = {i[1]: 'student'}
                d1 = {i[0]: i[1]}
                dict_key.update(d1)
                dict.update(d)
            dict.update(dict_key)
        except Exception as e:
            print(e)
        finally:
            if db is not None:
                db.commit()
            return dict

    def get_max_id(self):
        db = None
        cursor = None
        try:
            db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD, self.DATABASE)
            cur = db.cursor()
            sql = 'SELECT MAX(id) FROM post'
            cur.execute(sql)
            data = cur.fetchall()
            return int(data[0][0])
        except Exception as e:
            print(e)
            print("SQL Exception")

    def get_max_id_comments(self):
        db = None
        cursor = None
        try:
            db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD, self.DATABASE)
            cur = db.cursor()
            sql = 'SELECT MAX(comment_id) FROM comment'
            cur.execute(sql)
            data = cur.fetchall()
            return int(data[0][0])
        except Exception as e:
            print(e)
            print("SQL Exception")

    def signup_student(self, name, rollno, password, course, dob):
        db = None
        cursor = None
        insert = False
        try:
            db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD, self.DATABASE)
            cur = db.cursor()
            sql = 'INSERT INTO student (rollno,password,name,course,dob) VALUES (%s,%s,%s,%s,%s)'
            args = (rollno, password, name, course, dob)
            cur.execute(sql, args)
            insert = True
        except Exception as e:
            print(e)
            print("SQL Exception")
        finally:
            if db is not None:
                db.commit()
            return insert

    def signup_teacher(self, username, name, password, course, dob):
        db = None
        cursor = None
        insert = False
        try:
            db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD, self.DATABASE)
            cur = db.cursor()
            sql = 'INSERT INTO teacher (name,username,password,course,dob) VALUES (%s,%s,%s,%s,%s)'
            args = (name, username, password, course, dob)
            cur.execute(sql, args)
            insert = True

        except Exception as e:
            print(e)
            print("SQL Exception")
        finally:
            if db is not None:
                db.commit()
            return insert

    def verifyDOB(self, key, dob, type):
        db = None
        cursor = None
        insert = False
        try:
            db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD, self.DATABASE)
            cur = db.cursor()
            if type == 'Student':
                sql = 'SELECT dob from student where rollno = %s'
            else:
                sql = 'SELECT dob from teacher where username = %s'
            cur.execute(sql, (key))
            data = cur.fetchall()
            if dob == data[0][0]:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            print("SQL Exception")
        finally:
            if db is not None:
                db.commit()

    def changePassword(self, key, type, password):
        db = None
        cursor = None
        insert = False
        try:
            db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD, self.DATABASE)
            cur = db.cursor()
            if type == 'Student':
                sql = 'UPDATE student SET password = %s WHERE rollno = %s'
            else:
                sql = 'UPDATE teacher SET password = %s WHERE username = %s'
            print(sql)
            rw = cur.execute(sql, (password, key))
            print(rw)
        except Exception as e:
            print(e)
            print("SQL Exception")
        finally:
            if db is not None:
                db.commit()

    # umair kaam

    def message(self, sender, reciever, msg):
        db = None
        cursor = None
        insert = None
        try:
            db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD, self.DATABASE)
            cursor = db.cursor()
            sql = "insert into message(sender,reciever,body) values(%s, %s, %s) "
            args = (sender, reciever, msg)
            cursor.execute(sql, args)
            insert = True
        except Exception as e:
            print(e)
            print("sql exception")
        finally:
            if db is not None:
                db.commit()
                return insert

    def getTeachers(self, courses):
        db = None
        cursor = None
        data = None
        print('in getTeachers')
        teachers = []
        try:
            print('in try')
            db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD, self.DATABASE)
            cursor = db.cursor()
            sql = "select * from teacher where course=%s "
            x = 1
            print('appending courses')
            print(len(courses) - 1)
            while x in range(len(courses)):
                print('while 1')
                sql = sql + 'or course=%s '
                print('while 1')
                x = x + 1
            cursor.execute(sql, tuple(courses))
            data = cursor.fetchall()
            print('query executed')
            i = 0
            for x in data:
                teacher = [data[i][0], data[i][1], data[i][3]]
                teachers.append(teacher)
                i += 1
            print('got data')
            print(teacher)
        except Exception as e:
            print(e)
            print('sql exception in getTeachers')
        finally:
            db.commit()
            return teachers

    def getStudents(self, courses):
        db = None
        cursor = None
        data = None
        print('in getStudents')
        students = []
        try:
            print('in try')
            db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD, self.DATABASE)
            cursor = db.cursor()
            sql = "select * from student where course=%s "
            x = 1
            while x in range(len(courses)):
                sql1 = 'or course' + x
                sql = sql + sql1
                x = x + 1
            cursor.execute(sql, tuple(courses))
            data = cursor.fetchall()
            i = 0
            print('query executed')
            print(data[0][0])
            for x in data:
                student = [data[i][0], data[i][1], data[i][3]]
                students.append(student)
                i += 1
        except Exception as e:
            print(e)
            print('sql exception')
        finally:
            db.commit()
            return students

    def getMessagess(self, sender, reciever):
        db = None
        cursor = None
        data = None
        teachers = []
        try:
            db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD, self.DATABASE)
            cursor = db.cursor()
            sql = "select * from message where (sender=%s and reciever=%s) or (reciever=%s and sender=%s) "
            args = (sender, reciever, sender, reciever)
            cursor.execute(sql, args)
            data = cursor.fetchall()
        except Exception as e:
            print(e)
            print('sql exception in getStudents')
        finally:
            db.commit()
            return data

    def changeStatus(self, status, id, type):
        db = None
        cursor = None
        insert = False
        print(status)
        print(type)
        try:
            db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD, self.DATABASE)
            cur = db.cursor()
            if type == "Student":
                sql1 = 'update student set status=%s where rollno = %s '
                args1 = (status, id)
                cur.execute(sql1, args1)
            else:
                sql1 = 'update teacher set status=%s where username = %s '
                args1 = (status, id)
                cur.execute(sql1, args1)
        except Exception as e:
            print(e)
            print("some error in changeStatus")

    def deletePost(self, id, key):
        db = None
        cursor = None
        insert = False
        try:
            db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD, self.DATABASE)
            cur = db.cursor()
            sql = 'DELETE from post WHERE id=%s and owner_key = %s'
            args = (id, key)
            row = cur.execute(sql, args)
            if row:
                insert = True
            else:
                insert = False
        except Exception as e:
            print(e)
            print("SQL Exception")
        finally:
            if db is not None:
                db.commit()
            return insert

# umair end

# hasaaaan

    def add_course(self, id, course):
        db = None
        cur = None
        add = False
        try:
            db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD, self.DATABASE)
            cur = db.cursor()
            sql = "select course2,course3 from student where rollno = %s"
            args = id
            cur.execute(sql, args)
            arr = list(cur.fetchone())
            print(len(arr))

            if arr[0] is None:
                sqladd = "update student set course2 = %s where rollno = %s"
                argstring = (course, id)
                cur.execute(sqladd, argstring)
            else:
                sqladd = "update student set course3 = %s where rollno = %s"
                argstring = (course, id)
                cur.execute(sqladd, argstring)
            add = True
        except Exception as e:
            print(e)
        finally:
            if db is not None:
                db.commit()
            return add


    def isidexist(self, id, type):
        db = None
        cursor = None
        exist = False
        try:
            db = pymysql.connect(self.DATABASEIP, self.DB_USER, self.DB_PASSWORD, self.DATABASE)
            cur = db.cursor()
            if type == "student":
                sql = 'Select rollno from student where rollno = %s'
                args = id
                cur.execute(sql, args)
                # for row in cur.fetchall():
                data = cur.fetchone()
                if data:
                    exist = True
            else:
                sql = 'Select username from teacher where username = %s'
                args = id
                cur.execute(sql, args)
                data = cur.fetchone()
                if data:
                    exist = True
        except Exception as e:
            print(e)
            print("some error")
        finally:
            if db is not None:
                db.commit()
            if str(data) == '()':
                return ''
            else:
                return exist