import json
import os
from calculator import BallisticsToTarget, OutOfRangeException
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title('Create Big Cannons : Absolute 360° Calculator')
root.geometry("1150x520")

CONFIG_FILE = "mortar_absolute_config.json"

def save_config():
    data = {
        "xCannon": xCannon.get(), "yCannon": yCannon.get(), "zCannon": zCannon.get(),
        "xTarget": xTarget.get(), "yTarget": yTarget.get(), "zTarget": zTarget.get()
    }
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception:
        pass

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                xCannon.insert(0, data.get("xCannon", ""))
                yCannon.insert(0, data.get("yCannon", ""))
                zCannon.insert(0, data.get("zCannon", ""))
                xTarget.insert(0, data.get("xTarget", ""))
                yTarget.insert(0, data.get("yTarget", ""))
                zTarget.insert(0, data.get("zTarget", ""))
            controlButton()
        except Exception:
            pass

def callback(P):
    if P == "" or P == "-" or P == "." or P == "-.":
        return True
    try: 
        float(P)
        return True
    except ValueError:
        return False

def controlButton(*args):
    if all(var.get() for var in [xCannon, yCannon, zCannon, xTarget, yTarget, zTarget]):
        button.configure(state="normal")
    else:
        button.configure(state="disabled")

def getAngles():
    try:
        cannonCoords = tuple(map(float, (xCannon.get(), yCannon.get(), zCannon.get())))
        targetCoords = tuple(map(float, (xTarget.get(), yTarget.get(), zTarget.get())))
        res = BallisticsToTarget(cannonCoords, targetCoords)
    except OutOfRangeException as e:
        statusMessage.set(str(e))
        status.configure(text_color="#980404")
    except ValueError:
        statusMessage.set("Ошибка! Проверь формат координат.")
        status.configure(text_color="#980404")
    else:
        pitch, yaw, ticks, secs, fuze = res

        # Переводим общее время взрывателя в секунды и остаток тиков
        fuze_seconds = fuze // 20
        fuze_ticks = fuze % 20

        varPitch.set(f"Pitch (Наклон): {round(pitch, 2)}°")
        varYaw.set(f"Yaw (Поворот): {round(yaw, 2)}°")
        varAirtime.set(f"Ticks: {round(ticks, 1)}")
        varAirtimeSeconds.set(f"Seconds: {secs}s")
        
        # Новый красивый вывод взрывателя
        varFuzeTime.set(f"Fuze: {fuze_seconds} сек. {fuze_ticks} тик.")

        statusMessage.set("Расчет завершен!")
        status.configure(text_color="#50bc54")
        save_config()

def main():
    global xCannon, yCannon, zCannon, xTarget, yTarget, zTarget, button, statusMessage, status,\
    varPitch, varYaw, varAirtime, varAirtimeSeconds, varFuzeTime

    titre = ctk.CTkLabel(master=root, text="CBC Absolute 360° Cannon Calculator", font=("Roboto", 32), fg_color="#1E538D", corner_radius=12)
    titre.pack(pady=15, padx=40, fill="x")

    help_text = "Автоматический расчет углов и таймингов. Взрыватель (Fuze) переведен в секунды и тики."
    help_label = ctk.CTkLabel(master=root, text=help_text, font=("Roboto", 13, "italic"), text_color="#aaaaaa")
    help_label.pack(pady=2)

    frame = ctk.CTkFrame(master=root, corner_radius=15)
    frame.pack(pady=15, padx=30, fill="both", expand=True)

    cannonFrame = ctk.CTkFrame(master=frame)
    targetFrame = ctk.CTkFrame(master=frame)

    cannonCoord = ctk.CTkLabel(master=cannonFrame, text="Coordinates of Cannon (X;Y;Z): ", font=("Roboto", 14))
    targetCoord = ctk.CTkLabel(master=targetFrame, text="Coordinates of Target (X;Y;Z): ", font=("Roboto", 14))

    isvalidinput = root.register(callback)
    statusMessage = ctk.StringVar(value="Ожидание координат...")
    status = ctk.CTkLabel(master=frame, textvariable=statusMessage, font=("Roboto", 14, "bold"))

    xCannon = ctk.CTkEntry(master=cannonFrame, placeholder_text="X", validate="key", validatecommand=(isvalidinput, '%P'))
    yCannon = ctk.CTkEntry(master=cannonFrame, placeholder_text="Y", validate="key", validatecommand=(isvalidinput, '%P'))
    zCannon = ctk.CTkEntry(master=cannonFrame, placeholder_text="Z", validate="key", validatecommand=(isvalidinput, '%P'))

    xTarget = ctk.CTkEntry(master=targetFrame, placeholder_text="X", validate="key", validatecommand=(isvalidinput, '%P'))
    yTarget = ctk.CTkEntry(master=targetFrame, placeholder_text="Y", validate="key", validatecommand=(isvalidinput, '%P'))
    zTarget = ctk.CTkEntry(master=targetFrame, placeholder_text="Z", validate="key", validatecommand=(isvalidinput, '%P'))

    varPitch = ctk.StringVar(value="Pitch (Наклон): ?")
    varYaw = ctk.StringVar(value="Yaw (Поворот): ?")
    varAirtime = ctk.StringVar(value="Ticks: ?")
    varAirtimeSeconds = ctk.StringVar(value="Seconds: ?")
    varFuzeTime = ctk.StringVar(value="Fuze: ?")

    results = ctk.CTkFrame(master=frame, fg_color="#242424", border_width=2, border_color="#1E538D", corner_radius=10)
    for col in range(5): results.columnconfigure(col, weight=1)

    labelPitch = ctk.CTkLabel(master=results, textvariable=varPitch, font=("Roboto", 14, "bold"), text_color="#7cb1f2")
    labelYaw = ctk.CTkLabel(master=results, textvariable=varYaw, font=("Roboto", 14, "bold"), text_color="#7cb1f2")
    labelAirtime = ctk.CTkLabel(master=results, textvariable=varAirtime, font=("Roboto", 13))
    labelAirtimeSeconds = ctk.CTkLabel(master=results, textvariable=varAirtimeSeconds, font=("Roboto", 13))
    labelFuzeTime = ctk.CTkLabel(master=results, textvariable=varFuzeTime, font=("Roboto", 14, "bold"), text_color="#ffb03a")

    button = ctk.CTkButton(master=frame, text="Calculate Fire Mission!", command=getAngles, state="disabled", width=280, height=40, font=("Roboto", 14, "bold"))

    cannonFrame.pack(fill="x", padx=15, pady=10)
    cannonCoord.pack(side="left", padx=10, pady=5)
    xCannon.pack(side="left", padx=5, expand=True, fill="x")
    yCannon.pack(side="left", padx=5, expand=True, fill="x")
    zCannon.pack(side="left", padx=5, expand=True, fill="x")

    targetFrame.pack(fill="x", padx=15, pady=10)
    targetCoord.pack(side="left", padx=10, pady=5)
    xTarget.pack(side="left", padx=5, expand=True, fill="x")
    yTarget.pack(side="left", padx=5, expand=True, fill="x")
    zTarget.pack(side="left", padx=5, expand=True, fill="x")

    button.pack(pady=15)
    results.pack(fill="x", padx=25, pady=10)

    labelPitch.grid(column=0, row=0, padx=15, pady=15, sticky="w")
    labelYaw.grid(column=1, row=0, padx=15, pady=15, sticky="w")
    labelAirtime.grid(column=2, row=0, padx=10, pady=15)
    labelAirtimeSeconds.grid(column=3, row=0, padx=10, pady=15)
    labelFuzeTime.grid(column=4, row=0, padx=15, pady=15, sticky="e")

    status.pack(pady=5)
    load_config()

    root.bind("<Key>", controlButton)
    root.mainloop()

if __name__ == "__main__":
    main()