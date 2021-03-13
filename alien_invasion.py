import sys
import pygame


class AlienInvasion:
    """初始化游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()  # 初始化背景设置，让 Pygame 能正常工作
        self.screen = pygame.display.set_mode(
            (1200, 800))  # 创建一个显示窗口。参数是元组，单位为像素，返回对象是surface（屏幕的一部分，用于显示游戏元素,这里表示整个游戏窗口）
        pygame.display.set_caption("Alien Invasion")

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            for event in pygame.event.get():  # 得到一个监听键盘和鼠标事件列表（上一次被调用后发生的所有事件）
                if event.type == pygame.QUIT:
                    sys.exit()  # 退出游戏
            pygame.display.flip()  # 让最近绘制的屏幕可见


# 检查特殊变量 __name__，此变量为程序执行时设置。若此文件作为主程序执行，则此变量被设置为'__main__'；若此文件被测试框架导入，则变量将不是'__main__'
if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
