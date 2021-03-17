import sys
from time import sleep
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard


class AlienInvasion:
    """初始化游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()  # 初始化背景设置，让 Pygame 能正常工作
        self.settings = Settings()  # 创建Settings实例并用它来访问设置
        # 创建一个显示窗口。参数是元组，单位为像素，返回对象是surface（屏幕的一部分，用于显示游戏元素,这里表示整个游戏窗口）
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.stats = GameStats(self)  # 创建存储游戏统计信息的实例
        self.scoreboard = ScoreBoard(self)  # 创建记分牌
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()  # 创建用于存储子弹的编组
        self.aliens = pygame.sprite.Group()  # 创建用于存储外星人的编组
        self.play_button = Button(self, "Play")  # 创建 Play 按钮
        self._create_fleet()
        pygame.display.set_caption("Alien Invasion")

    def run_game(self):
        """开始游戏的主循环"""
        while True:  # 通过辅助方法将事务管理与游戏的其他方面（如更新屏幕）分离——重构，使循环变得简单
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

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
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 玩家点击 Play 按钮
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """响应按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _create_fleet(self):
        """创建外星人群"""
        # 创建第一个外星人并计算一行可容纳多少个外星人
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        available_space_x = self.settings.screen_width - alien_width
        available_space_y = self.settings.screen_height - 3 * alien_height - self.ship.rect.height
        num_aliens_x = available_space_x // (2 * alien_width)
        num_aliens_rows = available_space_y // (2 * alien_height)

        # 创建外星人群
        for row_number in range(num_aliens_rows):
            for alien_number in range(num_aliens_x):
                self._create_alien(alien_number, row_number, alien_width, alien_height)

    def _create_alien(self, alien_number, row_number, alien_width, alien_height):
        """创建一个外星人群"""
        alien = Alien(self)
        alien.x = alien_width + alien_number * alien_width * 2
        alien.y = alien_height + 10 + row_number * alien_height * 2
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets中"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)  # !! 别忘了传入 ai_game
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹的位置并删除消失的子弹"""
        self.bullets.update()  # 对编组调用update()时，编组自动对其中的每个精灵调用 update()

        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))

        self._check_bullet_alien_collisions()  # 射杀外星人

    def _check_bullet_alien_collisions(self):
        """检查子弹和为行人的碰撞"""
        # 检查是否有子弹击中了外星人，若有则删除相应的子弹和外星人
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:  # 记分
            for aliens in collisions.values():  # 保证消灭的每个外星人都计入得分，aliens是个列表
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

        # 若外星人群被消灭，则删除现有的子弹并新建一群外星人，并加快游戏的节奏，提升玩家等级
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.scoreboard.prep_level()

    def _update_aliens(self):
        """检查是否有外星人位于屏幕边缘，并更新外星人群中所有外星人的位置"""
        self._check_fleet_edge()
        self.aliens.update()

        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 检查是否有外星人到达屏幕底端
        self._check_aliens_bottom()

    def _check_fleet_edge(self):
        """有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edge():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整群外星人下移，并改变方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """飞船被外星人撞到"""

        if self.stats.ships_left > 0:
            # 将ship_left - 1
            self.stats.ships_left -= 1
            # 更新记分牌
            self.scoreboard.prep_ships()

            # 清空剩余的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人，并将飞船放在屏幕底部中央
            self._create_fleet()
            self.ship.center_ship()

            # 暂停半秒钟
            sleep(0.5)
        else:
            self.stats.game_active = False  # 游戏结束
            pygame.mouse.set_visible(True)  # 显示隐藏的光标

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕底端"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.screen.get_rect().bottom:
                self._ship_hit()  # 像飞船被撞到一样处理
                break

    def _check_play_button(self, mouse_pos):
        """在玩家单击 Play 按钮时开始新游戏"""
        button_checked = self.play_button.rect.collidepoint(mouse_pos)
        if button_checked and not self.stats.game_active:  # 防止用户在游戏过程中点击了按钮所在区域时，游戏重新开始
            # 隐藏鼠标光标
            pygame.mouse.set_visible(False)

            # 重置游戏设置
            self.settings.initialize_dynamic_settings()

            # 重置游戏统计信息
            self.stats.reset_stats()
            self.stats.game_active = True
            self.scoreboard.prep_score()  # 分数要改变
            self.scoreboard.prep_level()  # 等级要改变
            self.scoreboard.prep_ships()  # 余下飞船数要改变

            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人，并将飞船放在屏幕底部中央
            self._create_fleet()
            self.ship.center_ship()

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
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # 如果游戏处于非活动状态，就绘制Play按钮
        if not self.stats.game_active:
            self.play_button.draw_button()

        self.scoreboard.show_score_level_ships()  # 显示得分、等级和飞船条数
        pygame.display.flip()  # 让最近绘制的屏幕可见


# 检查特殊变量 __name__，此变量为程序执行时设置。若此文件作为主程序执行，则此变量被设置为'__main__'；若此文件被测试框架导入，则变量将不是'__main__'
if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
