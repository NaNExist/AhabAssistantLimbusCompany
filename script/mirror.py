import os
import time
from time import sleep

import pyautogui

from command.get_position import get_pic_position, get_pic_position_without_cap, get_all_pic_position
from command.mouse_activity import mouse_click, mouse_scroll_farthest, mouse_drag_down, mouse_click_blank, mouse_drag
from command.polymerization import wait_to_click
from my_decorator.decorator import begin_and_finish_time_log
from my_error.my_error import unableToFindTeamError
from my_log.my_log import my_log
from my_ocr.ocr import get_theme_pack, compare_the_blacklist, commom_ocr, commom_gain_text, commom_all_ocr, \
    commom_range_ocr, find_and_click_text
from script import fusion_material
from script.all_retry_question import retry
from script.back_init_menu import back_init_menu
from script.decision_event_handling import decision_event_handling
from script.in_battle import battle
from script.some_script_in_MD import get_reward_card
from script.team_formation import team_formation, select_battle_team, check_team
from os import environ

scale_factors = [0.75, 1.0, 0.5, 0.625, 1.25, 1.5]
# 存放位置
systems = {"burn": "./pic/mirror/event/shop/enhance/burn.png",
           "sinking": "./pic/mirror/event/shop/enhance/sinking.png",
           "charge": "./pic/mirror/event/shop/enhance/charge.png",
           "bleed": "./pic/mirror/event/shop/enhance/bleed.png",
           "tremor": "./pic/mirror/event/shop/enhance/tremor.png",
           "rupture": "./pic/mirror/event/shop/enhance/rupture.png",
           "poise": "./pic/mirror/event/shop/enhance/poise.png",
           "pierce": "./pic/mirror/event/shop/enhance/pierce.png",
           "slash": "./pic/mirror/event/shop/enhance/slash.png",
           "blunt": "./pic/mirror/event/shop/enhance/blunt.png"}
systems_big_pic = {"burn": "./pic/mirror/event/shop/enhance/big_burn.png",
                   "sinking": "./pic/mirror/event/shop/enhance/big_sinking.png",
                   "charge": "./pic/mirror/event/shop/enhance/big_charge.png",
                   "bleed": "./pic/mirror/event/shop/enhance/big_bleed.png",
                   "tremor": "./pic/mirror/event/shop/enhance/big_tremor.png",
                   "rupture": "./pic/mirror/event/shop/enhance/big_rupture.png",
                   "poise": "./pic/mirror/event/shop/enhance/big_poise.png",
                   "pierce": "./pic/mirror/event/shop/enhance/big_pierce.png",
                   "slash": "./pic/mirror/event/shop/enhance/big_slash.png",
                   "blunt": "./pic/mirror/event/shop/enhance/big_blunt.png"}
systems_shop = {"burn": "./pic/mirror/event/shop/shop_burn.png",
                "sinking": "./pic/mirror/event/shop/shop_sinking.png",
                "charge": "./pic/mirror/event/shop/shop_charge.png",
                "bleed": "./pic/mirror/event/shop/shop_bleed.png",
                "tremor": "./pic/mirror/event/shop/shop_tremor.png",
                "rupture": "./pic/mirror/event/shop/shop_rupture.png",
                "poise": "./pic/mirror/event/shop/shop_poise.png",
                "pierce": "./pic/mirror/event/shop/shop_pierce.png",
                "slash": "./pic/mirror/event/shop/shop_slash.png",
                "blunt": "./pic/mirror/event/shop/shop_blunt.png"}

must_to_buy_path = "./pic/mirror/event/shop/must_to_buy/"
must_to_buy = []
for root, dirs, files in os.walk(must_to_buy_path):
    for file in files:
        # 拼接完整的文件路径
        full_path = os.path.join(root, file)
        # 将文件路径添加到列表中
        must_to_buy.append(full_path)

must_to_sell_path = "./pic/mirror/event/shop/must_to_sell/"
must_to_sell = []
for root, dirs, files in os.walk(must_to_sell_path):
    for file in files:
        # 拼接完整的文件路径
        full_path = os.path.join(root, file)
        # 将文件路径添加到列表中
        must_to_sell.append(full_path)


def road_to_mir():
    back_init_menu()
    while get_pic_position("./pic/scenes/drive_features.png") is None:
        mouse_click(get_pic_position("./pic/scenes/init_drive.png"))
    mouse_click(get_pic_position("./pic/scenes/mirror_dungeons.png"))


def enter_mir(system="random", team=1, fuse_switch=False):
    all_systems = {"bleed": "./pic/mirror/select_team/bleed_ego_gift",
                   "burn": "./pic/mirror/select_team/burn_ego_gift",
                   "tremor": "./pic/mirror/select_team/tremor_ego_gift",
                   "rupture": "./pic/mirror/select_team/rupture_ego_gift",
                   "sinking": "./pic/mirror/select_team/sinking_ego_gift",
                   "poise": "./pic/mirror/select_team/poise_ego_gift",
                   "charge": "./pic/mirror/select_team/charge_ego_gift",
                   "slash": "./pic/mirror/select_team/slash_ego_gift",
                   "pierce": "./pic/mirror/select_team/pierce_ego_gift",
                   "blunt": "./pic/mirror/select_team/blunt_ego_gift"}
    precision = 0.8
    while get_pic_position("./pic/mirror/enter_mirror_button.png", precision=precision) is None:
        if precision > 0.7:
            precision -= 0.01
    mouse_click(get_pic_position("./pic/mirror/enter_mirror_button.png", precision=precision))
    if enter_normal_mir := get_pic_position("./pic/mirror/enter_normal_mirror.png"):
        mouse_click(enter_normal_mir)
        sleep(2)
        chance_to_select_team = 5
        while not select_battle_team(team):
            chance_to_select_team -= 1
            if chance_to_select_team < 0:
                my_log("error", "无法寻得队伍")
                raise unableToFindTeamError("无法寻得队伍，请检查队伍名称是否为默认名称")
        wait_to_click("./pic/mirror/select_team_confirm.png")

        # mirror5
        while (get_pic_position("./pic/mirror/mirror5/grace_of_stars_passive.png") is None
               and get_pic_position("./pic/mirror/starlight.png", 0.9) is None):
            retry()
        if fuse_switch is False:
            mouse_click(get_pic_position("./pic/mirror/mirror5/20_stars.png"))
            mouse_click(get_pic_position("./pic/mirror/mirror5/40_stars.png"))
            if stars_button := get_pic_position("./pic/mirror/mirror5/60_stars.png"):
                mouse_click(stars_button)
            if stars_button := get_pic_position("./pic/mirror/mirror5/40_stars_2.png"):
                mouse_click(stars_button)
            if stars_button := get_pic_position("./pic/mirror/mirror5/20_stars_2.png"):
                mouse_click(stars_button)
            if stars_button := get_pic_position("./pic/mirror/mirror5/10_stars.png"):
                mouse_click(stars_button)
        else:
            # 根据B站UP主 绅士丶蚂蚱 《镜牢5完全攻略》制定
            mouse_click(get_pic_position("./pic/mirror/mirror5/20_stars.png"))
            mouse_click(get_pic_position("./pic/mirror/mirror5/20_stars_2.png"))
            mouse_click(get_pic_position("./pic/mirror/mirror5/10_stars.png"))
            if stars_button := get_pic_position("./pic/mirror/mirror5/60_stars.png"):
                mouse_click(stars_button)
            if stars_button := get_pic_position("./pic/mirror/mirror5/30_stars.png"):
                mouse_click(stars_button)
            if stars_button := get_pic_position("./pic/mirror/mirror5/30_stars_2.png"):
                mouse_click(stars_button)
            if stars_button := get_pic_position("./pic/mirror/mirror5/10_stars_2.png"):
                mouse_click(stars_button)
        mouse_click(get_pic_position("./pic/mirror/mirror5/select_stars_enter.png"))
        mouse_click(get_pic_position("./pic/mirror/mirror5/select_stars_confirm.png"))

        while get_pic_position("./pic/mirror/select_init_ego_gift.png") is None:
            retry()

        if system == "slash" or system == "pierce" or system == "blunt":
            slash_button = get_pic_position("./pic/mirror/select_team/slash_ego_gift.png")
            mouse_drag(slash_button, time=0.2, x=0, y=-200)

        mouse_click(get_pic_position(sys := all_systems[system] + '.png'))
        mouse_click(get_pic_position(sys := all_systems[system] + '_1.png'))
        mouse_click(get_pic_position(sys := all_systems[system] + '_2.png'))
        mouse_click(get_pic_position(sys := all_systems[system] + '_3.png'))
        mouse_click(get_pic_position("./pic/mirror/select_team/select_ego_gift.png"))
        while get_pic_position("./pic/mirror/ego_gift_get.png") is None:
            retry()
        while ego_gift_get_confirm := get_pic_position("./pic/mirror/ego_gift_get_confirm.png"):
            mouse_click(ego_gift_get_confirm)
            sleep(1)

    elif resume := get_pic_position("./pic/mirror/resume_mir.png"):
        mouse_click(resume)


@begin_and_finish_time_log(task_name="选择镜牢主题包")
# 选择镜牢主题包
def select_theme_pack():
    fail_count = 0
    count_max = 60
    while get_pic_position("./pic/mirror/theme_pack_features.png") is None:
        sleep(1)
        fail_count += 1
        if fail_count > count_max:
            msg="镜牢主题包获取失败，超出最大尝试次数"
            my_log("debug",msg)
            return 0
    if hard_button := get_pic_position("./pic/mirror/mirror5/hard_theme_pack.png"):
        mouse_click(hard_button)
    if get_pic_position("./pic/mirror/theme_pack_features.png"):
        sleep(4)
        all_pic_byte_stream = get_theme_pack("./pic/mirror/theme_pack_features.png")
        for pic in all_pic_byte_stream:
            if compare_the_blacklist(pic[0]):
                mouse_drag_down(pic[1])
                return 0
    if refresh_button := get_pic_position("./pic/mirror/refresh_theme_pack.png"):
        mouse_click(refresh_button)
    if get_pic_position("./pic/mirror/theme_pack_features.png"):
        sleep(4)
        all_pic_byte_stream = get_theme_pack("./pic/mirror/theme_pack_features.png")
        for pic in all_pic_byte_stream:
            if compare_the_blacklist(pic[0]):
                mouse_drag_down(pic[1])
                sleep(3)
                return 0
    mouse_drag_down(get_pic_position("./pic/mirror/theme_pack_features.png"))
    sleep(3)


@begin_and_finish_time_log(task_name="镜牢寻路")
def search_road():
    for _ in range(3):
        if search_road_default_distanc():
            return True
    for _ in range(3):
        if search_road_farthest_distanc():
            return True
    if search_road_farthest_distanc() is False:
        # 如果寻路失败，退出镜牢重进
        if button := get_pic_position("./pic/mirror/setting.png"):
            mouse_click(button)
        if button := get_pic_position("./pic/mirror/to_window.png"):
            mouse_click(button)
        if button := get_pic_position("./pic/mirror/to_window_confirm.png"):
            mouse_click(button)
        road_to_mir()
        enter_mir()


# 在默认缩放情况下，进行镜牢寻路
def search_road_default_distanc():
    scale = 0
    if environ.get('window_size'):
        scale = int(environ.get('window_size'))
    three_roads = [[500 * scale_factors[scale], 0],
                   [500 * scale_factors[scale], -400 * scale_factors[scale]],
                   [500 * scale_factors[scale], 450 * scale_factors[scale]]]
    if bus_position := get_pic_position("./pic/mirror/mybus_default_distanc.png"):
        for road in three_roads:
            road[0] += bus_position[0]
            road[1] += bus_position[1]
            if 0 < road[0] < 2560 * scale_factors[scale] and 0 < road[1] < 1440 * scale_factors[scale]:
                mouse_click(road)
                sleep(0.5)
                if enter := get_pic_position("./pic/mirror/enter_room.png"):
                    mouse_click(enter)
                    return True
        mouse_click(bus_position)
        if enter := get_pic_position("./pic/mirror/enter_room.png"):
            mouse_click(enter)
            return True
    else:
        return False


# 如果默认缩放无法镜牢寻路，进行滚轮缩放后继续寻路
def search_road_farthest_distanc():
    scale = 0
    if environ.get('window_size'):
        scale = int(environ.get('window_size'))
    mouse_click_blank()
    mouse_scroll_farthest()
    three_roads = [[250 * scale_factors[scale], -200 * scale_factors[scale]],
                   [250 * scale_factors[scale], 0],
                   [250 * scale_factors[scale], 225 * scale_factors[scale]]]
    if bus_position := get_pic_position("./pic/mirror/mybus_maximum_distance.png"):
        for road in three_roads:
            road[0] += bus_position[0]
            road[1] += bus_position[1]
            if 0 < road[0] < 2560 * scale_factors[scale] and 0 < road[1] < 1440 * scale_factors[scale]:
                mouse_click(road)
                if enter := get_pic_position("./pic/mirror/enter_room.png"):
                    mouse_click(enter)
                    return True
        return False
    else:
        return False


# 为EGO饰品升级
def ego_gift_to_power_up():
    while ego_gift_power_up := get_pic_position("./pic/mirror/event/shop/enhance/ego_gift_power_up.png"):
        mouse_click(ego_gift_power_up)
        sleep(0.2)
        if power_up_confirm := get_pic_position("./pic/mirror/event/shop/enhance/power_up_confirm.png"):
            mouse_click(power_up_confirm)
            if get_pic_position("./pic/mirror/event/shop/enhance/power_up_confirm.png"):
                mouse_click(get_pic_position("./pic/mirror/event/shop/enhance/power_up_cancel.png"))
                return False
        elif get_pic_position_without_cap("./pic/mirror/event/shop/enhance/cannot_enhance.png"):
            return True
        else:
            return True


def buy_gifts(system):
    # 购买必买项（回血饰品）
    for commodity in must_to_buy:
        if item := get_pic_position(commodity):
            mouse_click(item)
            mouse_click(get_pic_position("./pic/mirror/event/shop/purchase.png"))
            while ego_gift_get_confirm := get_pic_position("./pic/mirror/ego_gift_get_confirm.png"):
                mouse_click(ego_gift_get_confirm)
    # 购买体系饰品
    if gifts := get_all_pic_position(systems_shop[system]):
        for gift in gifts:
            mouse_click(gift)
            if get_pic_position("./pic/mirror/event/shop/purchase.png"):
                mouse_click(get_pic_position("./pic/mirror/event/shop/purchase.png"))
                while ego_gift_get_confirm := get_pic_position("./pic/mirror/ego_gift_get_confirm.png"):
                    mouse_click(ego_gift_get_confirm)
            if get_pic_position("./pic/mirror/event/shop/ego_info.png"):
                mouse_click_blank()


def fuse_useless_gifts(shop_sell_list):
    """合成无用饰品"""

    def processing_coordinates(my_gift_list, scale=0):
        """将列表从左上到右下排序，然后去重"""
        # 排序
        sorted_list = sorted(my_gift_list, key=lambda x: (x[1], x[0]))

        # 获取分辨率
        if environ.get('window_size'):
            scale = int(environ.get('window_size'))

        # 去除重复坐标
        unique_list = []
        for coord in sorted_list:
            if not any(abs(coord[0] - x[0]) <= 40 * scale_factors[scale] and
                       abs(coord[1] - x[1]) <= 40 * scale_factors[scale] for x in unique_list):
                unique_list.append(coord)

        return unique_list

    block = False
    while True:
        gift_list = []

        # 获取无用饰品列表
        for commodity in must_to_sell:
            item = get_all_pic_position(commodity, 0.85)
            if item:
                gift_list.extend(list(g) for g in item)
        for sell_system in shop_sell_list:
            path = "./pic/mirror/event/shop/enhance/"
            my_sell_system = path + sell_system + ".png"
            gift = get_all_pic_position(my_sell_system)
            if gift:
                gift_list.extend(list(g) for g in gift)

        # 选择至多3样无用饰品
        my_list = processing_coordinates(gift_list)
        if len(my_list) <= 1:
            msg = f"饰品放弃列表数量不足，结束合成"
            my_log("debug", msg)
        else:
            for sequence in range(3):
                try:
                    mouse_click(my_list[sequence])
                except IndexError:
                    msg = f"饰品放弃列表已经没有第{sequence + 1}项了"
                    my_log("debug", msg)

        wait_to_click("./pic/mirror/event/shop/fuse_ego_gift_caption.png")
        mouse_click(get_pic_position("./pic/mirror/event/shop/fuse_check.png"))
        sleep(0.5)
        if get_pic_position("./pic/mirror/event/shop/fuse_recognize.png") and get_pic_position(
                "./pic/mirror/event/shop/fuse_confirm.png"):
            mouse_click(get_pic_position("./pic/mirror/event/shop/fuse_confirm.png"))
            wait_to_click("./pic/mirror/ego_gift_get_confirm.png")
        else:
            list_block = get_pic_position("./pic/mirror/event/shop/gifts_list_block.png")
            if list_block is not None and block is False:
                mouse_drag(list_block, time=1, y=500)
                block = True
                continue
            mouse_click_blank()
            break


def fuse_system_gifts(system, times):
    """合成体系饰品"""
    # 第几次合成
    i = times - 1

    # 获取合成公式
    system_gifts = fusion_material[system]
    if len(system_gifts) == 2:
        my_fuse_system_gifts = [system_gifts[0], system_gifts[1]]
    else:
        my_fuse_system_gifts = [system_gifts, []]
    # 标记合成可行性
    fusion = True
    fusion_position = {}
    # 如果无第二合成公式，返回
    if len(my_fuse_system_gifts[i]) == 0:
        return

    # 如果找到合成素材，记录位置后点击
    for select_gift in my_fuse_system_gifts[i]:
        pos = get_pic_position(f"./pic/mirror/event/shop/fusion_material/{select_gift}")
        if pos is None:
            if select_gift not in fusion_position:
                fusion_position[select_gift] = pos
        else:
            if select_gift in fusion_position:
                if fusion_position[select_gift] is None:
                    fusion_position[select_gift] = pos
            else:
                fusion_position[select_gift] = pos
            mouse_click(pos)
            wait_to_click("./pic/mirror/event/shop/fuse_ego_gift_caption.png")

    list_block = get_pic_position("./pic/mirror/event/shop/gifts_list_block.png")
    block = False
    if list_block is not None:
        block = True
        mouse_drag(list_block, time=1, y=500)

    if block:
        # 如果找到合成素材，如果是无记录位置的，记录位置后点击
        for select_gift in my_fuse_system_gifts[i]:
            pos = get_pic_position(f"./pic/mirror/event/shop/fusion_material/{select_gift}")
            if pos is not None:
                if select_gift in fusion_position:
                    if fusion_position[select_gift] is None:
                        fusion_position[select_gift] = pos
                        mouse_click(pos)
                        wait_to_click("./pic/mirror/event/shop/fuse_ego_gift_caption.png")
                else:
                    fusion_position[select_gift] = pos
                    mouse_click(pos)
                    wait_to_click("./pic/mirror/event/shop/fuse_ego_gift_caption.png")

    for name in (my_fuse_system_gifts[i]):
        if fusion_position[name] is None:
            fusion = False

    if fusion:
        mouse_click(get_pic_position("./pic/mirror/event/shop/fuse_check.png"))
        sleep(0.5)
        if get_pic_position("./pic/mirror/event/shop/fuse_recognize.png") and get_pic_position(
                "./pic/mirror/event/shop/fuse_confirm.png"):
            mouse_click(get_pic_position("./pic/mirror/event/shop/fuse_confirm.png"))
            wait_to_click("./pic/mirror/event/shop/fuse_ego_gift_caption.png")
            msg = f"成功合成{system}体系饰品{i+1}号"
            my_log("debug", msg)

    mouse_click_blank(times=2)


def sell_gifts(shop_sell_list):
    for sell_system in shop_sell_list:
        path = "./pic/mirror/event/shop/enhance/"
        my_sell_system = path + sell_system + ".png"
        while gift := get_pic_position(my_sell_system):
            mouse_click(gift)
            mouse_click(get_pic_position("./pic/mirror/event/shop/sell_button.png"))
            mouse_click(get_pic_position("./pic/mirror/event/shop/sell_confirm.png"))
    for commodity in must_to_sell:
        if item := get_pic_position(commodity):
            mouse_click(item)
            mouse_click(get_pic_position("./pic/mirror/event/shop/sell_button.png"))
            mouse_click(get_pic_position("./pic/mirror/event/shop/sell_confirm.png"))
            sleep(1)


def fuse_gift(shop_sell_list, system):
    fuse_times = 3
    if system not in fusion_material:
        fuse_times = 1
    for i in range(fuse_times):
        if fuse_gifts_button := get_pic_position("./pic/mirror/event/shop/fuse_gifts.png"):
            mouse_click(fuse_gifts_button)
            wait_to_click("./pic/mirror/event/shop/fuse_gifts_select_system.png")
            mouse_click(get_pic_position(f"./pic/mirror/mirror5/shop/keyword_{system}.png"))
            sleep(0.2)
            mouse_click(get_pic_position("./pic/mirror/event/shop/fusion_keyword_selection_confirm.png"))
            if i == 0:
                fuse_useless_gifts(shop_sell_list)
            else:
                fuse_system_gifts(system, i)


@begin_and_finish_time_log(task_name="镜牢商店")
# 在商店的处理
def in_shop(system, shop_sell_list, store_floors, fuse_switch):
    # 全体治疗
    if heal_sinner := get_pic_position("./pic/mirror/event/shop/heal_sinner.png"):
        mouse_click(heal_sinner)
        sleep(0.5)
        if heal_sinner_button := get_pic_position("./pic/mirror/event/shop/heal_sinner_button.png"):
            mouse_click(heal_sinner_button)
            sleep(1)
            while get_pic_position("./pic/event/return.png") is None:
                retry()
            if return_button := get_pic_position("./pic/event/return.png"):
                mouse_click(return_button)

    # 出售无用饰品
    if fuse_switch is False:
        if sell_gifts_button := get_pic_position("./pic/mirror/event/shop/sell_gifts.png"):
            mouse_click(sell_gifts_button)
            sell_gifts(shop_sell_list)

            if sell_list_block := get_pic_position("./pic/mirror/event/shop/gifts_list_block.png"):
                mouse_drag(sell_list_block, time=1, y=500)
                sell_gifts(shop_sell_list)

            while get_pic_position("./pic/mirror/event/shop/sell_close_button.png") is None:
                retry()
            mouse_click(get_pic_position("./pic/mirror/event/shop/sell_close_button.png"))

    # 购买ego饰品
    buy_gifts(system)
    if store_floors >= 4 or (fuse_switch and store_floors <= 2):
        if store_floors <= 2:
            for _ in range(2):
                if refresh_shop := get_pic_position("./pic/mirror/mirror5/shop/keyword_refresh.png"):
                    mouse_click(refresh_shop)
                    sleep(0.5)
                    mouse_click(get_pic_position(f"./pic/mirror/mirror5/shop/keyword_{system}.png"))
                    mouse_click(get_pic_position("./pic/mirror/mirror5/shop/refresh_shop_confirm.png"))
                    sleep(1)
                    buy_gifts(system)
        else:
            while refresh_shop := get_pic_position("./pic/mirror/mirror5/shop/keyword_refresh.png"):
                mouse_click(refresh_shop)
                sleep(0.5)
                mouse_click(get_pic_position(f"./pic/mirror/mirror5/shop/keyword_{system}.png"))
                mouse_click(get_pic_position("./pic/mirror/mirror5/shop/refresh_shop_confirm.png"))
                sleep(1)
                buy_gifts(system)

    mouse_click_blank(times=3)

    if fuse_switch:
        # 合成饰品
        fuse_gift(shop_sell_list, system)

    mouse_click_blank(times=3)

    # 升级体系ego饰品
    if enhance_gifts_button := get_pic_position("./pic/mirror/event/shop/enhance_gifts.png"):
        mouse_click(enhance_gifts_button)
        if get_pic_position(systems_big_pic[system]):
            ego_gift_to_power_up()
        if gifts := get_all_pic_position(systems[system]):
            for gift in gifts:
                mouse_click(gift)
                if ego_gift_to_power_up() is False:
                    break
        if sell_list_block := get_pic_position("./pic/mirror/event/shop/gifts_list_block.png"):
            mouse_drag(sell_list_block, time=1, y=500)
            if gifts := get_all_pic_position(systems[system]):
                for gift in gifts:
                    mouse_click(gift)
                    if ego_gift_to_power_up() is False:
                        break
        if ego_gift_power_up_close := get_pic_position(
                "./pic/mirror/event/shop/enhance/ego_gift_power_up_close.png"):
            mouse_click(ego_gift_power_up_close)

    mouse_click_blank(times=3)
    # 离开商店
    precision = 0.8
    while get_pic_position("./pic/mirror/event/shop/leave_shop_confirm.png") is None:
        mouse_click(get_pic_position("./pic/mirror/event/shop/leave_shop.png", precision=precision))
        if precision > 0.7:
            precision -= 0.01
    mouse_click(get_pic_position("./pic/mirror/event/shop/leave_shop_confirm.png"))


# 输出时间统计
def to_log_with_time(msg, elapsed_time):
    # 将总秒数转换为小时、分钟和秒
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    time_string = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    my_log("info", f"{msg} 总耗时:{time_string}")


# 一次镜本流程
def execute_a_mirror(sinner_team, which_team, shop_sell_list, fuse_switch, system="burn"):
    print(shop_sell_list)
    # 计时开始
    start_time = time.time()

    pick_total_time = 0
    find_road_total_time = 0
    battle_total_time = 0
    shop_total_time = 0
    event_total_time = 0
    acquire_total_time = 0

    # 记录商店楼层
    store_floors = 1

    if get_pic_position("./pic/teams/to_battle.png"):
        mouse_click(get_pic_position("./pic/scenes/the_back_button.png"))
    if get_pic_position("./pic/scenes/road_in_mirror.png") is None and get_pic_position(
            "./pic/mirror/theme_pack_features.png") is None:
        road_to_mir()
        enter_mir(system, which_team, fuse_switch)
    # 判断是否首次进入战斗，如果是则重新配队
    first_battle = True
    # 未到达奖励页不会停止
    while get_pic_position("./pic/mirror/total_progress.png") is None:
        # 选择楼层主题包的情况
        if get_pic_position("./pic/scenes/mirror_select_theme_pack.png"):
            pick_total_time += select_theme_pack()
            continue

        # 在镜牢中寻路
        if get_pic_position("./pic/scenes/road_in_mirror.png"):
            find_road_total_time += search_road()

        # 战斗配队的情况
        if get_pic_position("./pic/teams/announcer.png"):
            # 如果第一次启动脚本，还没进行编队，就先编队
            if first_battle:
                team_formation(sinner_team)
                first_battle = False
            # 检测罪人幸存人数是否少于10人
            if not (get_pic_position("./pic/teams/12_sinner_live.png", 0.9) or
                    get_pic_position("./pic/teams/11_sinner_live.png", 0.9) or
                    get_pic_position("./pic/teams/10_sinner_live.png", 0.9)):
                continue_mirror = check_team()
                # 如果还有至少5人能战斗就继续，不然就退出重开
                if continue_mirror is False and first_battle is False:
                    return False
            mouse_click(get_pic_position("./pic/teams/to_battle.png"))
            sleep(0.5)

            if get_pic_position("./pic/teams/select_none.png"):
                mouse_click_blank()
                first_battle = True
            else:
                battle_total_time += battle()

            sleep(2)
            if get_pic_position("./pic/mirror/select_encounter_reward_card.png"):
                sleep(1)  # 防止过快点击导致脚本卡死
                get_reward_card()
            if get_pic_position("./pic/mirror/leave_reward_card.png"):
                mouse_click(get_pic_position("./pic/mirror/leave_reward_card_cancel.png"))

            continue

        event_start_time = time.time()
        event_trigger = False

        # 遇到有SKIP的情况
        while skip_button := get_pic_position("./pic/mirror/event/skip.png"):
            # 如果存在SKIP按钮，多次点击
            mouse_click(skip_button, 6)

            # 触发事件
            event_trigger = True

            # 针对不同事件进行处理，优先选需要判定的
            if gain_ego := get_pic_position("./pic/mirror/event/advantage_check.png"):
                mouse_click(gain_ego)
            elif gain_ego := get_pic_position("./pic/mirror/event/selet_to_gain_ego.png"):
                mouse_click(gain_ego)
            elif gain_ego := get_pic_position("./pic/mirror/event/gain_a_ego_depending_on_result.png"):
                mouse_click(gain_ego)
            elif get_pic_position("./pic/mirror/event/random_to_choose_event.png") and \
                    get_pic_position("./pic/mirror/event/choices.png"):
                mouse_click(get_pic_position("./pic/mirror/event/random_to_choose_event.png"))

            # 如果是右下角的红色按钮
            if proceed_button := get_pic_position("./pic/mirror/event/proceed.png"):
                mouse_click(proceed_button)
            if continue_button := get_pic_position("./pic/mirror/event/continue.png"):
                mouse_click(continue_button)

            # 如果遇到判定事件
            if get_pic_position("./pic/event/perform_the_check_features_1.png") and get_pic_position(
                    "./pic/event/perform_the_check_features_2.png"):
                decision_event_handling()

            # 如果事件结束，得到饰品
            if get_pic_position("./pic/mirror/ego_gift_get.png"):
                if ego_gift_get_confirm := get_pic_position("./pic/mirror/ego_gift_get_confirm.png"):
                    mouse_click(ego_gift_get_confirm)

            retry()

        if event_trigger:
            event_end_time = time.time()
            event_elapsed_time = event_end_time - event_start_time
            event_total_time += event_elapsed_time
            # 将总秒数转换为小时、分钟和秒
            hours, remainder = divmod(event_elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_string = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
            msg = f"此次事件共花费{time_string}"
            my_log("debug", msg)

        # 如果遇到获取ego饰品的情况
        if acquire_ego_gift := get_pic_position("./pic/mirror/acquire_ego_gift.png"):

            acquire_start_time = time.time()

            # 还可以加些判断！！！
            if get_pic_position("./pic/mirror/black_list/white_gossypium.png"):
                mouse_click(get_pic_position("./pic/mirror/refuse_gift.png"))
            else:
                get_gift_path = "./pic/mirror/acquire_ego_gift/"
                select_path = get_gift_path + system + ".png"
                if select_gift := get_pic_position(select_path):
                    mouse_click(select_gift)
                else:
                    mouse_click(acquire_ego_gift)
                if select_ego_gift := get_pic_position("./pic/mirror/select_team/select_ego_gift.png"):
                    mouse_click(select_ego_gift)
                    if ego_gift_get_confirm := get_pic_position("./pic/mirror/ego_gift_get_confirm.png"):
                        mouse_click(ego_gift_get_confirm)

            acquire_end_time = time.time()
            acquire_elapsed_time = acquire_end_time - acquire_start_time
            acquire_total_time += acquire_elapsed_time
            # 将总秒数转换为小时、分钟和秒
            hours, remainder = divmod(acquire_elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_string = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
            msg = f"此次获取ego饰品共花费{time_string}"
            my_log("debug", msg)

            continue

        # 防卡死
        if ego_gift_get_confirm := get_pic_position("./pic/mirror/ego_gift_get_confirm.png"):
            mouse_click(ego_gift_get_confirm)
        retry()

        # 商店事件
        if get_pic_position("./pic/mirror/event/shop/shop_features_1.png") and \
                get_pic_position("./pic/mirror/event/shop/shop_features_2.png"):
            shop_total_time += in_shop(system, shop_sell_list, store_floors, fuse_switch)
            store_floors += 1

            continue

        if get_pic_position("./pic/mirror/select_encounter_reward_card.png"):
            sleep(1)  # 防止过快点击导致脚本卡死
            get_reward_card()
        if get_pic_position("./pic/mirror/leave_reward_card.png"):
            mouse_click(get_pic_position("./pic/mirror/leave_reward_card_cancel.png"))

        if get_pic_position("./pic/mirror/event/select_event_effect.png"):
            mouse_click(get_pic_position("./pic/mirror/event/event_effect_button.png"))
            mouse_click(get_pic_position("./pic/mirror/event/select_event_effect_confirm.png"))

        if enter := get_pic_position("./pic/mirror/enter_room.png"):
            mouse_click(enter)
        if enter_mir_confirm := get_pic_position("./pic/mirror/enter_mir_confirm.png"):
            mouse_click(enter_mir_confirm)

        # 如果战斗退出过快导致没有点击结算按钮
        if get_pic_position("./pic/mirror/victory.png"):
            mouse_click(get_pic_position("./pic/mirror/victory_confirm.png"))
    msg = f"开始进行镜牢奖励领取"
    my_log("info", msg)
    if claim_rewards := get_pic_position("./pic/mirror/claim_rewards.png"):
        mouse_click(claim_rewards)
        sleep(1)
    mouse_click(get_pic_position("./pic/mirror/claim.png"))
    mouse_click(get_pic_position("./pic/mirror/claim_confirm.png"))
    while get_pic_position("./pic/mirror/claim_last_confirm.png") is None:
        retry()
    if claim_last_confirm := get_pic_position("./pic/mirror/claim_last_confirm.png"):
        mouse_click(claim_last_confirm)
        sleep(1)
    if claim_last_confirm := get_pic_position("./pic/mirror/claim_last_confirm.png"):
        mouse_click(claim_last_confirm)

    # 计时结束
    end_time = time.time()
    elapsed_time = end_time - start_time

    # 输出战斗总时间
    msg = f"此次镜牢在战斗"
    to_log_with_time(msg, battle_total_time)

    # 输出事件总时间
    msg = f"此次镜牢在事件"
    to_log_with_time(msg, event_total_time)

    # 输出商店总时间
    msg = f"此次镜牢中在商店"
    to_log_with_time(msg, shop_total_time)

    # 输出寻路总时间
    msg = f"此次镜牢中在寻路"
    to_log_with_time(msg, find_road_total_time)

    # debug输出时间
    my_log("debug",
           f"战斗时间:{battle_total_time} 事件时间:{event_total_time} 商店时间:{shop_total_time} 寻路时间:{find_road_total_time} 总时间:{elapsed_time}")

    # 输出镜牢总时间
    msg = f"此次镜牢使用{system}体系队伍"
    to_log_with_time(msg, elapsed_time)

    return True
