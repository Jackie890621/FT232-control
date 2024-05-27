import sys
import ftd2xx as ftd
import time
import tkinter as tk

class RFFE:
    def __init__(self):
        self.gio = ftd.open(0)
        print(self.gio.getDeviceInfo())

        self.GIO_MASK = 0xFF
        self.gio.setBitMode(self.GIO_MASK, 1)
        self.gio.setBaudRate(460900)

        initial_state = bytes([0])
        self.ft_write(initial_state)

        self.checkboxes = []
        self.pin_name = ['TXD', 'RXD', 'RTS', 'CTS', 'DTR', 'DSR', 'DCD', 'RI']
        self.is_on = [False] * 8
        self.button = [None] * 8

    def ft_write(self, data):
        self.gio.write(data)

    def change_color(self, i):
        if self.is_on[i]:
            self.button[i].config(bg="red")
            self.is_on[i] = False
        else:
            self.button[i].config(bg="green3")
            self.is_on[i] = True

    def UI(self):
        self.root = tk.Tk()
        self.root.title("FT232RQ GPIO Control")

        title_label = tk.Label(self.root, text="GPIO Control", font=("Helvetica", 30))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        for i in range(8):
            var = tk.IntVar()
            var.set(0)
            self.button[i] = tk.Checkbutton(self.root, text=self.pin_name[i], variable=var)
            self.button[i].grid(row=i + 1, column=0, padx=10, pady=5)

            # Customize the appearance of the switch
            self.button[i].config(font=("Helvetica", 20))  # Set the font
            self.button[i].config(width=10)  # Adjust the width
            self.button[i].config(bg="red")  # Background color
            if i == 0:
                self.button[i].config(command=lambda: self.change_color(0))
            elif i == 1:
                self.button[i].config(command=lambda: self.change_color(1))
            elif i == 2:
                self.button[i].config(command=lambda: self.change_color(2))
            elif i == 3:
                self.button[i].config(command=lambda: self.change_color(3))
            elif i == 4:
                self.button[i].config(command=lambda: self.change_color(4))
            elif i == 5:
                self.button[i].config(command=lambda: self.change_color(5))
            elif i == 6:
                self.button[i].config(command=lambda: self.change_color(6))
            else:
                self.button[i].config(command=lambda: self.change_color(7))

            self.checkboxes.append(var)

        update_button = tk.Button(self.root, text="Update GPIO", command=self.update_gpio, font=("Helvetica", 20), bg="gray60")
        update_button.grid(row=9, column=0, pady=10)

        self.status_label = tk.Label(self.root, text="Status:", font=("Helvetica", 20))
        self.status_label.grid(row=1, column=1, rowspan=8, columnspan=2, pady=10)

    def update_gpio(self):
        self.gio.setBitMode(self.GIO_MASK, 1)
        self.gio.setBaudRate(460900)

        t="Status:\n"
        state_byte = 0
        for i in range(8):
            if self.checkboxes[i].get():
                state_byte += 2 ** i
                t += self.pin_name[i] + " ON\n"
            else:
                t += self.pin_name[i] + " OFF\n"
        
        state_byte = bytes([state_byte])
        self.ft_write(state_byte)
        self.status_label.config(text=t)
    
    def run(self):       
        self.root.mainloop()

if __name__ == '__main__':  
    rffe = RFFE()
    rffe.UI()
    rffe.run()
    # duration = int(input("duration time:"))

    # t = 0.1
    # cycle = int(duration // t // 2)

    # for _ in range(cycle):
    #     rffe.ft_write(b'x01')
    #     time.sleep(t)
    #     rffe.ft_write(b'x00')
    #     time.sleep(t)

    # print("finish")
 