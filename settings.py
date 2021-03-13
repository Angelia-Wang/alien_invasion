class Settings:
    """存储游戏《外星人入侵》中所有设置的类"""

    def __init__(self):
        """初始化游戏的设置"""
        # 屏幕设置
        self.screen_width = 1200  # 屏幕宽度，单位像素
        self.screen_height = 800  # 屏幕高度，单位像素
        self.bg_color = (230, 230, 230)  # 背景颜色
