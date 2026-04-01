import sys

# 0. 시뮬레이션을 위한 가상의 그래픽 환경 (Mock Graphics)
class Graphics:
    def draw_sphere(self, pos, rad): print(f"  [Graphics] Drawing sphere at {pos} with radius {rad}")
    def light_on(self): print("  [Graphics] Light ON (Sun Effect)")
    def light_off(self): print("  [Graphics] Light OFF")

# 1. 기초 데이터 구조 및 메타데이터
class Property:
    def __init__(self, name, p_type, value=None):
        self.name = name
        self.type = p_type
        self.value = value

# 2. 도메인 모델 (상속과 다형성)
class BaseObject:
    def __init__(self, name):
        self.name = name

class Planet(BaseObject):
    def __init__(self, name, position=(0, 0, 0), radius=10):
        super().__init__(name)
        self.position = position
        self.radius = radius
        self.properties = {}

    def render(self, gr):
        gr.draw_sphere(self.position, self.radius)

    def set_property(self, name, value):
        self.properties[name] = value

    def get_property(self, name):
        return self.properties.get(name)

class Sun(Planet):
    def render(self, gr):
        gr.light_on()         # 기능 확장
        super().render(gr)    # 부모 로직 재사용
        gr.light_off()

class Creature(BaseObject):
    def __init__(self, name):
        super().__init__(name)
        self.life = 100

# 3. 모델 관리 및 팩토리 패턴 (Universe)
class UniverseModel:
    def __init__(self):
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)
        print(f"[Model] '{obj.name}' added to the universe.")

class UniverseFactory:
    """싱글톤 패턴이 적용된 객체 생성 팩토리"""
    _instance = None

    @staticmethod
    def get_factory():
        if UniverseFactory._instance is None:
            UniverseFactory._instance = UniverseFactory()
        return UniverseFactory._instance

    def create_object(self, obj_type, name):
        if obj_type == 'sun':
            return Sun(name, radius=50)
        elif obj_type == 'planet':
            return Planet(name)
        elif obj_type == 'creature':
            return Creature(name)
        return BaseObject(name)

class Scenario:
    def __init__(self):
        # 시나리오에 따른 생성 목록
        self.talks = ['planet', 'sun', 'creature']

class God:
    """객체 생성 및 조립을 담당하는 오케스트레이터"""
    def do_something(self, scenario):
        factory = UniverseFactory.get_factory()
        model = UniverseModel()
        
        print("--- God is creating the world ---")
        for t in scenario.talks:
            obj = factory.create_object(t, f"My_{t}")
            model.add_object(obj)
        return model

# 4. View 레이어 (전략 패턴)
class View1D:
    def render(self, model):
        print("\n--- 1D Console View ---")
        for obj in model.objects:
            print(f"  - [Obj]: {obj.name} (Type: {type(obj).__name__})")

class View3D:
    def render(self, model, gr):
        print("\n--- 3D Graphics View ---")
        for obj in model.objects:
            if hasattr(obj, 'render'):
                obj.render(gr)

# 5. Command 패턴 (행위의 객체화)
class Command:
    def __init__(self, name):
        self.name = name
    def execute(self):
        pass

class RainCommand(Command):
    def execute(self):
        print(f"  >> [Action] Rain is falling... (Cmd: {self.name})")

class PowerCommand(Command):
    def execute(self):
        print(f"  >> [Action] Cosmic power surging! (Cmd: {self.name})")

class Control:
    """커맨드를 관리하고 실행하는 인보커(Invoker)"""
    def __init__(self, model):
        self._model = model
        self._commands = {}

    def add_command(self, key, cmd):
        self._commands[key] = cmd

    def execute(self, key):
        if key in self._commands:
            self._commands[key].execute()
        else:
            print(f"  [Error] Command '{key}' is unknown.")

# 6. 실행 루프 (Main)
def main():
    # 초기 설정
    gr = Graphics()
    scenario = Scenario()
    god = God()
    
    # 모델 생성
    universe_model = god.do_something(scenario)
    
    # 컨트롤러 및 커맨드 등록
    ctrl = Control(universe_model)
    ctrl.add_command('rain', RainCommand('RainMaker_v1'))
    ctrl.add_command('power', PowerCommand('SuperNova_v1'))
    
    # 뷰 출력
    view_1d = View1D()
    view_3d = View3D()
    
    view_1d.render(universe_model)
    view_3d.render(universe_model, gr)

    # 인터랙션 시뮬레이션
    print("\n--- Interaction Loop ---")
    simulated_inputs = ['rain', 'power', 'unknown_cmd', 'exit']
    
    for user_input in simulated_inputs:
        if user_input == 'exit':
            print("System terminated.")
            break
        print(f"User Input: {user_input}")
        ctrl.execute(user_input)

if __name__ == "__main__":
    main()