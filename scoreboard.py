import pygame.font
from pygame.sprite import Group
from ship import Ship


class ScoreBoard:
    """显示得分信息的类"""

    def __init__(self, ai_game):
        """初始化显示得分涉及的属性"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 24)

        # 准备初始得分、等级和飞船图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """将得分转换为一副渲染的图像"""
        rounded_score = round(self.stats.score, -1)  # 舍入到10的整数倍
        score_str = "current score: " + "{:,}".format(rounded_score)  # 将数值转换为字符串时，在其中插入逗号（千位分隔符）
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # 在屏幕右上角显示得分
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 10
        self.score_rect.top = 10

    def prep_high_score(self):
        """将最高得分转换为渲染的图像"""
        rounded_high_score = round(self.stats.high_score, -1)
        high_score_str = "highest score: " + "{:,}".format(rounded_high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # 在屏幕顶部中央显示得分
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """将等级转换为渲染的图像"""
        level_str = "level: " + str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        # 将等级放在得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.top = self.score_rect.bottom + 5
        self.level_rect.right = self.score_rect.right

    def prep_ships(self):
        """显示还余下多少飞船"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score_level_ships(self):
        """在屏幕上显示得分、等级和余下飞船数"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        """检查是否诞生了新的最高得分"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()