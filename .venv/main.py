import random
from arcade import Camera2D
import io
import arcade
import arcade as ar
from PIL import Image, ImageDraw
from PIL.ImageOps import scale
from arcade import View
from arcade.gui import UIManager, UIFlatButton, UILabel, UIDropdown, UISlider, UITextureButton
from pyglet.event import EVENT_HANDLE_STATE

screen_width = 800
screen_height = 600
volume = 100
full_screen = False
TITLE = 'Game'  # Потом заменить имя приложения


class OptionsScene(ar.View):
    def __init__(self, window):
        super().__init__(window, ar.color.BLUE_SAPPHIRE)# Поменять цвет на фон
        global screen_width, screen_height
        self.scale_x, self.scale_y = screen_width / 800, screen_height / 600
        self.window = window
        self.manager = UIManager()
        self.manager.enable()
        options_label = UILabel(
            text='Настройки',
            x=200 * self.scale_x,
            y=459 * self.scale_y,
            height=81 * self.scale_x,
            width=400 * self.scale_y,
            font_size=30 * self.scale_y,
            align='center',
            text_color=ar.color.WHITE
        )
        volume_label = UILabel(
            text='Громкость звука',
            x=160 * self.scale_x,
            y=450 * self.scale_y,
            height=20 * self.scale_x,
            width=171 * self.scale_y,
            font_size=20 * self.scale_y,
            align='left',
            text_color=ar.color.WHITE
        )
        self.main_button = UIFlatButton(
            text='Выйти в главное меню',
            x=50 * self.scale_x,
            y=200 * self.scale_y,
            height=40 * self.scale_x,
            width=250 * self.scale_y,
            font_size=20 * self.scale_y,
            align='center',
            text_color=ar.color.WHITE
        )
        self.random_color_background = UIFlatButton(
            text='Сменить цвет фона',
            x=350 * self.scale_x,
            y=200 * self.scale_y,
            height=40 * self.scale_x,
            width=160 * self.scale_y,
            font_size=20 * self.scale_y,
            align='center',
            text_color=ar.color.WHITE,
        )
        self.set_default_color = UIFlatButton(
            text='Начальный фон',
            x=600 * self.scale_x,
            y=200 * self.scale_y,
            height=40 * self.scale_x,
            width=150 * self.scale_y,
            font_size=20 * self.scale_y,
            align='center',
            text_color=ar.color.WHITE
        )
        resolution_label = UILabel(
            text='Разрешение',
            x=160 * self.scale_x,
            y=360 * self.scale_y,
            height=20 * self.scale_x,
            width=171 * self.scale_y,
            font_size=20 * self.scale_y,
            align='left',
            text_color=ar.color.WHITE
        )
        full_screen_label = UILabel(
            text='Полный экран',
            x=160 * self.scale_x,
            y=270 * self.scale_y,
            height=20 * self.scale_x,
            width=171 * self.scale_y,
            font_size=20 * self.scale_y,
            align='left',
            text_color=ar.color.WHITE
        )
        self.slider_label = UILabel(
            text=str(volume),
            x=544 * self.scale_x,
            y=460 * self.scale_y,
            height=21 * self.scale_x,
            width=16 * self.scale_y,
            font_size=10 * self.scale_y,
            align='left',
            text_color=ar.color.WHITE
        )
        self.slider = UISlider(
            value=volume,
            x=464 * self.scale_x,
            y=430 * self.scale_y,
            width=171 * self.scale_x,
            height=22 * self.scale_y,
            min_value=0,
            max_value=100,
            step=1
        )
        self.resolution_button = UIDropdown(
            x=464 * self.scale_x,
            y=360 * self.scale_y,
            width=171 * self.scale_x,
            height=22 * self.scale_y,
            options=[
                '800:600',
                '1600:900',
                '1920:1080',
                '2560:1440',
                '3840:2160'
            ],
            default=f'{screen_width}:{screen_height}',
            font_size=20 * self.scale_y
        )
        self.full_screen_button = UIDropdown(
            x=530 * self.scale_x,
            y=270 * self.scale_y,
            width=40 * self.scale_x,
            height=20 * self.scale_y,
            options=[
                'Да',
                'Нет'
            ],
            default=str('Да' if self.window.fullscreen else 'Нет'),
            font_size=20 * self.scale_y
        )
        self.exit_button = UIFlatButton(
            x=314 * self.scale_x,
            y=150 * self.scale_y,
            width=171 * self.scale_x,
            height=22 * self.scale_y,
            text='Назад'
        )
        self.slider.on_change = self.volume_change
        self.resolution_button.on_change = self.resolution_change
        self.full_screen_button.on_change = self.full_screen_change
        self.main_button.on_click = self.go_to_main_menu
        self.random_color_background.on_click = self.set_random_color
        self.set_default_color.on_click = self.set_color_default
        self.exit_button.on_click = self.escape
        self.manager.add(options_label)
        self.manager.add(self.set_default_color)
        self.manager.add(resolution_label)
        self.manager.add(volume_label)
        self.manager.add(self.random_color_background)
        self.manager.add(self.main_button)
        self.manager.add(full_screen_label)
        self.manager.add(self.slider_label)
        self.manager.add(self.slider)
        self.manager.add(self.full_screen_button)
        self.manager.add(self.resolution_button)
        self.manager.add(self.exit_button)
        self.ui = [
            options_label,
            resolution_label,
            full_screen_label,
            volume_label,
            self.slider_label,
            self.slider,
            self.full_screen_button,
            self.resolution_button,
            self.exit_button
        ]

    def on_draw(self) -> bool | None:
        self.clear()
        self.manager.draw()
        return

    def escape(self, event):
        self.window.show_view_new(self.window.sub_view(self.window))

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == ar.key.ESCAPE:
            self.window.show_view_new(self.window.sub_view(self.window))
        return True

    def set_color_default(self, event):
        self.background_color = ar.color.BLUE_SAPPHIRE

    def volume_change(self, event):
        global volume
        volume = int(self.slider.value)
        self.slider_label.text = str(volume)

    def set_random_color(self, event):
        self.background_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def resolution_change(self, event):
        global screen_height, screen_width
        self.scale_x, self.scale_y = ([int(i) for i in self.resolution_button.value.split(':')][0] / screen_width,
                                      [int(i) for i in self.resolution_button.value.split(':')][1] / screen_height)
        screen_width, screen_height = [int(i) for i in self.resolution_button.value.split(':')]
        self.window.set_fullscreen(False)
        self.window.set_size(screen_width, screen_height)
        self.window.options_view = OptionsScene(self.window)
        self.window.show_view(self.window.options_view)
        '''return
        global screen_height, screen_width
        self.scale_x, self.scale_y = ([int(i) for i in self.resolution_button.value.split(':')][0] / screen_width,
                                      [int(i) for i in self.resolution_button.value.split(':')][1] / screen_height)
        screen_width, screen_height = [int(i) for i in self.resolution_button.value.split(':')]
        self.window.set_size(screen_width, screen_height)
        for i in self.ui:
            x, y = i.center_x, i.center_y
            i.resize(width=i.size[0] * self.scale_x, height=i.size[1] * self.scale_y)
            i.move(x * self.scale_x - x, y * self.scale_y - y)
            try:
                i.font_size = i.font_size * self.scale
            except Exception:
                pass'''

    def go_to_main_menu(self, event):
        self.window.show_view_new(self.window.first_scene)

    def full_screen_change(self, event):
        global screen_height, screen_width
        import screeninfo
        if self.full_screen_button.value == 'Да':
            self.window.pre_size = screen_width, screen_height
            screen_width, screen_height = screeninfo.get_monitors()[0].width, screeninfo.get_monitors()[0].height
        else:
            screen_width, screen_height = self.window.pre_size
        self.window.set_fullscreen(self.full_screen_button.value == 'Да')
        self.window.options_view = OptionsScene(self.window)
        self.window.show_view(self.window.options_view)
        if not self.window.fullscreen:
            self.window.set_size(screen_width, screen_height)
        '''return
        global screen_height, screen_width
        import screeninfo
        self.scale_x, self.scale_y = (screeninfo.get_monitors()[0].width / screen_width,
                                      screeninfo.get_monitors()[0].height / screen_height)
        screen_width, screen_height = screeninfo.get_monitors()[0].width, screeninfo.get_monitors()[0].height
        self.window.set_size(screen_width, screen_height)
        for_delete = []
        for i in self.ui:
            x, y = i.center_x, i.center_y
            i.resize(width=i.size[0] * self.scale_x, height=i.size[1] * self.scale_y)
            i.move(x * self.scale_x - x, y * self.scale_y - y)
            if i is UILabel:
                self.manager.remove(i)
                for_delete.append(i)
                self.manager.add(UILabel(
                    text=i.text,
                    x=i.center_x,
                    y=i.center_y,
                    width=i.width,
                    height=i.height,
                    font_size=i.font_size * self.scale_y
                ))
        for i in for_delete:
            self.ui.remove(i)
        self.window.set_fullscreen(self.full_screen_button.value == 'Да')'''


class FirstScene(ar.View):
    def __init__(self, window):
        super().__init__(window, ar.color.BLUE_SAPPHIRE) # Поменять цвет на фон\
        global screen_height, screen_width
        self.scale_x, self.scale_y = screen_width / 800, screen_height / 600
        self.manager = UIManager()
        self.manager.enable()
        main_menu_label = UILabel(
            text="Главное Меню",
            font_size=30 * self.scale_y,
            text_color=ar.color.WHITE,
            width=400 * self.scale_x,
            align="center",
            x=200 * self.scale_x,
            y=520 * self.scale_y
        )
        play_button = UIFlatButton(
            x=285 * self.scale_x,
            y=360 * self.scale_y,
            text='Играть',
            width=230 * self.scale_x,
            height=31 * self.scale_y
        )
        options_button = UIFlatButton(
            x=285 * self.scale_x,
            y=300 * self.scale_y,
            text='Настройки',
            width=230 * self.scale_x,
            height=31 * self.scale_y
        )
        autors_button = UIFlatButton(
            x=285 * self.scale_x,
            y=240 * self.scale_y,
            text='Авторы',
            width=230 * self.scale_x,
            height=31 * self.scale_y
        )
        exit_button = UIFlatButton(
            x=285 * self.scale_x,
            y=180 * self.scale_y,
            text='Выйти',
            width=230 * self.scale_x,
            height=31 * self.scale_y
        )
        play_button.on_click = self.start_game
        exit_button.on_click = self.exit
        options_button.on_click = self.options
        autors_button.on_click = self.autors
        self.manager.add(main_menu_label)
        self.manager.add(play_button)
        self.manager.add(options_button)
        self.manager.add(autors_button)
        self.manager.add(exit_button)

    def on_draw(self) -> bool | None:
        self.clear()
        self.manager.draw()
        return

    def exit(self, event):
        self.window.close()

    def options(self, event):
        self.window.options_view = OptionsScene(self.window)
        self.window.show_view_new(self.window.options_view)

    def autors(self, event):
        self.window.show_view_new(AutorsScene(self.window))

    def start_game(self, event):
        # Включаем игровой режим в основном окне
        self.window.game_mode = True
        # Возвращаем управление основному окну
        self.window.show_view_new(self)


class AutorsScene(ar.View):
    def __init__(self, window):
        super().__init__(window)
        from random import choice, randint
        self.window = window
        global screen_height, screen_width
        self.scale_x, self.scale_y = screen_width / 800, screen_height / 600
        self.background_color = ar.color.BLUE_SAPPHIRE
        self.manager = UIManager(window)
        self.manager.enable()
        self.autors_label = UILabel(
            x=randint(50, 750) * self.scale_x,
            y=randint(50, 550) * self.scale_y,
            width=400 * self.scale_x,
            height=50 * self.scale_y,
            text='Авторы',
            align='center',
            font_size=40 * self.scale_y
        )
        self.first_autor_label = UILabel(
            x=randint(50, 750) * self.scale_x,
            y=randint(50, 550) * self.scale_y,
            width=400 * self.scale_x,
            height=50 * self.scale_y,
            text='Tim',
            align='center',
            font_size=25 * self.scale_y
        )
        self.second_autor_label = UILabel(
            x=randint(50, 750) * self.scale_x,
            y=randint(50, 550) * self.scale_y,
            width=400 * self.scale_x,
            height=50 * self.scale_y,
            text='Ner',
            align='center',
            font_size=25 * self.scale_y
        )
        self.second_autor_label.dirr = [choice((-1, 1)), choice((-1, 1))]
        self.first_autor_label.dirr = [choice((-1, 1)), choice((-1, 1))]
        self.autors_label.dirr = [choice((-1, 1)), choice((-1, 1))]
        self.ui = [
            self.autors_label,
            self.second_autor_label,
            self.first_autor_label
        ]
        self.manager.add(self.autors_label)
        self.manager.add(self.first_autor_label)
        self.manager.add(self.second_autor_label)

    def on_draw(self) -> bool | None:
        from random import randint
        import time
        self.clear()
        self.manager.draw()

    def on_update(self, delta_time: float) -> bool | None:
        from random import randint
        for i in self.ui:
            i.move(randint(0, 20) * self.scale_x * i.dirr[0] * delta_time * 60,
                   randint(0, 20) * self.scale_y * i.dirr[1] * delta_time * 60)
            if 0 >= i.center_x:
                i.dirr[0] = 1
            if i.center_x >= screen_width:
                i.dirr[0] = -1
            if 0 >= i.center_y:
                i.dirr[1] = 1
            if i.center_y >= screen_height:
                i.dirr[1] = -1

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == ar.key.ESCAPE:
            self.window.show_view_new(self.window.sub_view(self.window))
        return True

class AnimatedPlayer(arcade.Sprite):

    def __init__(self, scale=1.0):
        super().__init__(scale=scale)

        # --- Стояние с прозрачным фоном ---
        stand_image = Image.open("images_for_game/PMCStand.bmp").convert("RGBA")

        # ---- делаем белый цвет прозрачным ----
        datas = stand_image.getdata()
        newData = []
        for item in datas:
            if item[0] > 240 and item[1] > 240 and item[2] > 240:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        stand_image.putdata(newData)

        # превращаем в texture для arcade
        buf = io.BytesIO()
        stand_image.save(buf, format="PNG")
        buf.seek(0)
        self.stand_texture = arcade.load_texture(buf)
        self.texture = self.stand_texture

        # --- Бег (GIF → два списка текстур: вправо и влево) ---
        self.run_textures_right = []
        self.run_textures_left = []

        gif = Image.open("images_for_game/KahkisRun.gif")
        for i in range(gif.n_frames):
            gif.seek(i)
            frame = gif.convert("RGBA")

            # ---- делаем белый цвет прозрачным ----
            datas = frame.getdata()
            newData = []
            for item in datas:
                # если почти белый, делаем прозрачным
                if item[0] > 240 and item[1] > 240 and item[2] > 240:
                    newData.append((255, 255, 255, 0))
                else:
                    newData.append(item)
            frame.putdata(newData)

            # обычный кадр (вправо)
            buf = io.BytesIO()
            frame.save(buf, format="PNG")
            buf.seek(0)
            tex_right = arcade.load_texture(buf)
            self.run_textures_right.append(tex_right)

            # зеркальный кадр (влево)
            frame_left = frame.transpose(Image.FLIP_LEFT_RIGHT)
            buf_left = io.BytesIO()
            frame_left.save(buf_left, format="PNG")
            buf_left.seek(0)
            tex_left = arcade.load_texture(buf_left)
            self.run_textures_left.append(tex_left)

        # --- Состояние анимации ---
        self.state = "stand"
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_duration = 100  # мс на кадр

        # --- Направление ---
        self.facing_right = True

    # --- переключение состояния ---
    def run(self):
        self.state = "run"

    def stand(self):
        self.state = "stand"
        if self.facing_right:
            self.texture = self.stand_texture
        else:
            self.texture = self.stand_texture.flip_horizontally()

    # --- обновление анимации ---
    def update_animation(self, delta_time: float):
        if self.state == "run":
            self.frame_timer += delta_time * 1000
            if self.frame_timer >= self.frame_duration:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.run_textures_right)

                # выбираем направление
                if self.facing_right:
                    self.texture = self.run_textures_right[self.current_frame]
                else:
                    self.texture = self.run_textures_left[self.current_frame]

    # --- установка направления ---
    def set_direction(self, right: bool):
        self.facing_right = right
        if self.state == "stand":
            self.stand()

class Bullet(arcade.Sprite):
    def __init__(self, texture: arcade.Texture, start_x: float, start_y: float, facing_right: bool, speed: float = 500):
        super().__init__(texture, scale=1.0)
        self.center_x = start_x + 20
        self.center_y = start_y + 25
        self.speed = speed

        if facing_right:
            self.change_x = self.speed  # летит вправо
            self.angle = 0
        else:
            self.change_x = -self.speed  # летит влево
            self.angle = 180

        self.change_y = 0

    def update(self, delta_time: float):
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

class Game(ar.Window):

    def __init__(self):
        super().__init__(screen_width, screen_height, TITLE)
        arcade.set_background_color(arcade.color.TEA_GREEN)
        self.first_scene = FirstScene(self)
        self.options_view = OptionsScene(self)
        self.sub_view = self.first_scene.__class__
        self.game_mode = False
        self.pres_view = self.first_scene.__class__
        self.show_view_new(self.first_scene)
        self.sub_view = self.first_scene
        self.on_resize_old = self.on_resize
        # ===== Игрок =====
        self.player = AnimatedPlayer(scale=1.5)
        self.player.center_x = screen_width // 2
        self.player.center_y = screen_height // 2

        # Список спрайтов
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        # Платформа
        self.platform = arcade.SpriteSolidColor(
            width = 700,
            height = 20,
            color = arcade.color.BLACK
         )
        self.platform1 = arcade.SpriteSolidColor(
            width=400,
            height=20,
            color=arcade.color.BLACK
        )
        self.platform.center_x = screen_width // 2
        self.platform.center_y = screen_height // 2 - 30

        self.platform1.center_x = screen_width // 2 + 300
        self.platform1.center_y = screen_height // 2 + 200

        self.platform_list = arcade.SpriteList()
        self.platform_list.append(self.platform)
        self.platform_list.append(self.platform1)

        # ===== КАМЕРА Camera2D =====
        self.camera = ar.camera.Camera2D(
            position=(self.player.center_x, self.player.center_y)
        )
        # ========================================

        # Флаги движения
        self.moving_left = False
        self.moving_right = False
        self.jump = False
        self.speed = 200  # пикселей в секунду

        self.is_jumping = False
        self.vertical_speed = 0
        self.gravity = 1000
        self.jump_strength = 700
        self.ground_level = screen_height // 2 - 10

        self.bullet_list = arcade.SpriteList()  # Список для хранения всех пуль
        try:
            self.bullet_texture = arcade.load_texture("images_for_game/bullet.png")
        except FileNotFoundError:
            print("Файл images_for_game/bullet.png не найден.")
            self.bullet_texture = None


    #def on_resize(self, width: int, height: int) -> EVENT_HANDLE_STATE:
#       self.on_resize_old(screen_width, screen_height)

    def show_view_new(self, new_view: View) -> None:
        self.sub_view = self.pres_view
        self.pres_view = new_view.__class__
        self.show_view(new_view)

        # ===== Отрисовка =====

    def on_draw(self):
        self.clear()
        if self.game_mode:
            self.camera.use()
            self.platform_list.draw()
            self.player_list.draw()
            self.bullet_list.draw()
        else:
            # Рисуем текущую сцену (меню)
            if self.current_view:
                self.current_view.on_draw()



        # ===== Обновление =====

    def on_update(self, delta_time):
        if self.game_mode:
            # Обновляем игровую логику
            if self.moving_left:
                self.player.center_x -= self.speed * delta_time
                self.player.set_direction(False)
            if self.moving_right:
                self.player.center_x += self.speed * delta_time
                self.player.set_direction(True)

            if self.moving_left or self.moving_right:
                self.player.run()
            else:
                self.player.stand()

            self.vertical_speed -= self.gravity * delta_time

            # Изменяем позицию по Y
            self.player.center_y += self.vertical_speed * delta_time

            collisions = self.player.collides_with_list(self.platform_list)
            if collisions:
                if self.vertical_speed < 0:
                    platform = collisions[0]
                    self.player.center_y = platform.center_y + platform.height / 2 + self.player.height / 2
                    self.vertical_speed = 0
                    self.is_jumping = False

            if self.jump and not self.is_jumping:
                self.vertical_speed = self.jump_strength
                self.is_jumping = True

            left_boundary = self.camera.position[0] - screen_width // 2
            right_boundary = self.camera.position[0] + screen_width // 2
            bottom_boundary = self.camera.position[1] - screen_height // 2

            if (self.player.center_y < bottom_boundary - 100 or
                    self.player.center_x < left_boundary - 200 or
                    self.player.center_x > right_boundary + 200):

                self.player.center_x = self.platform.center_x
                self.player.center_y = self.platform.center_y + self.platform.height / 2 + self.player.height / 2
                self.vertical_speed = 0
                self.is_jumping = False
                print("Игрок восстановлен на платформе!")  # Для отладки*

            # Камера следует за игроком
            target_x = self.player.center_x
            target_y = self.player.center_y
            self.camera.position = (
                self.camera.position[0] + (target_x - self.camera.position[0]) * 0.1,
                self.camera.position[1] + (target_y - self.camera.position[1]) * 0.1
            )

            self.player_list.update_animation(delta_time)

            self.bullet_list.update(delta_time)

            camera_left = self.camera.position[0] - screen_width // 2 - 100
            camera_right = self.camera.position[0] + screen_width // 2 + 100
            bullets_to_remove = []
            for bullet in self.bullet_list:
                if bullet.center_x < camera_left or bullet.center_x > camera_right:
                    bullets_to_remove.append(bullet)

            # Удаляем их после цикла
            for bullet in bullets_to_remove:
                bullet.remove_from_sprite_lists()


    # ===== Нажатие клавиши =====
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.A:
            self.moving_left = True
            self.player.set_direction(False)
        elif symbol == arcade.key.D:
            self.moving_right = True
            self.player.set_direction(True)
        if symbol == arcade.key.SPACE:
            self.jump = True


    # ===== Отпуск клавиши =====
    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.A:
            self.moving_left = False
            self.player.set_direction(False)
        elif symbol == arcade.key.D:
            self.moving_right = False
            self.player.set_direction(True)
        if symbol == arcade.key.SPACE:
            self.jump = False

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.game_mode and button == arcade.MOUSE_BUTTON_LEFT:
            if self.bullet_texture:
                bullet = Bullet(
                    texture=self.bullet_texture,
                    start_x=self.player.center_x,
                    start_y=self.player.center_y,
                    facing_right=self.player.facing_right,
                    speed=600
                )

                self.bullet_list.append(bullet)
if __name__ == "__main__":
    window = Game()  # Создаём окно
    arcade.run()
