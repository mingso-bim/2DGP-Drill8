from pico2d import load_image, open_canvas, get_time
from state_machine import *


class Idle:
    @staticmethod
    def enter(boy, e):
        if left_up(e) or right_down(e):
            boy.action = 2
        elif right_up(e) or left_down(e) or start_event(e):
            boy.action = 3

        boy.frame = 0
        boy.dir = 0
        # 시작 시간을 기록
        boy.start_time = get_time()

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 1:
            boy.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100,
                            100, 100, boy.x, boy.y)



class Sleep:
    @staticmethod
    def enter(boy, e):
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        if boy.action == 2:
            boy.image.clip_composite_draw(
                boy.frame * 100, 300, 100, 100,
                3.141592 / 2,  # 회전 각도
                'v',  # 좌우상하 반전 X
                boy.x + 25, boy.y - 25, 100, 100)
        if boy.action == 3:
            boy.image.clip_composite_draw(
                boy.frame * 100, 300, 100, 100,
                3.141592 / 2,  # 회전 각도
                '',  # 좌우상하 반전 X
                boy.x - 25, boy.y - 25, 100, 100
            )


class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e):
            boy.action = 1
            boy.dir = 1
        elif left_down(e) or right_up(e):
            boy.action = 0
            boy.dir = -1
        boy.frame = 0

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 3

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(
            boy.frame * 100, boy.action * 100, 100, 100,
            boy.x, boy.y
        )


class AutoRun:
    @staticmethod
    def enter(boy):
        pass

    @staticmethod
    def exit(boy):
        pass

    @staticmethod
    def do(boy):
        pass

    @staticmethod
    def draw(boy):
        pass


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self) # 소년 객체를 위한 상태머신인지 알려줄 필요
        self.state_machine.start(Idle)  # 객체를 생성한 게 아니고 직접 Idle 클래스 사용
        self.state_machine.set_transitions(
            {
                Idle: { right_down: Run, left_down:Run,left_up: Run, right_up: Run, time_out: Sleep },
                Run : { right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle },
                Sleep: { right_down: Run, left_down:Run,left_up: Run, right_up: Run, space_down:Idle }
            }
        )


    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # event : input event
        # state machine event : (이벤트 종류, 값)
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
