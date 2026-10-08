# -*- coding: utf-8 -*-
"""
舟舟算价助手 - 安卓版
功能：材质算价、快捷备注、邀请下单
"""

import re
import json
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.utils import get_color_from_hex

# ========== 版本号 ==========
VERSION = "1.0.0"

# ========== 全局设置 ==========
DISCOUNT = 0.9  # 默认九折
MIN_PRICE = 20  # 最低价20元

# ========== 材质数据（内置） ==========
MATERIALS = [
    {"name": "硅藻泥2.5mm（G2）", "price": 65, "max_width": 0, "weight": 2.0},
    {"name": "硅藻泥3.5mm（G3）", "price": 75, "max_width": 0, "weight": 2.0},
    {"name": "硅藻泥3.5mm（G3）（凯彼得、丹逸）", "price": 75, "max_width": 0, "weight": 2.0},
    {"name": "皮革pvc1mm（P1）", "price": 45, "max_width": 0, "weight": 1.8},
    {"name": "皮革pvc2mm（P2）（凯彼得）", "price": 55, "max_width": 0, "weight": 1.8},
    {"name": "皮革pvc2mm（P2）（丹逸）", "price": 55, "max_width": 0, "weight": 1.8},
    {"name": "皮革pvc3mm（P3）", "price": 65, "max_width": 0, "weight": 1.1},
    {"name": "皮革pvc5mm（P5）", "price": 85, "max_width": 0, "weight": 1.7},
    {"name": "皮革pvc5mm（P5）（凯彼得）", "price": 85, "max_width": 0, "weight": 1.7},
    {"name": "皮革pvc5mm（P5）（丹逸）", "price": 85, "max_width": 0, "weight": 1.7},
    {"name": "亚麻1mm（Y1）", "price": 55, "max_width": 0, "weight": 1.5},
    {"name": "亚麻2mm（Y2）", "price": 65, "max_width": 0, "weight": 1.6},
    {"name": "亚麻3mm（Y3）", "price": 75, "max_width": 0, "weight": 1.7},
    {"name": "麻布1mm（M1）", "price": 50, "max_width": 0, "weight": 1.4},
    {"name": "麻布2mm（M2）", "price": 60, "max_width": 0, "weight": 1.5},
    {"name": "麻布3mm（M3）", "price": 70, "max_width": 0, "weight": 1.6},
    {"name": "雪尼尔1mm（X1）", "price": 60, "max_width": 0, "weight": 1.8},
    {"name": "雪尼尔2mm（X2）", "price": 70, "max_width": 0, "weight": 1.9},
    {"name": "雪尼尔3mm（X3）", "price": 80, "max_width": 0, "weight": 2.0},
    {"name": "涤纶1mm（D1）", "price": 40, "max_width": 0, "weight": 1.2},
    {"name": "涤纶2mm（D2）", "price": 50, "max_width": 0, "weight": 1.3},
    {"name": "涤纶3mm（D3）", "price": 60, "max_width": 0, "weight": 1.4},
    {"name": "丙纶1mm（B1）", "price": 35, "max_width": 0, "weight": 1.1},
    {"name": "丙纶2mm（B2）", "price": 45, "max_width": 0, "weight": 1.2},
    {"name": "丙纶3mm（B3）", "price": 55, "max_width": 0, "weight": 1.3},
    {"name": "尼龙1mm（N1）", "price": 55, "max_width": 0, "weight": 1.3},
    {"name": "尼龙2mm（N2）", "price": 65, "max_width": 0, "weight": 1.4},
    {"name": "尼龙3mm（N3）", "price": 75, "max_width": 0, "weight": 1.5},
    {"name": "橡胶1mm（XJ1）", "price": 30, "max_width": 0, "weight": 2.5},
    {"name": "橡胶2mm（XJ2）", "price": 40, "max_width": 0, "weight": 3.0},
    {"name": "橡胶3mm（XJ3）", "price": 50, "max_width": 0, "weight": 3.5},
    {"name": "硅胶1mm（GJ1）", "price": 45, "max_width": 0, "weight": 1.8},
    {"name": "硅胶2mm（GJ2）", "price": 55, "max_width": 0, "weight": 2.0},
    {"name": "硅胶3mm（GJ3）", "price": 65, "max_width": 0, "weight": 2.2},
    {"name": "海绵5mm（HM5）", "price": 25, "max_width": 0, "weight": 0.5},
    {"name": "海绵10mm（HM10）", "price": 35, "max_width": 0, "weight": 0.8},
    {"name": "EVA2mm（EVA2）", "price": 20, "max_width": 0, "weight": 0.6},
    {"name": "EVA3mm（EVA3）", "price": 28, "max_width": 0, "weight": 0.8},
]

# ========== 快捷备注默认按钮 ==========
DEFAULT_NOTE_BUTTONS = [
    {"name": "横版", "template": "#{small}x{large}cm横版*1块"},
    {"name": "竖版", "template": "#{large}x{small}cm竖版*1块"},
    {"name": "L型", "template": "【L型】#{small}x{large}x{narrow}cm【{corner}】*1块"},
    {"name": "L型异型", "template": "【L型异形】#{small}x{large}cm【{corner}】*1块"},
    {"name": "换图", "template": "【换图】"},
    {"name": "改图", "template": "【改图】"},
]


# ========== 单位智能转换 ==========
def parse_dimension(text):
    """解析尺寸文本，返回(长m, 宽m, 原始描述)"""
    text = text.strip()
    # 提取所有数字和单位
    pattern = r'(\d+\.?\d*)\s*(m|cm|mm|米|厘米|毫米)?'
    matches = re.findall(pattern, text, re.IGNORECASE)

    numbers = []
    for value_str, unit in matches:
        if not value_str:
            continue
        value = float(value_str)
        unit = unit.lower() if unit else ''

        # 带单位的直接转换
        if unit in ['m', '米']:
            meters = value
        elif unit in ['cm', '厘米']:
            meters = value / 100.0
        elif unit in ['mm', '毫米']:
            meters = value / 1000.0
        else:
            # 无单位：<10按m，>=10按cm
            if value < 10:
                meters = value
            else:
                meters = value / 100.0
        numbers.append(meters)

    if len(numbers) < 2:
        return None, None, "无法识别尺寸，请输入如 100x120 或 1m x 1.2m"

    length = numbers[0]
    width = numbers[1]
    desc = f"识别到：{length*100:.0f}cm x {width*100:.0f}cm = {length:.2f}m x {width:.2f}m"
    return length, width, desc


# ========== 撩尺计算 ==========
def liao_chi(short_edge, material_name=""):
    """撩尺：只撩短边，长边不变"""
    # 凯彼得材质不撩尺
    if "凯彼得" in material_name:
        return short_edge, "凯彼得材质，无需撩尺"

    short_cm = short_edge * 100  # 转成cm

    # <40按40
    if short_cm < 40:
        result = 40
        reason = f"短边{short_cm:.0f}cm<40，按40算"
    # <=200按20间隔向上取整
    elif short_cm <= 200:
        result = ((int(short_cm) + 19) // 20) * 20
        if result == int(short_cm):
            reason = f"短边{short_cm:.0f}cm正好是整数，无需撩尺"
        else:
            reason = f"短边{short_cm:.0f}cm，撩尺到{result}cm（20间隔）"
    # >200按50间隔
    else:
        result = ((int(short_cm) + 49) // 50) * 50
        reason = f"短边{short_cm:.0f}cm，撩尺到{result}cm（50间隔）"

    return result / 100.0, reason


# ========== 算价核心 ==========
def calculate_price(length, width, material, discount=DISCOUNT):
    """计算价格，返回(原价, 折扣价, 撩尺后长, 撩尺后宽, 面积, 重量, 说明)"""
    # 确定长短边
    if length >= width:
        long_edge = length
        short_edge = width
    else:
        long_edge = width
        short_edge = length

    # 撩尺
    liao_short, liao_reason = liao_chi(short_edge, material["name"])

    # 撩尺后的尺寸
    final_long = long_edge
    final_short = liao_short
    area = final_long * final_short

    # 算原价
    original_price = area * material["price"]

    # 最低价20元
    if original_price < MIN_PRICE:
        original_price = MIN_PRICE
        price_reason = f"原价{area * material['price']:.2f}元<20，按最低价20元算"
    else:
        price_reason = f"面积{area:.2f}㎡ x 单价{material['price']}元/㎡ = {original_price:.2f}元"

    # 折扣价
    discount_price = original_price * discount
    if discount_price < MIN_PRICE:
        discount_price = MIN_PRICE

    # 重量（按原尺寸面积，不按撩尺后）
    weight = (length * width) * material.get("weight", 0)

    return (round(original_price, 2), round(discount_price, 2),
            round(final_long, 2), round(final_short, 2),
            round(area, 2), round(weight, 2),
            f"{liao_reason}\n{price_reason}")


# ========== 快捷备注话术生成 ==========
def generate_note(button_name, input_text):
    """根据按钮和输入生成备注话术"""
    # 提取数字
    numbers = []
    for match in re.finditer(r'(\d+\.?\d*)', input_text):
        numbers.append(float(match.group(1)))

    if len(numbers) < 2:
        return "请输入至少两个尺寸，如 100 200"

    # 识别大数小数
    sorted_nums = sorted(numbers)
    small = sorted_nums[0]
    large = sorted_nums[-1]

    # 三个数时，最小的是窄边
    narrow = None
    corner = "拐角方向"
    if len(numbers) >= 3:
        narrow = sorted_nums[0]
        small = sorted_nums[1]
        large = sorted_nums[2]

    # 检查是否有左/右/左拐/右拐
    input_lower = input_text.lower()
    if "左拐" in input_lower or "左" in input_lower:
        corner = "左拐"
    elif "右拐" in input_lower or "右" in input_lower:
        corner = "右拐"

    # 格式化数字
    def fmt(n):
        if n == int(n):
            return str(int(n))
        return str(n)

    small_str = fmt(small)
    large_str = fmt(large)
    narrow_str = fmt(narrow) if narrow else ""

    # 根据按钮生成
    if button_name == "横版":
        return f"#{small_str}x{large_str}cm横版*1块"
    elif button_name == "竖版":
        return f"#{large_str}x{small_str}cm竖版*1块"
    elif button_name == "L型":
        return f"【L型】#{small_str}x{large_str}x{narrow_str}cm【{corner}】*1块"
    elif button_name == "L型异型":
        return f"【L型异形】#{small_str}x{large_str}cm【{corner}】*1块"
    elif button_name == "换图":
        return "【换图】"
    elif button_name == "改图":
        return "【改图】"
    else:
        return f"#{small_str}x{large_str}cm {button_name} *1块"


# ========== 邀请下单计算 ==========
def calculate_invite(num1, num2):
    """邀请下单：大数÷小数取整数（不四舍五入），整数×小数=余数"""
    if num1 <= 0 or num2 <= 0:
        return None, None, None, "请输入大于0的数字"

    large = max(num1, num2)
    small = min(num1, num2)

    # 取整数（向下取整，不四舍五入）
    integer = int(large // small)
    # 余数 = 大数 - 整数×小数
    remainder = large - integer * small

    return integer, remainder, large, small, f"{large} ÷ {small} = {integer} 余 {remainder:.2f}"


# ========== 主界面 ==========
class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(8)

        # 当前选中的材质
        self.current_material = MATERIALS[0]

        self.build_ui()

    def build_ui(self):
        # 标题
        title = Label(
            text=f"[b]舟舟算价助手 v{VERSION}[/b]",
            markup=True,
            font_size=dp(18),
            size_hint_y=None,
            height=dp(40)
        )
        self.add_widget(title)

        # Tab切换
        self.tab_panel = TabbedPanel(
            do_default_tab=False,
            tab_width=Window.width / 3,
            size_hint_y=1
        )

        # 算价Tab
        tab_price = TabbedPanelItem(text='算价')
        tab_price.add_widget(self.build_price_tab())
        self.tab_panel.add_widget(tab_price)

        # 快捷备注Tab
        tab_note = TabbedPanelItem(text='快捷备注')
        tab_note.add_widget(self.build_note_tab())
        self.tab_panel.add_widget(tab_note)

        # 邀请下单Tab
        tab_invite = TabbedPanelItem(text='邀请下单')
        tab_invite.add_widget(self.build_invite_tab())
        self.tab_panel.add_widget(tab_invite)

        self.add_widget(self.tab_panel)

    def build_price_tab(self):
        """算价Tab"""
        layout = BoxLayout(orientation='vertical', spacing=dp(8), padding=dp(5))

        # 材质选择
        material_label = Label(text="选择材质：", font_size=dp(14), size_hint_y=None, height=dp(25))
        layout.add_widget(material_label)

        material_names = [m["name"] for m in MATERIALS]
        self.material_spinner = Spinner(
            text=MATERIALS[0]["name"],
            values=material_names,
            size_hint_y=None,
            height=dp(45),
            font_size=dp(12)
        )
        self.material_spinner.bind(text=self.on_material_selected)
        layout.add_widget(self.material_spinner)

        # 尺寸输入
        size_label = Label(text="输入尺寸（如 100x120 或 1m x 1.2m）：", font_size=dp(14), size_hint_y=None, height=dp(25))
        layout.add_widget(size_label)

        self.size_input = TextInput(
            hint_text="例如：100x120",
            multiline=False,
            size_hint_y=None,
            height=dp(45),
            font_size=dp(16)
        )
        layout.add_widget(self.size_input)

        # 算价按钮
        calc_btn = Button(
            text="开始算价",
            size_hint_y=None,
            height=dp(50),
            font_size=dp(16),
            background_color=get_color_from_hex('#3B82F6')
        )
        calc_btn.bind(on_press=self.do_calculate)
        layout.add_widget(calc_btn)

        # 结果显示
        self.result_label = Label(
            text="请输入尺寸后点击算价",
            font_size=dp(14),
            halign='left',
            valign='top',
            markup=True
        )
        self.result_label.bind(size=self.result_label.setter('text_size'))
        result_scroll = ScrollView(size_hint_y=1)
        result_scroll.add_widget(self.result_label)
        layout.add_widget(result_scroll)

        return layout

    def build_note_tab(self):
        """快捷备注Tab"""
        layout = BoxLayout(orientation='vertical', spacing=dp(8), padding=dp(5))

        # 输入尺寸
        input_label = Label(text="输入尺寸（如 100 200，三个数时最小为窄边）：", font_size=dp(13), size_hint_y=None, height=dp(25))
        layout.add_widget(input_label)

        self.note_input = TextInput(
            hint_text="例如：100 200",
            multiline=False,
            size_hint_y=None,
            height=dp(45),
            font_size=dp(16)
        )
        layout.add_widget(self.note_input)

        # 按钮区域
        btn_label = Label(text="选择备注类型：", font_size=dp(14), size_hint_y=None, height=dp(25))
        layout.add_widget(btn_label)

        btn_grid = GridLayout(cols=3, spacing=dp(8), size_hint_y=None)
        btn_grid.bind(minimum_height=btn_grid.setter('height'))

        self.note_buttons = []
        for btn_data in DEFAULT_NOTE_BUTTONS:
            btn = Button(
                text=btn_data["name"],
                size_hint_y=None,
                height=dp(45),
                font_size=dp(13),
                background_color=get_color_from_hex('#A855F7')
            )
            btn.bind(on_press=lambda instance, name=btn_data["name"]: self.do_generate_note(name))
            btn_grid.add_widget(btn)
            self.note_buttons.append(btn)

        layout.add_widget(btn_grid)

        # 输出区域
        out_label = Label(text="生成的话术：", font_size=dp(14), size_hint_y=None, height=dp(25))
        layout.add_widget(out_label)

        self.note_output = TextInput(
            readonly=True,
            multiline=True,
            font_size=dp(14),
            background_color=get_color_from_hex('#1E1E1E')
        )
        layout.add_widget(self.note_output)

        # 复制按钮
        copy_btn = Button(
            text="一键复制话术",
            size_hint_y=None,
            height=dp(45),
            font_size=dp(15),
            background_color=get_color_from_hex('#22C55E')
        )
        copy_btn.bind(on_press=self.copy_note)
        layout.add_widget(copy_btn)

        return layout

    def build_invite_tab(self):
        """邀请下单Tab"""
        layout = BoxLayout(orientation='vertical', spacing=dp(8), padding=dp(5))

        # 第一个数字
        label1 = Label(text="第一个数字：", font_size=dp(14), size_hint_y=None, height=dp(25))
        layout.add_widget(label1)

        self.invite_input1 = TextInput(
            hint_text="输入数字",
            multiline=False,
            size_hint_y=None,
            height=dp(45),
            font_size=dp(16)
        )
        layout.add_widget(self.invite_input1)

        # 第二个数字
        label2 = Label(text="第二个数字：", font_size=dp(14), size_hint_y=None, height=dp(25))
        layout.add_widget(label2)

        self.invite_input2 = TextInput(
            hint_text="输入数字",
            multiline=False,
            size_hint_y=None,
            height=dp(45),
            font_size=dp(16)
        )
        layout.add_widget(self.invite_input2)

        # 计算按钮
        calc_btn = Button(
            text="自动取整计算",
            size_hint_y=None,
            height=dp(50),
            font_size=dp(16),
            background_color=get_color_from_hex('#F97316')
        )
        calc_btn.bind(on_press=self.do_invite_calc)
        layout.add_widget(calc_btn)

        # 结果显示
        self.invite_result = Label(
            text="请输入两个数字后点击计算",
            font_size=dp(15),
            halign='left',
            valign='top',
            markup=True
        )
        self.invite_result.bind(size=self.invite_result.setter('text_size'))
        result_scroll = ScrollView(size_hint_y=1)
        result_scroll.add_widget(self.invite_result)
        layout.add_widget(result_scroll)

        return layout

    def on_material_selected(self, spinner, text):
        """材质选择变化"""
        for m in MATERIALS:
            if m["name"] == text:
                self.current_material = m
                break

    def do_calculate(self, instance):
        """执行算价"""
        text = self.size_input.text.strip()
        if not text:
            self.result_label.text = "[color=#FF6B6B]请输入尺寸[/color]"
            return

        length, width, desc = parse_dimension(text)
        if length is None:
            self.result_label.text = f"[color=#FF6B6B]{desc}[/color]"
            return

        original, discount, final_l, final_w, area, weight, reason = calculate_price(
            length, width, self.current_material, DISCOUNT
        )

        result_text = f"[b]{desc}[/b]\n\n"
        result_text += f"材质：{self.current_material['name']}\n"
        result_text += f"单价：{self.current_material['price']}元/㎡\n\n"
        result_text += f"[color=#FFD700]{reason}[/color]\n\n"
        result_text += f"撩尺后尺寸：{final_l}m x {final_w}m\n"
        result_text += f"合计面积：{area}㎡\n"
        result_text += f"重量：{weight}kg\n\n"
        result_text += f"[size=20][color=#FF6B6B]原价：¥{original:.2f}[/color][/size]\n"
        result_text += f"[size=20][color=#4ADE80]9折价：¥{discount:.2f}[/color][/size]\n\n"
        result_text += f"[color=#AAAAAA]亲亲~原价 {original:.2f}元，立减优惠到 {discount:.2f}元【不支持平台优惠券和红包哦】[/color]"

        self.result_label.text = result_text

    def do_generate_note(self, button_name):
        """生成备注话术"""
        text = self.note_input.text.strip()
        if not text:
            self.note_output.text = "请先输入尺寸"
            return

        result = generate_note(button_name, text)
        self.note_output.text = result

    def copy_note(self, instance):
        """复制备注话术到剪贴板"""
        text = self.note_output.text.strip()
        if not text or text == "请先输入尺寸":
            return

        # Kivy剪贴板
        from kivy.core.clipboard import Clipboard
        Clipboard.copy(text)

        # 显示提示
        popup = Popup(
            title='成功',
            content=Label(text='话术已复制到剪贴板！\n去千牛粘贴即可'),
            size_hint=(None, None),
            size=(dp(300), dp(150))
        )
        popup.open()

    def do_invite_calc(self, instance):
        """邀请下单计算"""
        try:
            num1 = float(self.invite_input1.text.strip())
            num2 = float(self.invite_input2.text.strip())
        except ValueError:
            self.invite_result.text = "[color=#FF6B6B]请输入有效的数字[/color]"
            return

        result = calculate_invite(num1, num2)
        if result[0] is None:
            self.invite_result.text = f"[color=#FF6B6B]{result[4]}[/color]"
            return

        integer, remainder, large, small, desc = result

        result_text = f"[b]计算结果[/b]\n\n"
        result_text += f"大数：{large}\n"
        result_text += f"小数：{small}\n\n"
        result_text += f"[color=#FFD700]{desc}[/color]\n\n"
        result_text += f"[size=18][color=#4ADE80]取整数：{integer}[/color][/size]\n"
        result_text += f"[size=18][color=#FFA500]余数：{remainder:.2f}[/color][/size]"

        self.invite_result.text = result_text


# ========== 应用主类 ==========
class PriceCalculatorApp(App):
    def build(self):
        Window.clearcolor = get_color_from_hex('#1A1A2E')
        return MainLayout()

    def on_start(self):
        # 安卓悬浮窗权限请求（如果需要）
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.SYSTEM_ALERT_WINDOW])
        except:
            pass


if __name__ == '__main__':
    PriceCalculatorApp().run()
