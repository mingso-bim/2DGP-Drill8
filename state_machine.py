# event (종류 문자열, 실제 입력 값)
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT


def space_down(e):
    return (e[0] == 'INPUT' and
            e[1].type == SDL_KEYDOWN and
            e[1].key == SDLK_SPACE)


def time_out(e):
    return e[0] == 'TIME_OUT'


def start_event(e):
    return e[0] == 'START'


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


# 상태 머신을 처리 관리해주는 클래스
class StateMachine:
    def __init__(self, o):
        self.o = o   #boy(self)가 전달, self.o 상태머신과 연결된 캐릭터 객체
        self.event_que = [] # 발생하는 이벤트를 담는 곳

    def update(self):
        self.cur_state.do(self.o) # Idle.do()
        # 이벤트가 발생했는지 확인하고, 거기에 따라서 상태 변환을 수행
        if self.event_que:   #list에 요소가 있으면, list 값은 True
            e = self.event_que.pop(0)   #list의 첫 번째 요소를 꺼냄
            for check_event, next_state in self.transitions[self.cur_state].items():
                if check_event(e):  # e가 지금 check_event이면? space_down(e) ?
                    self.cur_state.exit(self.o, e)
                    print(f'EXIT from {self.cur_state}')
                    self.cur_state = next_state
                    self.cur_state.enter(self.o, e)
                    print(f'ENTER into {next_state}')
                    return

    def start(self, start_state):
        # 현재 상태를 시작 상태로 만듦
        self.cur_state = start_state # Idle
        # 새로운 상태로 시작됐기 때문에 enter를 실행해야 한다
        self.cur_state.enter(self.o, ('START', 0))
        print(f'ENTER into {self.cur_state}')

    def draw(self):
        self.cur_state.draw(self.o)

    def set_transitions(self, transitions):
        self.transitions = transitions

    def add_event(self, e):
        self.event_que.append(e)    # 상태머신용 이벤트 추가
        print(f'    DEBUG: new event {e} is added.')
