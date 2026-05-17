import requests as r, customtkinter as ctk, threading, time, dotenv, os, json
from datetime import datetime as dt

dotenv.load_dotenv()
ctk.set_appearance_mode("dark")

primaryGreen = "#0bda51"
secondaryGreen = "#06420b"

status = "online"
customText = ""

def changeStatus() -> None:
    now = dt.now().strftime("[ %H : %M ]")
    if customText and customText != "": t = f"{now} // {customText}"
    else: t = f"It's {now} for me"
    res = r.patch("https://discord.com/api/v10/users/@me/settings?", headers={"Content-Type": "application/json", "Authorization": os.getenv("ACCTOKEN")},
           data=json.dumps({
                "status": status,
                "custom_status": {
                    "text": t[:128],
                    "emoji_id": None,
                    "emoji_name": None,
                    "expires_at": None,
                }
           })
    )
    print(f"{res.status_code}: {res.reason}")

def Main() -> None:
    last = dt.now().minute-1
    while True:
        time.sleep(.25)
        if dt.now().minute == last: continue
        last = dt.now().minute
        changeStatus()

class App(ctk.CTk):
    def Update(self) -> None:
        global customText, status
        status = self.Status.get()
        customText = self.ExtraText.get("1.0", "128.0").strip()
        changeStatus()

    def __init__(self):
        super().__init__()
        # Window
        self.geometry("400x400")
        self.title("AVeemo's Super Duper Cool Discord Time Status Program")
        self.resizable(False,False)

        # Extra Text
        self.ExtraText = ctk.CTkTextbox(self, 200, 50,16, wrap="none",
                                        font=ctk.CTkFont("sans-serif", 16),
                                        activate_scrollbars=False, border_width=2, border_color=primaryGreen,
                                        fg_color=secondaryGreen)
        self.ExtraText.grid(row=0, column=0, padx=100, pady=20, sticky="nsew")

        # Status
        self.Status = ctk.CTkOptionMenu(self, 200, 50, 16, values=["online", "idle",
                                                                   "dnd", "invisible"],
                                        font=ctk.CTkFont("sans-serif", 22),
                                        button_color=primaryGreen, hover=False, fg_color=secondaryGreen,
                                        dropdown_fg_color=secondaryGreen)
        self.Status.grid(row=1, column=0, padx=100, pady=5, sticky="nsew")

        # Change
        self.Change = ctk.CTkButton(self, 200, 50, 16, 2, text="Change",
                                    font=ctk.CTkFont("sans-serif",  26),
                                    border_color=primaryGreen,
                                    fg_color=secondaryGreen,
                                    command=self.Update)
        self.Change.grid(row=2, column=0, padx=100, pady=15, sticky="nsew")

threading.Thread(target=Main).start()  
App().mainloop()