class PlayerDetail(object):
    def __init__(self, info: list):
        super(PlayerDetail, self).__init__()
        self.index = int(info[0])
        self.name = info[1]
        self.top_win_handler = int(info[2])
        self.bind_win_handler = int(info[3])
        self.is_in_android = True if int(info[4]) == 1 else False
        self.pid = int(info[5])
        self.virtual_box_pid = int(info[6])

    def is_running(self) -> bool:
        return self.is_in_android

    def __str__(self):
        index = self.index
        name = self.name
        r = str(self.is_in_android)
        twh = self.top_win_handler
        bwh = self.bind_win_handler
        pid = self.pid
        virtual_box_pid = self.virtual_box_pid
        return "\n index:%d name:%s top:%08X bind:%08X running:%s pid:%d virtual_box_pid:%d\n" % (
            index, name, twh, bwh, r, pid, virtual_box_pid)
