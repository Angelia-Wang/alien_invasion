class Settings:
    """存储游戏《外星人入侵》中所有设置的类"""

    def __init__(self):
        """初始化游戏的设置"""
        # 屏幕设置
        self.screen_width = 1200  # 屏幕宽度，单位像素
        self.screen_height = 800  # 屏幕高度，单位像素
        self.bg_color = (230, 230, 230)  # 背景颜色

        # 飞船设置
        self.ship_speed = 1.5
        self.ship_limit = 3  # 可用总飞船数目

        # 子弹设置
        self.bullet_speed = 1.5
        self.bullet_with = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3  # 最大子弹数

        # 外星人设置
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10  # 行下移动的速度
        self.fleet_direction = 1  # 1表示往右移动，-1表示往左移动
