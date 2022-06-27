import re

import mysql.connector
import datetime

def connect():
    try:
        mydb = mysql.connector.connect(user='root', password='minaahmadi77',
                                       host='127.0.0.1', port=3306,
                                       auth_plugin='mysql_native_password',
                                       database="mydb")
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS mydb")

        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS users (first_name varchar(20) not null,last_name varchar(20) not null,phone_number varchar(20) not null unique key,user_id varchar(20) not null primary key unique key,pass varchar(128) not null,email varchar(50) not null unique key,sec_answer varchar(64) not null,login varchar(20) not null,number_wrong int(20) not null,number_wrong_Q int(20) not null,date_wrong datetime not null);")
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS message (message_id int not null primary key unique key auto_increment,text_content varchar(256) not null,sender varchar(20) not null,receiver varchar(20) not null,send_date datetime not null,seen varchar(20) not null,liked varchar(20) not null,foreign key(sender) references users(user_id),foreign key(receiver) references users(user_id));")
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS logss (log_id varchar(20) not null,text_content varchar(256),log_date datetime not null,foreign key(log_id) references users(user_id));")
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS blocks (blocker varchar(20) not null,blocked varchar(20) not null,primary key (blocker, blocked),foreign key(blocker) references users(user_id),foreign key(blocked) references users(user_id));")
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS requests(follower varchar(20) not null,followed varchar(20) not null,primary key (follower, followed),foreign key(follower) references users(user_id),foreign key(followed) references users(user_id));")
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS friends (follower varchar(20) not null,followed varchar(20) not null,primary key (follower, followed),foreign key(follower) references users(user_id),foreign key(followed) references users(user_id));")
        # Query
        # mycursor.execute("SELECT DISTINCT STNAME FROM st,stco,co WHERE COTYPE='p'AND YR='94-95'AND TR=2 AND st.STID=stco.STID AND stco.COID=co.COID;")
        # mycursor.execute("SELECT STNAME FROM(SELECT STNAME,COUNT(co.CREDIT) AS g,(SELECT COUNT(co.CREDIT) AS b FROM co WHERE CREDIT=4) AS f FROM st,stco,co WHERE CREDIT=4 AND st.STID=stco.STID AND stco.COID=co.COID GROUP BY st.STNAME)AS n WHERE n.g>=n.f;")
        # mycursor.execute("SELECT employee.EmpID,employee.EmpName,employee.Salary,employee.DepID FROM employee,(SELECT employee.DepID,AVG(employee.Salary)AS avrage FROM employee  GROUP BY employee.DepID)AS n WHERE employee.DepID=n.DepID AND employee.Salary>n.avrage;")
        return mydb
        myresult = mycursor.fetchall()

        for x in myresult:
            print(x)

        mydb.close()

    except Exception as e:
        print(e)


# mydb.close()

def register(command,mydb):
    strr= str(datetime.datetime.now())
    newComm=new_command(command,mydb)
    x = datetime.datetime.now()
    query = "insert into `users`(`first_name`, `last_name`,`phone_number`, `user_id`, `pass`, `email`, `sec_answer`,`login`,`number_wrong`,`number_wrong_Q`,`date_wrong`) values(" + \
            newComm[0] + "," + newComm[1] + "," + newComm[2] + "," + newComm[3] + "," + newComm[4] + "," + newComm[
                5] + "," + newComm[6] + "," + '"no"' + "," + "0" + "," + "0" + "," +'"'+ str(x)+'"' + ");"
    myresult =fertchall_query(query,mydb)
    mydb.commit()

def new_command(command):
    newComm = []
    for i in command:
        i = '"' + i + '"'
        newComm.append(i)
    return newComm

def fertchall_query(query,mydb):
    mycursor = mydb.cursor()
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    return myresult

def check_login(cammand,mydb):
    newComm = new_command(command)
    if(user_exist(newComm[0],mydb)):
        query = "select user_id from users where users.user_id =" + newComm[0] + "and users.pass=" + newComm[1] + "and login ='no';"
        myresult=fertchall_query(query,mydb)
        if(myresult):
            query = "SELECT date_wrong FROM users WHERE user_id=" + newComm[0] + ";"
            date_wrong = fertchall_query(query, mydb)
            time_now = datetime.datetime.now()
            query = "SELECT number_wrong FROM users WHERE user_id=" + newComm[0] + ";"
            number_wrong=fertchall_query(query,mydb)
            difference=time_now - date_wrong[0][0]
            seconds_in_day = 24 * 60 * 60
            minutes_in_day=24*60
            result=divmod(difference.days * seconds_in_day + difference.seconds, 60)
            print(result)
            if(number_wrong[0][0]<3 or result[0]>=minutes_in_day ):
                myresult=''
                query = "select user_id from users where users.user_id =" + newComm[0] +"and users.pass="+newComm[1]+ ";"
                myresult=fertchall_query(query,mydb)
                if(myresult):

                    global user
                    user=cammand[0]
                    print(user)
                    query="UPDATE users SET login='yes' WHERE users.user_id ="+newComm[0]+";"
                    fertchall_query(query,mydb)
                    mydb.commit()
                    print("login is successful")
                    new=0
                    query="UPDATE users SET number_wrong=" + '"' + str(new) + '"' + "WHERE user_id=" +newComm[0] + ";"
                    myresult=fertchall_query(query,mydb)
                    mydb.commit()
                    login(cammand,mydb)

                else:
                    time = datetime.datetime.now()
                    query="UPDATE users SET date_wrong="+'"'+str(time)+'"'+"WHERE user_id=" + newComm[0]+ ";"
                    myresult=fertchall_query(query,mydb)
                    mydb.commit()
                    c=number_wrong[0][0]
                    c+=1
                    query = "UPDATE users SET number_wrong=" + '"' + str(c) + '"' + "WHERE user_id=" + newComm[0] + ";"
                    myresult=fertchall_query(query,mydb)
                    mydb.commit()
                    print("password is not correct!!")
            else:
                print("you can not login before one day!")
        else:
            print("you can not login because you'r loged in from somewhere else, pls sing out from there first !!")
    else:
        print("user not found!!")

def print_help():
    print(
        'Enter \'/\' between arguments.\n'
        'find_person\t\t\t\t/<username (string)>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t - to find\n'
        'get_friends\t\t\t\t/<username (string)>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t - to show your friends\n'
        'get_request\t\t\t\t/<username (string)>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t - to show your followers\n'
        'get_blocks\t\t\t\t/<username (string)>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t - to block others\n'
        'follow\t\t\t\t/<username (string)>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t - to follow others\n'
        'accept\t\t\t\t/<username (string)>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t - to accept followers\n'
        'remove_friends\t\t\t\t/<username (string)>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t - to remove accepts \n'
        'block\t\t\t\t/<username (string)>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t - to block others\n'
        'unblock\t\t\t\t/<username (string)>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t - to unblock others\n'
        'show_messages\t\t/<username (string)>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t - to show messages of one person\n'
        'send_message\t\t/<type (0=ava or 1=text)>/<ava id (int)>/<text (string)>/<receiver send_message(string)> - to send message\n'
        'like_message\t\t\t/<ava id (int)>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t - to like ava\n'
        'sign_out \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t - to sign out\n'
        'password_recovery \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t - to sign out\n'
        'delete_account \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t - to sign out')


def password_recovery(my_user,mydb):

    try:
        query = "SELECT number_wrong_Q FROM users WHERE user_id=" + '"' + my_user + '"' + ";"
        number_wrong_Q=fertchall_query(query,mydb)
        if(number_wrong_Q[0][0]<5):
            print("pls enter the answer of security answer (What is your favorite color?) :")
            input1=input()
            query = "SELECT number_wrong_Q FROM users WHERE user_id=" + '"' + my_user + '"' +"and sec_answer="+'"'+input1+'"'+ ";"
            myresult=fertchall_query(query,mydb)
            print(myresult)
            if(myresult):
                print("pls enter your new password:")
                input2=input()
                if re.fullmatch(r'[A-Za-z0-9]{8,}',input2):
                    query="UPDATE users SET pass="+'"'+input2+'"'+"WHERE user_id=" + '"' + my_user + '"'+ ";"
                    myresult=fertchall_query(query,mydb)
                    mydb.commit()
                    new =0
                    query = "UPDATE users SET number_wrong_Q=" + '"' + str(new) + '"' + "WHERE user_id=" + '"' + my_user + '"' + ";"
                    myresult = fertchall_query(query, mydb)
                    mydb.commit()
                    print("recovery successful")

                else:
                    print("pls check password format")
            else:
                new=number_wrong_Q[0][0]
                new+=1
                query="UPDATE users SET number_wrong_Q="+'"'+str(new)+'"'+"WHERE user_id=" + '"' + my_user + '"'+ ";"
                myresult=fertchall_query(query,mydb)
                mydb.commit()
                print("your answer is wrong!!")
        else:

            print("you can not recovery password with security answer(just with phone and email)")

    except Exception as e:
        print(e)



def like_message(com,mydb):
    newComm=new_command(com)

    try:
        query = "SELECT message_id FROM message WHERE message_id=" + newComm[1] + "and receiver=" + '"' + user + '"' + ";"
        myresult=fertchall_query(query,mydb)
        if(myresult):
            query = "UPDATE message SET liked='yes' WHERE message_id=" + newComm[1] + "and receiver=" + '"' + user + '"' + ";"
            myresult=fertchall_query(query,mydb)
            mydb.commit()
            print("message liked")
        else:
            print("this message was not exist ")
    except Exception as e:
        print(e)
def show_messages(mydb):
    query = "SELECT * FROM message WHERE receiver=" + '"' + user + '"' + ";"
    try:
        myresult=fertchall_query(query,mydb)
        if(myresult):
            print("show messages like this format:")
            print("message_code : (message_id, text , sender , receiver , send_date , seen (yes or no), like(yes or no))")
            print()
            for x in myresult:
                print(x)
            query="UPDATE message SET seen='yes' WHERE receiver=" + '"' + user + '"' + ";"
            myresult=fertchall_query(query,mydb)
            mydb.commit()
        else:
            print("you have not any message")
    except Exception as e:
        print(e)
def send_message(com,mydb):
    newComm=new_command(com)
    if(user_exist(newComm[1],mydb)):
        query="SELECT follower FROM friends WHERE followed=" + '"' + user + '"' + 'and follower=' + newComm[1]+ ";"
        myresult=fertchall_query(query,mydb)
        if(myresult):
            x = datetime.datetime.now()
            query="insert into message (text_content,sender,receiver,send_date,seen,liked) values(" +newComm[2] + "," +'"'+user+'"'+","+ newComm[1] +","+'"'+str(x)+'"'+","+"'no'"+","+"'no'"+ ");"
            try:
                myresult=fertchall_query(query,mydb)
                mydb.commit()
                print("message sent")
            except Exception as e:
                print(e)
        else:
            print("you can not send message because you are not his/him friend")
    else:
        print("user not found")
def user_exist(user1,mydb):
    query="SELECT user_id FROM users WHERE user_id=" + user1  + ";"
    myresult=fertchall_query(query,mydb)
    if(myresult):
        return True
    else:
        return False
def block(com,mydb):
    newComm=new_command(com)
    if(user_exist(newComm[1],mydb)):
        try:
            query="insert into blocks (blocker,blocked) values(" + '"' + user + '"' + "," + newComm[1] + ");"
            myresult=fertchall_query(query,mydb)
            mydb.commit()
            print("block successful")
            query1 = "DELETE FROM friends WHERE (follower=" + '"' + user + '"' + 'and followed=' + newComm[1] + ")or (follower="+newComm[1]+'"' + user + '")'+" ;"
            query2 = "DELETE FROM requests WHERE (follower=" + '"' + user + '"' + 'and followed=' + newComm[1] + ")or (follower=" + newComm[1] + '"' + user + '")' + " ;"
            try:
                myresult=fertchall_query(query1,mydb)
                mydb.commit()
                myresult = fertchall_query(query2, mydb)
                mydb.commit()
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)
    else:
        print("this user does not exist")
def unblock(com,mydb):
    newComm = new_command(com)
    try:
        query="SELECT blocker FROM blocks WHERE blocker=" + '"' + user + '"' + 'and blocked=' + newComm[1] + ";"
        myresult=fertchall_query(query,mydb)
        if(myresult):
            query="DELETE FROM blocks WHERE blocker=" + '"' + user + '"' + 'and blocked=' + newComm[1] + ";"
            myresult = fertchall_query(query, mydb)
            mydb.commit()
            print("unblock successful")
        else:
            print("you did not block this user")
    except Exception as e:
        print(e,"mmmm")
def get_friends(mydb):
    query = "SELECT follower FROM friends WHERE followed=" + '"' + user + '"' + ";"
    try:
        myresult=fertchall_query(query,mydb)
        if(myresult):
            for x in myresult:
                print(x)
        else:
            print("you have not any friends")
    except Exception as e:
        print(e)
def get_blocks(mydb):
    query = "SELECT blocked FROM blockss WHERE blocker=" + '"' + user + '"' + ";"
    try:
        myresult=fertchall_query(query,mydb)
        if(myresult):
            for x in myresult:
                print(x)
        else:
            print("you have not blocklist")
    except Exception as e:
        print(e)
def get_request(mydb):
    query = "SELECT follower FROM requests WHERE followed=" + '"' + user + '"' + ";"
    try:
        myresult=fertchall_query(query,mydb)
        if(myresult):
            for x in myresult:
                print(x)
        else:
            print("you have not any request")
    except Exception as e:
        print(e)

def remove_friends(com,mydb):
    newComm=com[1]
    try:
        query = "SELECT follower FROM friends WHERE followed=" + '"' + user + '"' + 'and follower=' + '"' + newComm + '"' + ";"
        myresult=fertchall_query(query,mydb)
        mydb.commit()
        if(myresult):
            query = "DELETE FROM friends WHERE followed=" + '"' + user + '"' + 'and follower=' + '"' + newComm + '"' + ";"
            myresult=fertchall_query(query,mydb)
            mydb.commit()
            print("delete successful")
        else:
            print("this friend is not exist")
    except Exception as e:
        print(e)


def follow(com,mydb):
    newComm=new_command(com)
    query="select blocker from blocks where blocker="+newComm[1]+"and blocked="+'"'+user+'"'+");"
    try:
        myresult=fertchall_query(query,mydb)
        if(myresult):
            print("you can not follow this user because you'r blocked!!")
        else:
            query = "insert into requests (follower,followed) values(" + '"' + user + '"' + "," + newComm[1] + ");"
            myresult=fertchall_query(query,mydb)
            mydb.commit()
            print("follow succesful")
    except Exception as e:
        print(e)

def accept(com,mydb):

    newComm=new_command(com)
    query=query = "select follower from requests where followed=" + '"' + user + '"' + 'and follower=' + newComm[1] + ";"
    try:
        myresult=fertchall_query(query,mydb)
        if(myresult):
            query1 = "insert into friends (follower,followed) values(" +  newComm[1]  + "," + '"' + user + '"'+");"
            myresult = fertchall_query(query1, mydb)
            mydb.commit()
            query2 = "insert into friends (follower,followed) values(" + '"' + user + '"'  + "," + newComm[1] +");"
            myresult = fertchall_query(query2, mydb)
            mydb.commit()
            query3 = "DELETE FROM requests WHERE followed=" + '"' + user + '"' + 'and follower=' + newComm[1] + ";"
            myresult = fertchall_query(query3, mydb)
            mydb.commit()

            print("user accepted and now is your friend")

        else:
            print("this user has not requested to you")


    except Exception as e:
        print(e)

def finder(com,mydb):
    newComm= com

    query="select user_id from users where user_id LIKE '%"+newComm+"%';"

    myresult=fertchall_query(query,mydb)
    if(myresult):
        for x in myresult:
            print(x)
    else:
        print("can not find anyone")

def sign_out(mydb):

    query="UPDATE users SET login='no' WHERE users.user_id ="+'"'+user+'"'+";"
    myresult=fertchall_query(query,mydb)
    print("sign out successfuly")

def login(command,mydb):
    newComm=new_command(command)
    print_help()
    while True:
        com = input().split('/')
        if com[0]=='find_person' and len(com) - 1 == 1:
            finder(com[1],mydb)
        elif com[0]=='sign_out' and len(com) - 1 == 0:
            sign_out(mydb)
            break
        elif com[0]=='follow'and len(com) - 1 == 1:
            follow(com,mydb)
        elif com[0]=='accept'and len(com) - 1 == 1:
            accept(com,mydb)
        elif com[0]=='remove_friends' and len(com) - 1 == 1:
            remove_friends(com,mydb)
        elif com[0]=='get_friends' and len(com) - 1 == 0:
            get_friends(mydb)
        elif com[0]=='get_requests' and len(com) - 1 == 0:
            get_friends(mydb)
        elif com[0]=='get_blocks'and len(com) - 1 == 0:
            get_blocks(mydb)
        elif com[0]=='block'and len(com) - 1 == 1:
            block(com,mydb)
        elif com[0]=='unblock'and len(com) - 1 == 1:
            unblock(com,mydb)
        elif com[0]=='send_message'and len(com) - 1 == 2:
            send_message(com,mydb)
        elif com[0]=='show_messages'and len(com) - 1 == 0:
            show_messages(mydb)
        elif com[0]=='like_message'and len(com) - 1 == 1:
            like_message(com,mydb)
        elif com[0]=='password_recovery'and len(com) - 1 == 0:
            password_recovery(mydb)
if __name__ == '__main__':
    mydb=connect()
    # query="UPDATE users SET login='no' WHERE users.user_id = 'm412';"
    # myresult=fertchall_query(query,mydb)
    # mydb.commit()
    # query="UPDATE users SET login='no' WHERE users.user_id = 'e412';"
    # myresult=fertchall_query(query,mydb)
    # mydb.commit()
    # query="UPDATE users SET login='no' WHERE users.user_id = 'mkkk412';"
    # myresult=fertchall_query(query,mydb)
    # mydb.commit()
    # query="UPDATE users SET login='no' WHERE users.user_id = 'moo412';"
    # myresult=fertchall_query(query,mydb)
    # mydb.commit()
    # query="UPDATE users SET login='no' WHERE users.user_id = 'oo412';"
    # myresult=fertchall_query(query,mydb)
    # mydb.commit()
    while True:
        sign_flag = True
        inp = input('Please enter a number:\n'
                    '1- Sign Up\n'
                    '2- Sign In\n'
                    '3- recovery_pass\n'
                    '4- Exit\n')
        if inp == "1":
            while True:
                command = input('Please enter first_name/last_name/phone_number/user_id/password/email/answer the question(What is your favorite color?) \n'
                                'for example: mina/ahmadi/09124567893/m412/Mina1377/1999minaahmadi@gmail.com/pink\n').split('/')

                if len(command) == 7 and re.fullmatch(r"[\d]{11}",command[2]) and re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$',command[5]) and re.fullmatch(r'[A-Za-z0-9]{8,}',command[4]):
                    register(command,mydb)
                    print('ddd')
                    break
                else:
                    print("Wrong input.")
        elif inp == "2":
            while True:

                command = input('Please enter user_name/password\n'
                                'for example: ali98/123456\n').split('/')
                if len(command) == 2:
                    check_login(command,mydb)
                else:
                    print("Wrong input.")
        elif inp=="3":
            command = input('Please enter user_name\n'
                            'for example: ali98\n')
            password_recovery(command,mydb)
        elif inp == "4":
            close_DB()
            sys.exit(0)
        elif sign_flag:
            print("Wrong input.")