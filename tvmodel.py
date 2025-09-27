class TV:
    def __init__(self):
        self.is_on = False
        self.volume = 10         
        self.channel = 1        
        self.is_muted = False


    def power(self):
        """Toggle the TV on/off."""
        self.is_on = not self.is_on
        return f"TV power {'ON' if self.is_on else 'OFF'}"

    def set_channel(self, channel):
        if self.is_on:
            self.channel = channel
            return f"Channel set to {channel}"
        return "TV is OFF"

    def volume_up(self):
        if self.is_on and not self.is_muted and self.volume < 100:
            self.volume += 1
            return f"Volume: {self.volume}"
        return "Cannot change volume"

    def volume_down(self):
        if self.is_on and not self.is_muted and self.volume > 0:
            self.volume -= 1
            return f"Volume: {self.volume}"
        return "Cannot change volume"
    
    def channnel_up(self):            
        if self.is_on:
            self.channel += 1
            return f"Channel: {self.channel}"
        return "TV is OFF"

    def channel_down(self):
        if self.is_on:
            self.channel -= 1
            return f"Channel: {self.channel}"
        return "TV is OFF"
    
    def mute(self):
        if self.is_on:
            self.is_muted = not self.is_muted
            return f"Mute {'ON' if self.is_muted else 'OFF'}"
        return "TV is OFF"

    def get_info(self):
        return {
            "Power": "ON" if self.is_on else "OFF",
            "Channel": self.channel,
            "Volume": self.volume,
            "Muted": self.is_muted
        }


class Remote:
    def __init__(self, tv):
        self.tv = tv
    def power(self): return self.tv.power()
    def vol_up(self): return self.tv.volume_up()
    def vol_down(self): return self.tv.volume_down()
    def set_channel(self, ch): return self.tv.set_channel(ch)
    def channel_up(self): return self.tv.channnel_up()
    def channel_down(self): return self.tv.channel_down()
    def mute(self): return self.tv.mute()
    def get_info(self): return self.tv.get_info()

    
if __name__ == "__main__":
    my_tv = TV()
    remote = Remote(my_tv)

    print("TV Remote Control")
    print("Choose an option:")
    print("1. Power On/Off")
    print("2. Change Channel")
    print("3. Volume Up")
    print("4. Volume Down")
    print("5. Mute/Unmute")
    print("6. Get TV Info")
    print("7. channel up")
    print("8. channel down")
    print("9. EXit")

    while True:
        choice = input("Enter your choice (1-9):").strip()

        if choice == "1": # User wants to toggle power
            print(remote.power())
        elif choice == "2": # User wants to change channel
            channel_input = input("Enter channel number: ").strip()
            if channel_input.isdigit():
                print(remote.set_channel(int(channel_input)))
            else:
                print("Invalid input. Please enter a number for the channel.")
        elif choice == "3": # User wants to increase volume
            print(remote.vol_up())
        elif choice == "4": # User wants to decrease volume
            print(remote.vol_down())
        elif choice == "5": # User wants to toggle mute
            print(remote.mute())
        elif choice == "6": # User wants TV information
            info = my_tv.get_info() # Changed to directly access TV info
            print(f"Power: {info['Power']}, Channel: {info['Channel']}, Volume: {info['Volume']}, Muted: {info['Muted']}")
        elif choice =="7":# User wants to increase channel
            print(remote.channel_up())
        elif choice =="8":# User wants to decrease channel
            print(remote.channel_down())
        elif choice == "9":# User wants to exit
            print("Exiting TV Remote.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")