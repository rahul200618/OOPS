class Device:
    def __init__(self, name, device_type, power_status=False):
        self.name = name
        self.device_type = device_type
        self.power_status = power_status

    def show_status(self):
        return f"Device: {self.name} ({self.device_type}), Power: {'ON' if self.power_status else 'OFF'}"

    def turn_on(self):
        self.power_status = True
        return f"{self.name} is now ON."

    def turn_off(self):
        self.power_status = False
        return f"{self.name} is now OFF"

class Light(Device):
    def __init__(self, name, power_status=False, brightness=100):
        super().__init__(name, "Light", power_status)
        self.brightness = brightness

    def set_brightness(self, brightness):
        if self.power_status and 0 <= brightness <= 100:
            self.brightness = brightness
            return f"{self.name} brightness set to {self.brightness}%."
        return f"Cannot set brightness for {self.name} (is {'OFF' if not self.power_status else 'invalid brightness'})."

    def show_status(self):
        return f"Device: {self.name} ({self.device_type}), Power: {'ON' if self.power_status else 'OFF'}, Brightness: {self.brightness}%"

class Fan(Device):
    def __init__(self, name, power_status=False, speed=0):
        super().__init__(name, "Fan", power_status)
        self.speed = speed # 0 for off, 1-3 for speeds

    def set_speed(self, speed):
        if self.power_status and 0 <= speed <= 3:
            self.speed = speed
            return f"{self.name} speed set to {self.speed}."
        return f"Cannot set speed for {self.name} (is {'OFF' if not self.power_status else 'invalid speed'})."

    def show_status(self):
        return f"Device: {self.name} ({self.device_type}), Power: {'ON' if self.power_status else 'OFF'}, Speed: {self.speed}"

class AirConditioner(Device):
    def __init__(self, name, power_status=False, temperature=24):
        super().__init__(name, "Air Conditioner", power_status)
        self.temperature = temperature # in Celsius

    def set_temperature(self, temperature):
        if self.power_status and 18 <= temperature <= 30: # Example range
            self.temperature = temperature
            return f"{self.name} temperature set to {self.temperature}°C."
        return f"Cannot set temperature for {self.name} (is {'OFF' if not self.power_status else 'invalid temperature'})."

    def show_status(self):
        return f"Device: {self.name} ({self.device_type}), Power: {'ON' if self.power_status else 'OFF'}, Temperature: {self.temperature}°C"

class WashingMachine(Device):
    def __init__(self, name, power_status=False, program="Off"):
        super().__init__(name, "Washing Machine", power_status)
        self.program = program # e.g., "Off", "Delicate", "Cotton", "Quick Wash"

    def set_program(self, program):
        if self.power_status and program in ["Delicate", "Cotton", "Quick Wash", "Off"]:
            self.program = program
            return f"{self.name} program set to '{self.program}'."
        return f"Cannot set program for {self.name} (is {'OFF' if not self.power_status else 'invalid program'})."

    def show_status(self):
        return f"Device: {self.name} ({self.device_type}), Power: {'ON' if self.power_status else 'OFF'}, Program: {self.program}"

class Schedule:
    def __init__(self, device, start_time, end_time):
        self.device = device
        self.start_time = start_time
        self.end_time = end_time

    def get_schedule_info(self):
        return f"Schedule for {self.device.name}: ON from {self.start_time} to {self.end_time}"

class SmartHomeSystem:
    def __init__(self):
        self.devices = {}
        self.schedules = []

    def add_device(self, device_name, device_type, initial_power_status=False):
        if device_name not in self.devices:
            if device_type.lower() == "light":
                new_device = Light(device_name, initial_power_status)
            elif device_type.lower() == "fan":
                new_device = Fan(device_name, initial_power_status)
            elif device_type.lower() == "air conditioner":
                new_device = AirConditioner(device_name, initial_power_status)
            elif device_type.lower() == "washing machine":
                new_device = WashingMachine(device_name, initial_power_status)
            else:
                new_device = Device(device_name, device_type, initial_power_status)
            self.devices[device_name] = new_device
            return f"Device '{device_name}' added to the system."
        return f"Device '{device_name}' already exists."

    def remove_device(self, device_name):
        if device_name in self.devices:
            del self.devices[device_name]
            # Also remove any schedules associated with this device
            self.schedules = [s for s in self.schedules if s.device.name != device_name]
            return f"Device '{device_name}' removed from the system."
        return f"Device '{device_name}' not found."

    def get_device_status(self, device_name):
        if device_name in self.devices:
            return self.devices[device_name].show_status()
        return f"Device '{device_name}' not found."

    def turn_on_device(self, device_name):
        if device_name in self.devices:
            return self.devices[device_name].turn_on()
        return f"Device '{device_name}' not found."

    def turn_off_device(self, device_name):
        if device_name in self.devices:
            return self.devices[device_name].turn_off()
        return f"Device '{device_name}' not found."

    def list_all_devices(self):
        if not self.devices:
            print("No devices in the system.")
            return
        for device in self.devices.values():
            print(device.show_status())

    def add_schedule(self, device_name, start_time, end_time):
        if device_name in self.devices:
            device = self.devices[device_name]
            schedule = Schedule(device, start_time, end_time)
            self.schedules.append(schedule)
            return f"Schedule added for {device_name}: ON from {start_time} to {end_time}."
        return f"Device '{device_name}' not found."

    def list_schedules(self):
        if not self.schedules:
            print("No schedules set.")
            return
        print("\n--- All Schedules ---")
        for schedule in self.schedules:
            print(schedule.get_schedule_info())

if __name__ == "__main__":
    device_types = ["Light", "Fan", "Air Conditioner", "Washing Machine", "Thermostat", "Door Lock", "Other"]

    def get_device_type_input(): # Changed to allow user to choose a number for device type
        print("Available device types:")
        for i, d_type in enumerate(device_types):
            print(f"{i+1}. {d_type}")
        while True:
            try:
                choice = int(input("Enter the number corresponding to the device type: ").strip())
                if 1 <= choice <= len(device_types):
                    return device_types[choice - 1]
                else:
                    print("Invalid choice. Please enter a number within the given range.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            else: print("Invalid device type. Please choose from the available types.")
    smarthome = SmartHomeSystem()

    print("""
  _  _
 /____\\
|  []  |
| _  _ | Smart Home System
|_||_|_| Control Panel
""")
    while True:
        print("\n--- Main Menu ---")
        print("1. Add a new device")
        print("2. Remove a device")
        print("3. Turn on a device")
        print("4. Turn off a device")
        print("5. Get device status")
        print("6. List all devices and their status")
        print("7. Add a schedule")
        print("8. List all schedules")
        print("9. Control specific device features (e.g., brightness, speed, temperature, program)")
        print("10. Exit")

        choice = input("Enter your choice (1-10): ").strip()

        if choice == '1':
            device_name = input("Enter the name of the new device: ").strip()
            device_type = get_device_type_input()
            initial_status_input = input(f"Should the {device_name} be ON initially? (yes/no): ").strip().lower()
            initial_status = initial_status_input == 'yes'
            print(smarthome.add_device(device_name, device_type, initial_status))



        elif choice == '2':
            device_name = input("Enter the name of the device to remove: ").strip()
            print(smarthome.remove_device(device_name))

        elif choice == '3':
            device_name = input("Enter the name of the device to turn ON: ").strip()
            print(smarthome.turn_on_device(device_name))

        elif choice == '4':
            device_name = input("Enter the name of the device to turn OFF: ").strip()
            print(smarthome.turn_off_device(device_name))

        elif choice == '5':
            device_name = input("Enter the name of the device to get status for: ").strip()
            print(smarthome.get_device_status(device_name))

        elif choice == '6':
            if not smarthome.devices:
                print("No devices in the system.")
            else:
                print("\n--- All Devices ---")
                smarthome.list_all_devices()

        elif choice == '7': # Add schedule
            device_name = input("Enter the name of the device to schedule: ").strip()
            start_time = input("Enter start time (e.g., 08:00): ").strip()
            end_time = input("Enter end time (e.g., 22:00): ").strip()
            print(smarthome.add_schedule(device_name, start_time, end_time))

        elif choice == '8': # List schedules
            smarthome.list_schedules()

        elif choice == '9': # Control specific device features
            device_name = input("Enter the name of the device to control: ").strip()
            device = smarthome.devices.get(device_name)
            if not device:
                print(f"Device '{device_name}' not found.")
                continue
            if isinstance(device, Light):
                try:
                    brightness = int(input(f"Enter brightness level for {device_name} (0-100): ").strip())
                    print(device.set_brightness(brightness))
                except ValueError:
                    print("Invalid brightness. Please enter a number.")
            elif isinstance(device, Fan):
                try:
                    speed = int(input(f"Enter speed level for {device_name} (0-3): ").strip())
                    print(device.set_speed(speed))
                except ValueError:
                    print("Invalid speed. Please enter a number.")
            elif isinstance(device, AirConditioner):
                try:
                    temperature = int(input(f"Enter temperature for {device_name} (18-30°C): ").strip())
                    print(device.set_temperature(temperature))
                except ValueError:
                    print("Invalid temperature. Please enter a number.")
            elif isinstance(device, WashingMachine):
                print("Available programs: Delicate, Cotton, Quick Wash, Off")
                program = input(f"Enter program for {device_name}: ").strip()
                print(device.set_program(program))
            else:
                print(f"Device '{device_name}' is a {device.device_type} and does not have specific controls in this menu.")

        elif choice == '10': # Changed exit option to 8
            print("BYEEEEEEE😭😭😭😭😭😭😭😭😭😭😭😭😭😭")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 10.")
