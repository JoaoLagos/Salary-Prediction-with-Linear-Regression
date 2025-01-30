import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import explained_variance_score, max_error
import matplotlib.pyplot as plt
from joblib import dump, load

class LinearRegressionModel:
    def __init__(self, dataset_path):
        """Inicializa o modelo de regressão linear"""
        self.data = pd.read_csv(dataset_path)
        self.model = LinearRegression()
        self._prepare_data()
    
    def _prepare_data(self):
        """Prepara os dados para treinamento e teste"""
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.data['YearsExperience'].values.reshape(-1, 1),
            self.data['Salary'],
            test_size=0.2,
            random_state=42
        )
    
    def train(self):
        """Treina o modelo"""
        self.model.fit(self.X_train, self.y_train)
        return self
    
    def evaluate(self, show_metrics=True):
        """Avalia o modelo e mostra os gráficos e métricas"""
        y_pred = self.model.predict(self.X_test)
        
        # Cálculo das métricas
        mse = np.mean((y_pred - self.y_test) ** 2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(y_pred - self.y_test))
        r2 = self.model.score(self.X_test, self.y_test)
        mape = np.mean(np.abs((self.y_test - y_pred) / self.y_test)) * 100
        ev_score = explained_variance_score(self.y_test, y_pred)
        max_err = max_error(self.y_test, y_pred)
        corr = np.corrcoef(self.y_test, y_pred)[0,1]
        
        if show_metrics:
            print("\n=== Métricas de Avaliação ===")
            print(f"MSE (Erro Quadrático Médio): {mse:.2f}")
            print(f"RMSE (Raiz do Erro Quadrático Médio): {rmse:.2f}")
            print(f"MAE (Erro Médio Absoluto): {mae:.2f}")
            print(f"MAPE (Erro Percentual Médio): {mape:.2f}%")
            print(f"R² (Coeficiente de Determinação): {r2:.4f}")
            print(f"Variância Explicada: {ev_score:.4f}")
            print(f"Erro Máximo: {max_err:.2f}")
            print(f"Correlação de Pearson: {corr:.4f}")
            
            print("\n=== Coeficientes do Modelo ===")
            print(f"Intercepto: {self.model.intercept_:.2f}")
            print(f"Inclinação: {self.model.coef_[0]:.2f}")
            
            # Visualizações originais
            plt.figure(figsize=(10, 5))
            plt.subplot(1, 2, 1)
            plt.scatter(self.data['YearsExperience'], self.data['Salary'])
            plt.plot(self.X_train, self.model.predict(self.X_train), '-', color='red')
            plt.title('Regressão Linear - Previsões vs Valores Reais')
            plt.xlabel('Anos de Experiência')
            plt.ylabel('Salário')
            
            # Scatter plot
            plt.subplot(1, 2, 2)
            plt.scatter(self.data['YearsExperience'], self.data['Salary'])
            plt.plot(self.X_test, self.model.predict(self.X_test), '-', color='red', linewidth=2)
            plt.title('Regressão Linear - Scatter Plot')
            plt.xlabel('Anos de Experiência')
            plt.ylabel('Salário')
            
            plt.tight_layout()
            plt.show()
    
    def save(self, filepath='model/linear_regression_salary_model.pkl'):
        """Salva o modelo treinado"""
        dump(self.model, filepath)
    
    def predict(self, X):
        """Realiza predições com o modelo"""
        return self.model.predict(X.reshape(-1, 1))
    
    def create(self, show_metrics=True):
        self.train()
        if show_metrics:
            self.evaluate(show_metrics=show_metrics)
        self.save()

if __name__ == "__main__":
    # Exemplo de uso
    model = LinearRegressionModel('dataset/Salary_dataset.csv')
    model.create()