import sys
import pygame

from settings import Settings
from ship import Ship


class AlienInvasion:
    """初始化游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()  # 初始化背景设置，让 Pygame 能正常工作
        self.settings = Settings()  # 创建Settings实例并用它来访问设置
        # 创建一个显示窗口。参数是元组，单位为像素，返回对象是surface（屏幕的一部分，用于显示游戏元素,这里表示整个游戏窗口）
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # 全屏
        self.settings.screen_width = self.screen.get_rect().width  # 更新settings中的配置
        self.settings.screen_height = self.screen.get_rect().height
        self.ship = Ship(self)
        pygame.display.set_caption("Alien Invasion")

    def run_game(self):
        """开始游戏的主循环"""
        while True:  # 通过辅助方法将事务管理与游戏的其他方面（如更新屏幕）分离——重构，使循环变得简单
            self._check_events()
            self.ship.update()
            # 每次循环时都重绘屏幕
            self._update_screen()

    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():  # 得到一个监听键盘和鼠标事件列表（上一次被调用后发生的所有事件）
            if event.type == pygame.QUIT:  # 玩家单击游戏窗口的关闭按钮时，将检测到 pygame.QUIT事件
                sys.exit()  # 退出游戏
            elif event.type == pygame.KEYDOWN:  # 玩家每次按键都被注册为一个KEYDOWN事件
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """响应按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()


    def _check_keyup_events(self, event):
        """响应松开"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)  # 颜色，fill()方法用于处理surface，只接受一个实参——一种颜色
        self.ship.blitme()  # 绘制飞船
        pygame.display.flip()  # 让最近绘制的屏幕可见


# 检查特殊变量 __name__，此变量为程序执行时设置。若此文件作为主程序执行，则此变量被设置为'__main__'；若此文件被测试框架导入，则变量将不是'__main__'
if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
