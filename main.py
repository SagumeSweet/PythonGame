from typing import override

import arcade

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 650
WINDOW_TITLE = "Platformer"

CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5

INIT_LOCATION = (64, 128)

# 玩家的移动速度，以每帧像素为单位
PLAYER_MOVEMENT_SPEED = 5

# 重力加速度
GRAVITY = 1
# 玩家跳跃速度
PLAYER_JUMP_SPEED = 20

# 滚动范围
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100


class Game1(arcade.Window):
    """
    安装并打开窗口
    """

    def __init__(self):
        # 初始化父类并设置窗口
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """
        初始化
        """
        pass

    @override
    def on_draw(self):
        """
        渲染屏幕
        """
        self.clear()


class Game2(Game1):
    """
    添加精灵
    """

    @override
    def __init__(self):
        super().__init__()
        # 创建纹理
        self._player_texture = arcade.load_texture(":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png")
        self._grass_texture = arcade.load_texture(":resources:images/tiles/grassMid.png")
        self._coordinate_texture = arcade.load_texture(":resources:images/tiles/boxCrate_double.png")

        # 创建精灵
        self._player_sprite = None
        # 创建精灵列表
        self._player_list = None
        # 创建墙壁列表
        self._wall_list = None

    @override
    def setup(self):
        """
        有了 setup 方法，以后可以很容易地在游戏中添加重置功能。调用setup函数将重置所有内容
        """
        # 创建玩家列表
        self._player_list = arcade.SpriteList()
        # 创建墙壁列表
        # 当设置use_spatial_hash参数为 True 时，Arcade 会使用一种叫做 空间哈希（spatial hash） 的算法来优化碰撞检测。
        # 适合静态对象（不会动的，比如地板、墙），碰撞检测的性能大幅提升，特别是对象很多的时候
        self._wall_list = arcade.SpriteList(use_spatial_hash=True)

        # 创建玩家
        self._player_sprite = arcade.Sprite(self._player_texture, scale=CHARACTER_SCALING)
        self._player_sprite.center_x = INIT_LOCATION[0]
        self._player_sprite.center_y = INIT_LOCATION[1]
        self._player_list.append(self._player_sprite)

        # 创建背景, 使用循环水平放置多个精灵
        for x in range(0, 1250, 64):
            wall = arcade.Sprite(self._grass_texture, scale=TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self._wall_list.append(wall)

        # 把一些板条箱放在地上, 使用坐标列表来放置精灵
        coordinate_list = [[512, 96], [256, 96], [768, 96]]
        for coordinate in coordinate_list:
            # 添加一个地板
            wall = arcade.Sprite(self._coordinate_texture, scale=TILE_SCALING)
            wall.position = coordinate
            self._wall_list.append(wall)

    @override
    def on_draw(self):
        super().on_draw()
        # 绘制精灵
        self._player_list.draw()
        self._wall_list.draw()


class Game3(Game2):
    """
    添加用户控制
    """
    @override
    def __init__(self):
        super().__init__()
        # 创建物理引擎
        self._physics_engine = None
        # 是否在按移动按键
        self._is_left_moving = False
        self._is_right_moving = False

    @override
    def setup(self):
        super().setup()
        # 创建物理引擎
        self._physics_engine = arcade.PhysicsEnginePlatformer(
            self._player_sprite, self._wall_list
        )

    def _left_right_press(self, key: int):
        """
        水平移动
        """
        if key == arcade.key.LEFT or key == arcade.key.A:
            self._is_left_moving = True
            self._player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self._is_right_moving = True
            self._player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def _up_down_press(self, key: int):
        """
        垂直移动
        """
        if key == arcade.key.UP or key == arcade.key.X:
            self._player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self._player_sprite.change_y = -PLAYER_MOVEMENT_SPEED

    @override
    def on_key_press(self, key: int, modifiers: int):
        """
        键盘按下事件
        """
        if key == arcade.key.ESCAPE:
            self.setup()
        self._up_down_press(key)
        self._left_right_press(key)

    def _on_left_right_release(self, key: int):
        if key == arcade.key.LEFT or key == arcade.key.A and self._is_left_moving:
            self._is_left_moving = False
            if self._is_right_moving:
                self._player_sprite.change_x = PLAYER_MOVEMENT_SPEED
            else:
                self._player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D and self._is_right_moving:
            self._is_right_moving = False
            if self._is_left_moving:
                self._player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
            else:
                self._player_sprite.change_x = 0

    def _on_up_down_release(self, key: int):
        if key == arcade.key.UP or key == arcade.key.X or key == arcade.key.DOWN or key == arcade.key.S:
            self._player_sprite.change_y = 0

    @override
    def on_key_release(self, key: int, modifiers: int):
        """
        键盘释放事件
        """
        self._on_left_right_release(key)
        self._on_up_down_release(key)

    @override
    def on_update(self, delta_time: float):
        """
        更新游戏状态
        """
        # 用物理引擎移动玩家
        self._physics_engine.update()
        print(self._player_sprite.change_y)
        if self._player_sprite.center_y < -1000:
            self.setup()
        return super().on_update(delta_time)


class Game4(Game3):
    """
    添加重力
    """

    @override
    def setup(self):
        super().setup()
        # 添加重力
        self._physics_engine = arcade.PhysicsEnginePlatformer(
            self._player_sprite, walls=self._wall_list, gravity_constant=GRAVITY
        )

    @override
    def _up_down_press(self, key: int):
        if (key == arcade.key.UP or key == arcade.key.X) and self._physics_engine.can_jump():
            self._player_sprite.change_y = PLAYER_JUMP_SPEED
        if key == arcade.key.DOWN or key == arcade.key.S:
            self._player_sprite.change_y = -PLAYER_MOVEMENT_SPEED

    @override
    def _on_up_down_release(self, key: int):
        pass


class Game5(Game4):
    """
    添加滚动
    """

    @override
    def __init__(self):
        super().__init__()
        # 创建相机
        self._camera = None

    @override
    def setup(self):
        super().setup()
        # 创建相机
        self._camera = arcade.Camera2D(position=(self.width / 2, self.height / 2))

    def _draw_world(self):
        """
        绘制世界
        """
        self._player_list.draw()
        self._wall_list.draw()

    @override
    def on_draw(self):
        """
        渲染屏幕
        """
        self.clear()
        # 切换到相机
        with self._camera.activate():
            # 绘制世界
            self._draw_world()

    @override
    def on_update(self, delta_time: float):
        super().on_update(delta_time)
        # 更新相机
        self._camera.position = self._update_camera()

    def _update_camera(self) -> tuple[float, float]:
        """
        根据玩家位置更新相机
        """
        # 获取玩家位置
        player_x = self._player_sprite.center_x
        player_y = self._player_sprite.center_y

        # 相机位置
        new_x: float = self._camera.position[0]
        new_y: float = self._camera.position[1]

        # 水平滚动
        left_length: float = self.width / 2 - LEFT_VIEWPORT_MARGIN
        right_length: float = self.width / 2 - RIGHT_VIEWPORT_MARGIN
        left_max: float = new_x - left_length
        # 玩家距离边界距离
        distance: float = player_x - left_max

        if distance < 0:
            new_x = player_x + left_length
        elif distance > left_length + right_length:
            new_x = player_x - right_length

        # 垂直滚动
        top_length: float = self.height / 2 - TOP_VIEWPORT_MARGIN
        bottom_length: float = self.height / 2 - BOTTOM_VIEWPORT_MARGIN
        bottom_max: float = new_y - bottom_length
        # 玩家距离边界距离
        distance = player_y - bottom_max
        if distance < 0:
            new_y = player_y + bottom_length
        elif distance > bottom_length + top_length:
            new_y = player_y - top_length

        return new_x, new_y


class Game6(Game5):
    """
    添加硬币和声音
    """

    @override
    def __init__(self):
        super().__init__()
        # 创建金币纹理
        self._coin_texture = arcade.load_texture(":resources:images/items/coinGold.png")

        # 添加声音
        self._coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self._jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")

        # 创建金币列表
        self._coin_list = None

    @override
    def setup(self):
        super().setup()
        self._coin_list = arcade.SpriteList(use_spatial_hash=True)
        # 添加金币
        for x in range(0, 1250, 64):
            coin = arcade.Sprite(self._coin_texture, scale=COIN_SCALING)
            coin.center_x = x
            coin.center_y = 128
            self._coin_list.append(coin)

    @override
    def _up_down_press(self, key: int):
        if (key == arcade.key.UP or key == arcade.key.X) and self._physics_engine.can_jump():
            self._player_sprite.change_y = PLAYER_JUMP_SPEED
            # 播放跳跃声音
            arcade.play_sound(self._jump_sound)
        if key == arcade.key.DOWN or key == arcade.key.S:
            self._player_sprite.change_y = -PLAYER_MOVEMENT_SPEED

    def _on_catch_coin(self, coin_hit_list: list[arcade.Sprite]):
        """
        检测金币碰撞
        """
        # 删除碰撞的金币
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            # 播放金币声音
            arcade.play_sound(self._coin_sound)

    @override
    def on_update(self, delta_time: float):
        super().on_update(delta_time)
        # 检测碰撞
        coin_hit_list = arcade.check_for_collision_with_list(
            self._player_sprite, self._coin_list
        )
        self._on_catch_coin(coin_hit_list)

    @override
    def _draw_world(self):
        """
        绘制世界
        """
        super()._draw_world()
        # 绘制金币
        self._coin_list.draw()


class Game7(Game6):
    """
    显示分数
    """

    @override
    def __init__(self):
        super().__init__()
        # 声明GUI相机
        self._gui_camera = None
        self._score = 0
        self._score_text = None

    @override
    def setup(self):
        super().setup()
        # 创建GUI相机
        self._gui_camera = arcade.Camera2D()
        self._score = 0
        self._score_text = arcade.Text(f"Score: {self._score}", x=0, y=5)

    def _draw_gui(self):
        """
        绘制用户界面
        """
        # 绘制分数
        self._score_text.draw()

    @override
    def on_draw(self):
        super().on_draw()
        # 切换到GUI相机
        with self._gui_camera.activate():
            # 绘制用户界面
            self._draw_gui()

    @override
    def _on_catch_coin(self, coin_hit_list: list[arcade.Sprite]):
        """
        收集金币处理
        """
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            # 播放金币声音
            arcade.play_sound(self._coin_sound)
            # 更新分数
            self._score += 1
            self._score_text.text = f"Score: {self._score}"


def main(game_type: type[Game1]):
    game = game_type()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main(Game7)
