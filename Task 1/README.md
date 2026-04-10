📚 图书馆座位预约系统 (Library Seat Reservation System)
这是一个基于 Python 和 Tkinter 构建的带有图形界面 (GUI) 的图书馆座位预约系统。该系统支持用户注册、登录、座位查看、预约、释放座位，以及管理员对系统座位的管理，并通过本地 JSON 文件实现用户数据的持久化存储。

🛠️ 环境要求 (Prerequisites)
Python 3.7+: 本项目依赖于 Python 3 环境，请确保你的电脑上已经正确安装。

Tkinter: Python 的标准 GUI 库。在大多数 Windows 和 macOS 的 Python 安装中，它已经默认自带。

注：如果你使用的是 Linux (如 Ubuntu)，可能需要手动安装 Tkinter，命令为：sudo apt-get install python3-tk

📁 文件结构 (Project Structure)
在运行程序之前，请确保以下所有的文件都放置在同一个文件夹目录下：

gui.py - 主图形界面和程序运行入口

system.py - 系统的核心逻辑、数据处理与排序算法

user.py - 用户基类及派生类（Customer 和 Admin）

seat.py - 座位基类及派生类（StandardSeat 和 ComputerSeat）

reservation.py - 预约记录管理及倒计时逻辑

reminder.py - 系统提醒与时间检查模块

user_data.json - 本地数据存储文件。用于保存已注册的账号、密码和角色信息。初始为空 []，表示当前无任何注册用户。

🚀 如何运行 (How to Run)
打开终端 (Terminal) 或 命令提示符 (Command Prompt)。

导航到项目目录：使用 cd 命令进入你存放上述所有代码文件的文件夹。

Bash
cd 你的/文件/路径
运行主程序：执行以下命令启动 GUI 界面。

Bash
python gui.py
(注：在某些系统如 macOS 或 Linux 上，你可能需要使用 python3 gui.py)

💡 首次使用指南 (Getting Started)
当你成功启动程序后，会看到系统的欢迎和登录界面。

注册新账号 (Register)：

由于 user_data.json 初始为空，系统中没有任何预设用户。

请先在输入框中填入你想要的 Username（用户名）和 Password（密码）。

点击 "Register as Customer"（注册为普通顾客）或 "Register as Admin"（注册为管理员）。

注册成功后，你的账号信息会立刻自动写入并保存在 user_data.json 文件中。下次重启程序时，你可以直接登录。

登录系统 (Login)：

使用刚刚注册的账号和密码点击 "Login" 进入对应的控制台 (Dashboard)。

体验核心功能 (Features)：

系统在每次初始化时会自动生成 5个测试座位（3个普通桌椅，2个电脑座位），你可以点击 "View all seats" 来查看它们。

尝试输入座位号和预约时间进行 预约 (Reserve a seat)。

预约成功后，控制台下方会启动实时倒计时 (Timer)，显示距离开始或结束的时间，并在关键节点弹出提示框 (Reminder)。
  
  
  
