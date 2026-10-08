# -*- coding: utf-8 -*-
"""
舟舟算价助手 - 安卓版 v2.1 极简稳定版
只保留算价功能
"""

import re
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import get_color_from_hex

# ========== 版本号 ==========
VERSION = "2.1.0"

# ========== 全局设置 ==========
DISCOUNT = 0.9
MIN_PRICE = 20

# ========== 材质数据 ==========
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

# ========== 中文字体 ==========
def get_font():
    fonts = [
        '/system/fonts/NotoSansCJK-Regular.ttc',
        '/system/fonts/NotoSansSC-Regular.otf',
        '/system/fonts/DroidSansFallback.ttf',
        '/system/fonts/SourceHanSansCN-Regular.otf',
    ]
    for f in fonts:
        if os.path.exists(f):
            return f
    return None

FONT = get_font()

# ========== 单位转换 ==========
def parse_dimension(text):
    text = text.strip()
    pattern = r'(\d+\.?\d*)\s*(m|cm|mm|米|厘米|毫米)?'
    matches = re.findall(pattern, text, re.IGNORECASE)
    numbers = []
    for value_str, unit in matches:
        if not value_str:
            continue
        value = float(value_str)
        unit = unit.lower() if unit else ''
        if unit in ['m', '米']:
            meters = value
        elif unit in ['cm', '厘米']:
            meters = value / 100.0
        elif unit in ['mm', '毫米']:
            meters = value / 1000.0
        else:
            if value < 10:
                meters = value
            else:
                meters = value / 100.0
        numbers.append(meters)
    if len(numbers) < 2:
        return None, None, "无法识别尺寸，请输入如 100x120"
    length = numbers[0]
    width = numbers[1]
    desc = f"识别：{length*100:.0f}cm x {width*100:.0f}cm"
    return length, width, desc

# ========== 撩尺 ==========
def liao_chi(short_edge, material_name=""):
    if "凯彼得" in material_name:
        return short_edge, "凯彼得材质，无需撩尺"
    short_cm = short_edge * 100
    if short_cm < 40:
        result = 40
        reason = f"短边{short_cm:.0f}cm<40，按40算"
    elif short_cm <= 200:
        result = ((int(short_cm) + 19) // 20) * 20
        reason = f"短边{short_cm:.0f}cm，撩尺到{result}cm"
    else:
        result = ((int(short_cm) + 49) // 50) * 50
        reason = f"短边{short_cm:.0f}cm，撩尺到{result}cm"
    return result / 100.0, reason

# ========== 算价 ==========
def calculate_price(length, width, material, discount=DISCOUNT):
    if length >= width:
        long_edge = length
        short_edge = width
    else:
        long_edge = width
        short_edge = length
    liao_short, liao_reason = liao_chi(short_edge, material["name"])
    area = long_edge * liao_short
    original_price = area * material["price"]
    if original_price < MIN_PRICE:
        original_price = MIN_PRICE
    discount_price = original_price * discount
    if discount_price < MIN_PRICE:
        discount_price = MIN_PRICE
    weight = (length * width) * material.get("weight", 0)
    return original_price, discount_price, long_edge, liao_short, area, weight, liao_reason


# ========== 主界面 ==========
class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(15)
        self.spacing = dp(12)
        
        # 背景色
        self.window = Window
        self.window.clearcolor = get_color_from_hex('#1a1a2e')
        
        # 标题
        title = Label(
            text=f"舟舟算价助手 v{VERSION}",
            font_size=dp(22),
            bold=True,
            color=get_color_from_hex('#ffffff'),
            size_hint_y=None,
            height=dp(40),
        )
        if FONT:
            title.font_name = FONT
        self.add_widget(title)
        
        # 材质选择
        mat_label = Label(
            text="选择材质",
            font_size=dp(15),
            color=get_color_from_hex('#b0b0d0'),
            size_hint_y=None,
            height=dp(25),
        )
        if FONT:
            mat_label.font_name = FONT
        self.add_widget(mat_label)
        
        self.material_spinner = Spinner(
            text=MATERIALS[0]["name"],
            values=[m["name"] for m in MATERIALS],
            size_hint_y=None,
            height=dp(50),
            background_color=get_color_from_hex('#2a2a4a'),
        )
        if FONT:
            self.material_spinner.font_name = FONT
        self.add_widget(self.material_spinner)
        
        # 材质信息
        self.mat_info = Label(
            text=f"单价：{MATERIALS[0]['price']}元/㎡",
            font_size=dp(13),
            color=get_color_from_hex('#00d9a0'),
            size_hint_y=None,
            height=dp(25),
        )
        if FONT:
            self.mat_info.font_name = FONT
        self.add_widget(self.mat_info)
        
        # 尺寸输入
        size_label = Label(
            text="输入尺寸（如 100x200）",
            font_size=dp(15),
            color=get_color_from_hex('#b0b0d0'),
            size_hint_y=None,
            height=dp(25),
        )
        if FONT:
            size_label.font_name = FONT
        self.add_widget(size_label)
        
        self.size_input = TextInput(
            hint_text="例如：100x200",
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            background_color=get_color_from_hex('#2a2a4a'),
            foreground_color=get_color_from_hex('#ffffff'),
            cursor_color=get_color_from_hex('#e94560'),
            font_size=dp(16),
        )
        if FONT:
            self.size_input.font_name = FONT
        self.add_widget(self.size_input)
        
        # 计算按钮
        calc_btn = Button(
            text="开始算价",
            size_hint_y=None,
            height=dp(55),
            background_normal='',
            background_color=get_color_from_hex('#e94560'),
            color=get_color_from_hex('#ffffff'),
            font_size=dp(18),
            bold=True,
        )
        if FONT:
            calc_btn.font_name = FONT
        calc_btn.bind(on_press=self.calculate)
        self.add_widget(calc_btn)
        
        # 结果区域（可滚动）
        self.result_label = Label(
            text="请输入尺寸后点击算价",
            font_size=dp(15),
            color=get_color_from_hex('#ffffff'),
            size_hint_y=None,
            height=dp(300),
            text_size=(self.width - dp(30), None),
            valign='top',
        )
        if FONT:
            self.result_label.font_name = FONT
        
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.result_label)
        self.add_widget(scroll)
        
        self.current_material = MATERIALS[0]
        self.material_spinner.bind(text=self.on_material_select)
    
    def on_material_select(self, spinner, text):
        for m in MATERIALS:
            if m["name"] == text:
                self.current_material = m
                self.mat_info.text = f"单价：{m['price']}元/㎡ | 重量：{m['weight']}kg/㎡"
                break
    
    def calculate(self, instance):
        text = self.size_input.text.strip()
        if not text:
            self.result_label.text = "请先输入尺寸"
            return
        
        length, width, desc = parse_dimension(text)
        if length is None:
            self.result_label.text = desc
            return
        
        original_price, discount_price, final_long, final_short, area, weight, reason = calculate_price(
            length, width, self.current_material
        )
        
        result = (
            f"{desc}\n\n"
            f"撩尺后：{final_long*100:.0f}cm x {final_short*100:.0f}cm\n"
            f"面积：{area:.2f}㎡\n"
            f"重量：{weight:.2f}kg\n\n"
            f"原价：{original_price:.2f}元\n"
            f"九折价：{discount_price:.2f}元\n\n"
            f"{reason}"
        )
        self.result_label.text = result


# ========== 应用 ==========
class ZhouzhouPriceApp(App):
    def build(self):
        return MainLayout()


if __name__ == '__main__':
    ZhouzhouPriceApp().run()
