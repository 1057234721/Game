import time
from threading import Thread

from Crack_Onmyoji.crack_service import CrackService


class CrackEntry:
    def __init__(self, number_of_team_members: int,
                 mode: str, inviter: int = -1, invite_members: {(str, str)} = None,
                 year_beast: bool = False, foster: bool = False, group_break_through: bool = True):
        self.number_of_team_members = number_of_team_members
        self.mode = mode
        self.inviter = inviter
        self.invite_members = invite_members
        self.year_beast = year_beast
        if self.year_beast:
            self.need_to_fight_year_beast = True
        self.foster = foster
        if self.foster:
            self.need_to_foster = True
        self.group_break_through = group_break_through
        if self.group_break_through:
            self.need_to_group_break_through = True
        self.crack = []
        for i in range(number_of_team_members):
            self.crack.append(CrackService(i))

    def start(self):
        start_time = time.ctime()
        while True:
            if self.year_beast and self.need_to_fight_year_beast:
                pass
            if self.foster and self.need_to_foster:
                pass
            if self.group_break_through and self.need_to_group_break_through:
                g_b_t = Thread(target=self.crack[0].group_break_through())
                g_b_t.start()
                g_b_t.join()
                self.need_to_group_break_through = False
