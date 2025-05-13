import tkinter as tk
from tkinter import messagebox
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # Настройка основного окна приложения
        self.title("Помогатор")
        self.geometry("400x300")
        self.mode = tk.StringVar(value="calculator")  # Стандартный режим
        self.create()

    def create(self):
        # Рамка для выбора режима
        mode_frame = tk.Frame(self)
        mode_frame.pack(pady=10)
         # Переключатели для выбора режима
        tk.Radiobutton(mode_frame, text="Калькулятор", variable=self.mode, value="calculator", command=self.show_cal).pack(side=tk.LEFT)
        tk.Radiobutton(mode_frame, text="Уравнятор", variable=self.mode, value="equations", command=self.show_eq).pack(side=tk.LEFT)
        tk.Radiobutton(mode_frame, text="Графикатор", variable=self.mode, value="graph", command=self.show_graph).pack(side=tk.LEFT)
        # Рамка для содержимого, которая будет обновляться согласно выбранному режиму
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(pady=5)
        # Отобразить содержимое для режима калькулятора по умолчанию
        self.show_cal()
        
    def show_cal(self):
        # Очистка предыдущего содержимого
        self.clear_content()
        # Метка для ввода арифметического выражения
        tk.Label(self.content_frame, text="Вводим пример, который хотим решить").pack()
        self.expr_entry = tk.Entry(self.content_frame)# Поле ввода
        self.expr_entry.pack()
        # Кнопка для вычисления введенного выражения
        tk.Button(self.content_frame, text="Получаем", command=self.calculate).pack()
        self.result_label = tk.Label(self.content_frame, text="")# Метка для отображения результата
        self.result_label.pack()

    def calculate(self):
        try:
            res = eval(self.expr_entry.get())# Вычисляем результат с помощью eval
            self.result_label.config(text=f"Результат: {res:.2f}")# Отображаем результат на метке с 2-мя знаками после запятой
        except Exception:
            self.show_error("Некорректное арифметическое выражение.")# Обработка ошибки

    def show_eq(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Выбираем тип уравнения:").pack()
        self.equation_type = tk.StringVar(value="linear")
        # Метка и переключатели для выбора типа уравнения
        tk.Radiobutton(self.content_frame, text="Линейное (ax+b=0)", variable=self.equation_type, value="linear").pack()
        tk.Radiobutton(self.content_frame, text="Квадратное (ax^2+bx+c=0)", variable=self.equation_type, value="quadratic").pack()
        # Поле ввода для уравнения
        tk.Label(self.content_frame, text="Вводим коэффициенты").pack()
        self.eq_entry = tk.Entry(self.content_frame)
        self.eq_entry.pack()
        # Кнопка для решения уравнения
        tk.Button(self.content_frame, text="Получаем", command=self.solve_equation).pack()
        self.equation_result = tk.Label(self.content_frame, text="")# Метка для отображения результата уравнения
        self.equation_result.pack()

    def solve_equation(self):
        if self.equation_type.get() == "linear":
            self.solve_linear_equation(self.eq_entry.get()) #Решение линейного уравнения
        else:
            self.solve_quadratic_equation(self.eq_entry.get())  # Либо решение квадратного уравнения

    def solve_linear_equation(self, eq):
        try:
            a, b = [float(i) for i in eq.split() if i] #Ввод должен быть вида "a b"
            if a == 0:
                if b == 0:
                    self.equation_result.config(text="Бесконечнооо решений")
                else:
                    self.equation_result.config(text="Нет решений")
            else:
                sol = -b/a
                self.equation_result.config(text=f"Решение: {sol}")
        except Exception:
            self.show_error("Некорректное линейное уравнение")

    def solve_quadratic_equation(self, eq):
        try:
                        # Обработка квадратного уравнения
            eq = eq.replace('^', '**')  # Заменить '^' на '**' для eval
            a, b, c = [float(i) for i in eq.split() if i]  # Ввод должен быть вида "a b c"
            dis = b**2 - 4*a*c
            
            if dis > 0:
                x1 = (-b + dis**0.5) / (2*a)
                x2 = (-b - dis**0.5) / (2*a)
                self.equation_result.config(text=f"Два решения: x1 = {x1}, x2 = {x2}")
            elif dis == 0:
                x = -b / (2*a)
                self.equation_result.config(text=f"Одно решение: x = {x}")
            else:
                self.equation_result.config(text="Нет действительных решений")
        except Exception:
            self.show_error("Некорректное квадратное уравнение")

    def show_graph(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Вводим функцию y(x):").pack()
        self.func_entry = tk.Entry(self.content_frame)
        self.func_entry.pack()

        tk.Label(self.content_frame, text="Вводим границы x_min и x_max (через пробел):").pack()
        self.bounds_entry = tk.Entry(self.content_frame)
        self.bounds_entry.pack()

        tk.Button(self.content_frame, text="Строим график", command=self.plot_graph).pack()

    def plot_graph(self):
        func = self.func_entry.get()
        try:
            bounds = list(map(float, self.bounds_entry.get().split())) # Извлечение границ из ввода
            if len(bounds) != 2:	# Проверка на количество границ
                raise ValueError("Должно быть указано два значения.")
            x = np.linspace(bounds[0], bounds[1], 100)	# Генерация значений x
            y = eval(func) # Вычисление значений y по функции
            plt.plot(x, y)
            plt.title("График классной функции")
            plt.xlabel("x")
            plt.ylabel("y")
            plt.grid()
            plt.show()	 # Отображение графика
        except Exception:
            self.show_error("Некорректная функция или границы")

    def show_error(self, message):
        messagebox.showerror("Ошибка ввода", message)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
