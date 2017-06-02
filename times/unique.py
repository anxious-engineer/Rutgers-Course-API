import sqlite3, json

data = {}
totalRooms = 0
totalTimes = 0

def addRoom(ca, bu, ro):
    global data, totalRooms

    if ca not in data:
        # print("Created %s" % ca)
        data[ca] = {}

    if bu not in data[ca]:
        # print("Created %s" % bu)
        data[ca][bu] = {}

    if ro not in data[ca][bu]:
        # print("Created %s" % ro)
        data[ca][bu][ro] = []
        for i in range(0, 7):
            arr = ['o'] * 1440
            data[ca][bu][ro].append(arr)
        totalRooms += 7

        # print(data[ca][bu][ro])



def lookupDay(day):
    week = {'U': 0, 'M': 1, 'T': 2, 'W': 3, 'TH': 4, 'F': 5, 'S': 6}
    print(week[day])
    return week[day]


def blockOff(array, begin, end):

    bh = int(str(begin)[:2])
    bmin = int(str(begin)[3:-3])

    lower = (bh*60) + bmin

    eh = int(str(end)[:2])
    emin = int(str(end)[3:-3])

    upper = (eh*60) + emin

    print('%d to %d' % (lower, upper))

    for i in range(lower, upper):
        # print(len(array))
        array[i] = 'c'


def addTime(ca, bu, ro, ti):
    global data, totalTimes

    if str(ti[1]) == 'None':
        print("Syntax Error, No Day Found")
        return

    room = data[ca][bu][ro]

    # print(room)

    print(str(ti[1]))
    day = room[lookupDay(str(ti[1]))]

    begin = ti[2]
    end = ti[3]


    blockOff(day, begin, end)
    totalTimes += 1


def minutesToTime(minutes):
    tHours = str(minutes / 60)
    tMinutes = str(minutes % 60)

    if int(tHours) < 10:
        tHours = '0' + tHours

    if int(tMinutes) < 10:
        tMinutes = '0' + tMinutes

    return '%s%s' % (tHours, tMinutes)


def parseBlocks(blocks):
    status = blocks[0]

    pivot = 0
    output = []

    i = 1
    while i < 1440:
        if blocks[i] != status:
            # TODO : Handle 20 Minute Lecture Transition Period
            # if (i - pivot) < 21:
            #     stype = "CT"
            stype = 'Open' if status == 'o' else 'Closed'
            status = blocks[i]
            # TODO : Handle Title for JSON
            # output.append('%s from %s to %s' % (stype, pivot, endOfSession))
            output.append({'str': minutesToTime(pivot), 'end': minutesToTime(i), 'title': stype})
            pivot = i
        i += 1

    endOfSession = minutesToTime(i)
    stype = 'Open' if status == 'o' else 'Closed'
    # TODO : Handle Title for JSON
    output.append({'str': minutesToTime(pivot), 'end': minutesToTime(i), 'title': stype})
    return output


def collapseTimes(base):
    for c in base:
        for b in base[c]:
            for r in base[c][b]:
                print('%s - %s - %s' % (c, b, r))
                for day in range(0, 7):
                    times = parseBlocks(base[c][b][r][day])
                    base[c][b][r][day] = []
                    base[c][b][r][day] = times
                    print('\t%d -> %s' % (day, base[c][b][r][day]))


def main():

    global data, totalRooms

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
                # print('%s - %s - %s' % (camp[0], build[0], room[0]))

                addRoom(str(camp[0]), str(build[0]), str(room[0]))

                cond = "(campus_name=\'" + str(camp[0]) + "\' AND building_code=\'" + str(build[0]) + "\' AND room_number=\'" + str(room[0]) + "\')"

                # print('\t' + cond)
                c.execute("SELECT course_title, meeting_day, begin_time, end_time FROM times WHERE {c}".format(c=cond))

                times = c.fetchall()

                for t in times:
                    # continue
                    print(t)
                    addTime(str(camp[0]), str(build[0]), str(room[0]), t)

                # print(times)


    collapseTimes(data)
    print('%d total times found.' % totalTimes)

    # print(data['BUSCH']['HLL']['009'][lookupDay('W')])

    with open('../data/uniqueRoomsByCampus&Building.json', 'w') as outfile:
        json.dump(data, outfile)

    c.close()

    conn.close()


if __name__ == '__main__':
    main()