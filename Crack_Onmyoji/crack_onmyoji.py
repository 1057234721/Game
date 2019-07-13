import random
import re
import sys
import threading
import time
from Crack_Onmyoji.log_recorder import LogRecorder
from Crack_Onmyoji.thunder_controller import ThunderController
from Crack_Onmyoji.onmyoji import Onmyoji


class Cracker(threading.Thread):

    def __init__(self, index: int, task_list: list = None, onmyoji: Onmyoji = None) -> None:
        super(Cracker, self).__init__()
        self.index = index
        self.start_time = time.ctime()
        self.task_list: list = task_list
        self.onmyoji = onmyoji

    def run(self) -> None:
        while len(self.task_list) != 0:
            current_task = self.task_list.pop(0)
            if len(current_task) == 1:
                eval("self." + current_task[0])()
            else:
                eval("self." + current_task[0])(*current_task[1:])

    def start_onmyoji(self) -> None:
        if ThunderController.is_player_running(self.index):
            ThunderController.reboot_player_and_start_app(self.index, Onmyoji.game_package_name)
        else:
            ThunderController.launch_player_and_start_app(self.index, Onmyoji.game_package_name)
        ThunderController.random_sleep(20, 25)
        ThunderController.random_click(self.index, Onmyoji.left_up_position, Onmyoji.right_down_position)
        self.any_pages_back_to_home_page()

    def is_home_page_or_not(self):
        return ThunderController.wait_picture(self.index, 1, ThunderController.share_path + "/bonus.png")[0]

    def any_pages_back_to_home_page(self):
        while True:
            if self.is_home_page_or_not():
                break
            else:
                exist, page_location, _ = \
                    ThunderController.check_picture_list(self.index, Onmyoji.close)
                if exist:
                    ThunderController.touch(self.index, ThunderController.cheat(page_location))
                    ThunderController.random_sleep(1.2, 1.8)
                else:
                    print("not found ...")

    def leave_team(self):
        while True:
            exist, location = ThunderController.wait_picture(self.index, 3, ThunderController.share_path +
                                                             "/team_leave.png")
            if not exist:
                break
            else:
                ThunderController.touch(self.index, ThunderController.cheat(location))
                ThunderController.random_sleep()
                _, location = ThunderController.wait_picture(self.index, 3,
                                                             ThunderController.share_path +
                                                             "/team_confirm_leave.png")
                ThunderController.touch(self.index, ThunderController.cheat(location))
                ThunderController.random_sleep()

    def accept_invite(self, acceptor: bool = True):
        auto_accept_flag = False
        auto_invite_flag = False
        inviter = not acceptor
        count = 0
        while True:
            if acceptor and not auto_accept_flag:
                exist, location, template = ThunderController.check_picture_list(self.index, Onmyoji.invite)
                if exist:
                    if template == './Onmyoji_images\\team2_invite.png':
                        auto_accept_flag = True
                    ThunderController.touch(self.index, ThunderController.cheat(location))
            if inviter and not auto_invite_flag:
                exist, location = ThunderController.wait_picture(
                    self.index, 1,
                    ThunderController.share_path + '/invite_in_default.png')
                if exist:
                    ThunderController.touch(self.index, ThunderController.cheat(location))
                    exist, location = ThunderController.wait_picture(
                        self.index, 1,
                        ThunderController.share_path + '/invite_in_default_confirm.png')
                    if exist:
                        ThunderController.touch(self.index, ThunderController.cheat(location))
                        auto_invite_flag = True
            ThunderController.random_sleep()
            exist, location, template = ThunderController.check_picture_list(self.index, Onmyoji.victory)
            if exist:
                if template == './Onmyoji_images\\battle_victory.png':
                    ThunderController.random_sleep(3, 4)
                    count += 1
                    print(count)
                ThunderController.touch(self.index, ThunderController.cheat(location))

    # def break_through(self):
    #     refresh = False
    #     while True:
    #         screen = ThunderController.screen_shot(self.index)
    #         click_locations = ThunderController.find_all_pictures(
    #             screen,
    #             ThunderController.share_path + '/zero_star.png', 0.95)
    #         click_position = None
    #         if len(click_locations) > 0:
    #             ticket = ThunderController.intercept_rectangle_from_picture(self.index,
    #                                                                         Onmyoji.break_through_ticket_left_up,
    #                                                                         Onmyoji.break_through_ticket_right_down)
    #             result = ThunderController.fetch_number_from_picture(ticket)
    #             result = int(result[:-2])
    #             print('have ', result, 'tickets')
    #             if result == 0:
    #                 break
    #             word_pic = ThunderController.intercept_rectangle_from_picture(self.index,
    #                                                                           Onmyoji.break_through_word_left_up,
    #                                                                           Onmyoji.break_through_word_right_down)
    #             result = ThunderController.fetch_number_from_picture(word_pic)
    #             result = int(result)
    #             print("already beat... ", result)
    #             if result >= 3:
    #                 if result == 3:
    #                     exist, location, template = ThunderController.check_picture_list(self.index, Onmyoji.victory)
    #                     if exist:
    #                         ThunderController.touch(self.index, ThunderController.cheat(location))
    #                         ThunderController.random_sleep()
    #                 refresh = True
    #             if not refresh:
    #                 screen = ThunderController.screen_shot(self.index)
    #                 remove_locations = ThunderController.find_all_pictures(screen,
    #                                                                        ThunderController.share_path
    #                                                                        + '/break_through_fail_flag.png')
    #                 if len(remove_locations) > 0:
    #                     to_remove = []
    #                     for click in click_locations:
    #                         for remove in remove_locations:
    #                             if 130 >= remove[0] - click[0] >= 70 and 80 >= click[1] - remove[1] >= 40:
    #                                 to_remove.append(click)
    #                     for remove in to_remove:
    #                         click_locations.remove(remove)
    #                 print(click_locations)
    #                 if len(click_locations) > 0:
    #                     click_position = click_locations[random.randint(0, len(click_locations) - 1)]
    #                 else:
    #                     refresh = True
    #             if not refresh:
    #                 ThunderController.touch(self.index, ThunderController.cheat(click_position))
    #                 ThunderController.random_sleep()
    #                 exist, location = ThunderController.wait_picture(
    #                     self.index, 10,
    #                     ThunderController.share_path + '/attack_star.png')
    #                 if exist:
    #                     ThunderController.touch(self.index, ThunderController.cheat(location))
    #                     ThunderController.random_sleep(10, 12)
    #         exist, location, template = ThunderController.check_picture_list(self.index, Onmyoji.victory)
    #         if exist:
    #             ThunderController.touch(self.index, ThunderController.cheat(location))
    #             ThunderController.random_sleep()
    #         if refresh:
    #             exist, location = ThunderController.wait_picture(self.index, 1,
    #                                                              ThunderController.share_path +
    #                                                              '/breakthrough_refresh.png')
    #             if exist:
    #                 ThunderController.touch(self.index, ThunderController.cheat(location))
    #                 ThunderController.random_sleep()
    #                 exist, location = ThunderController.wait_picture(self.index, 10,
    #                                                                  ThunderController.share_path +
    #                                                                  '/breakthrough_refresh_confirm.png')
    #                 if exist:
    #                     ThunderController.touch(self.index, ThunderController.cheat(location))
    #                     ThunderController.random_sleep(3, 4)
    #                     screen = ThunderController.screen_shot(self.index)
    #                     locations = ThunderController.find_all_pictures(screen, ThunderController.share_path +
    #                                                                     '/zero_star.png', 0.95)
    #                     print('zero star number: ', len(locations))
    #                     if len(locations) >= 3:
    #                         refresh = False
    #             else:
    #                 sleep_time = ThunderController.intercept_rectangle_from_picture(
    #                     self.index,
    #                     Onmyoji.break_through_sleep_left_up,
    #                     Onmyoji.break_through_sleep_right_down)
    #                 result = ThunderController.fetch_number_from_picture(sleep_time)
    #                 minute = int(result[:2])
    #                 second = int(result[2:])
    #                 sleep_time = 60 * minute + second
    #                 print('need to sleep... ', sleep_time)
    #                 ThunderController.random_sleep(sleep_time, sleep_time + 10)

    def break_through(self):
        refresh = False
        ticket = ThunderController.intercept_rectangle_from_picture(self.index,
                                                                    Onmyoji.break_through_ticket_left_up,
                                                                    Onmyoji.break_through_ticket_right_down)
        result = ThunderController.fetch_number_from_picture(ticket)
        result = int(result[:-2])
        ticket = result
        while True:
            print('have ', ticket, 'tickets')
            if ticket <= 2:
                break
            exist, location, template = ThunderController.check_picture_list(self.index, Onmyoji.victory)
            if exist:
                if template in ['./Onmyoji_images\\2_victory.png', './Onmyoji_images\\3_victory.png']:
                    ThunderController.random_sleep(3, 4)
                    exist, _ = ThunderController.wait_picture(self.index, 1,
                                                              ThunderController.share_path
                                                              + '/break_through_money_flag.png')
                    if exist:
                        print("already beat 3 players")
                        ticket -= 3
                        refresh = True
                        ThunderController.random_sleep(3, 4)
                ThunderController.touch(self.index, ThunderController.cheat(location))
                ThunderController.random_sleep()
            screen = ThunderController.screen_shot(self.index)
            click_locations = ThunderController.find_all_pictures(screen,
                                                                  ThunderController.share_path + '/zero_star.png', 0.95)
            click_position = None
            if len(click_locations) > 0:
                exist, location, template = ThunderController.check_picture_list(self.index, Onmyoji.victory)
                if exist:
                    if template in ['./Onmyoji_images\\2_victory.png', './Onmyoji_images\\3_victory.png']:
                        ThunderController.random_sleep(3, 4)
                        exist, _ = ThunderController.wait_picture(self.index, 1,
                                                                  ThunderController.share_path
                                                                  + '/break_through_money_flag.png')
                        if exist:
                            print("already beat 3 players")
                            ticket -= 3
                            refresh = True
                            ThunderController.random_sleep(3, 4)
                    ThunderController.touch(self.index, ThunderController.cheat(location))
                    ThunderController.random_sleep()
                screen = ThunderController.screen_shot(self.index)
                locations = ThunderController.find_all_pictures(
                    screen,
                    ThunderController.share_path + '/broken2_flag.png', 0.7)
                print('beat' + str(len(locations)))
                if len(locations) >= 3:
                    refresh = True
                if not refresh:
                    screen = ThunderController.screen_shot(self.index)
                    remove_locations = ThunderController.find_all_pictures(screen,
                                                                           ThunderController.share_path
                                                                           + '/break_through_fail_flag.png')
                    if len(remove_locations) > 0:
                        to_remove = []
                        for click in click_locations:
                            for remove in remove_locations:
                                if 130 >= remove[0] - click[0] >= 70 and 80 >= click[1] - remove[1] >= 40:
                                    to_remove.append(click)
                        for remove in to_remove:
                            click_locations.remove(remove)
                    print(click_locations)
                    if len(click_locations) > 0:
                        click_position = click_locations[random.randint(0, len(click_locations) - 1)]
                    else:
                        refresh = True
                if not refresh:
                    ThunderController.touch(self.index, ThunderController.cheat(click_position))
                    ThunderController.random_sleep()
                    exist, location = ThunderController.wait_picture(self.index, 10,
                                                                     ThunderController.share_path + '/attack_star.png')
                    if exist:
                        ThunderController.touch(self.index, ThunderController.cheat(location))
                        ThunderController.random_sleep(10, 12)
            if refresh:
                exist, location = ThunderController.wait_picture(self.index, 1,
                                                                 ThunderController.share_path +
                                                                 '/breakthrough_refresh.png')
                if exist:
                    ThunderController.touch(self.index, ThunderController.cheat(location))
                    ThunderController.random_sleep()
                    exist, location = ThunderController.wait_picture(self.index, 10,
                                                                     ThunderController.share_path +
                                                                     '/breakthrough_refresh_confirm.png')
                    if exist:
                        ThunderController.touch(self.index, ThunderController.cheat(location))
                        ThunderController.random_sleep(3, 4)
                        screen = ThunderController.screen_shot(self.index)
                        locations = ThunderController.find_all_pictures(screen, ThunderController.share_path +
                                                                        '/zero_star.png', 0.95)
                        print('zero star number: ', len(locations))
                        if len(locations) >= 3:
                            refresh = False
                else:
                    sleep_time = ThunderController.intercept_rectangle_from_picture(
                        self.index,
                        Onmyoji.break_through_sleep_left_up,
                        Onmyoji.break_through_sleep_right_down)
                    result = ThunderController.fetch_number_from_picture(sleep_time)
                    minute = int(result[:2])
                    second = int(result[2:])
                    sleep_time = 60 * minute + second
                    print('need to sleep... ', sleep_time)
                    ThunderController.random_sleep(sleep_time, sleep_time + 10)

    def original_fire(self):
        while True:
            exist, location, template = ThunderController.check_picture_list(self.index, Onmyoji.victory)
            if exist:
                ThunderController.touch(self.index, ThunderController.cheat(location))
                if template == './Onmyoji_images\\challenge_victory.png':
                    ThunderController.random_sleep(55, 65)

    def in_chapter_battle(self):
        screen = ThunderController.screen_shot(self.index)
        locations = ThunderController.find_all_pictures(screen, ThunderController.share_path + '/max_level_flag.png')
        max_level_flag = False
        if len(locations) != 0:
            for x, y, w, h in locations:
                if x in range(*Onmyoji.chapter_attendant_position_3_stand_width) and y in range(
                        *Onmyoji.chapter_attendant_position_3_stand_height):
                    max_level_flag = True
            if max_level_flag:
                ThunderController.random_click(self.index, Onmyoji.chapter_attendant_click_left_up,
                                               Onmyoji.chapter_attendant_click_right_down)
                ThunderController.random_click(self.index, Onmyoji.chapter_attendant_click_left_up,
                                               Onmyoji.chapter_attendant_click_right_down)
                ThunderController.random_sleep()
                exist, location, template = ThunderController.check_picture_list(self.index, Onmyoji.champion_class)
                if exist:
                    if template != './Onmyoji_images\\N_class.png':
                        ThunderController.touch(self.index, ThunderController.cheat(location))
                        ThunderController.random_sleep()
                        exist, location = ThunderController.wait_picture(self.index, 1,
                                                                         ThunderController.share_path + '/N_class.png')
                        if exist:
                            ThunderController.touch(self.index, ThunderController.cheat(location))
                            ThunderController.random_sleep()
                    while True:
                        exist, location = ThunderController.wait_picture(self.index, 1,
                                                                         ThunderController.share_path +
                                                                         '/level_one_flag.png')
                        if exist:
                            height = random.randint(*Onmyoji.chapter_attendant_position_3_drag_height)
                            width = random.randint(*Onmyoji.chapter_attendant_position_3_drag_width)
                            drag_time = random.randint(1000, 2000)
                            ThunderController.swipe(self.index, location, (width, height), drag_time)
                            ThunderController.random_sleep()
                            break
                        else:
                            height = random.randint(*Onmyoji.chapter_backup_drag_height)
                            left = random.randint(*Onmyoji.chapter_backup_drag_left)
                            right = random.randint(*Onmyoji.chapter_backup_drag_right)
                            drag_time = random.randint(1000, 2000)
                            ThunderController.swipe(self.index, (right, height), (left, height), drag_time)
                            ThunderController.random_sleep()
        ThunderController.random_sleep(2, 3)
        exist, location = ThunderController.wait_picture(self.index, 1,
                                                         ThunderController.share_path + '/prepare_flag.png')
        if exist:
            ThunderController.touch(self.index, ThunderController.cheat(location))
        ThunderController.random_sleep()
        while True:
            exist, location, _ = ThunderController.check_picture_list(self.index, Onmyoji.victory)
            if exist:
                ThunderController.touch(self.index, ThunderController.cheat(location))
            exist, _, _ = ThunderController.check_picture_list(self.index,
                                                               [ThunderController.share_path +
                                                                '/fix_team_flag.png',
                                                                ThunderController.share_path +
                                                                '/out2_of_chapter_flag.png'])
            if exist:
                break

    def chapter_solo(self):

        def drag_to_left():
            height = random.randint(*Onmyoji.chapter_drag_height)
            left = random.randint(*Onmyoji.chapter_drag_left)
            right = random.randint(*Onmyoji.chapter_drag_right)
            drag_time = random.randint(1000, 2000)
            ThunderController.swipe(self.index, (left, height), (right, height), drag_time)

        def drag_to_right():
            height = random.randint(*Onmyoji.chapter_drag_height)
            left = random.randint(*Onmyoji.chapter_drag_left)
            right = random.randint(*Onmyoji.chapter_drag_right)
            drag_time = random.randint(1000, 2000)
            ThunderController.swipe(self.index, (right, height), (left, height), drag_time)

        exist, _ = ThunderController.wait_picture(self.index, 1,
                                                  ThunderController.share_path + '/fix_team_flag.png')
        if exist:
            ThunderController.random_sleep()
            while True:
                exist, location, _ = ThunderController.check_picture_list(self.index, Onmyoji.chapter_battle)
                if exist:
                    ThunderController.touch(self.index, location[:2])
                    ThunderController.random_sleep(3.5, 4.5)
                    self.in_chapter_battle()
                    ThunderController.random_sleep()
                else:
                    if random.uniform(0, 1) > 0.5:
                        drag_to_right()
                    else:
                        drag_to_left()
                exist, _, template = ThunderController.check_picture_list(self.index, Onmyoji.out_of_chapter)
                if exist:
                    if template == './Onmyoji_images\\gift_chapter_flag.png':
                        exist, location = ThunderController.wait_picture(self.index, 1,
                                                                         ThunderController.share_path +
                                                                         '/backward3_close.png')
                        if exist:
                            ThunderController.touch(self.index, ThunderController.cheat(location))
                        ThunderController.random_sleep()
                        exist, location = ThunderController.wait_picture(self.index, 1,
                                                                         ThunderController.share_path +
                                                                         '/backward3_confirm_close.png')
                        if exist:
                            ThunderController.touch(self.index, ThunderController.cheat(location))
                    break


def main():
    sys.stdout = LogRecorder('./logs/' + '_'.join(re.split(r'[\\ |:]', time.ctime())) + '_log.txt')
    c0 = Cracker(0, [['accept_invite']], Onmyoji())
    # c1 = Cracker(1, [['accept_invite', False]])
    # c2 = Cracker(2, [['accept_invite', False]])
    # c0.start()
    # c1.start()
    # c2.start()
    c0.break_through()
    # c0.chapter_solo()


if __name__ == '__main__':
    main()
