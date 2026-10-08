# -*- coding: utf-8 -*-
"""
舟舟算价助手 - 安卓版 v2.0
功能：材质算价、快捷备注、邀请下单
风格：柔光玻璃材质
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
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, RoundedRectangle, Rectangle

# ========== 版本号 ==========
VERSION = "2.0.0"

# ========== 全局设置 ==========
DISCOUNT = 0.9  # 默认九折
MIN_PRICE = 20  # 最低价20元

# ========== 颜色主题（柔光玻璃） ==========
COLORS = {
    'bg_dark': '#1a1a2e',
    'bg_medium': '#16213e',
    'bg_light': '#0f3460',
    'card_bg': '#2a2a4a',
    'card_border': '#4a4a7a',
    'text_primary': '#ffffff',
    'text_secondary': '#b0b0d0',
    'accent': '#e94560',
    'accent_light': '#ff6b81',
    'success': '#00d9a0',
    'warning': '#ffc107',
    'glass': 'rgba(255, 255, 255, 0.1)',
    'glass_border': 'rgba(255, 255, 255, 0.2)',
}

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


# ========== 中文字体设置 ==========
def get_chinese_font():
    """获取中文字体路径"""
    # 尝试安卓系统中文字体
    android_fonts = [
        '/system/fonts/NotoSansCJK-Regular.ttc',
        '/system/fonts/NotoSansSC-Regular.otf',
        '/system/fonts/DroidSansFallback.ttf',
        '/system/fonts/SourceHanSansCN-Regular.otf',
    ]
    for font_path in android_fonts:
        if os.path.exists(font_path):
            return font_path
    
    # 尝试项目目录下的字体
    local_fonts = ['NotoSansSC-Regular.ttf', 'font.ttf', 'chinese.ttf']
    for font_name in local_fonts:
        if os.path.exists(font_name):
            return font_name
    
    return None

CHINESE_FONT = get_chinese_font()


class GlassLabel(Label):
    """柔光玻璃风格标签"""
    def __init__(self, **kwargs):
        kwargs.setdefault('color', get_color_from_hex(COLORS['text_primary']))
        kwargs.setdefault('font_size', dp(14))
        if CHINESE_FONT:
            kwargs.setdefault('font_name', CHINESE_FONT)
        super().__init__(**kwargs)


class GlassButton(Button):
    """柔光玻璃风格按钮"""
    def __init__(self, **kwargs):
        kwargs.setdefault('background_normal', '')
        kwargs.setdefault('background_color', get_color_from_hex(COLORS['card_bg']))
        kwargs.setdefault('color', get_color_from_hex(COLORS['text_primary']))
        kwargs.setdefault('font_size', dp(14))
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', dp(45))
        if CHINESE_FONT:
            kwargs.setdefault('font_name', CHINESE_FONT)
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(rgba=get_color_from_hex(COLORS['glass_border']))
            self.border = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])
        self.bind(pos=self.update_border, size=self.update_border)
    
    def update_border(self, *args):
        self.border.pos = self.pos
        self.border.size = self.size


class AccentButton(GlassButton):
    """强调按钮（红色）"""
    def __init__(self, **kwargs):
        kwargs.setdefault('background_color', get_color_from_hex(COLORS['accent']))
        super().__init__(**kwargs)


class SuccessButton(GlassButton):
    """成功按钮（绿色）"""
    def __init__(self, **kwargs):
        kwargs.setdefault('background_color', get_color_from_hex(COLORS['success']))
        kwargs.setdefault('color', (0, 0, 0, 1))
        super().__init__(**kwargs)


class GlassCard(BoxLayout):
    """柔光玻璃卡片"""
    def __init__(self, **kwargs):
        kwargs.setdefault('orientation', 'vertical')
        kwargs.setdefault('padding', dp(12))
        kwargs.setdefault('spacing', dp(8))
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(rgba=get_color_from_hex(COLORS['card_bg']))
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
            Color(rgba=get_color_from_hex(COLORS['glass_border']))
            self.border = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
        self.bind(pos=self.update_bg, size=self.update_bg)
    
    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.border.pos = self.pos
        self.border.size = self.size


# ========== 单位智能转换 ==========
def parse_dimension(text):
    """解析尺寸文本，返回(长m, 宽m, 原始描述)"""
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
        return None, None, "无法识别尺寸，请输入如 100x120 或 1m x 1.2m"

    length = numbers[0]
    width = numbers[1]
    desc = f"识别到：{length*100:.0f}cm x {width*100:.0f}cm = {length:.2f}m x {width:.2f}m"
    return length, width, desc


# ========== 撩尺计算 ==========
def liao_chi(short_edge, material_name=""):
    """撩尺：只撩短边，长边不变"""
    if "凯彼得" in material_name:
        return short_edge, "凯彼得材质，无需撩尺"

    short_cm = short_edge * 100

    if short_cm < 40:
        result = 40
        reason = f"短边{short_cm:.0f}cm<40，按40算"
    elif short_cm <= 200:
        result = ((int(short_cm) + 19) // 20) * 20
        if result == int(short_cm):
            reason = f"短边{short_cm:.0f}cm正好是整数，无需撩尺"
        else:
            reason = f"短边{short_cm:.0f}cm，撩尺到{result}cm（20间隔）"
    else:
        result = ((int(short_cm) + 49) // 50) * 50
        reason = f"短边{short_cm:.0f}cm，撩尺到{result}cm（50间隔）"

    return result / 100.0, reason


# ========== 算价核心 ==========
def calculate_price(length, width, material, discount=DISCOUNT):
    """计算价格，返回(原价, 折扣价, 撩尺后长, 撩尺后宽, 面积, 重量, 说明)"""
    if length >= width:
        long_edge = length
        short_edge = width
    else:
        long_edge = width
        short_edge = length

    liao_short, liao_reason = liao_chi(short_edge, material["name"])

    final_long = long_edge
    final_short = liao_short
    area = final_long * final_short

    original_price = area * material["price"]

    if original_price < MIN_PRICE:
        original_price = MIN_PRICE
        price_reason = f"原价{area * material['price']:.2f}元<20，按最低价20元算"
    else:
        price_reason = f"面积{area:.2f}㎡ x 单价{material['price']}元/㎡ = {original_price:.2f}元"

    discount_price = original_price * discount
    if discount_price < MIN_PRICE:
        discount_price = MIN_PRICE

    weight = (length * width) * material.get("weight", 0)

    return (round(original_price, 2), round(discount_price, 2),
            round(final_long, 2), round(final_short, 2),
            round(area, 2), round(weight, 2),
            f"{liao_reason}\n{price_reason}")


# ========== 快捷备注话术生成 ==========
def generate_note(button_name, input_text):
    """根据按钮和输入生成备注话术"""
    numbers = []
    for match in re.finditer(r'(\d+\.?\d*)', input_text):
        numbers.append(float(match.group(1)))

    if len(numbers) < 2:
        return "请输入至少两个尺寸，如 100 200"

    sorted_nums = sorted(numbers)
    small = sorted_nums[0]
    large = sorted_nums[-1]

    narrow = None
    corner = "拐角方向"
    if len(numbers) >= 3:
        narrow = sorted_nums[0]
        small = sorted_nums[1]
        large = sorted_nums[2]

    input_lower = input_text.lower()
    if "左拐" in input_lower or "左" in input_lower:
        corner = "左拐"
    elif "右拐" in input_lower or "右" in input_lower:
        corner = "右拐"

    def fmt(n):
        if n == int(n):
            return str(int(n))
        return str(n)

    small_str = fmt(small)
    large_str = fmt(large)
    narrow_str = fmt(narrow) if narrow else ""

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

    integer = int(large // small)
    remainder = large - integer * small

    return integer, remainder, large, small, f"{large} ÷ {small} = {integer} 余 {remainder:.2f}"


# ========== 材质算价页面 ==========
class PriceCalculatorTab(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(12)
        self.spacing = dp(10)

        # 标题
        title = GlassLabel(text=f"舟舟算价助手 v{VERSION}", font_size=dp(20), bold=True, size_hint_y=None, height=dp(35))
        self.add_widget(title)

        # 材质选择卡片
        material_card = GlassCard()
        material_card.add_widget(GlassLabel(text="选择材质", font_size=dp(14), bold=True, size_hint_y=None, height=dp(25)))
        
        self.material_spinner = Spinner(
            text=MATERIALS[0]["name"],
            values=[m["name"] for m in MATERIALS],
            size_hint_y=None,
            height=dp(45),
            background_color=get_color_from_hex(COLORS['card_bg']),
        )
        if CHINESE_FONT:
            self.material_spinner.font_name = CHINESE_FONT
        self.material_spinner.bind(text=self.on_material_select)
        material_card.add_widget(self.material_spinner)
        
        self.material_info = GlassLabel(text=f"单价：{MATERIALS[0]['price']}元/㎡ | 重量：{MATERIALS[0]['weight']}kg/㎡", 
                                         font_size=dp(12), color=get_color_from_hex(COLORS['text_secondary']),
                                         size_hint_y=None, height=dp(20))
        material_card.add_widget(self.material_info)
        self.add_widget(material_card)

        # 尺寸输入卡片
        size_card = GlassCard()
        size_card.add_widget(GlassLabel(text="输入尺寸（如 100x200 或 1m x 1.2m）", 
                                         font_size=dp(14), bold=True, size_hint_y=None, height=dp(25)))
        self.size_input = TextInput(
            hint_text="例如：100x200",
            multiline=False,
            size_hint_y=None,
            height=dp(45),
            background_color=get_color_from_hex('#1a1a2e'),
            foreground_color=get_color_from_hex(COLORS['text_primary']),
            cursor_color=get_color_from_hex(COLORS['accent']),
        )
        if CHINESE_FONT:
            self.size_input.font_name = CHINESE_FONT
        size_card.add_widget(self.size_input)
        self.add_widget(size_card)

        # 计算按钮
        calc_btn = AccentButton(text="开始算价", size_hint_y=None, height=dp(50))
        calc_btn.bind(on_press=self.calculate)
        self.add_widget(calc_btn)

        # 结果卡片
        self.result_card = GlassCard()
        self.result_card.add_widget(GlassLabel(text="计算结果", font_size=dp(16), bold=True, 
                                                size_hint_y=None, height=dp(25)))
        self.result_label = GlassLabel(text="请输入尺寸后点击算价", font_size=dp(13),
                                        size_hint_y=None, height=dp(150))
        self.result_card.add_widget(self.result_label)
        self.add_widget(self.result_card)

        self.current_material = MATERIALS[0]

    def on_material_select(self, spinner, text):
        for m in MATERIALS:
            if m["name"] == text:
                self.current_material = m
                self.material_info.text = f"单价：{m['price']}元/㎡ | 重量：{m['weight']}kg/㎡"
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

        result_text = (
            f"{desc}\n\n"
            f"撩尺后尺寸：{final_long*100:.0f}cm x {final_short*100:.0f}cm\n"
            f"面积：{area:.2f}㎡\n"
            f"重量：{weight:.2f}kg\n\n"
            f"原价：{original_price:.2f}元\n"
            f"九折价：{discount_price:.2f}元\n\n"
            f"{reason}"
        )
        self.result_label.text = result_text


# ========== 快捷备注页面 ==========
class QuickNoteTab(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(12)
        self.spacing = dp(10)

        title = GlassLabel(text="快捷备注", font_size=dp(20), bold=True, size_hint_y=None, height=dp(35))
        self.add_widget(title)

        # 输入卡片
        input_card = GlassCard()
        input_card.add_widget(GlassLabel(text="输入尺寸（如 100 200，L型可输三个数）", 
                                          font_size=dp(14), bold=True, size_hint_y=None, height=dp(25)))
        self.note_input = TextInput(
            hint_text="例如：100 200",
            multiline=False,
            size_hint_y=None,
            height=dp(45),
            background_color=get_color_from_hex('#1a1a2e'),
            foreground_color=get_color_from_hex(COLORS['text_primary']),
            cursor_color=get_color_from_hex(COLORS['accent']),
        )
        if CHINESE_FONT:
            self.note_input.font_name = CHINESE_FONT
        input_card.add_widget(self.note_input)
        self.add_widget(input_card)

        # 按钮网格
        btn_grid = GridLayout(cols=2, spacing=dp(10), size_hint_y=None)
        btn_grid.bind(minimum_height=btn_grid.setter('height'))
        
        for btn_info in DEFAULT_NOTE_BUTTONS:
            btn = GlassButton(text=btn_info["name"], size_hint_y=None, height=dp(50))
            btn.bind(on_press=lambda instance, name=btn_info["name"]: self.generate_note(name))
            btn_grid.add_widget(btn)
        
        self.add_widget(btn_grid)

        # 结果卡片
        result_card = GlassCard()
        result_card.add_widget(GlassLabel(text="生成结果", font_size=dp(16), bold=True, 
                                           size_hint_y=None, height=dp(25)))
        self.result_label = GlassLabel(text="点击按钮生成备注话术", font_size=dp(14),
                                       size_hint_y=None, height=dp(80))
        result_card.add_widget(self.result_label)
        
        copy_btn = SuccessButton(text="复制结果", size_hint_y=None, height=dp(45))
        copy_btn.bind(on_press=self.copy_result)
        result_card.add_widget(copy_btn)
        
        self.add_widget(result_card)

    def generate_note(self, button_name):
        text = self.note_input.text.strip()
        if not text:
            self.result_label.text = "请先输入尺寸"
            return
        result = generate_note(button_name, text)
        self.result_label.text = result

    def copy_result(self, instance):
        text = self.result_label.text
        try:
            from kivy.core.clipboard import Clipboard
            Clipboard.copy(text)
            self.result_label.text = "已复制到剪贴板！\n\n" + text
        except:
            pass


# ========== 邀请下单页面 ==========
class InviteOrderTab(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(12)
        self.spacing = dp(10)

        title = GlassLabel(text="邀请下单计算", font_size=dp(20), bold=True, size_hint_y=None, height=dp(35))
        self.add_widget(title)

        # 输入卡片
        input_card = GlassCard()
        input_card.add_widget(GlassLabel(text="输入两个数字", font_size=dp(14), bold=True, 
                                          size_hint_y=None, height=dp(25)))
        
        self.num1_input = TextInput(
            hint_text="第一个数",
            multiline=False,
            size_hint_y=None,
            height=dp(45),
            background_color=get_color_from_hex('#1a1a2e'),
            foreground_color=get_color_from_hex(COLORS['text_primary']),
            cursor_color=get_color_from_hex(COLORS['accent']),
        )
        input_card.add_widget(self.num1_input)
        
        self.num2_input = TextInput(
            hint_text="第二个数",
            multiline=False,
            size_hint_y=None,
            height=dp(45),
            background_color=get_color_from_hex('#1a1a2e'),
            foreground_color=get_color_from_hex(COLORS['text_primary']),
            cursor_color=get_color_from_hex(COLORS['accent']),
        )
        input_card.add_widget(self.num2_input)
        self.add_widget(input_card)

        # 计算按钮
        calc_btn = AccentButton(text="开始计算", size_hint_y=None, height=dp(50))
        calc_btn.bind(on_press=self.calculate)
        self.add_widget(calc_btn)

        # 结果卡片
        result_card = GlassCard()
        result_card.add_widget(GlassLabel(text="计算结果", font_size=dp(16), bold=True, 
                                           size_hint_y=None, height=dp(25)))
        self.result_label = GlassLabel(text="请输入数字后点击计算", font_size=dp(14),
                                       size_hint_y=None, height=dp(120))
        result_card.add_widget(self.result_label)
        self.add_widget(result_card)

    def calculate(self, instance):
        try:
            num1 = float(self.num1_input.text.strip())
            num2 = float(self.num2_input.text.strip())
        except ValueError:
            self.result_label.text = "请输入有效的数字"
            return

        integer, remainder, large, small, desc = calculate_invite(num1, num2)
        if integer is None:
            self.result_label.text = desc
            return

        result_text = (
            f"{desc}\n\n"
            f"大数：{large}\n"
            f"小数：{small}\n"
            f"整数倍：{integer}\n"
            f"余数：{remainder:.2f}"
        )
        self.result_label.text = result_text


# ========== 主界面 ==========
class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # 设置背景
        with self.canvas.before:
            Color(rgba=get_color_from_hex(COLORS['bg_dark']))
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        # 标签页
        self.tab_panel = TabbedPanel(
            do_default_tab=False,
            tab_width=Window.width / 3,
            background_color=get_color_from_hex(COLORS['bg_medium']),
        )
        
        tab1 = TabbedPanelItem(text="材质算价")
        tab1.add_widget(PriceCalculatorTab())
        
        tab2 = TabbedPanelItem(text="快捷备注")
        tab2.add_widget(QuickNoteTab())
        
        tab3 = TabbedPanelItem(text="邀请下单")
        tab3.add_widget(InviteOrderTab())
        
        if CHINESE_FONT:
            for tab in [tab1, tab2, tab3]:
                tab.font_name = CHINESE_FONT
        
        self.tab_panel.add_widget(tab1)
        self.tab_panel.add_widget(tab2)
        self.tab_panel.add_widget(tab3)
        
        self.add_widget(self.tab_panel)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size


# ========== 应用主类 ==========
class ZhouzhouPriceApp(App):
    def build(self):
        # 强制竖屏
        Window.rotation = 0
        return MainLayout()

    def on_start(self):
        # 再次确保竖屏
        Window.rotation = 0


if __name__ == '__main__':
    ZhouzhouPriceApp().run()
