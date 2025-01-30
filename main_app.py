import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from linear_regression import LinearRegressionModel
from src.salary_predictor import SalaryPredictor
import numpy as np
from ttkbootstrap import Style

class SalaryPredictorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Preditor de Salários")
        self.root.geometry("400x350")
        self.root.iconphoto(False, tk.PhotoImage(file="images/icon.png"))
        
        # Carregando o modelo
        try:
            self.predictor = SalaryPredictor()
        except:
            messagebox.showerror("Erro", "Modelo não encontrado! Estamos tentando recriar o modelo...")
            try:
                model = LinearRegressionModel("dataset/Salary_dataset.csv")
                model.create(show_metrics=False)

                self.predictor = SalaryPredictor()
                
                messagebox.showinfo("Sucesso", "Modelo recriado com sucesso!")
            except:
                messagebox.showerror("Erro", "Modelo não encontrado!")
                root.destroy()
                return
        
        # Frame principal
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(
            main_frame, 
            text="Predição de Salário por Anos de Experiência",
            font=("Helvetica", 12, "bold"),
            wraplength=300,
            justify="center"
        )
        title_label.pack(pady=20)
        
        # Frame para entrada
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        # Label e entrada
        input_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="Anos de Experiência:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.years_entry = ttk.Entry(input_frame, width=10)
        self.years_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Botão de predição
        ttk.Button(
            main_frame,
            text="Prever Salário",
            command=self.predict_salary,
            style="primary.TButton"
        ).pack(pady=20)
        
        # Label para resultado
        self.result_var = tk.StringVar()
        self.result_var.set("R$ 0,00/anual\nR$ 0,00/mensal")
        result_label = ttk.Label(
            main_frame,
            textvariable=self.result_var,
            font=("Helvetica", 16, "bold")
        )
        result_label.pack(pady=20)
    
    @staticmethod
    def format_currency_br(value):
        """Formata o valor para o padrão brasileiro de moeda"""
        value_str = f"{value:.2f}"
        parts = value_str.split('.')
        int_part = ''
        for i, digit in enumerate(reversed(parts[0])):
            if i > 0 and i % 3 == 0:
                int_part = '.' + int_part
            int_part = digit + int_part
        return f"R$ {int_part},{parts[1]}"
    
    def predict_salary(self):
        try:
            years = self.years_entry.get()
            annual_salary, monthly_salary = self.predictor.predict(years)
            
            # Formatando o resultado usando o método local
            salary_annual = self.format_currency_br(annual_salary)
            salary_monthly = self.format_currency_br(monthly_salary)
            formatted_salary = f"{salary_annual}/anual\n{salary_monthly}/mensal"
            self.result_var.set(formatted_salary)
            
        except ValueError as e:
            messagebox.showerror(
                "Erro", 
                "Por favor, insira um número válido de anos de experiência!"
            )
        except Exception as e:
            messagebox.showerror("Erro", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = SalaryPredictorApp(root)
    root.mainloop()
