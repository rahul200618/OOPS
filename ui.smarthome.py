import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from smarthome import SmartHomeSystem, Light, Fan, AirConditioner, WashingMachine

class SmartHomeUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Home Control Panel")
        self.geometry("820x520")
        self.smarthome = SmartHomeSystem()
        self.create_widgets()
        self.refresh_device_list()

    def create_widgets(self):
        # Left frame: device list and actions
        left = ttk.Frame(self, padding=10)
        left.pack(side="left", fill="y")

        ttk.Label(left, text="Devices").pack(anchor="w")
        self.device_list = tk.Listbox(left, width=30, height=20)
        self.device_list.pack(fill="y")
        self.device_list.bind("<<ListboxSelect>>", self.on_device_select)

        btn_frame = ttk.Frame(left)
        btn_frame.pack(pady=8, fill="x")
        ttk.Button(btn_frame, text="Add", command=self.add_device_dialog).pack(side="left", expand=True, fill="x")
        ttk.Button(btn_frame, text="Remove", command=self.remove_selected).pack(side="left", expand=True, fill="x")

        # Right frame: details and controls
        right = ttk.Frame(self, padding=10)
        right.pack(side="left", fill="both", expand=True)

        self.status_var = tk.StringVar()
        ttk.Label(right, textvariable=self.status_var, font=("Segoe UI", 10)).pack(anchor="w")

        action_frame = ttk.Frame(right)
        action_frame.pack(fill="x", pady=6)
        ttk.Button(action_frame, text="Turn ON", command=self.turn_on_selected).pack(side="left", padx=4)
        ttk.Button(action_frame, text="Turn OFF", command=self.turn_off_selected).pack(side="left", padx=4)

        # Device-specific controls container
        self.controls_container = ttk.LabelFrame(right, text="Device Controls", padding=8)
        self.controls_container.pack(fill="x", pady=6)

        # Light control
        self.brightness_label = ttk.Label(self.controls_container, text="Brightness:")
        self.brightness_spin = tk.Spinbox(self.controls_container, from_=0, to=100, width=5, command=self.set_brightness)
        # Fan control
        self.speed_label = ttk.Label(self.controls_container, text="Speed:")
        self.speed_spin = tk.Spinbox(self.controls_container, from_=0, to=3, width=5, command=self.set_speed)
        # AC control
        self.temp_label = ttk.Label(self.controls_container, text="Temperature:")
        self.temp_spin = tk.Spinbox(self.controls_container, from_=18, to=30, width=5, command=self.set_temperature)
        # Washing machine control
        self.program_label = ttk.Label(self.controls_container, text="Program:")
        self.program_var = tk.StringVar(value="Off")
        self.program_menu = ttk.OptionMenu(self.controls_container, self.program_var, "Off", "Off", "Delicate", "Cotton", "Quick Wash", command=self.set_program)

        # Schedule area
        sched_frame = ttk.LabelFrame(right, text="Schedules", padding=8)
        sched_frame.pack(fill="both", expand=True, pady=6)
        self.schedule_list = tk.Listbox(sched_frame, height=6)
        self.schedule_list.pack(fill="both", expand=True)
        sched_btns = ttk.Frame(sched_frame)
        sched_btns.pack(fill="x", pady=4)
        ttk.Button(sched_btns, text="Add Schedule", command=self.add_schedule_dialog).pack(side="left", expand=True, fill="x")
        ttk.Button(sched_btns, text="Refresh", command=self.refresh_schedules).pack(side="left", expand=True, fill="x")

    def refresh_device_list(self):
        self.device_list.delete(0, tk.END)
        for name in self.smarthome.devices:
            self.device_list.insert(tk.END, name)
        self.clear_controls()

    def on_device_select(self, event):
        sel = self.device_list.curselection()
        if not sel:
            return
        name = self.device_list.get(sel[0])
        device = self.smarthome.devices.get(name)
        if device:
            self.status_var.set(device.show_status())
            self.show_controls_for(device)

    def clear_controls(self):
        for w in self.controls_container.winfo_children():
            w.pack_forget()

    def show_controls_for(self, device):
        self.clear_controls()
        if isinstance(device, Light):
            self.brightness_label.pack(side="left", padx=(0,6))
            self.brightness_spin.pack(side="left")
            self.brightness_spin.delete(0,"end")
            self.brightness_spin.insert(0, str(device.brightness))
        elif isinstance(device, Fan):
            self.speed_label.pack(side="left", padx=(0,6))
            self.speed_spin.pack(side="left")
            self.speed_spin.delete(0,"end")
            self.speed_spin.insert(0, str(device.speed))
        elif isinstance(device, AirConditioner):
            self.temp_label.pack(side="left", padx=(0,6))
            self.temp_spin.pack(side="left")
            self.temp_spin.delete(0,"end")
            self.temp_spin.insert(0, str(device.temperature))
        elif isinstance(device, WashingMachine):
            self.program_label.pack(side="left", padx=(0,6))
            self.program_menu.pack(side="left")
            self.program_var.set(device.program)

    def get_selected_device(self):
        sel = self.device_list.curselection()
        if not sel:
            messagebox.showinfo("Info", "No device selected.")
            return None
        name = self.device_list.get(sel[0])
        return self.smarthome.devices.get(name)

    def add_device_dialog(self):
        dlg = simpledialog.askstring("Add Device", "Enter device name:")
        if not dlg:
            return
        # choose type
        types = ["Light", "Fan", "Air Conditioner", "Washing Machine", "Thermostat", "Door Lock", "Other"]
        type_choice = simpledialog.askstring("Device Type", f"Choose type from: {', '.join(types)}")
        if not type_choice:
            return
        initial = messagebox.askyesno("Initial Power", "Should the device be ON initially?")
        res = self.smarthome.add_device(dlg.strip(), type_choice.strip(), initial)
        messagebox.showinfo("Result", res)
        self.refresh_device_list()

    def remove_selected(self):
        device = self.get_selected_device()
        if not device:
            return
        res = self.smarthome.remove_device(device.name)
        messagebox.showinfo("Result", res)
        self.refresh_device_list()
        self.refresh_schedules()

    def turn_on_selected(self):
        device = self.get_selected_device()
        if not device:
            return
        res = self.smarthome.turn_on_device(device.name)
        messagebox.showinfo("Result", res)
        self.refresh_device_list()
        self.on_device_select(None)

    def turn_off_selected(self):
        device = self.get_selected_device()
        if not device:
            return
        res = self.smarthome.turn_off_device(device.name)
        messagebox.showinfo("Result", res)
        self.refresh_device_list()
        self.on_device_select(None)

    # control handlers
    def set_brightness(self):
        device = self.get_selected_device()
        if isinstance(device, Light):
            try:
                value = int(self.brightness_spin.get())
                messagebox.showinfo("Result", device.set_brightness(value))
                self.on_device_select(None)
            except ValueError:
                messagebox.showerror("Error", "Invalid brightness value.")

    def set_speed(self):
        device = self.get_selected_device()
        if isinstance(device, Fan):
            try:
                value = int(self.speed_spin.get())
                messagebox.showinfo("Result", device.set_speed(value))
                self.on_device_select(None)
            except ValueError:
                messagebox.showerror("Error", "Invalid speed value.")

    def set_temperature(self):
        device = self.get_selected_device()
        if isinstance(device, AirConditioner):
            try:
                value = int(self.temp_spin.get())
                messagebox.showinfo("Result", device.set_temperature(value))
                self.on_device_select(None)
            except ValueError:
                messagebox.showerror("Error", "Invalid temperature value.")

    def set_program(self, _=None):
        device = self.get_selected_device()
        if isinstance(device, WashingMachine):
            prog = self.program_var.get()
            messagebox.showinfo("Result", device.set_program(prog))
            self.on_device_select(None)

    # schedules
    def add_schedule_dialog(self):
        device = self.get_selected_device()
        if not device:
            return
        start = simpledialog.askstring("Schedule", "Enter start time (e.g., 08:00):")
        if not start:
            return
        end = simpledialog.askstring("Schedule", "Enter end time (e.g., 22:00):")
        if not end:
            return
        res = self.smarthome.add_schedule(device.name, start.strip(), end.strip())
        messagebox.showinfo("Result", res)
        self.refresh_schedules()

    def refresh_schedules(self):
        self.schedule_list.delete(0, tk.END)
        for s in self.smarthome.schedules:
            self.schedule_list.insert(tk.END, s.get_schedule_info())

if __name__ == "__main__":
    app = SmartHomeUI()
    app.mainloop()