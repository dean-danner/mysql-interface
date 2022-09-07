import mysql.connector


def makeConnection():  # Connects to the database, change this accordingly
    c = mysql.connector.connect(user="root", db="createdb", password="root")
    cur = c.cursor()
    return c, cur


def chooseTable(cur):  # User selects which table they would like to modify
    print("Tables:")
    cur.execute("show tables")
    tblist = cur.fetchall()
    for i in tblist:
        print(i[0])

    table = input("Enter a table to modify or type 'quit': ")

    if table == "quit":
        quit()
    else:
        print("Table Attributes:")
        cur.execute("describe " + table)
        attr = cur.fetchall()
        for i in attr:
            print(i[0] + " | " + str(i[1])[2:-1])
        return table, attr


def selectTask(cur, table, attr):  # User selects whether to input or delete data from the selected table
    while True:
        ans = input("Would you like to 'insert' or 'delete' data? ")
        if ans == "insert":
            insertData(cur, table, attr)
        elif ans == "delete":
            deleteData(cur, table)
        else:
            print("Invalid input")


def insertData(cur, table, attr):  # Inserts the entered data into the selected table
    data = input("Enter the data like (ect1,ect2,ect2...): ").split(",")
    query = "insert into " + table + "("

    t = ""
    for i in attr[:-1]:
        t += i[0] + ","
    query += t + attr[-1][0] + ") values ("

    t = ""
    for dat in data[:-1]:
        if not dat.isnumeric():
            t += "'" + dat + "'"
        else:
            t += dat
        t += ","
    if not data[-1].isnumeric():
        t += "'" + data[-1] + "'"
    else:
        t += data[-1]
    query += t + ")"

    updateTable(cur, table, query)


def deleteData(cur, table):  # Deletes the selected row from the selected table
    displayTable(cur, table)
    while True:
        asked = input("Enter the ID of the row to delete from " + table + ": ")
        if asked.isnumeric():
            query = "delete from " + table + " where " + table + "id=" + str(asked)
            updateTable(cur, table, query)
        else:
            print("Invalid input")


def updateTable(cur, table, query):  # Executes the query and updates the database
    cur.execute(query)
    cur.execute("commit")
    displayTable(cur, table)
    restart(cur, table)


def displayTable(cur, table):  # Displays all of the data in a selected table
    print("Table Data:")
    cur.execute("select * from " + table)
    tblcont = cur.fetchall()
    for i in tblcont:
        print(i)


def showReport(cur, table):  # Generates a report of the tables modified by an action
    # displays every table that was modified by a delete or insert
    cur.execute("show tables")
    tblist = cur.fetchall()
    attrlist = []
    for i in tblist:
        for l in i:
            cur.execute("describe " + l)
            attrlist.append(cur.fetchall())
    for i in attrlist:
        for l in i:
            if l[0] == table + "id":
                print("Table: " + i[0][0][:-2])
                cur.execute("select * from " + i[0][0][:-2])
                info = cur.fetchall()
                for r in info:
                    print(r)


def restart(cur, table):  # Restart method with a report option used for after a modification is made
    while True:
        selection = input("Would you like to 'restart','quit', or show 'report'? ")
        if selection == "restart":
            main()
        elif selection == "quit":
            quit()
        elif selection == "report":
            showReport(cur, table)
        else:
            print("Invalid input")


def restartSimple():  # Simple restart method used if an error occurs
    while True:
        selection = input("Would you like to 'restart' or 'quit'? ")
        if selection == "restart":
            main()
        elif selection == "quit":
            quit()
        else:
            print("Invalid input")


def main():  # Puts everything together and handles exceptions
    while True:
        try:
            c, cur = makeConnection()
            table, attr = chooseTable(cur)
            selectTask(cur, table, attr)
        except ValueError:
            print("Invalid number")
            restartSimple()
        except mysql.connector.Error as err:
            print(err)
            restartSimple()
        else:
            cur.close()
            c.close()


main()
