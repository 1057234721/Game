import base64
import re
import glob
import json
import os
import random
import shutil
import sys
import time
from collections import defaultdict
import queue
import cv2 as cv
import threading
import requests


class LogRecorder(object):
    def __init__(self, file_name="./log.txt"):
        self.terminal = sys.stdout
        self.log = open(file_name, "w", encoding='utf-8')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


class ThunderPlayer(object):
    def __init__(self, info: list):
        super(ThunderPlayer, self).__init__()
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


class ThunderController:
    console = 'E:\\OnmyojiLibrary\\ChangZhi\\dnplayer2\\dnconsole.exe '
    ld = 'E:\\OnmyojiLibrary\\ChangZhi\\dnplayer2\\ld.exe '
    share_path = '.\\Onmyoji_images'

    # fetch all thunder simulators list
    @staticmethod
    def get_list() -> list:
        cmd = os.popen(ThunderController.console + 'list2')
        text = cmd.read()
        cmd.close()
        print("fetching all thunder simulators list......")
        info = text.split('\n')
        result = list()
        for line in info:
            if len(line) > 1:
                thunder_player_info = line.split(',')
                result.append(ThunderPlayer(thunder_player_info))
        return result

    # fetch all running thunder simulators list
    @staticmethod
    def get_running_list() -> list:
        result = list()
        all_players = ThunderController.get_list()
        for player in all_players:
            if player.is_running() is True:
                result.append(player)
        return result

    # test the specified index player is running or not
    @staticmethod
    def is_player_running(index: int) -> bool:
        all_players = ThunderController.get_list()
        if index >= len(all_players):
            raise IndexError('%d is not exist' % index)
        return all_players[index].is_running()

    # run ld cmd command on specified index player
    @staticmethod
    def ld_cmd(index: int, command: str, silence: bool = True) -> str:
        cmd = ThunderController.ld + '-s %d %s' % (index, command)
        if silence:
            os.system(cmd)
            return ''
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # run console command
    @staticmethod
    def console_cmd(command: str, silence: bool = False) -> str:
        cmd = ThunderController.console + " " + command
        if silence:
            os.system(cmd)
            return ''
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # install specified app, assuming the index player is running
    @staticmethod
    def install_app(index: int, path: str) -> str:
        shutil.copy(path, ThunderController.share_path + '/' + str(index) + 'app_to_install.apk')
        time.sleep(random.uniform(2.0, 4.0))
        return ThunderController.ld_cmd(index, 'pm install /sdcard/Pictures/' + str(index) + 'app_to_install.apk')

    # uninstall specified app, assuming the index player is running
    @staticmethod
    def uninstall_app(index: int, package: str) -> str:
        command = 'uninstallapp --index %d --packagename %s' % (index, package)
        return ThunderController.console_cmd(command, True)

    # start specified app, assuming the index player is running
    @staticmethod
    def invoke_app(index: int, package: str) -> str:
        command = 'runapp --index %d --packagename %s' % (index, package)
        return ThunderController.console_cmd(command)

    # stop specified app, assuming the index player is running
    @staticmethod
    def stop_app(index: int, package: str) -> str:
        command = 'killapp --index %d --packagename %s' % (index, package)
        return ThunderController.console_cmd(command)

    # input word, assuming the index player is running
    @staticmethod
    def input_text(index: int, text: str) -> str:
        command = 'action --index %d --key call.input --value %s' % (index, text)
        return ThunderController.console_cmd(command)

    # fetch installed app list, assuming the player is running
    @staticmethod
    def get_package_list(index: int) -> list:
        result = list()
        text = ThunderController.ld_cmd(index, 'pm list packages', False)
        info = text.split('\n')
        for i in info:
            if len(i) > 1:
                result.append(i.strip())
        return result

    # test the specified app is installed or not, assuming the player is running
    @staticmethod
    def has_app_installed(index: int, package: str) -> bool:
        if ThunderController.is_player_running(index) is False:
            return False
        return "package:" + package in ThunderController.get_package_list(index)

    # start player and then start specified app, assuming the player is not running
    @staticmethod
    def launch_player_and_start_app(index: int, package: str = "null") -> str:
        command = 'launchex --index ' + str(index) + ' --packagename ' + package
        return ThunderController.console_cmd(command)

    # reboot player and then start specified app, assuming the player is running
    @staticmethod
    def reboot_player_and_start_app(index: int, package: str = "null") -> str:
        command = 'action --index ' + str(index) + ' --key call.reboot --value ' + package
        return ThunderController.console_cmd(command)

    # modify the player's location, assuming the player is running
    @staticmethod
    def modify_location(index: int, location: str) -> str:
        command = 'action --index ' + str(index) + ' --key call.locate --value ' + location
        return ThunderController.console_cmd(command)

    # shutdown player, assuming the player is running
    @staticmethod
    def quit(index: int) -> str:
        command = 'quit --index ' + str(index)
        return ThunderController.console_cmd(command)

    # modify the screen resolution, assuming the player is not running
    @staticmethod
    def set_screen_resolution(index: int, resolution: str) -> str:
        command = 'modify --index %d --resolution ' % index + resolution
        return ThunderController.console_cmd(command)

    # tap or touch, assuming the player is running
    @staticmethod
    def touch(index: int, x: int, y: int) -> str:
        return ThunderController.ld_cmd(index, 'input tap %d %d' % (x, y))

    # swipe, assuming the player is running
    @staticmethod
    def swipe(index, coordinate_left_up: (int, int), coordinate_right_down: (int, int), delay: int = 0) -> str:
        x0 = coordinate_left_up[0]
        y0 = coordinate_left_up[1]
        x1 = coordinate_right_down[0]
        y1 = coordinate_right_down[1]
        if delay == 0:
            return ThunderController.ld_cmd(index, 'input swipe %d %d %d %d' % (x0, y0, x1, y1))
        else:
            return ThunderController.ld_cmd(index, 'input swipe %d %d %d %d %d' % (x0, y0, x1, y1, delay))

    # copy player, assuming the player is not running
    @staticmethod
    def copy(name: str, index: int = 0) -> str:
        command = 'copy --name %s --from %d' % (name, index)
        return ThunderController.console_cmd(command)

    # add player, assuming the player is not running
    @staticmethod
    def add(name: str) -> str:
        command = 'add --name %s' % name
        return ThunderController.console_cmd(command)

    # set auto rotate, assuming the player is not running
    @staticmethod
    def auto_rotate(index: int, auto_rate: bool = False) -> str:
        rate = 1 if auto_rate else 0
        command = 'modify --index %d --autorotate %d' % (index, rate)
        return ThunderController.console_cmd(command)

    # modify player info, assuming the player is not running
    @staticmethod
    def change_device_info(index: int) -> str:
        command = 'modify --index %d --imei auto --imsi' \
                  ' auto --simserial auto --androidid auto --mac auto' % index
        return ThunderController.console_cmd(command)

    # modify CPU core number, assuming the player is not running
    @staticmethod
    def change_cpu_count(index: int, number: int) -> str:
        command = 'modify --index %d --cpu %d' % (index, number)
        return ThunderController.console_cmd(command)

    # fetch current activity xml, assuming the player is running
    @staticmethod
    def get_cur_activity_xml(index: int) -> str:
        ThunderController.ld_cmd(index, 'uiautomator dump /sdcard/Pictures/activity.xml')
        time.sleep(random.uniform(0.5, 0.8))
        file = open(ThunderController.share_path + '/activity.xml', 'r', encoding='utf-8')
        result = file.read()
        file.close()
        return result

    # fetch current activity, assuming the player is running
    @staticmethod
    def get_activity_name(index: int) -> str:
        text = ThunderController.ld_cmd(index, '"dumpsys activity top | grep ACTIVITY"', False)
        text = text.split(' ')
        for index, word in enumerate(text):
            if len(word) == 0:
                continue
            if word == 'ACTIVITY':
                return text[index + 1]
        return ''

    # wait for specified activity, assuming the player is running
    @staticmethod
    def wait_activity(index: int, activity: str, timeout: int) -> bool:
        for i in range(timeout):
            if ThunderController.get_activity_name(index) == activity:
                return True
            time.sleep(random.uniform(0.5, 0.8))
        return False

    # find the matched picture, assuming the player is running
    @staticmethod
    def find_picture(screen: str, template: str, threshold: float = 0.001) -> (bool, (int, int), str):
        try:
            screen_shot = cv.imread(screen)
            template_picture = cv.imread(template)
            result = cv.matchTemplate(screen_shot, template_picture, cv.TM_SQDIFF_NORMED)
        except cv.error:
            print('wrong file：', screen, template)
            time.sleep(random.uniform(0.5, 0.8))
            try:
                screen_shot = cv.imread(screen)
                template_picture = cv.imread(template)
                result = cv.matchTemplate(screen_shot, template_picture, cv.TM_SQDIFF_NORMED)
            except cv.error:
                return False, None, None
        minimum_value, maximum_value, minimum_value_location, maximum_value_location = cv.minMaxLoc(result)
        if minimum_value > threshold:
            print(template, minimum_value, maximum_value, minimum_value_location, maximum_value_location,
                  " still finding...")
            return False, None, None
        print(template, minimum_value, minimum_value_location, "found---")
        return True, minimum_value_location, template

    # wait for specified picture, assuming the player is running
    @staticmethod
    def wait_picture(index: int, timeout: int, template: str, threshold: float = 0.001) -> (bool, (int, int), str):
        count = 0
        while count < timeout:
            ThunderController.ld_cmd(index, 'screencap -p /sdcard/Pictures/' + str(index) + 'apk_scr.png')
            time.sleep(random.uniform(0.5, 0.8))
            exist, location, page = ThunderController.find_picture(
                ThunderController.share_path + '/' + str(index) + 'apk_scr.png', template, threshold)
            if not exist:
                time.sleep(random.uniform(0.5, 0.8))
                count += 1
                continue
            return True, location, page
        return False, None, None

    # check the current screen for the pattern picture list, if there exists, then return it.
    # if there exist many pattern pictures then return the first one, assuming the player is running
    @staticmethod
    def check_picture_list(index: int, templates: list, threshold: float = 0.001) -> (bool, (int, int), str):
        ThunderController.ld_cmd(index, 'screencap -p /sdcard/Pictures/' + str(index) + 'apk_scr.png')
        time.sleep(random.uniform(0.5, 0.8))
        for template_index, template in enumerate(templates):
            exist, location, page = ThunderController.find_picture(
                ThunderController.share_path + '/' + str(index) + 'apk_scr.png', template, threshold)
            if exist:
                return template_index, location, page
        return -1, None, None

    # fetch the number (str) from the picture by using the api, must be png format
    @staticmethod
    def fetch_number_from_picture(path: str) -> str:
        url = "https://aip.baidubce.com/rest/2.0/ocr/v1/numbers?" \
              "access_token=24.23d29c67210387cca93ac7c6364e429d.2592000.1563507426.282335-16564125"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'image': base64.b64encode(cv.imencode('.png', cv.imread(path))[1]).decode(),
        }
        response = requests.post(url, data=data, headers=headers)
        result = json.loads(response.text)
        return result["words_result"][0]['words']

    # fetch the string (str) from the picture by using the api, must be png format
    @staticmethod
    def fetch_string_from_picture(path: str) -> str:
        url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?" \
              "access_token=24.23d29c67210387cca93ac7c6364e429d.2592000.1563507426.282335-16564125"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'image': base64.b64encode(cv.imencode('.png', cv.imread(path))[1]).decode(),
        }
        response = requests.post(url, data=data, headers=headers)
        result = json.loads(response.text)
        return result["words_result"]

    # fetch the number (str) from the picture by using the api, must be png format
    @staticmethod
    def intercept_rectangle_from_picture(path: str, left_up: (int, int),
                                         right_down: (int, int)) -> str:
        image = cv.imread(path)
        rectangle = image[left_up[1]:right_down[1], left_up[0]:right_down[0]]
        cv.imwrite(ThunderController.share_path + "/intercepted_picture.png", rectangle)
        return ThunderController.share_path + "/intercepted_picture.png"

    # given a rectangle and click in it randomly, assuming the player is running
    @staticmethod
    def random_click(index: int, left_up: (int, int),
                     right_down: (int, int)) -> str:
        x = random.uniform(left_up[0], right_down[0])
        y = random.uniform(left_up[1], right_down[1])
        return ThunderController.touch(index, x, y)

    # random sleep to avoid detection
    @staticmethod
    def random_sleep(start: float = 0.5, end: float = 0.8) -> None:
        sec = random.uniform(start, end)
        time.sleep(sec)

    # first find the picture and the click
    @staticmethod
    def click_found_picture_location(index: int, timeout: int, target: str) -> str:
        exist, location, template = ThunderController.wait_picture(index, timeout, target)
        if exist:
            ThunderController.random_sleep(0.2, 0.5)
            return ThunderController.touch(index, *location)
        else:
            return "don't find the picture and don't click"


class Cracker(threading.Thread):
    Global_Properties = defaultdict(list)
    Global_Properties['home_page_explore_click_area'] = [(495, 90), (519, 140)]
    Global_Properties['battle_victory_page_click_area'] = [(0, 170), (100, 350)]
    Global_Properties['left_up_position'] = [(0, 0)]
    Global_Properties['right_down_position'] = [(960, 540)]
    Global_Properties['all_pages'] = glob.glob(r'./Onmyoji_images/*_page*.png')
    Global_Properties['icon'] = glob.glob(r'./Onmyoji_images/*_icon*.png')
    Global_Properties['hint'] = glob.glob(r'./Onmyoji_images/*_hint*.png')
    Global_Properties['button'] = glob.glob(r'./Onmyoji_images/*_button*.png')
    Global_Properties['game_package_name'] = ["com.netease.onmyoji"]
    Global_Properties['game_video_activity_name'] = ["com.netease.onmyoji/.VideoPlayer"]
    Global_Properties['player_0'] = ["player_master"]
    Global_Properties['player_1'] = ["player_attendant_one"]
    Global_Properties['player_2'] = ["player_attendant_two"]

    def __init__(self, index: int, task_queue: queue = None) -> None:
        super(Cracker, self).__init__()
        self.index = index
        self.start_time = time.ctime()
        self.current_page = None
        self.mitama_battle_count = 0
        self.awake_battle_count = 0
        self.personal_breakthrough_battle_count = 0
        self.group_breakthrough_battle_count = 0
        self.chapter_single_battle_count = 0
        self.chapter_boss_battle_count = 0
        self.technical_battle_count = 0
        self.fetch_account_info()
        self.task_queue = task_queue
        self.status = None
        self.current_task = None

    def run(self) -> None:
        while not self.task_queue.empty():
            current_task = self.task_queue.get()
            self.status = 'in function'
            self.current_task = current_task
            if len(current_task) == 1:
                eval("self." + current_task[0])()
            else:
                eval("self." + current_task[0])(*current_task[1:])
            self.status = 'out function'
            self.current_task = None

    def add_task(self, task_name: str, task_params: str) -> None:
        self.task_queue.put([task_name, task_params])

    def fetch_account_info(self) -> None:
        pass

    def got_lost_and_regain_location_page(self) -> None:
        if self.current_page is None:
            if ThunderController.get_activity_name(self.index) == Cracker.Global_Properties.get(
                    'game_video_activity_name')[0]:
                ThunderController.random_sleep()
                ThunderController.random_click(self.index, (0, 0), (960, 540))
                ThunderController.random_sleep(1., 2.)
            else:
                self.current_page = ThunderController.check_picture_list(self.index,
                                                                         Cracker.Global_Properties.get('all_pages'))[2]

    def start_onmyoji(self) -> None:
        if ThunderController.is_player_running(self.index):
            ThunderController.reboot_player_and_start_app(self.index,
                                                          Cracker.Global_Properties.get("game_package_name")[0])
        else:
            ThunderController.launch_player_and_start_app(self.index,
                                                          Cracker.Global_Properties.get("game_package_name")[0])
        ThunderController.random_sleep(2, 2.5)
        self.current_page = "video_play_page"
        self.any_pages_back_to_home_page()

    def accept_invite(self, team_leader_index_and_where: [(int, str)], task: str):
        while True:
            if ThunderController.wait_picture(self.index, 10,
                                              ThunderController.share_path + '/invite_from_' +
                                              Cracker.get_user_name_by_index(
                                                  team_leader_index_and_where[0][0]) + "_icon.png")[0]:
                ThunderController.click_found_picture_location(self.index, 3, ThunderController.share_path +
                                                               "/invite_confirm_invite.png")
            ThunderController.random_sleep()
            if self.make_sure_team_member_is_in_team(team_leader_index_and_where):
                break
        ThunderController.click_found_picture_location(self.index, 2,
                                                       ThunderController.share_path + '/in_team_unlock_icon.png')
        if task == 'mitama':
            accept_invite_in_default_flag = False
            while True:
                if not accept_invite_in_default_flag:
                    ThunderController.click_found_picture_location(self.index, 3,
                                                                   ThunderController.share_path +
                                                                   '/auto_accept_invite.png')
                self.mitama_battle_count = self.mitama_battle_count + 1
                ThunderController.random_sleep()
                if self.make_sure_team_member_is_in_team(team_leader_index_and_where):
                    print("this is the " + str(self.mitama_battle_count + 1) + " time(s) to battle with mitama ")
                    ThunderController.random_sleep(16, 18)
                    if ThunderController.wait_picture(self.index, 15,
                                                      ThunderController.share_path +
                                                      "\\battle_info_icon.png")[0]:
                        ThunderController.random_sleep()
                        ThunderController.random_click(self.index,
                                                       *(Cracker.Global_Properties.get(
                                                           'battle_victory_page_click_area')))
                        ThunderController.random_sleep(2.5, 4)
                        ThunderController.random_click(self.index,
                                                       *(Cracker.Global_Properties.get(
                                                           'battle_victory_page_click_area')))
                        ThunderController.random_sleep(2.5, 4)
                        ThunderController.random_click(self.index,
                                                       *(Cracker.Global_Properties.get(
                                                           'battle_victory_page_click_area')))

    def leave_team(self):
        ThunderController.click_found_picture_location(self.index, 3,
                                                       ThunderController.share_path +
                                                       "/make_team_leave_team_close_button.png"
                                                       )
        ThunderController.random_sleep()
        if ThunderController.find_picture(ThunderController.share_path + "/" + str(self.index) + "apk_scr.png",
                                          ThunderController.share_path +
                                          "/make_team_leave_team_confirm_icon.png")[0]:
            ThunderController.click_found_picture_location(self.index, 3,
                                                           ThunderController.share_path +
                                                           "/make_team_leave_team_confirm_close_button.png")

    def make_sure_team_member_is_in_team(self, team_member_index_and_where: [(int, str)]):
        if len(team_member_index_and_where) == 1:
            return ThunderController.wait_picture(self.index, 5,
                                                  ThunderController.share_path + "/" +
                                                  Cracker.get_user_name_by_index(team_member_index_and_where[0][0]) +
                                                  "_in_team_icon.png", 0.009)[0]
        else:
            return ThunderController.wait_picture(self.index, 5,
                                                  ThunderController.share_path + "/" +
                                                  Cracker.get_user_name_by_index(team_member_index_and_where[0][0]) +
                                                  "_in_team_icon.png", 0.009)[0] and \
                   ThunderController.wait_picture(self.index, 5,
                                                  ThunderController.share_path + "/" +
                                                  Cracker.get_user_name_by_index(team_member_index_and_where[1][0]) +
                                                  "_in_team_icon.png", 0.009)[0]

    def is_home_page_or_not(self):
        return ThunderController.wait_picture(self.index, 3,
                                              ThunderController.share_path + "/bonus_icon.png")[0]

    def any_pages_back_to_home_page(self):
        while True:
            if self.is_home_page_or_not():
                break
            else:
                page_index, page_location, template = \
                    ThunderController.check_picture_list(self.index,
                                                         Cracker.Global_Properties.get("button"), 0.008)
                if page_index > -1:
                    print("find ", template)
                    ThunderController.touch(self.index, *page_location)
                    ThunderController.random_sleep(1.2, 1.8)
                else:
                    print("not found and random click...")
                    ThunderController.random_click(self.index, Cracker.Global_Properties.get(
                        "left_up_position")[0],
                                                   Cracker.Global_Properties.get(
                                                       "right_down_position")[0])
                    ThunderController.random_sleep(1.2, 1.8)

    def invite(self, user_index_and_user_location_list: [(int, str)], task: str):
        ThunderController.random_click(self.index,
                                       *Cracker.Global_Properties.get('home_page_explore_click_area'))
        if task == 'mitama':
            ThunderController.click_found_picture_location(self.index, 3,
                                                           ThunderController.share_path + "\\mitama_icon.png")
            ThunderController.click_found_picture_location(self.index, 3,
                                                           ThunderController.share_path + "\\mitama_dragon_icon.png",
                                                           )
        ThunderController.click_found_picture_location(self.index, 3, ThunderController.share_path +
                                                       "\\make_team_icon.png")
        ThunderController.random_sleep()
        ThunderController.click_found_picture_location(self.index, 3, ThunderController.share_path +
                                                       "\\make_team_create_team_icon.png")
        ThunderController.random_sleep()
        if not ThunderController.find_picture(ThunderController.share_path + "/" + str(self.index) + "apk_scr.png",
                                              ThunderController.share_path + "\\checked_not_open_icon.png")[0]:
            ThunderController.click_found_picture_location(self.index, 3, ThunderController.share_path +
                                                           "\\not_open_icon.png")
        ThunderController.click_found_picture_location(self.index, 3, ThunderController.share_path +
                                                       "\\make_team_create_icon.png")
        ThunderController.random_sleep()
        # while True:
        #     for index, location in user_index_and_user_location_list:
        #         ThunderController.click_found_picture_location(self.index, 3,
        #                                                        ThunderController.share_path +
        #                                                        "\\make_team_invite_icon.png")
        #         ThunderController.random_sleep()
        #         ThunderController.click_found_picture_location(self.index, 3,
        #                                                        ThunderController.share_path + "\\"
        #                                                        + location +
        #                                                        "_column_icon.png")
        #         ThunderController.random_sleep()
        #         ThunderController.click_found_picture_location(self.index, 3,
        #                                                        ThunderController.share_path + "\\" +
        #                                                        Cracker.get_user_name_by_index(index) +
        #                                                        "_in_invite_list_icon.png")
        #         ThunderController.random_sleep()
        #         ThunderController.click_found_picture_location(self.index, 3, ThunderController.share_path +
        #                                                        "/make_team_invite_comfirm_horizontal_close_button.png")
        #         ThunderController.random_sleep()
        #     if ThunderController.find_picture(ThunderController.share_path + "/" + str(self.index) + "apk_scr.png",
        #                                       ThunderController.share_path +
        #                                       "/make_team_in_team_quick_click_error_icon.png")[0]:
        #         ThunderController.click_found_picture_location(self.index, 5,
        #                                                        ThunderController.share_path +
        #                                                        "/make_team_in_team_quick_click_"
        #                                                        "error_solution_icon.png")
        #     ThunderController.random_sleep(4.0, 10.0)
        #     if self.make_sure_team_member_is_in_team(user_index_and_user_location_list[0][0]):
        #            break
        while True:
            ThunderController.click_found_picture_location(self.index, 3,
                                                           ThunderController.share_path +
                                                           "\\make_team_invite_icon.png")
            ThunderController.random_sleep()
            if len(user_index_and_user_location_list) == 1:
                ThunderController.click_found_picture_location(self.index, 3,
                                                               ThunderController.share_path + "\\"
                                                               + user_index_and_user_location_list[0][1] +
                                                               "_column_icon.png")
                ThunderController.random_sleep()
                ThunderController.click_found_picture_location(self.index, 3,
                                                               ThunderController.share_path + "\\"
                                                               + Cracker.get_user_name_by_index(
                                                                   user_index_and_user_location_list[0][0]) +
                                                               "_in_invite_list_icon.png")
            else:
                if user_index_and_user_location_list[0][1] == user_index_and_user_location_list[1][1]:
                    ThunderController.click_found_picture_location(self.index, 3,
                                                                   ThunderController.share_path + "\\"
                                                                   + user_index_and_user_location_list[0][1] +
                                                                   "_column_icon.png")
                    ThunderController.random_sleep()
                    ThunderController.click_found_picture_location(self.index, 3,
                                                                   ThunderController.share_path + "\\"
                                                                   + Cracker.get_user_name_by_index(
                                                                       user_index_and_user_location_list[0][0]) +
                                                                   "_in_invite_list_icon.png")
                    ThunderController.random_sleep()
                    ThunderController.click_found_picture_location(self.index, 3,
                                                                   ThunderController.share_path + "\\"
                                                                   + Cracker.get_user_name_by_index(
                                                                       user_index_and_user_location_list[1][0]) +
                                                                   "_in_invite_list_icon.png")
                else:
                    if user_index_and_user_location_list[0][1] == 'friend':
                        ThunderController.click_found_picture_location(self.index, 3,
                                                                       ThunderController.share_path + "\\"
                                                                       + Cracker.get_user_name_by_index(
                                                                           user_index_and_user_location_list[0][0]) +
                                                                       "_in_invite_list_icon.png")
                        ThunderController.random_sleep()
                        ThunderController.click_found_picture_location(self.index, 3,
                                                                       ThunderController.share_path + "\\"
                                                                       + user_index_and_user_location_list[1][1] +
                                                                       "_column_icon.png")
                        ThunderController.random_sleep()
                        ThunderController.click_found_picture_location(self.index, 3,
                                                                       ThunderController.share_path + "\\"
                                                                       + Cracker.get_user_name_by_index(
                                                                           user_index_and_user_location_list[1][0]) +
                                                                       "_in_invite_list_icon.png")
                    else:
                        ThunderController.click_found_picture_location(self.index, 3,
                                                                       ThunderController.share_path + "\\"
                                                                       + Cracker.get_user_name_by_index(
                                                                           user_index_and_user_location_list[1][0]) +
                                                                       "_in_invite_list_icon.png")
                        ThunderController.random_sleep()
                        ThunderController.click_found_picture_location(self.index, 3,
                                                                       ThunderController.share_path + "\\"
                                                                       + user_index_and_user_location_list[0][1] +
                                                                       "_column_icon.png")
                        ThunderController.random_sleep()
                        ThunderController.click_found_picture_location(self.index, 3,
                                                                       ThunderController.share_path + "\\"
                                                                       + Cracker.get_user_name_by_index(
                                                                           user_index_and_user_location_list[0][0]) +
                                                                       "_in_invite_list_icon.png")

            ThunderController.random_sleep()
            ThunderController.click_found_picture_location(self.index, 3, ThunderController.share_path +
                                                           "/make_team_invite_comfirm_horizontal_close_button.png")
            ThunderController.random_sleep(2.0, 5.0)
            if ThunderController.find_picture(ThunderController.share_path + "/" + str(self.index) + "apk_scr.png",
                                              ThunderController.share_path +
                                              "/make_team_in_team_quick_click_error_icon.png")[0]:
                ThunderController.click_found_picture_location(self.index, 5,
                                                               ThunderController.share_path +
                                                               "/make_team_in_team_quick_click_"
                                                               "error_solution_icon.png")
            ThunderController.random_sleep(4.0, 10.0)
            if self.make_sure_team_member_is_in_team(user_index_and_user_location_list):
                break
        if task == 'mitama':
            invite_in_default_flag = False
            while True:
                if self.make_sure_team_member_is_in_team(user_index_and_user_location_list):
                    print("this is the " + str(self.mitama_battle_count + 1) + " time(s) to battle with mitama")
                    ThunderController.click_found_picture_location(self.index, 15,
                                                                   ThunderController.share_path +
                                                                   "\\make_team_begin_battle_icon.png")
                    ThunderController.random_sleep(16, 18)
                    if ThunderController.wait_picture(self.index, 15,
                                                      ThunderController.share_path +
                                                      "\\battle_info_icon.png")[0]:
                        ThunderController.random_sleep()
                        ThunderController.random_click(self.index,
                                                       *(Cracker.Global_Properties.get(
                                                           'battle_victory_page_click_area')))
                        ThunderController.random_sleep(2.5, 4)
                        ThunderController.random_click(self.index,
                                                       *(Cracker.Global_Properties.get(
                                                           'battle_victory_page_click_area')))
                        ThunderController.random_sleep(2.5, 4)
                        ThunderController.random_click(self.index,
                                                       *(Cracker.Global_Properties.get(
                                                           'battle_victory_page_click_area')))
                    if not invite_in_default_flag:
                        exist, loc, template = ThunderController.wait_picture(self.index, 3,
                                                                              ThunderController.share_path +
                                                                              "\\invite_in_default_icon.png")
                        if exist:
                            ThunderController.touch(self.index, *loc)
                            invite_in_default_flag = True
                            ThunderController.click_found_picture_location(self.index, 5, ThunderController.share_path +
                                                                           "\\invite_in_default_confirm_close_button.png")
                    self.mitama_battle_count = self.mitama_battle_count + 1
                    ThunderController.random_sleep()

    @staticmethod
    def get_user_name_by_index(index: int) -> str:
        return Cracker.Global_Properties.get('player_' + str(index))[0]


def main():
    sys.stdout = LogRecorder('./logs/' + '_'.join(re.split(r'[\\ |:]', time.ctime())) + '_log.txt')
    cracker_0_task_queue = queue.Queue()
    cracker_1_task_queue = queue.Queue()
    cracker_2_task_queue = queue.Queue()
    cracker_0_task_queue.put(['start_onmyoji'])
    cracker_1_task_queue.put(['start_onmyoji'])
    cracker_2_task_queue.put(['start_onmyoji'])
    cracker_2_task_queue.put(('invite', [(0, "cross_section"), (1, "cross_section")], 'mitama'))
    cracker_0_task_queue.put(('accept_invite', [(2, 'cross_section')], 'mitama'))
    cracker_1_task_queue.put(('accept_invite', [(2, 'cross_section')], 'mitama'))
    cracker_0 = Cracker(0, cracker_0_task_queue)
    cracker_1 = Cracker(1, cracker_1_task_queue)
    cracker_2 = Cracker(2, cracker_2_task_queue)
    cracker_0.start()
    cracker_2.start()
    cracker_1.start()


if __name__ == '__main__':
    main()
