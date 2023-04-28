import subprocess
import threading
import tkinter
import tkinter.ttk as ttk

from dotenv import load_dotenv

import main

load_dotenv(".env")
subprocess.Popen(r"C:\Users\owner\Desktop\voice\COEIROINK-GPU-v.1.7.2\COEIROINK.exe")

select_voice_dict = {
    "VOICEVOX": {
        "四国めたん": 2,
        "四国めたんあまあま": 0,
        "四国めたんツンツン": 6,
        "四国めたんセクシー": 4,
        "四国めたんささやき": 36,
        "四国めたんヒソヒソ": 37,
        "ずんだもん": 3,
        "ずんだもんあまあま": 1,
        "ずんだもんツンツン": 7,
        "ずんだもんセクシー": 5,
        "ずんだもんささやき": 22,
        "ずんだもんヒソヒソ": 38,
        "春日部つむぎ": 8,
        "雨晴はう": 10,
        "波音リツ": 9,
        "冥鳴ひまり": 14,
        "九州そら": 16,
        "九州そらあまあま": 15,
        "九州そらツンツン": 18,
        "九州そらセクシー": 17,
        "九州そらささやき": 19,
        "もち子さん": 20,
        "WhiteCul": 23,
        "WhiteCulたのしい": 24,
        "WhiteCulかなしい": 25,
        "WhiteCulびえーん": 26,
        "後鬼人間": 27,
        "後鬼ぬいぐるみ": 28,
        "No.7": 29,
        "No.7アナウンス": 30,
        "No.7アナウンス": 30,
        "No.7読み聞かせ": 31,
        "櫻歌ミコ": 43,
        "櫻歌ミコ第二形態": 44,
        "櫻歌ミコロリ": 45,
        "sayo": 46,
        "ナースロボタイプT": 47,
        "ナースロボタイプT楽々": 48,
        "ナースロボタイプT恐怖": 49,
        "ナースロボタイプT内緒話": 50,
        "春歌ナナ": 54,
        "猫使アル": 55,
        "猫使アルおちつき": 56,
        "猫使アルうきうき": 57,
        "猫使ビィ": 58,
        "猫使ビィおちつき": 59,
        "猫使ビィ人見知り": 60,
    },
    "COEIROINK": {
        "つくよみちゃんれいせい": 0,
        "つくよみちゃんおしとやか": 5,
        "つくよみちゃんげんき": 6,
        "MANA": 1,
        "MANAいっしょうけんめい": 7,
        "MANAごきげん": 40,
        "ディアちゃん": 3,
        "アルマちゃん表v1": 4,
        "アルマちゃん表v2": 10,
        "アルマちゃん裏": 11,
        "KANA": 30,
        "KANAえんげき": 31,
        "KANAほうかご": 32,
        "MANA+ふくれっつら": 41,
        "MANA+しょんぼり": 42,
        "MANA+ないしょばなし": 43,
        "MANA+ひっさつわざ": 44,
        "AI声優朱花": 50,
        "リリンちゃん": 90,
        "リリンちゃんささやき": 91,
        "ろさちゃんsoft": 327965129,
        "ろさちゃんsoftはきはき": 1863560156,
        "ろさちゃんsoftQ": 1863560157,
        "ろさちゃんquiet": 1624935238,
        "ろさちゃんquietはきはき": 1505745522,
        "ろさちゃんpress": 1551844697,
        "ろさちゃんfaster": 2053618772,
    },
    "SHAREVOX": {
        "小春音アミ": 7,
        "小春音アミ喜び": 8,
        "小春音アミ怒り": 9,
        "小春音アミ悲しみ": 10,
        "つくよみちゃんおしとやか": 11,
    },
    "CapCut": {
        'カワボ': "",
        'お姉さん': "",
        '少女': "",
        '女子': "",
        '男子': "",
        '坊ちゃん': "",
        '癒し系女子': "",
        '女子アナ': "",
        '男性アナ': "",
        '元気ロリ': "",
        '明るいハニー': "",
        '優しいレディー': "",
        '風雅メゾソプラノ': "",
        'Naoki': "",
        'Sakura': "",
        'Keiko': "",
        'Miho': "",
        'ヒカキン': "",
        '丸山礼': "",
        '修一朗': "",
        'マツダ家の日常': "",
        'まちこりーた': "",
        'モジャオ': "",
        'モリスケ': "",
    },
}


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
        label = tkinter.Label(self, text="声を選択してください")
        label.pack(side="top")
        # 閉じるボタン
        stop_btn = tkinter.Button(self, text="会話を終える", command=self.stop_loop)
        stop_btn.pack(side='bottom')

        combobox_frame = tkinter.Frame(self)
        combobox_frame.pack(anchor="center")
        # 合成ソフトの選択
        selected = tkinter.StringVar()
        self.combobox1 = ttk.Combobox(
            combobox_frame,
            justify="center",
            state="readonly",
            values=list(select_voice_dict.keys()),
            textvariable=selected,
            width=10,
        )
        self.combobox1.set("VOICEVOX")
        self.combobox1.bind(
            "<<ComboboxSelected>>",
            lambda event: self.combobox2.configure(values=list(select_voice_dict[self.combobox1.get()].keys())))
        self.combobox1.set("VOICEVOX")
        self.combobox1.pack(side="left")

        # 話者の選択
        self.combobox2 = ttk.Combobox(
            combobox_frame,
            justify="center",
            state="readonly",
            values=list(select_voice_dict[self.combobox1.get()].keys()),
            width=20,
            height=20,
        )
        self.combobox2.pack(side="left")

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
            text = main.listen()
            ai_response = main.get_ai_response(text)
            if self.combobox1.get() == "VOICEVOX":
                main.voicevox_speak(ai_response, speaker=select_voice_dict["VOICEVOX"][self.combobox2.get()])
            elif self.combobox1.get() == "COEIROINK":
                main.coeiroink_speak(ai_response, speaker=select_voice_dict["COEIROINK"][self.combobox2.get()])
            elif self.combobox1.get() == "SHAREVOX":
                main.sharevox_speak(ai_response, speaker=select_voice_dict["SHAREVOX"][self.combobox2.get()])
            elif self.combobox1.get() == "CapCut":
                main.capcut_speak(ai_response, speaker=self.combobox2.get())


root = tkinter.Tk()
root.title("Talk Friends")
root.geometry("600x400")
app = Application(root=root)
app.mainloop()
