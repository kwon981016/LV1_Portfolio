# -*- coding: utf-8 -*-
import random
from time import sleep
import winsound
winsound.PlaySound('battle.mp3', winsound.SND_FILENAME)

import pygame
from pygame.locals import *
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 640
gameDisplay = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (250, 250, 50)
RED = (250, 50, 50)

FPS = 60


# 전투기 클래스 = 전투기 생성 하는거

class Fighter(pygame.sprite.Sprite):
    def __init__(self):
        super(Fighter, self).__init__()
        self.fighter_images = ['fighter.png', 'shieldfighter.png']
        self.image = pygame.image.load(self.fighter_images[0])  # 이미지 불러오기
        self.rect = self.image.get_rect()
        self.rect.x = int(WINDOW_WIDTH / 2)  # 전투기 x 축 위치
        self.rect.y = WINDOW_HEIGHT - self.rect.height  # 전투기 y 축 위치
        self.dx = 0  # 초기 전투기 방향설정 x 축
        self.dy = 0  # 초기 전투기 방향설정 y 축

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.x < 0 or self.rect.x + self.rect.width > WINDOW_WIDTH:
            self.rect.x -= self.dx
            # 만약 전투기가 옆으로 화면을 벗어나려고 하면 못 벗어나게 조건을 준다.

        if self.rect.y < 0 or self.rect.y + self.rect.height > WINDOW_HEIGHT:
            self.rect.y -= self.dy
                # 전투기가 위로 화면을 벗어나려고 하면 못 벗어나게 조건을 준다.

    def get_shield(self, shield):  # 쉴드
        self.shield = shield

    def draw(self, screen, shield):
        screen.blit(pygame.image.load(self.fighter_images[shield]), self.rect)

    # self = 전투기 이니까 스크린에 보여주는거 전투기를

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite


# 전투기 self 가 충돌을 하면( 반복문 이니 반복될때마다 ) / 리턴 시켜라

# 날라가는 투기체 생성

class Missile(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed, missile_num):  # 초기화 시켜주는 작업 / 미사일의 x포지션, y포지션, 속도를 초기화 할 예정
        super(Missile, self).__init__()  # super 상속시켜 self 정보를 가져오다
        self.missile_images = ['missile.png', 'boss_missile.png']  # 미사일과 보스 미사일
        self.missile_num = missile_num
        self.image = pygame.image.load(self.missile_images[self.missile_num])  # 투기체 이미지 가져오기
        self.rect = self.image.get_rect()  # self 이미지를 넣어주는?
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed
        self.sound = pygame.mixer.Sound('missile.wav')
        self.sound.set_volume(0.15)

    # 우주선에서 투기체가 날라가기 때문에 우주선에 위치를 이렇게 넣어주는거랜다

    def launch(self):
        self.sound.play()  # 미사일 날라갈때 소리 내주는 장치

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y + self.rect.height < 0:
            self.kill()
        # 미사일 이 수직으로만 움직이기 때문에 y 값만 설정
        # y가 천장 끝까지 올라가면 사라진다는 조건을 주었다.

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite  # 여기도 미사일이 충돌한다면 이라는 조건을 준거


class Rock(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Rock, self).__init__()  # 장애물 클래스 생성 후 받아올 거 또 받아옴
        rock_images = ('v1.png', 'v2.png', 'v3.png', 'v4.png', 'v5.png')

        self.image = pygame.image.load(random.choice(rock_images))
        # 장애물(이미지) 를 랜덤으로 떨어지게 만드는 작업
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    def all_kill(self):
        self.kill()

    def out_of_screen(self):
        if self.rect.y > WINDOW_HEIGHT:
            return True
class Rock2(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed,hp=3):
        super(Rock2, self).__init__()  # 장애물 클래스 생성 후 받아올 거 또 받아옴
        rock_images2 = ('vv2.png', 'vv1.png','vv3.png', 'vv4.png', 'vv5.png')

        self.image = pygame.image.load(random.choice(rock_images2))
        # 장애물(이미지) 를 랜덤으로 떨어지게 만드는 작업
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed
        self.hp = hp

    def update(self):
        self.rect.y += self.speed

    def all_kill(self):
        self.kill()

    def out_of_screen(self):
        if self.rect.y > WINDOW_HEIGHT:
            return True
# 운석은 위 > 아래로 떨어지니까 y값만, 스크린 밖으로 가면 True를 줘서 무슨상황을 만들예정


class Item(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, item_num):
        super(Item, self).__init__()
        item_images = ('item1.png', 'item2.png', 'item3.png', 'item4.png')
        
        self.item_num = item_num
        self.image = pygame.image.load(item_images[self.item_num])
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos

    def Item_num(self):
        return self.item_num

    def update(self):
        self.rect.y += 2

    def out_of_screen(self):
        if self.rect.y > WINDOW_HEIGHT:
            return True

class Boss(pygame.sprite.Sprite):  # 보스
    def __init__(self):
        super(Boss, self).__init__()
        self.image = pygame.image.load('boss.png')  # 보스 이미지
        self.rect = self.image.get_rect()
        self.rect.x = (WINDOW_WIDTH/2) - (self.rect.width)/2
        self.rect.y = -self.rect.height


    def draw(self, screen):
        screen.blit(pygame.image.load('boss.png'), self.rect)

    def update(self, boss_speedx,boss_speed):
        self.rect.x += boss_speedx
        self.rect.y += boss_speed

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite



def draw_text(text, font, surface, x, y, main_color):
    # 화면 텍스트 설정
    text_obj = font.render(text, True, main_color)
    text_rect = text_obj.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_obj, text_rect)  # blit 화면에 그리는거래


def occur_explosion(surface, x, y):
    explosion_image = pygame.image.load('explosion.png')
    explosion_rect = explosion_image.get_rect()
    explosion_rect.x = x
    explosion_rect.y = y
    surface.blit(explosion_image, explosion_rect)

    # 폭팔 이라는 함수를 넣어 폭팔이미지 그리는거,  x, y 축 설정

    explosion_sounds = ('explosion01.wav', 'explosion02.wav', 'explosion03.wav')
    explosion_sound = pygame.mixer.Sound(random.choice(explosion_sounds))
    explosion_sound.play()
    explosion_sound.set_volume(0.10)

    # 폭팔음을 랜덤으로 골라서 mixer(재생) 하는걸 설정 -1 무한반복



def game_loop():
    default_font = pygame.font.Font('NanumGothic.ttf', 28)
    background_image = pygame.image.load('background.png')
    gameover_img = pygame.image.load('gameover.png')
    gamewin_img = pygame.image.load('winbg.png')
    gameover_sound = pygame.mixer.Sound('gameover.wav')
    gameclear_sound = pygame.mixer.Sound('clear.mp3')
    gameover_sound.set_volume(0.40)
    gameclear_sound.set_volume(0.60)
    pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.20)

    # loop
    fps_clock = pygame.time.Clock()

    # 각 소리와 폰트를 불러오기 설정, 배경음악은 따로 지정 안하고 불러옴. -1 은 무한반복이라는 뜻

    fighter = Fighter()
    boss = Boss()
    missiles = pygame.sprite.Group()
    rocks = pygame.sprite.Group()
    rocks2 = pygame.sprite.Group()
    items = pygame.sprite.Group()
    boss_missiles = pygame.sprite.Group()
    
    # 미사일과 장애물은 스프라이트에 그룹으로 설정 이유는 많이 들어가서

    occur_prob1 = 100  # 확률적으로 얼마나 나오는지
    occur_prob2 = 200
    shot_count = 0

    count_missed = 0
    total_time = 30
    start_ticks = pygame.time.get_ticks()
    count_skill = 0

    fighter_speed = 3.5  # 초기 전투기 속도
    missile_speed = 5  # 초기 미사일 속도
    missile_num = 1  # 초기 미사일 개수
    shield = 0  # 초기 쉴드 개수
    boss_speed = 1  # 초기 보스 y 속도
    boss_speedx = 1 # 초기 보스 x 속도
    boss_hp = 60  # 보스 체력

    m1 = pygame.image.load('missile.png')  # 미사일 이미지 가져오기
    missileSize = m1.get_rect().size  # 미사일 크기 불러오기
    missileWidth = missileSize[0]  # 미사일 가로 길이

    done = False
    while not done:

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    fighter.dx -= fighter_speed
                elif event.key == pygame.K_RIGHT:
                    fighter.dx += fighter_speed
                elif event.key == pygame.K_UP:
                    fighter.dy -= fighter_speed
                elif event.key == pygame.K_DOWN:
                    fighter.dy += fighter_speed
                elif event.key == pygame.K_SPACE:
                    if missile_num == 1:
                        missile = Missile(fighter.rect.centerx - missileWidth/2, fighter.rect.y, missile_speed, 0)  # x의 정 가운데에서 미사일이 나간다
                        missile.launch()
                        missiles.add(missile)  # 미사일스 에 미사일 그룹을 추가
                    if missile_num == 2:
                        missile1 = Missile(fighter.rect.x, fighter.rect.y, missile_speed, 0)
                        missile2 = Missile(fighter.rect.x + fighter.rect.width - missileWidth, fighter.rect.y, missile_speed, 0)
                        missile1.launch()
                        missile2.launch()
                        missiles.add(missile1)
                        missiles.add(missile2)
                    if missile_num == 3:
                        missile1 = Missile(fighter.rect.x, fighter.rect.y, missile_speed, 0)
                        missile2 = Missile(fighter.rect.centerx - missileWidth/2, fighter.rect.y, missile_speed, 0)
                        missile3 = Missile(fighter.rect.x + fighter.rect.width - missileWidth, fighter.rect.y, missile_speed, 0)
                        missile1.launch()
                        missile2.launch()
                        missile3.launch()
                        missiles.add(missile1)
                        missiles.add(missile2)
                        missiles.add(missile3)

                elif event.key == pygame.K_a:
                    explosion_sounds = ('Pew.mp3')
                    explosion_sound = pygame.mixer.Sound((explosion_sounds))
                    explosion_sound.play()
                    explosion_sound.set_volume(0.10)



                    if count_skill == 0:
                        for rock in rocks:
                            rock.all_kill()
                        total_time = total_time + 10
                        count_skill = count_skill + 1

                    if count_skill == 1:
                        for rock2 in rocks2:
                            rock2.all_kill()
                        total_time = total_time + 10
                        count_skill = count_skill + 1
                        
                elif event.key == pygame.K_ESCAPE:
                    done = True


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a:
                    fighter.dx = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    fighter.dy = 0

        screen.blit(background_image, background_image.get_rect())

        occur_of_rocks = 2 + int(shot_count / 40)
        min_rock_speed = 1 + int(shot_count / 80)
        max_rock_speed = 1 + int(shot_count / 40)
        occur_of_rocks2 = 2 + int(shot_count / 80)
        min_rock2_speed = 1 + int(shot_count / 80)
        max_rock2_speed = 1 + int(shot_count / 40)
        # 장애물 파괴 카운트에 따라 난이도 줘서 떨어지는 장애물 양
        # 떨어지는 속도 를 더 해 난이도를 줌

        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
        timer = (str(int(total_time - elapsed_time)))

        if random.randint(1, occur_prob1) == 1 and elapsed_time < 100:
            for i in range(occur_of_rocks):
                speed = random.randint(min_rock_speed, max_rock_speed)
                rock = Rock(random.randint(0, WINDOW_WIDTH - 30), 0, speed)
                rocks.add(rock)
        if random.randint(1, occur_prob2) == 1 and elapsed_time < 100:
            for j in range(occur_of_rocks2):
                hp = 3
                speed = random.randint(min_rock2_speed, max_rock2_speed)
                rock2 = Rock2(random.randint(0, WINDOW_WIDTH - 30), 0, speed,hp)
                rocks2.add(rock2)

                
        # 40/1 확률 속도 랜덤은 민락스피드, 맥스스피드, 설정, x좌표는 -30 준거, y값은 0으로 떨어지는거

        if int(shot_count) > 50:


           # 여기 배경노래가 종료되고 다른 노래가 나왔으면 좋겠다 안되면 포기




            if boss.rect.y > 100:
                boss_speed = -1
            if boss.rect.y < - 50:
                boss_speed = 1

            if boss.rect.x < 0:
                boss_speedx = 1
            if boss.rect.x > WINDOW_WIDTH - boss.rect.width:
                boss_speedx = -1

            if boss.collide(missiles):
                missile = boss.collide(missiles)
                if missile:
                    missile.kill()
                    boss_hp -= 1
                    print(boss_hp)
                    if boss_hp < 1:
                        pygame.mixer_music.stop()
                        occur_explosion(screen, boss.rect.x, boss.rect.y)
                        pygame.display.update()
                        screen.blit(gamewin_img, gamewin_img.get_rect())
                        gameclear_sound.play()
                        pygame.display.update()
                        sleep(9)
                        done = True

            if random.randint(1, 30) == 1:
                speed = -3
                missile = Missile(random.randint(boss.rect.x, boss.rect.x + boss.rect.width), boss.rect.y + boss.rect.height, speed, 1)
                boss_missiles.add(missile)
                
            boss.draw(screen)
            boss.update(boss_speedx, boss_speed)
            boss_missiles.draw(screen)
            boss_missiles.update()

        if fighter.collide(boss_missiles):
            boss_missile = fighter.collide(boss_missiles)
            if shield == 0:
                pygame.mixer_music.stop()
                occur_explosion(screen, fighter.rect.x, fighter.rect.y)
                gameover_sound.play()
                screen.blit(gameover_img, gameover_img.get_rect())
                pygame.display.update()
                sleep(1)
                done = True
            else:
                shield = 0
                boss_missile.kill()

        draw_text('남은 시간: {} '.format(timer), default_font, screen, 85, 15, BLACK)
        draw_text('score: {}'.format(shot_count), default_font, screen, 60, 45, BLACK)  # shot_count로 추가시간 표현
        draw_text('팀: 일기예보', default_font, screen, 400, 15, BLACK)  # 팀명 표기
        """draw_text('박영범', default_font, screen, 400, 45, WHITE)
        draw_text('김예진', default_font, screen, 400, 75, WHITE)
        draw_text('권승현', default_font, screen, 400, 105, WHITE)
        draw_text('송하명', default_font, screen, 400, 135, WHITE)
        draw_text('오병훈', default_font, screen, 400, 165, WHITE)
        draw_text('최상준', default_font, screen, 400, 195, WHITE)"""

        # default 폰트로 저장, 스크린, x좌표값, y좌표값, 색 순으로 작성
        # show count 기준으로 일정 수치 이상일시 보스몹 스

        for missile in missiles:
            rock = missile.collide(rocks)
            if rock:
                missile.kill()
                rock.kill()
                occur_explosion(screen, rock.rect.x, rock.rect.y)
                shot_count += 1
                total_time += 1
        for missile in missiles:
            rock2 = missile.collide(rocks2)
            if rock2:
                missile.kill()
                rock2.hp-=1
                if rock2.hp == 0:
                    rock2.kill()
                    occur_explosion(screen, rock2.rect.x, rock2.rect.y)
                    item_type = random.randrange(20)
                    if item_type == 0:  # 1/20 확률로 0번 아이템
                        item_num = 0
                    elif item_type == 1 or item_type == 2 or item_type == 3:  # 3/20 확률로 1번 아이템
                        item_num = 1
                    elif 3 < item_type < 12:  # 2/5 확률로 2번 아이템
                        item_num = 2
                    else:  # 2/5 확률로 3번 아이템
                        item_num = 3
                    item = Item(rock2.rect.x, rock2.rect.y, item_num)
                    items.add(item)
                    
                    
                shot_count += 1
                total_time += 1

        # 미사일이 장애물 맞으면 장애물, 미사일 사라짐, 카운터 올라감 설정
        # 장애물 폭팔 이미지, 장애물 x,y 값 설정

        for rock in rocks:
            if rock.out_of_screen():
                rock.kill()
                count_missed += 1
                total_time -= 1  # 화면을 벗어날시 -1초
        for rock2 in rocks2:
            if rock2.out_of_screen():
                rock2.kill()
                count_missed += 1
                total_time -= 1

        for item in items:
            if item.out_of_screen():
                item.kill()

        if fighter.collide(items):
            item = fighter.collide(items)
            item.kill()
            
            if item.Item_num() == 0:  # 미사일 개수 증가
                missile_num += 1
                if missile_num > 3:  # 미시일 개수 최대 3개
                    missile_num = 3
            elif item.Item_num() == 1:  # 쉴드 
                shield = 1
            elif item.Item_num() == 2:  # 전투기 속도 증가
                fighter_speed += 0.1
            elif item.Item_num() == 3:  # 미사일 속도 증가
                missile_speed += 0.1

        # 장애물이 화면 밑으로 내려가면 장애물 삭제, 놓친갯수 1 증가S

        rocks.update()
        rocks.draw(screen)
        rocks2.update()
        rocks2.draw(screen)
        missiles.update()
        missiles.draw(screen)
        fighter.update()
        fighter.draw(screen, shield)
        items.update()
        items.draw(screen)       
        pygame.display.flip()

        # 각 항목들을 위에 내용으로 업데이트  한다는 뜻 그 걸 filp() 전체반영 해주는거래

        if fighter.collide(rocks):
            rock = fighter.collide(rocks)
            if shield == 0:
                pygame.mixer_music.stop()
                occur_explosion(screen, fighter.rect.x, fighter.rect.y)
                pygame.display.update()
                screen.blit(gameover_img, gameover_img.get_rect())
                gameover_sound.play()
                pygame.display.update()
                sleep(1)
                done = True
            else:
                shield = 0
                rock.kill()
                
        if fighter.collide(rocks2):
            rock2 = fighter.collide(rocks2)
            if shield == 0:
                pygame.mixer_music.stop()
                occur_explosion(screen, fighter.rect.x, fighter.rect.y)
                pygame.display.update()
                screen.blit(gameover_img, gameover_img.get_rect())
                gameover_sound.play()
                pygame.display.update()
                sleep(1)
                done = True
            else:
                shield = 0
                rock2.kill()

        if int(timer) <= 0:  # 타임 오버
            pygame.mixer_music.stop()
            occur_explosion(screen, fighter.rect.x, fighter.rect.y)
            gameover_sound.play()
            screen.blit(gameover_img, gameover_img.get_rect())
            pygame.display.update()
            sleep(1)
            done = True

        # 게임이 끝나는 조건을 줌 장애물 맞거나, 3개놓치면 노래종료, 전투기 폭팔, 디스플레이 업데이트,
        # 게임오버 노래 나오고 2초정도 화면이 쉰다. done = true 반복문 종료됨

        fps_clock.tick(FPS)

    return 'game_menu'


def game_menu():
    start_image = pygame.image.load('background.png')
    screen.blit(start_image, [0, 0])
    draw_x = int(WINDOW_WIDTH / 2)
    draw_y = int(WINDOW_HEIGHT / 4)
    font_70 = pygame.font.Font('NanumGothic.ttf', 70)
    font_40 = pygame.font.Font('NanumGothic.ttf', 40)

    draw_text('코로나 헌터', font_70, screen, draw_x, draw_y - 100, RED)
    draw_text('엔터 키를 누르면', font_40, screen, draw_x, draw_y + 400, BLACK)
    draw_text('게임이 시작됩니다.', font_40, screen, draw_x, draw_y + 450, BLACK)

    pygame.display.update()

    # 설정을 완료하면 항상 업데이트를 하는 거 같다
    # 게임메뉴 = 시작화면을 만들어서 위치 정하고 + 200, +250 y 값 위치 알려주는 거

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return 'play'
        if event.type == QUIT or event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                return 'quit'

    return 'game_menu'


def main():
    global screen

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('코로나헌터')

    action = 'game_menu'
    while action != 'quit':
        if action == 'game_menu':
            action = game_menu()
        elif action == 'play':
            action = game_loop()

    pygame.quit()

    # 메인메뉴 함수추가로 마지막 screen 역할과 게임메뉴창, 나가기 버튼 등을 활성화함


if __name__ == "__main__":
    main()
# 메인일 경우 게임 실행하는 거






