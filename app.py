import threading
import tkinter
import tkinter.ttk as ttk

from speech_assistant import get_ai_response, koeiro_speak, listen

select_style_list = [
        'talk',
        'happy',
        'sad',
        'angry',
        'fear',
        'surprised',
]


class Application(tkinter.Frame):
    def __init__(self, root=None):
        super().__init__(root, width=580, height=380, borderwidth=1, relief='groove')
        self.root = root
        self.pack()
        self.pack_propagate(0)
        self.create_widgets()
        self.stop_event = threading.Event()

    def create_widgets(self):
        label = tkinter.Label(self, text="ボタンを押してから「おしまい」と言うと会話が終了します")
        label.pack(side="bottom")
        label = tkinter.Label(self, text="スタイルを選択してください")
        label.pack(side="top")

        # 閉じるボタン
        stop_btn = tkinter.Button(self, text="会話を終える", command=self.stop_loop)
        stop_btn.pack(side='bottom')

        # スタイルの選択
        combobox_frame = tkinter.Frame(self)
        combobox_frame.pack(anchor="center")
        self.combobox = ttk.Combobox(
            combobox_frame,
            justify="center",
            state="readonly",
            values=select_style_list,
            width=20,
            height=20,
        )
        self.combobox.set("talk")
        self.combobox.pack()

        # speaker_xの数値の選択
        self.scale_x = tkinter.Scale(
            self,
            orient=tkinter.HORIZONTAL,
            from_=-3.00,
            to=3.00,
            tickinterval=1.00,
            resolution=0.01,
            label="speaker_x"
        )
        self.scale_x.pack(padx=20, fill="x")

        # speaker_yの数値の選択
        self.scale_y = tkinter.Scale(
            self,
            orient=tkinter.HORIZONTAL,
            from_=-3.00,
            to=3.00,
            tickinterval=1.00,
            resolution=0.01,
            label="speaker_y"
        )
        self.scale_y.pack(padx=20, fill="x")

        label = tkinter.Label(self, text="-3.00が男声より、3.00が女声よりです")
        label.pack()

        # 実行ボタン
        start_btn = tkinter.Button(self, text="会話を始める", command=self.start_loop)
        start_btn.pack(anchor="center", expand=1)

    def start_loop(self):
        self.stop_event.clear()
        self.is_running = True
        threading.Thread(target=self.loop, args=(self.stop_event,)).start()

    def stop_loop(self):
        self.stop_event.set()

    def loop(self, stop_event):
        while not stop_event.is_set():
            text = listen()
            ai_response =get_ai_response(text)
            koeiro_speak(
                text=ai_response,
                speaker_x=self.scale_x.get(),
                speaker_y=self.scale_y.get(),
                style=self.combobox.get(),
            )


root = tkinter.Tk()
root.title("Talk Friends")
root.geometry("600x400")
app = Application(root=root)
app.mainloop()
