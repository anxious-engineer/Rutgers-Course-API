
class TimeLL(object):

    def __init__(self):
        self.front = TimeNode('0000', TimeNode('2300', None))

    def __str__(self):
        output = ''
        ptr = self.front
        while ptr is not None:
            output += str(ptr) + ' -> '
            ptr = ptr.cdr

        output += '/'
        return output

    def add(self, time):

        ptr = self.front

        prev = None

        while (ptr is not None) and (int(ptr.car) < int(time)):
            prev = ptr
            ptr = ptr.cdr

        if ptr is None:
            if prev is None:
                self.front = TimeNode(time, None)
            else:
                prev.cdr = TimeNode(time, None)
        else:
            if prev is None:
                self.front = TimeNode(time, self.front)
            else:
                prev.cdr = TimeNode(time, ptr)


class TimeNode(object):
    def __init__(self, time, next = None):
        self.car = time
        self.cdr = next

    def __str__(self):
        return str(self.car)


times = TimeLL()

list = ['1130', '1230', '149', '956']

for i in list:
    times.add(i)

print(times)
