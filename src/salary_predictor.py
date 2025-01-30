import numpy as np
import joblib

class SalaryPredictor:
    def __init__(self, model_path="model/linear_regression_salary_model.pkl"):
        self.model = joblib.load(model_path)
    
    def predict(self, years_experience):
        """
        Realiza a predição do salário baseado nos anos de experiência
        Retorna: (salario_anual, salario_mensal)
        """
        if not isinstance(years_experience, (int, float)):
            years_experience = float(str(years_experience).replace(',', '.'))
            
        if years_experience < 0:
            raise ValueError("Anos de experiência não podem ser negativos")
            
        x_novo = np.array([[years_experience]])
        salary = self.model.predict(x_novo)[0]
        
        return salary, salary/12
