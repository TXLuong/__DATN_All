from logging import exception
import psycopg2
from entity.monitor import Monitor 
from datetime import date, datetime
import numpy as np
from support_api import Process_api 
import cv2
import base64
import json

# import Json
class MonitorService:
    connection = None
    def __init__(self, face, face_anti_smoofing):
        print("Khoi tao ")
        self.connection = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="postgres",
                password="postgres")
        self.face = face
        self.threshold_distance = 0.95
        self.face_anti_smoofing = face_anti_smoofing

    def get_monitors():
        pass
    def create_monitor(self, monitor):
        cursor = self.connection.cursor()
        try: 
            print("what's on the earth .... ")
            postgres_insert_query = """ INSERT INTO "monitor" ("username", "password") VALUES (%s,%s)"""
            record_to_insert = (monitor['username'], monitor['password'])
            cursor.execute(postgres_insert_query, record_to_insert)
            self.connection.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into mobile table")
        except (Exception, psycopg2.Error)  as error :
            print("Failed to insert record into mobile table", error)
        finally : 
            # closeing database connection 
            print("sacsdcsac", cursor)
            if  self.connection : 
                # cursor.close()
                # self.connection.close()
                # print("Database connection os close successful") 
                pass
    def get_monitors(self):
        try: 
            cursor = self.connection.cursor()
            print("what's on the earth .... ")
            postgres_insert_query = """ SELECT * FROM "monitor" """
            cursor.execute(postgres_insert_query)
            self.connection.commit()
            data = cursor.fetchall()
            print(data, "get list monitors successfully")
            return data
        except (Exception, psycopg2.Error)  as error :
            print("Failed to insert record into mobile table", error)
        finally : 
            # closeing database connection 
            if self.connection : 
                # cursor.close()
                # self.connection.close()
                # print("Database connection os close successful") 
                pass
    def find_monitor_by_email(self, email):
        try:
            # find user by email address in monitor table 
            cursor = self.connection.cursor()
            postgres_select_query_monitor = """ SELECT * FROM "monitor" WHERE email = %s"""
            print("asca")
            cursor.execute(postgres_select_query_monitor,(email,))
            self.connection.commit()
            data = cursor.fetchall()
            if data != None and len(data) > 0 : 
                print("User nhan duoc khi truy van voi email la : ", data)
                print(type(data))
                return data[0]
            return "error"


            # find user by email address in table employee
        except (Exception, psycopg2.Error)  as error :
            print("Failed to query table", error)
        finally : 
            pass
            # closeing database connection 
            # if self.connection : 
            #     cursor.close()
            #     self.connection.close()
            #     print("Database connection os close successful") 
    def find_employee_by_email(self, email):
        try:
            cursor = self.connection.cursor()
            # find user by email address in employee table
            print("find user by email address in employee table") 
            postgres_select_query_employee = """ SELECT * FROM "employee" WHERE email = %s """
            cursor.execute(postgres_select_query_employee, (email,))
            self.connection.commit()
            data = cursor.fetchall()
            if data != None or len(data) > 0 : 
                print("User nhan duoc khi truy van voi email la : ", data)
                print(type(data))

                return data[0]
            print("done find user by email address in employee table")
            return "error"


            # find user by email address in table employee
        except (Exception, psycopg2.Error)  as error :
            print("Failed to query table", error)
        finally : 
            pass
    def checkLogin(self, email, password, ):
        data, user_type = self.find_user_by_email(email)
        print("Loai cua data tra ve la : ", type(data))
        if data != None and len(data) > 0:
            roleid = None
            if user_type == "Monitor": 
                roleid = str(data[-1])
            elif user_type == "Employee":
                roleid = str(data[-2])
            print(data[1] + "--------------" + password[0:])
            return data[1] == password[0:], roleid
        return None, None
    def addWorkLog(self, data):
        try:
            sqlQuery = """INSERT INTO "worklog"("time", "employeeid", "monitorid", "userimage") VALUES(%s, %s, %s, %s)"""
            cursor = self.connection.cursor()
            print("flag1")
            print(data)
            cursor.execute(sqlQuery, tuple(data.values()))
            print("flag2")
            self.connection.commit()
        except (Exception, psycopg2.Error) as error :
            print("Failed to insert record into work log table", error)
        finally : 
            # print("close success")
            # self.connection.close()
            pass
    def check_spoof(self, imageBase64):
        # check base on machine learning model 
        # 1. Is this fake or real ?
        # 2. Who is this ?
        isFake = False
        isWho = None 
        return isFake, isWho
    def check_and_add_work_log(self, auth, imageBase64, success):
        email = auth['user']
        try:
            queryGetId = """ select id from employee where email = %s """
            cursor = self.connection.cursor()
            cursor.execute(queryGetId, (email,))
            self.connection.commit()
            idUser = cursor.fetchall()
            print("after get user id ")
            # create new worklog
            insertLogQuery = """insert into worklog(employeeid, userimage, daywork, logtime, success) values (%s, %s, %s, %s, %s ) """
            values = (idUser[0],imageBase64, date.today(),datetime.now(), success,)
            print(values)
            cursor.execute(insertLogQuery, values)
            self.connection.commit()
            print(idUser)
        except (Exception, psycopg2.Error) as error :
            print("Failed to insert record into work log table", error)
        finally : 
            pass
    def addFace(self,data):
        # extract features from image then save to the database
        try:
            # sqlQuery = """INSERT INTO "worklog"("time", "employeeid", "monitorid", "userimage") VALUES(%s, %s, %s, %s)"""
            sqlQuery = """ UPDATE employee set facenumpy = %s where id = 1 """
            # insertedNumpy = np.zeros((112,112,3))
            # insertedNumpy = [[[1,2],[2,3],[1,2],[2,3]]]
            # insertedNumpy = insertedNumpy.tolist()
            process_api = Process_api(None, None, None)
            # img = cv2.imread("../son.jpg")
            img = cv2.imread("../luong.png")
            _, im_arr = cv2.imencode('.png', img)
            im_bytes = im_arr.tobytes()
            im_b64 = base64.b64encode(im_bytes)
            base64String = str(im_b64)[2:-1]
            image = process_api.img_from_base64(base64String)
            print(image)
            print("type:")
            print(image.shape)
            print(type(image))
            cursor = self.connection.cursor()
            print("flag1")
            cursor.execute(sqlQuery, (image.tolist(),))
            print("flag2")
            self.connection.commit()
        except (Exception, psycopg2.Error) as error :
            print("Failed to insert record into work log table", error)
        finally : 
            print("close success")
            self.connection.close()
        pass
        # if worklog for today exist, just add 5 minutes to time column
        # select workLog for today of user with email auth['user]
    def get_feature(self, image):  # input image ,output one features or no
        features, faces = self.face.feature_img(image)
        if(len(features)==1):
            return features[0]
        return None
    # def get_feature(self, image):  # input image ,output one features or no
    #     features, faces = self.face.feature_img(image)
    #     if(len(features)==1):
    #         return features[0]
    #     return None
    def img_from_base64(self, img_base64):
        print("step1")
        img=base64.b64decode(img_base64)
        print("step2")
        img= np.frombuffer(img, dtype=np.uint8)
        print("step3")
        img = cv2.imdecode(img, flags=1)
        print("img", img)
        return img
    def add_employee(self,id_emp,img):
        print("begin add_employee", img)
        print("id ", id_emp)
        # id of employee and img 
        if(img is not None):
            # get feature from employee image
            feature = self.get_feature(img)
            print("feature : ", feature)
            if(feature is not None):
                self.features = np.concatenate((self.features, feature.reshape(1, 512)))
                print("features : ", self.features)
                # self.labels.append(id_emp)
                # print("Add new success : "+ str(id_emp) + ", "+ str(self.features.shape) + ", " +str(len(self.labels)))
                # self.connector.add_user(id_emp,feature.tolist())
                return feature
            return None
        return None
    def change_monitor_profile(self, data):
        try:
            cursor = self.connection.cursor()
            insertLogQuery = """ UPDATE monitor set firstname = %s, lastname = %s, email = %s WHERE id = %s """
            values = (data['firstname'], data['lastname'],data['email'],data['id'],)
            print(values)
            cursor.execute(insertLogQuery, values)
            self.connection.commit()
        except (Exception, psycopg2.Error) as error :
            print("Failed to update record into monitor table", error)
        finally : 
            print("updated success")
    def change_employee_profile(self, data):
        try:
            cursor = self.connection.cursor()
            insertLogQuery = """ UPDATE employee set firstname = %s, lastname = %s, email = %s WHERE id = %s """
            values = (data['firstname'], data['lastname'],data['email'],data['id'],)
            print(values)
            cursor.execute(insertLogQuery, values)
            self.connection.commit()
        except (Exception, psycopg2.Error) as error :
            print("Failed to update record into monitor table", error)
        finally : 
            print("updated success")
    def find_user_by_email(self, email):
        try:
            # find user by email address in monitor table 
            cursor = self.connection.cursor()
            postgres_select_query_monitor = """ SELECT * FROM "monitor" WHERE email = %s"""
            print("asca")
            cursor.execute(postgres_select_query_monitor,(email,))
            self.connection.commit()
            data = cursor.fetchall()
            if data != None and len(data) > 0 : 
                print("User nhan duoc khi truy van voi email la : ", data)
                print(type(data))
                return data[0], "Monitor"
            # find user by email address in employee table
            print("find user by email address in employee table") 
            postgres_select_query_employee = """ SELECT * FROM "employee" WHERE email = %s """
            cursor.execute(postgres_select_query_employee, (email,))
            self.connection.commit()
            data = cursor.fetchall()
            if data != None or len(data) > 0 : 
                print("User nhan duoc khi truy van voi email la : ", data)
                print(type(data))

                return data[0], "Employee"
            print("done find user by email address in employee table")
            return "error"
        except (Exception, psycopg2.Error)  as error :
            print("Failed to query table", error)
        finally : 
            pass
    def find_employee_by_id(self, employee_id):
        try:
            cursor = self.connection.cursor()
            # find user by employee id in employee table
            postgres_select_query_employee = """ SELECT * FROM "employee" WHERE id = %s """
            cursor.execute(postgres_select_query_employee, (employee_id,))
            self.connection.commit()
            data = cursor.fetchall()
            if data != None or len(data) > 0 : 
                print("Employee nhan duoc khi truy van voi Id la : ", data)
                print(type(data))
                return data[0]
            print("done find user by id in employee table")
            return "error"
        except (Exception, psycopg2.Error)  as error :
            print("Failed to query table", error)
        finally : 
            pass
    def find_monitor_by_id(self, monitor_id):
        try:
            cursor = self.connection.cursor()
            # find user by employee id in employee table
            postgres_select_query_employee = """ SELECT * FROM monitor WHERE id = %s """
            cursor.execute(postgres_select_query_employee, (monitor_id,))
            self.connection.commit()
            data = cursor.fetchall()
            if data != None or len(data) > 0 : 
                print("Employee nhan duoc khi truy van voi Id la : ", data)
                print(type(data))
                return data[0]
            print("done find user by id in employee table")
            return "error"
        except (Exception, psycopg2.Error)  as error :
            print("Failed to query table", error)
        finally : 
            pass
    def change_employee_password(self, data):
        try:
            cursor = self.connection.cursor()
            insertLogQuery = """ UPDATE employee set password = %s WHERE id = %s """
            values = (data['newPassword'], data['id'],)
            print(values)
            cursor.execute(insertLogQuery, values)
            self.connection.commit()
        except (Exception, psycopg2.Error) as error :
            print("Failed to update record into monitor table", error)
        finally : 
            print("updated success")
    def change_monitor_password(self,data):
        try:
            cursor = self.connection.cursor()
            insertLogQuery = """ UPDATE monitor set password = %s WHERE id = %s """
            values = (data['newPassword'], data['id'],)
            print(values)
            cursor.execute(insertLogQuery, values)
            self.connection.commit()
        except (Exception, psycopg2.Error) as error :
            print("Failed to update record into monitor table", error)
        finally : 
            print("updated success")
    def save_new_employees(self,features, information):
        try:
            cursor = self.connection.cursor()
            print("begin insert face")
            sqlQuery = """INSERT INTO employee("password", "firstname", "lastname", "email", "roleid", "facenumpy") VALUES(%s, %s, %s, %s, %s, %s)"""
            data = ('123',information['firstName'],information['lastName'],information['email'],2,features.tolist(),)
            print("data", data)
            cursor.execute(sqlQuery, data)
            print("adding employee")
            self.connection.commit()
        except (Exception, psycopg2.Error) as error :
            print("Failed to insert record into employee ", error)
        finally : 
            pass
    def process_date_client(self, date):
        print("process date")
        print(type(date))
        print(date)
        date_client = date.split("/")
        print(date_client)
        date_server = [date_client[2],date_client[0],date_client[1]]
        res = [str(i) for i in date_server]
        return '-'.join(res)
    def process_date_server(self, date):
        date_server = date.split("-")
        date_client = [date_server[1],date_server[2], date_server[0]]
        res = [str(i) for i in date_client]
        return '-'.join(res)

    def time_for_employee(self, email, times):
        try: 
            
            cursor = self.connection.cursor()
            postgres_select_query = """ select log.daywork as "day", min(log.logtime) as "time_in", max(log.logtime) as "time_out", sum(log.success)*5/60.0 as "total_time"
                                        from worklog log where log.employeeid in (
                                            select emp.id from employee emp where emp.email = %s
                                        )
                                        group by log.daywork

                                        having log.daywork >= %s and log.daywork <= %s """
            values = (email, (times['dateFrom']), (times['dateTo']),)
            print("values", values)
            cursor.execute(postgres_select_query, values)
            self.connection.commit()
            data = cursor.fetchall()
            print("get list log time successfully", data)
            print(type(data))
            results = []
            for i in range(len(data)):
                day = data[i][0].__str__()
                time_in = data[i][1].__str__().split(" ")[1].split(".")[0]
                time_out = data[i][2].__str__().split(" ")[1].split(".")[0]
                sum_time = str(round(data[i][3],2))
                results.append(
                    {
                        "day" : self.process_date_server(day),
                        "time_in" : time_in,
                        "time_out" : time_out,
                        "sum_time" : sum_time
                    }
                )
            return results
        except (Exception, psycopg2.Error)  as error :
            print("Failed to select record table worklog", error)
        finally : 
            if self.connection : 
                pass

    def get_feature_from_db(self, email):
        try: 
            cursor = self.connection.cursor()
            print("what's on the earth .... ")
            postgres_insert_query = """ SELECT facenumpy FROM  employee where email = %s  """
            values = (email,)
            cursor.execute(postgres_insert_query, values)
            self.connection.commit()
            data = cursor.fetchall()
            print("get facenumpy successfully")
            return data
        except (Exception, psycopg2.Error)  as error :
            print("Failed to select employee table", error)
        finally : 
            pass
    def get_employees(self):
        try: 
            cursor = self.connection.cursor()
            postgres_select_query = """ select emp.id, concat(emp.firstname,' ', emp.lastname) as "fullname" from employee emp """
            cursor.execute(postgres_select_query)
            self.connection.commit()
            data = cursor.fetchall()
            print("get list employees successfully")
            return data
        except (Exception, psycopg2.Error)  as error :
            print("Failed to select employee table", error)
        finally : 
            pass
    def see_particular_employee(self, id, times):
        try: 
            cursor = self.connection.cursor()
            postgres_select_query = """ select log.daywork as "day", min(log.logtime) as "time_in", max(log.logtime) as "time_out", sum(log.success)*5/60.0 as "total_time"
                                        from worklog log where log.employeeid = %s
                                        group by log.daywork
                                        having log.daywork >= %s and log.daywork <= %s """
            values = (id, (times['dateFrom']), (times['dateTo']),)
            print("values", values)
            cursor.execute(postgres_select_query, values)
            self.connection.commit()
            data = cursor.fetchall()
            print(type(data))
            results = []
            for i in range(len(data)):
                day = data[i][0].__str__()
                time_in = data[i][1].__str__().split(" ")[1].split(".")[0]
                time_out = data[i][2].__str__().split(" ")[1].split(".")[0]
                sum_time = str(round(data[i][3],2))
                results.append(
                    {
                        "day" : self.process_date_server(day),
                        "time_in" : time_in,
                        "time_out" : time_out,
                        "sum_time" : sum_time
                    }
                )
            return results
        except (Exception, psycopg2.Error)  as error :
            print("Failed to select record table worklog", error)
        finally : 
            if self.connection : 
                pass
