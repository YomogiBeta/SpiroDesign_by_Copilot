from tkinter import Button, Frame, Label, simpledialog
from tkinter.ttk import Scale
from tkinter import LEFT


class ScaleDialog(simpledialog.Dialog):
    def __init__(self, master, callback, min_number: int, max_number: int, init_value: int) -> None:
        self.a_callback = callback
        self.a_init_value = init_value
        self.a_min = min_number
        self.a_max = max_number
        super(ScaleDialog, self).__init__(parent=master, title="Select Value")

    def body(self, master):

        self.a_value_label = Label(master, text="None")

        self.a_scale = Scale(master,
                             command=self.update_value_label,
                             from_=self.a_min,
                             to=self.a_max,
                             length=320
                             )
        self.a_scale.set(self.a_init_value)

        self.a_scale.pack()
        self.a_value_label.pack()

    def buttonbox(self):
        box = Frame(self)

        self.a_ok_button = Button(box, text="OK", width=10, command=self.ok_button_clicked)
        self.a_ok_button.pack(side=LEFT, padx=5, pady=5)

        box.pack()

    def ok_button_clicked(self):
        """OKボタンが押されたときの処理"""
        value = self.a_scale.get()
        self.a_callback(round(value, 2))
        self.destroy()

    def update_value_label(self, value):
        """スケールの値が変更されたときに、ラベルの値を更新します

        Args:
            value (str):
                スケールの値
        """
        self.a_value_label["text"] = str(round(float(value), 2))
