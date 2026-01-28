from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any

# --- 관련 데이터 타입 정의 (Placeholders) ---
class GeoLocation:
    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon
    def __repr__(self): return f"({self.lat}, {self.lon})"

class DeviceStatus:
    ONLINE = "Online"
    OFFLINE = "Offline"

class SensorType:
    TEMPERATURE = "Temperature"
    HUMIDITY = "Humidity"

class SensorData:
    def __init__(self, value: float): self.value = value
    def __repr__(self): return f"Data({self.value})"

class SimulationParams: pass
class SimResult: pass
class Prediction: pass
class Scenario: pass
class Report: pass
class DataStream: pass
class Alert: pass
class Command: pass
class Result: pass

# --- 클래스 정의 ---

class IoTDevice(ABC):
    """ 추상 클래스 (A) """
    def __init__(self, device_id: str, status: str = DeviceStatus.OFFLINE):
        self.device_id = device_id
        self.status = status

    def connect(self) -> bool:
        self.status = DeviceStatus.ONLINE
        print(f"Device {self.device_id} connected.")
        return True

    def send_heartbeat(self):
        print(f"Device {self.device_id} is beating...")

class EnvironmentalSensor(IoTDevice):
    def __init__(self, device_id: str, sensor_type: str):
        super().__init__(device_id)
        self.sensor_type = sensor_type

    def measure_data(self) -> SensorData:
        print(f"Sensor {self.device_id} measuring {self.sensor_type}...")
        return SensorData(24.5)

class ControlActuator(IoTDevice):
    def __init__(self, device_id: str, target_zone: str):
        super().__init__(device_id)
        self.target_zone = target_zone

    def execute_command(self, cmd: Command) -> Result:
        print(f"Actuator {self.device_id} executing command in {self.target_zone}.")
        return Result()

class MicroClimateZone:
    """ IoTDevice들과의 집합(Aggregation) 관계 (1:N) """
    def __init__(self, zone_id: str, current_temp: float, air_quality_index: int):
        self.zone_id = zone_id
        self.current_temp = current_temp
        self.air_quality_index = air_quality_index
        self.devices: List[IoTDevice] = []

    def add_device(self, device: IoTDevice):
        self.devices.append(device)

    def get_status(self) -> str:
        return f"Zone {self.zone_id}: Temp={self.current_temp}, AQI={self.air_quality_index}"

class ScenarioManager:
    def create_scenario(self) -> Scenario:
        print("Creating a new scenario...")
        return Scenario()

    def compare_scenarios(self, s1: Scenario, s2: Scenario) -> Report:
        print("Comparing scenarios...")
        return Report()

class SimulationEngine:
    """ ScenarioManager를 사용하여 시나리오 생성 """
    def __init__(self, model_type: str):
        self.model_type = model_type
        self.scenario_manager = ScenarioManager()

    def run_cfd(self, params: SimulationParams) -> SimResult:
        print(f"Running CFD with model {self.model_type}...")
        return SimResult()

    def predict_future(self, time: datetime) -> Prediction:
        print(f"Predicting future for {time}...")
        return Prediction()

class AnomalyDetector:
    def __init__(self, thresholds: Dict[str, float]):
        self.thresholds = thresholds

    def analyze_stream(self, data: DataStream) -> Alert:
        print("Analyzing data stream for anomalies...")
        return Alert()

class DigitalTwinModel:
    """ MicroClimateZone과의 구성(Composition) 관계 (1:N) """
    def __init__(self, twin_id: str, location: GeoLocation):
        self.twin_id = twin_id # 주석 달아오기. 2026.1.28 과제
        self.location = location
        self.last_sync_time = datetime.now()
        self.zones: List[MicroClimateZone] = [] # UML다이어그램에서 구성(1:N) 관계
        
        # 'Uses' 관계의 인스턴스들
        self.engine = SimulationEngine("General_Fluid_Dynamics")
        self.detector = AnomalyDetector({"temp_threshold": 40.0})

    def add_zone(self, zone: MicroClimateZone):
        self.zones.append(zone)

    def sync_data(self):
        self.last_sync_time = datetime.now()
        print(f"Twin {self.twin_id} synchronized at {self.last_sync_time}.")

    def visualize(self):
        print(f"Visualizing Digital Twin {self.twin_id} at {self.location}...")
        for zone in self.zones:
            print(f" - {zone.get_status()}")

# --- 테스트 실행부 (main 함수) ---

def main():
    # 1. 디지털 트윈 생성
    location = GeoLocation(37.5665, 126.9780)
    my_twin = DigitalTwinModel(twin_id="DT-SEOUL-01", location=location)

    # 2. 구역(MicroClimateZone) 생성 및 추가
    zone_a = MicroClimateZone(zone_id="Zone_A", current_temp=22.5, air_quality_index=45)
    my_twin.add_zone(zone_a)

    # 3. IoT 장치 생성 및 구역에 등록 (집합 관계)
    temp_sensor = EnvironmentalSensor(device_id="SENS-001", sensor_type=SensorType.TEMPERATURE)
    actuator = ControlActuator(device_id="ACT-001", target_zone="Zone_A")
    
    zone_a.add_device(temp_sensor)
    zone_a.add_device(actuator)

    # 4. 기능 테스트
    print("--- Digital Twin System Operation ---")
    my_twin.sync_data()
    my_twin.visualize()
    
    # 센서 및 엔진 동작 시뮬레이션
    temp_sensor.connect()
    data = temp_sensor.measure_data()
    
    my_twin.engine.run_cfd(SimulationParams())
    my_twin.detector.analyze_stream(DataStream())
    
    print("--- Operation Completed ---")

if __name__ == "__main__":
    main()