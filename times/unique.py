import sqlite3, json


def addRoom(ca, bu, ro):
    global data, totalRooms

    if ca not in data:
        # print("Created %s" % ca)
        data[ca] = {}

    if bu not in data[ca]:
        # print("Created %s" % bu)
        data[ca][bu] = []

    if ro not in data[ca][bu]:
        # print("Created %s" % ro)
        data[ca][bu].append(ro)
        totalRooms += 1


data = {}
totalRooms = 0

conn = sqlite3.connect('times.db')

c = conn.cursor()

c.execute("SELECT DISTINCT campus_name FROM times")

# print("Unique Campuses")

uCampus = c.fetchall()
# print(uCampus)

for camp in uCampus:
    if str(camp[0]) == 'None':
        continue
    cond = "(campus_name=\'" + str(camp[0]) + "\')"
    # print(cond)
    c.execute("SELECT DISTINCT building_code FROM times WHERE {c}".format(c=cond))

    uBuild = c.fetchall()
    # print('\t' + str(uBuild))

    for build in uBuild:
        if str(build[0]) == 'None':
            continue
        cond = "(campus_name=\'" + str(camp[0]) + "\' AND building_code=\'" + str(build[0]) + "\')"
        # print('\t' + cond)
        c.execute("SELECT DISTINCT room_number FROM times WHERE {c}".format(c=cond))

        uRoom = c.fetchall()
        # print('\t\t' + str(uRoom))

        for room in uRoom:
            if str(room[0]) == 'None':
                continue
            print('%s - %s - %s' % (camp[0], build[0], room[0]))

            addRoom(str(camp[0]), str(build[0]), str(room[0]))

print('%d total rooms found.' % totalRooms)

with open('../data/uniqueRoomsByCampus&Building.json', 'w') as outfile:
    json.dump(data, outfile)

# print("Unique Days of Week")
#
# r = c.fetchone()
#
# while r is not None:
#     print(r)
#     r = c.fetchone()
#
# c.execute("SELECT DISTINCT building_code FROM times")
#
# print("Unique Buildings")
#
# r = c.fetchone()
#
# while r is not None:
#     print(r)
#     r = c.fetchone()

c.close()

conn.close()

