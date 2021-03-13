import pygame


class Ship:
    """管理飞船的类"""

    def __init__(self, ai_game):  # 参数：引用self和指向当前AlienInvasion实例的引用，这让Ship能访问AlienInvasion中定义的所有游戏资源
        """初始化飞船并设置其初始位置"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()  # get_rect()访问屏幕的属性rect

        # 加载飞船图片并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # 对每艘新飞船，都将其放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)
