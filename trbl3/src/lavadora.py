import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Entradas
quantidade = ctrl.Antecedent(np.arange(1, 11, 1), 'quantidade')
sujeira = ctrl.Antecedent(np.arange(1, 11, 1), 'sujeira')

# Saída
pressao = ctrl.Consequent(np.arange(1, 101, 1), 'pressao')


print(quantidade, sujeira, pressao)

# Funções de pertinência
quantidade['pouca'] = fuzz.trimf(quantidade.universe, [1, 1, 4])
quantidade['media'] = fuzz.trimf(quantidade.universe, [3, 5, 7])
quantidade['muita'] = fuzz.trimf(quantidade.universe, [6, 10, 10])

sujeira['leve'] = fuzz.trimf(sujeira.universe, [1, 1, 4])
sujeira['moderada'] = fuzz.trimf(sujeira.universe, [3, 5, 7])
sujeira['pesada'] = fuzz.trimf(sujeira.universe, [6, 10, 10])

pressao['baixa'] = fuzz.trimf(pressao.universe, [1, 1, 40])
pressao['media'] = fuzz.trimf(pressao.universe, [30, 50, 70])
pressao['alta'] = fuzz.trimf(pressao.universe, [60, 100, 100])

# Regras fuzzy
regra1 = ctrl.Rule(quantidade['pouca'] & sujeira['leve'], pressao['baixa'])
regra2 = ctrl.Rule(quantidade['media'] & sujeira['leve'], pressao['media'])
regra3 = ctrl.Rule(quantidade['muita'] | sujeira['pesada'], pressao['alta'])
regra4 = ctrl.Rule(quantidade['media'], pressao['media'])

# Sistema de controle
pressao_ctrl = ctrl.ControlSystem([regra1, regra2, regra3, regra4])
simulador = ctrl.ControlSystemSimulation(pressao_ctrl)

# Entrada de exemplo
simulador.input['quantidade'] = 6
simulador.input['sujeira'] = 8
simulador.compute()

print(f"Pressão recomendada: {simulador.output['pressao']:.2f}%")
pressao.view(sim=simulador)
plt.show()