from abc import ABC, abstractmethod
from google.adk.agents.llm_agent import Agent

class Vehicle(ABC):
    def __init__(self, plate: str, owner: str):
        self.plate = plate
        self.owner = owner

    @abstractmethod
    def parking_rate(self) -> float:
        pass

class Car(Vehicle):
    def parking_rate(self) -> float:
        return 30.0

class Truck(Vehicle):
    def __init__(self, plate: str, owner: str, weight_tons: float):
        super().__init__(plate, owner)
        self.weight_tons = weight_tons

    def parking_rate(self) -> float:
        return 50.0 + (self.weight_tons * 5.0)

class ParkingLot:
    def __init__(self):
        self.__parked: dict[str, tuple[Vehicle, float]] = {}

    def park(self, vehicle: Vehicle, entry_hour: float):
        self.__parked[vehicle.plate] = (vehicle, entry_hour)

    def leave(self, plate: str, exit_hour: float) -> dict:
        if plate not in self.__parked:
            return {"error": "Vehicle not found"}

        vehicle, entry_hour = self.__parked.pop(plate)
        hours = exit_hour - entry_hour
        if hours < 0:
            hours = 0
            
        total_cost = vehicle.parking_rate() * hours
        
        return {
            "plate": plate,
            "owner": vehicle.owner,
            "hours": round(hours, 2),
            "total_cost": round(total_cost, 2)
        }

    def list_parked(self) -> list:
        return [
            {"plate": plate, "owner": data[0].owner, "entry": data[1]}
            for plate, data in self.__parked.items()
        ]

def calculate_parking_cost(vehicle_type: str, hours: float, weight_tons: float = 0.0) -> dict:
    """Розраховує вартість стоянки для 'car' або 'truck' на вказану кількість годин."""
    temp_plate = "TEMP"
    temp_owner = "Client"
    v_type = vehicle_type.lower()
    
    if "car" in v_type or "легк" in v_type:
        vehicle = Car(plate=temp_plate, owner=temp_owner)
    elif "truck" in v_type or "вантаж" in v_type:
        vehicle = Truck(plate=temp_plate, owner=temp_owner, weight_tons=float(weight_tons))
    else:
        return {"error": "Unknown vehicle type"}

    rate = vehicle.parking_rate()
    cost = rate * float(hours)
    
    return {
        "vehicle_type": "Car" if isinstance(vehicle, Car) else "Truck",
        "hours": float(hours),
        "rate_per_hour": rate,
        "total_cost": round(cost, 2)
    }

root_agent = Agent(
    model='gemini-2.5-flash',
    name='parking_operator',
    description='AI-оператор паркувального майданчика.',
    instruction=(
        'Ти оператор паркінгу. Розраховуй вартість стоянки за допомогою '
        'інструменту calculate_parking_cost. Якщо клієнт на вантажівці (truck), '
        'обов’язково запитуй її вагу в тоннах. Спілкуйся українською мовою.'
    ),
    tools=[calculate_parking_cost]
)