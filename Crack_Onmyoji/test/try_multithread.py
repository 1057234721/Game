import threading


class Count(threading.Thread):
    count = 1

    def __init__(self, print_count):
        super(Count, self).__init__()
        self.print_count = print_count

    def run(self):
        while Count.count <= 10000000:
            if self.print_count:
                print(Count.count)
            else:
                Count.count += 1


count_1 = Count(False)
count_2 = Count(True)
count_1.start()
count_2.start()
count_1.join()
count_2.join()
