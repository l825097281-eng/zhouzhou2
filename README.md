# 舟舟算价助手 - 安卓版

## 功能说明

### 1. 材质算价
- 39种材质可选，每种材质有不同的单价
- 智能单位转换：输入100x120自动识别为1m x 1.2m
- 撩尺计算：短边自动撩尺（凯彼得材质不撩尺）
- 最低价20元保护
- 显示原价和9折价
- 显示重量（按原尺寸面积计算）
- 一键复制话术

### 2. 快捷备注
- 6种预设备注类型：横版、竖版、L型、L型异型、换图、改图
- 自动识别大数小数
- 三个数时最小的为窄边
- 自动识别左拐/右拐
- 一键复制话术

### 3. 邀请下单
- 输入两个数字
- 自动计算大数÷小数取整数（不四舍五入）
- 自动计算余数

## 打包APK方法

### 方法一：WSL2 + Buildozer（推荐，本地打包）

#### 1. 安装WSL2
以管理员身份打开PowerShell，运行：
```powershell
wsl --install -d Ubuntu
```
安装完成后重启电脑，设置Ubuntu用户名和密码。

#### 2. 在Ubuntu中安装依赖
打开Ubuntu终端，运行：
```bash
sudo apt update
sudo apt install -y python3-pip build-essential git zlib1g-dev ncurses-dev \
  libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev \
  automake libtool pkg-config openjdk-17-jdk unzip zip wget

# 安装Buildozer
pip3 install --user buildozer cython

# 添加环境变量
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
source ~/.bashrc
```

#### 3. 安装Android SDK和NDK
Buildozer会自动下载，但是比较慢，也可以手动安装：
```bash
# 创建目录
mkdir -p ~/android-sdk/cmdline-tools
cd ~/android-sdk/cmdline-tools

# 下载命令行工具
wget https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip
unzip commandlinetools-linux-9477386_latest.zip
mv cmdline-tools latest

# 设置环境变量
echo 'export ANDROIDSDK=~/android-sdk' >> ~/.bashrc
echo 'export ANDROIDNDK=~/android-ndk' >> ~/.bashrc
echo 'export PATH=$PATH:$ANDROIDSDK/cmdline-tools/latest/bin:$ANDROIDSDK/platform-tools' >> ~/.bashrc
source ~/.bashrc

# 安装SDK组件
sdkmanager "platforms;android-33" "build-tools;33.0.0" "platform-tools"
sdkmanager --licenses
```

#### 4. 复制项目文件到Ubuntu
```bash
# 在Windows的文件资源管理器中输入：
# \\wsl$\Ubuntu\home\你的用户名
# 把"舟舟算价助手_安卓"文件夹复制进去
```

#### 5. 打包APK
```bash
cd ~/舟舟算价助手_安卓
buildozer android debug
```

打包完成后，APK文件在 `bin/` 目录下：
`舟舟算价助手-1.0.0-arm64-v8a-debug.apk`

把APK传到手机上安装即可。

### 方法二：Google Colab在线打包（不需要装Linux）

1. 打开 https://colab.research.google.com/
2. 新建笔记本
3. 把项目文件上传到Colab
4. 运行以下代码：
```python
# 安装依赖
!apt update -qq
!apt install -y -qq build-essential git zlib1g-dev ncurses-dev \
  libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev \
  automake libtool pkg-config openjdk-17-jdk unzip zip wget

!pip install buildozer cython

# 打包
!buildozer android debug
```

5. 打包完成后下载APK文件

## 注意事项

1. 第一次打包会比较慢（需要下载Android SDK、NDK等，大约30分钟-1小时）
2. 安卓17手机可以安装，因为设置了minapi=21（安卓5.0），兼容性很好
3. 悬浮窗功能需要手动授权：设置 → 应用 → 舟舟算价助手 → 显示在其他应用上层
4. 材质数据和配置都内置在APK里，不需要额外下载

## 版本历史

- v1.0.0：初始版本，包含材质算价、快捷备注、邀请下单三大功能
