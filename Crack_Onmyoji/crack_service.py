import random
import time
from Crack_Onmyoji.crack_controller import ThunderController
from Crack_Onmyoji.onmyoji_detail import Onmyoji


class Cracker:

    def __init__(self, index: int, task_list: list = None, onmyoji: Onmyoji = None) -> None:
        self.index = index
        self.start_time = time.ctime()
        self.task_list: list = task_list
        self.onmyoji = onmyoji

    def start_onmyoji(self) -> None:
        if ThunderController.is_player_running(self.index):
            ThunderController.reboot_player_and_start_app(self.index, Onmyoji.game_package_name)
        else:
            ThunderController.launch_player_and_start_app(self.index, Onmyoji.game_package_name)
        ThunderController.random_sleep(20, 25)
        ThunderController.random_click(self.index, Onmyoji.left_up_position, Onmyoji.right_down_position)
        self.any_pages_back_to_home_page()

    def is_home_page_or_not(self) -> bool:
        return ThunderController.wait_picture(self.index, 1,
                                              ThunderController.share_path + "bonus.png")[0] \
               and not ThunderController.wait_picture(self.index, 1,
                                                      ThunderController.share_path + "yard_close.png")[0]

    def any_pages_back_to_home_page(self) -> None:
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

    def leave_team(self) -> None:
        while True:
            exist, location = ThunderController.wait_picture(self.index, 3, ThunderController.share_path +
                                                             "team_leave.png")
            if not exist:
                break
            else:
                ThunderController.touch(self.index, ThunderController.cheat(location))
                ThunderController.random_sleep()
                _, location = ThunderController.wait_picture(self.index, 3,
                                                             ThunderController.share_path +
                                                             "team_confirm_leave.png")
                ThunderController.touch(self.index, ThunderController.cheat(location))
                ThunderController.random_sleep()
        self.any_pages_back_to_home_page()

    def accept_invite(self, acceptor: bool = True) -> None:
        auto_accept_flag = False
        auto_invite_flag = False
        inviter = not acceptor
        count = 0
        while True:
            if acceptor and not auto_accept_flag:
                exist, location, template = ThunderController.check_picture_list(self.index, Onmyoji.invite)
                if exist:
                    if template == 'Onmyoji_images\\team2_invite.png':
                        auto_accept_flag = True
                    ThunderController.touch(self.index, ThunderController.cheat(location))
            if inviter and not auto_invite_flag:
                exist, location = ThunderController.wait_picture(
                    self.index, 1,
                    ThunderController.share_path + 'invite_in_default.png')
                if exist:
                    ThunderController.touch(self.index, ThunderController.cheat(location))
                    exist, location = ThunderController.wait_picture(
                        self.index, 1,
                        ThunderController.share_path + 'invite_in_default_confirm.png')
                    if exist:
                        ThunderController.touch(self.index, ThunderController.cheat(location))
                        auto_invite_flag = True
            ThunderController.random_sleep()
            exist, location, template = ThunderController.check_picture_list(self.index, Onmyoji.victory)
            if exist:
                if template == 'Onmyoji_images\\battle_victory.png':
                    ThunderController.random_sleep(3, 4)
                    count += 1
                    print(count)
                ThunderController.touch(self.index, ThunderController.cheat(location))

    def personal_break_through(self) -> None:
        if not self.is_home_page_or_not():
            self.any_pages_back_to_home_page()
        ThunderController.random_sleep()
        ThunderController.random_click(self.index, Onmyoji.home_page_explore_left_up,
                                       Onmyoji.home_page_explore_right_down)
        ThunderController.random_sleep(1.5, 3)
        exist, location = ThunderController.wait_picture(self.index, 2,
                                                         ThunderController.share_path + 'breakthrough_icon.png')
        if exist:
            ThunderController.touch(self.index, ThunderController.cheat(location))
        ThunderController.random_sleep(1.5, 3)
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
                self.any_pages_back_to_home_page()
                break
            exist, location, template = ThunderController.check_picture_list(self.index, Onmyoji.victory)
            if exist:
                if template in ['Onmyoji_images\\2_victory.png', 'Onmyoji_images\\3_victory.png']:
                    ThunderController.random_sleep(3, 4)
                    exist, _ = ThunderController.wait_picture(self.index, 1,
                                                              ThunderController.share_path
                                                              + 'break_through_money_flag.png')
                    if exist:
                        print("already beat 3 players")
                        ticket -= 3
                        refresh = True
                        ThunderController.random_sleep(3, 4)
                ThunderController.touch(self.index, ThunderController.cheat(location))
                ThunderController.random_sleep()
            screen = ThunderController.screen_shot(self.index)
            click_locations = ThunderController.find_all_pictures(screen,
                                                                  ThunderController.share_path + 'zero_star.png', 0.95)
            click_position = None
            if len(click_locations) > 0:
                exist, location, template = ThunderController.check_picture_list(self.index, Onmyoji.victory)
                if exist:
                    if template in ['Onmyoji_images\\2_victory.png', 'Onmyoji_images\\3_victory.png']:
                        ThunderController.random_sleep(3, 4)
                        exist, _ = ThunderController.wait_picture(self.index, 1,
                                                                  ThunderController.share_path
                                                                  + 'break_through_money_flag.png')
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
                    ThunderController.share_path + 'broken2_flag.png', 0.7)
                print('beat' + str(len(locations)))
                if len(locations) >= 3:
                    refresh = True
                if not refresh:
                    screen = ThunderController.screen_shot(self.index)
                    remove_locations = ThunderController.find_all_pictures(screen,
                                                                           ThunderController.share_path
                                                                           + 'break_through_fail_flag.png')
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
                                                                     ThunderController.share_path + 'attack_star.png')
                    if exist:
                        ThunderController.touch(self.index, ThunderController.cheat(location))
                        ThunderController.random_sleep(10, 12)
            if refresh:
                exist, location = ThunderController.wait_picture(self.index, 1,
                                                                 ThunderController.share_path +
                                                                 'breakthrough_refresh.png')
                if exist:
                    ThunderController.touch(self.index, ThunderController.cheat(location))
                    ThunderController.random_sleep()
                    exist, location = ThunderController.wait_picture(self.index, 10,
                                                                     ThunderController.share_path +
                                                                     'breakthrough_refresh_confirm.png')
                    if exist:
                        ThunderController.touch(self.index, ThunderController.cheat(location))
                        ThunderController.random_sleep(3, 4)
                        screen = ThunderController.screen_shot(self.index)
                        locations = ThunderController.find_all_pictures(screen, ThunderController.share_path +
                                                                        'zero_star.png', 0.95)
                        print('zero star number: ', len(locations))
                        if len(locations) >= 3:
                            refresh = False
                else:
                    sleep_time = ThunderController.intercept_rectangle_from_picture(
                        self.index,
                        Onmyoji.break_through_sleep_left_up,
                        Onmyoji.break_through_sleep_right_down)
                    result = ThunderController.fetch_number_from_picture(sleep_time)
                    if len(result) >= 4:
                        minute = int(result[:2])
                        second = int(result[2:])
                    else:
                        minute = 0
                        second = 0
                    sleep_time = 60 * minute + second
                    print('need to sleep... ', sleep_time)
                    ThunderController.random_sleep(sleep_time, sleep_time + 10)

    def solo_mode(self, mode: str, addition_arg: str) -> None:
        if not self.is_home_page_or_not():
            self.any_pages_back_to_home_page()
        ThunderController.random_sleep()
        ThunderController.random_click(self.index, Onmyoji.home_page_explore_left_up,
                                       Onmyoji.home_page_explore_right_down)
        ThunderController.random_sleep(1.5, 3)
        if mode == 'mitama':
            exist, location = ThunderController.wait_picture(self.index, 2,
                                                             ThunderController.share_path + 'mitama_icon.png')
            if exist:
                ThunderController.touch(self.index, ThunderController.cheat(location))
                ThunderController.random_sleep(1.5, 3)
                exist, location = ThunderController.wait_picture(self.index, 2,
                                                                 ThunderController.share_path + addition_arg +
                                                                 '_mitama.png')
                if exist:
                    ThunderController.touch(self.index, ThunderController.cheat(location))
                ThunderController.random_sleep(1.5, 3)
        if mode == 'awake':
            exist, location = ThunderController.wait_picture(self.index, 2,
                                                             ThunderController.share_path + 'awake_icon.png')
            if exist:
                ThunderController.touch(self.index, ThunderController.cheat(location))
                ThunderController.random_sleep(1.5, 3)
                exist, location = ThunderController.wait_picture(self.index, 2,
                                                                 ThunderController.share_path + addition_arg +
                                                                 '_awake.png')
                if exist:
                    ThunderController.touch(self.index, ThunderController.cheat(location))
                ThunderController.random_sleep(1.5, 3)
        if mode == 'imperial_spirit':
            exist, location = ThunderController.wait_picture(self.index, 2,
                                                             ThunderController.share_path + 'imperial_spirit_icon.png')
            if exist:
                ThunderController.touch(self.index, ThunderController.cheat(location))
                ThunderController.random_sleep(1.5, 3)
                exist, location = ThunderController.wait_picture(self.index, 2,
                                                                 ThunderController.share_path + addition_arg +
                                                                 '_imperial_spirit.png')
                if exist:
                    ThunderController.touch(self.index, ThunderController.cheat(location))
                ThunderController.random_sleep(1.5, 3)
        while True:
            exist, location, template = ThunderController.check_picture_list(self.index, Onmyoji.victory)
            if exist:
                ThunderController.touch(self.index, ThunderController.cheat(location))
                if template == 'Onmyoji_images\\challenge_victory.png':
                    if mode == 'mitama':
                        ThunderController.random_sleep(20, 30)
                    if mode == 'awake':
                        ThunderController.random_sleep(15, 20)
                    if mode == 'imperial_spirit':
                        ThunderController.random_sleep(55, 65)

    def _in_chapter_battle(self) -> None:
        screen = ThunderController.screen_shot(self.index)
        locations = ThunderController.find_all_pictures(screen, ThunderController.share_path + 'max_level_flag.png')
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
                ThunderController.random_sleep(1.5, 3)
                exist, location, template = ThunderController.check_picture_list(self.index, Onmyoji.champion_class)
                if exist:
                    if template != 'Onmyoji_images\\N_class.png':
                        ThunderController.touch(self.index, ThunderController.cheat(location))
                        ThunderController.random_sleep()
                        exist, location = ThunderController.wait_picture(self.index, 1,
                                                                         ThunderController.share_path + 'N_class.png')
                        if exist:
                            ThunderController.touch(self.index, ThunderController.cheat(location))
                            ThunderController.random_sleep()
                    while True:
                        exist, location = ThunderController.wait_picture(self.index, 1,
                                                                         ThunderController.share_path +
                                                                         'level_one_flag.png')
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
                                                         ThunderController.share_path + 'prepare_flag.png')
        if exist:
            ThunderController.touch(self.index, ThunderController.cheat(location))
        ThunderController.random_sleep()
        while True:
            exist, location, _ = ThunderController.check_picture_list(self.index, Onmyoji.victory)
            if exist:
                ThunderController.touch(self.index, ThunderController.cheat(location))
            exist, _, _ = ThunderController.check_picture_list(self.index,
                                                               [ThunderController.share_path +
                                                                'fix_team_flag.png',
                                                                ThunderController.share_path +
                                                                'out2_of_chapter_flag.png'])
            if exist:
                break

    def chapter_solo(self) -> None:

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

        if not self.is_home_page_or_not():
            self.any_pages_back_to_home_page()
        ThunderController.random_click(self.index, Onmyoji.home_page_explore_left_up,
                                       Onmyoji.home_page_explore_right_down)
        ThunderController.random_sleep(1.5, 3)
        exist, location = ThunderController.wait_picture(self.index, 2,
                                                         ThunderController.share_path + 'chapter_28_flag.png')
        if exist:
            ThunderController.touch(self.index, ThunderController.cheat(location))
        ThunderController.random_sleep(1.5, 3)
        exist, location = ThunderController.wait_picture(self.index, 2,
                                                         ThunderController.share_path + 'explore_start_icon.png')
        if exist:
            ThunderController.touch(self.index, ThunderController.cheat(location))
        ThunderController.random_sleep(1.5, 3)
        exist, _ = ThunderController.wait_picture(self.index, 1,
                                                  ThunderController.share_path + 'fix_team_flag.png')
        if exist:
            ThunderController.random_sleep()
            while True:
                exist, location, _ = ThunderController.check_picture_list(self.index, Onmyoji.chapter_battle)
                if exist:
                    ThunderController.touch(self.index, location[:2])
                    ThunderController.random_sleep(3.5, 4.5)
                    self._in_chapter_battle()
                    ThunderController.random_sleep()
                else:
                    if random.uniform(0, 1) > 0.5:
                        drag_to_right()
                    else:
                        drag_to_left()
                exist, _, template = ThunderController.check_picture_list(self.index, Onmyoji.out_of_chapter)
                if exist:
                    if template == 'Onmyoji_images\\gift_chapter_flag.png':
                        exist, location = ThunderController.wait_picture(self.index, 1,
                                                                         ThunderController.share_path +
                                                                         'backward3_close.png')
                        if exist:
                            ThunderController.touch(self.index, ThunderController.cheat(location))
                        ThunderController.random_sleep()
                        exist, location = ThunderController.wait_picture(self.index, 1,
                                                                         ThunderController.share_path +
                                                                         'backward3_confirm_close.png')
                        if exist:
                            ThunderController.touch(self.index, ThunderController.cheat(location))
                    break
            self.any_pages_back_to_home_page()

    def hundred_ghosts(self, count: int) -> None:
        if not self.is_home_page_or_not():
            self.any_pages_back_to_home_page()
        exist, location = ThunderController.wait_picture(self.index, 1,
                                                         ThunderController.share_path + "to_yard_icon.png")
        if exist:
            ThunderController.touch(self.index, ThunderController.cheat(location))
        ThunderController.random_sleep(1.5, 3)
        exist, location = ThunderController.wait_picture(self.index, 1,
                                                         ThunderController.share_path + "hundred_ghosts_flag.png", 0.7)
        if exist:
            ThunderController.touch(self.index, ThunderController.cheat(location))
        ThunderController.random_sleep()
        ticket = ThunderController.intercept_rectangle_from_picture(self.index,
                                                                    Onmyoji.hundred_ghosts_ticket_left_up,
                                                                    Onmyoji.hundred_ghosts_ticket_right_down)
        result = ThunderController.fetch_number_from_picture(ticket)
        result = int(result)
        ticket = result
        times = 0
        while ticket >= 0 and times < count:
            print('have ', ticket, ' tickets')
            exist, location, template = ThunderController.check_picture_list(self.index, Onmyoji.hundred_ghosts)
            if exist:
                if template == 'Onmyoji_images\\enter_hundred_ghosts.png':
                    ThunderController.touch(self.index, ThunderController.cheat(location))
                    print(self.index, ' begin ', times, ' hundred ghosts')
                elif template == 'Onmyoji_images\\begin_hundred_ghosts.png':
                    choose_pool = [(Onmyoji.hundred_ghosts_choose_king_first_left_up,
                                    Onmyoji.hundred_ghosts_choose_king_first_right_down),
                                   (Onmyoji.hundred_ghosts_choose_king_second_left_up,
                                    Onmyoji.hundred_ghosts_choose_king_second_right_down),
                                   (Onmyoji.hundred_ghosts_choose_king_third_left_up,
                                    Onmyoji.hundred_ghosts_choose_king_third_right_down)]
                    for _ in range(1):
                        random_king = random.randint(0, 2)
                        king_locations = choose_pool[random_king]
                        ThunderController.random_click(self.index, *king_locations)
                        ThunderController.random_sleep()
                    ThunderController.random_sleep(1.8, 3)
                    ThunderController.touch(self.index, ThunderController.cheat(location))
                    ThunderController.random_sleep(2, 3)
                    exist, location = ThunderController.wait_picture(self.index, 1,
                                                                     ThunderController.share_path
                                                                     + 'five_ghosts.png')
                    if exist:
                        ticket -= 1
                        times += 1
                        height = random.randint(*Onmyoji.hundred_ghosts_drag_height)
                        width = random.randint(*Onmyoji.hundred_ghosts_drag_width)
                        drag_time = random.randint(1000, 2000)
                        ThunderController.swipe(self.index, location,
                                                (width, height), drag_time)
                        ThunderController.random_sleep(0.4, 0.6)
                    else:
                        break
                    low_high = Onmyoji.hundred_ghosts_throw_height
                    throw_pool = [((i * 180, low_high[0]), ((i + 1) * 180, low_high[1])) for i in range(1, 5)]
                    begin_time = time.time()
                    while True:
                        current_time = time.time()
                        if current_time - begin_time >= 40:
                            ThunderController.random_sleep()
                            exist, _, _ = ThunderController.check_picture_list(self.index, Onmyoji.hundred_ghosts)
                            if exist:
                                break
                        ThunderController.random_sleep(0.4, 0.8)
                        random_area = random.randint(0, 3)
                        area_locations = throw_pool[random_area]
                        on_fire = random.uniform(0, 1) >= 0.8
                        if on_fire:
                            for i in range(3):
                                print('on fire ', i)
                                ThunderController.random_click(self.index, *area_locations)
                                ThunderController.random_sleep(0.4, 0.6)
                        ThunderController.random_click(self.index, *area_locations)
                else:
                    ThunderController.touch(self.index, ThunderController.cheat(location))
        ThunderController.random_sleep()
        self.any_pages_back_to_home_page()

    def open_close_buff(self, buff_type: str, buff_option: bool) -> None:
        if not self.is_home_page_or_not():
            self.any_pages_back_to_home_page()
        exist, location = ThunderController.wait_picture(self.index, 1,
                                                         ThunderController.share_path + "bonus.png")
        if exist:
            ThunderController.touch(self.index, ThunderController.cheat(location))
        ThunderController.random_sleep()
        if buff_type == 'mitama':
            mitama_flag = self._buff_check_in_location(Onmyoji.mitama_buff_check_left_up,
                                                       Onmyoji.mitama_buff_check_right_down)
            if mitama_flag ^ buff_option:
                ThunderController.random_click(self.index, Onmyoji.mitama_buff_left_up, Onmyoji.mitama_buff_right_down)
        if buff_type == 'awake':
            awake_flag = self._buff_check_in_location(Onmyoji.awake_buff_check_left_up,
                                                      Onmyoji.awake_buff_check_right_down)
            if awake_flag ^ buff_option:
                ThunderController.random_click(self.index, Onmyoji.awake_buff_left_up, Onmyoji.awake_buff_right_down)
        ThunderController.random_sleep()
        exist, location = ThunderController.wait_picture(self.index, 1,
                                                         ThunderController.share_path + "bonus.png")
        if exist:
            ThunderController.touch(self.index, ThunderController.cheat(location))

    def _buff_check_in_location(self, left_up: (int, int), right_down: (int, int)) -> bool:
        exist, location = ThunderController.wait_picture(self.index, 1,
                                                         ThunderController.share_path + "buff_check.png")
        if exist:
            return location[0] in range(left_up[0], right_down[0]) and location[1] in range(left_up[1], right_down[1])
        else:
            return False

    def _invite_friend_to_team(self, mode: str, addition_arg: str, column_name_list: [(str, str)]):
        if not self.is_home_page_or_not():
            self.any_pages_back_to_home_page()
        ThunderController.random_sleep()
        ThunderController.random_click(self.index, Onmyoji.home_page_explore_left_up,
                                       Onmyoji.home_page_explore_right_down)
        ThunderController.random_sleep(1.5, 3)
        if mode == 'mitama':
            exist, location = ThunderController.wait_picture(self.index, 2,
                                                             ThunderController.share_path + 'mitama_icon.png')
            if exist:
                ThunderController.touch(self.index, ThunderController.cheat(location))
                ThunderController.random_sleep(1.5, 3)
                exist, location = ThunderController.wait_picture(self.index, 2,
                                                                 ThunderController.share_path +
                                                                 'dragon_mitama.png')
                if exist:
                    ThunderController.touch(self.index, ThunderController.cheat(location))
                ThunderController.random_sleep(1.5, 3)
                exist, location = ThunderController.wait_picture(self.index, 2,
                                                                 ThunderController.share_path +
                                                                 'mitama_level_' + addition_arg + '.png')
                if exist:
                    ThunderController.touch(self.index, ThunderController.cheat(location))
                ThunderController.random_sleep(1.5, 3)
        if mode == 'awake':
            exist, location = ThunderController.wait_picture(self.index, 1,
                                                             ThunderController.share_path + 'awake_icon.png')
            if exist:
                ThunderController.touch(self.index, ThunderController.cheat(location))
                ThunderController.random_sleep(1.5, 3)
                exist, location = ThunderController.wait_picture(self.index, 1,
                                                                 ThunderController.share_path + addition_arg +
                                                                 '_awake.png')
                if exist:
                    ThunderController.touch(self.index, ThunderController.cheat(location))
                ThunderController.random_sleep(1.5, 3)
        exist, location = ThunderController.wait_picture(self.index, 1,
                                                         ThunderController.share_path + 'invite\\make_up_team.png')
        if exist:
            ThunderController.touch(self.index, ThunderController.cheat(location))
        ThunderController.random_sleep(1.5, 3)
        exist, location = ThunderController.wait_picture(self.index, 1,
                                                         ThunderController.share_path + 'invite\\create_team_bar.png')
        if exist:
            ThunderController.touch(self.index, ThunderController.cheat(location))
        ThunderController.random_sleep(1.5, 3)
        exist, location = ThunderController.wait_picture(self.index, 1,
                                                         ThunderController.share_path + 'invite\\not_open.png')
        if exist:
            ThunderController.touch(self.index, ThunderController.cheat(location))
        ThunderController.random_sleep(1.5, 3)
        exist, location = ThunderController.wait_picture(self.index, 1,
                                                         ThunderController.share_path + 'invite\\create_bar.png')
        if exist:
            ThunderController.touch(self.index, ThunderController.cheat(location))
        ThunderController.random_sleep(1.5, 3)
        for column_name in column_name_list:
            exist, location = ThunderController.wait_picture(self.index, 1,
                                                             ThunderController.share_path + 'invite\\invite_icon.png')
            if exist:
                ThunderController.touch(self.index, ThunderController.cheat(location))
            ThunderController.random_sleep(1.5, 3)
            exist, location = ThunderController.wait_picture(self.index, 1,
                                                             ThunderController.share_path + 'invite\\' + column_name[
                                                                 0] + '_column.png')
            if exist:
                ThunderController.touch(self.index, ThunderController.cheat(location))
            ThunderController.random_sleep(1.5, 3)
            exist, location = ThunderController.wait_picture(self.index, 1,
                                                             ThunderController.share_path + 'invite\\name_' +
                                                             column_name[
                                                                 1] + '.png')
            if exist:
                ThunderController.touch(self.index, ThunderController.cheat(location))
            ThunderController.random_sleep(1.5, 3)
            exist, location = ThunderController.wait_picture(self.index, 1,
                                                             ThunderController.share_path + 'invite\\invite_bar.png')
            if exist:
                ThunderController.touch(self.index, ThunderController.cheat(location))
            ThunderController.random_sleep(12, 15)

    def mitama_or_awake_invite(self, mode: str, addition_arg: str, column_name_list: [(str, str)]):
        self._invite_friend_to_team(mode, addition_arg, column_name_list)
        ThunderController.random_sleep(1.5, 3)
        self.accept_invite(False)

    def group_break_through(self):
        if not self.is_home_page_or_not():
            self.any_pages_back_to_home_page()
        ThunderController.random_sleep()
        ThunderController.random_click(self.index, Onmyoji.home_page_explore_left_up,
                                       Onmyoji.home_page_explore_right_down)
        ThunderController.random_sleep(1.5, 3)
        exist, location = ThunderController.wait_picture(self.index, 2,
                                                         ThunderController.share_path + 'breakthrough_icon.png')
        if exist:
            ThunderController.touch(self.index, ThunderController.cheat(location))
        ThunderController.random_sleep(1.5, 3)
        exist, location = ThunderController.wait_picture(self.index, 2,
                                                         ThunderController.share_path +
                                                         'group_break_through_icon.png')
        if exist:
            ThunderController.touch(self.index, ThunderController.cheat(location))
        ThunderController.random_sleep(1.5, 3)
        scroll = False
        not_exist_times = 0
        while True:
            exist, location, template = ThunderController.check_picture_list(self.index, Onmyoji.victory)
            if exist:
                ThunderController.touch(self.index, ThunderController.cheat(location))
            exist, location = ThunderController.wait_picture(self.index, 1, ThunderController.share_path +
                                                             'group_break_through_flag.png')
            if exist:
                exist, location = ThunderController.wait_picture(self.index, 1,
                                                                 ThunderController.share_path +
                                                                 'group_break_through_target.png')
                if exist:
                    not_exist_times = 0
                    ThunderController.touch(self.index, ThunderController.cheat(location))
                    ThunderController.random_sleep()
                    exist, _ = ThunderController.wait_picture(self.index, 1, ThunderController.share_path +
                                                              'group_tickets_not_enough.png')
                    if exist:
                        break
                    exist, location = ThunderController.wait_picture(self.index, 1,
                                                                     ThunderController.share_path +
                                                                     'attack_star.png')
                    if exist:
                        ThunderController.touch(self.index, ThunderController.cheat(location))
                else:
                    scroll = True
                    not_exist_times += 1
            if scroll:
                exist, location = ThunderController.wait_picture(self.index, 2,
                                                                 ThunderController.share_path +
                                                                 'group_break_through_scroll.png')
                if exist:
                    flag = random.uniform(self.index, 1) > 0.75
                    ThunderController.swipe(0, location[:2],
                                            (location[0], location[1] - 120 if flag else location[1] + 120),
                                            1800)
                    scroll = False
            if not_exist_times >= 5:
                break
        self.any_pages_back_to_home_page()
