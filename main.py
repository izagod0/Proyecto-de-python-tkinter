import tkinter as tk
from controlador import ControladorHotel


def main():
    root = tk.Tk()
    app = ControladorHotel(root)
    root.mainloop()


if __name__ == "__main__":
    main()