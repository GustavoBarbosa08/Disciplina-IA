#Sistema Fuzzy para uma lavadora inteligente
# Gustavo Barbosa Neves 
# Thalles Augusto Monteiro Martins 
import numpy as np
import pandas as pd
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Universos
quant_range = np.arange(1, 11, 1)
suj_range = np.arange(1, 11, 1)
press_range = np.arange(1, 101, 1)

# Funções de pertinência para três tipos
def definir_pertinencia(tipo, quantidade, sujeira, pressao):
    if tipo == 'triangular':
        quantidade['pouca'] = fuzz.trimf(quant_range, [1, 1, 4])
        quantidade['media'] = fuzz.trimf(quant_range, [3, 5, 7])
        quantidade['muita'] = fuzz.trimf(quant_range, [6, 10, 10])
        
        sujeira['leve'] = fuzz.trimf(suj_range, [1, 1, 4])
        sujeira['moderada'] = fuzz.trimf(suj_range, [3, 5, 7])
        sujeira['pesada'] = fuzz.trimf(suj_range, [6, 10, 10])

        pressao['baixa'] = fuzz.trimf(press_range, [1, 1, 40])
        pressao['media'] = fuzz.trimf(press_range, [30, 50, 70])
        pressao['alta'] = fuzz.trimf(press_range, [60, 100, 100])

    elif tipo == 'trapezoidal':
        quantidade['pouca'] = fuzz.trapmf(quant_range, [1, 1, 2, 4])
        quantidade['media'] = fuzz.trapmf(quant_range, [3, 4, 6, 7])
        quantidade['muita'] = fuzz.trapmf(quant_range, [6, 8, 10, 10])

        sujeira['leve'] = fuzz.trapmf(suj_range, [1, 1, 2, 4])
        sujeira['moderada'] = fuzz.trapmf(suj_range, [3, 4, 6, 7])
        sujeira['pesada'] = fuzz.trapmf(suj_range, [6, 8, 10, 10])

        pressao['baixa'] = fuzz.trapmf(press_range, [1, 1, 10, 40])
        pressao['media'] = fuzz.trapmf(press_range, [30, 40, 60, 70])
        pressao['alta'] = fuzz.trapmf(press_range, [60, 90, 100, 100])

    elif tipo == 'gaussiana':
        quantidade['pouca'] = fuzz.gaussmf(quant_range, 2, 1)
        quantidade['media'] = fuzz.gaussmf(quant_range, 5, 1)
        quantidade['muita'] = fuzz.gaussmf(quant_range, 8, 1)

        sujeira['leve'] = fuzz.gaussmf(suj_range, 2, 1)
        sujeira['moderada'] = fuzz.gaussmf(suj_range, 5, 1)
        sujeira['pesada'] = fuzz.gaussmf(suj_range, 8, 1)

        pressao['baixa'] = fuzz.gaussmf(press_range, 20, 10)
        pressao['media'] = fuzz.gaussmf(press_range, 50, 10)
        pressao['alta'] = fuzz.gaussmf(press_range, 80, 10)

# Parâmetros
tipos = ['triangular', 'trapezoidal', 'gaussiana']
defuzz_methods = ['centroid', 'bisector', 'mom', 'som', 'lom']
resultados = []
entrada_qtd = 6.0
entrada_suj = 8.0

for tipo in tipos:
    for metodo in defuzz_methods:
        quantidade = ctrl.Antecedent(quant_range, 'quantidade')
        sujeira = ctrl.Antecedent(suj_range, 'sujeira')
        pressao = ctrl.Consequent(press_range, 'pressao')
        definir_pertinencia(tipo, quantidade, sujeira, pressao)
        pressao.defuzzify_method = metodo

        # Regras
        regras = [
            ctrl.Rule(quantidade['pouca'] & sujeira['leve'], pressao['baixa']),
            ctrl.Rule(quantidade['media'] & sujeira['leve'], pressao['media']),
            ctrl.Rule(quantidade['muita'] | sujeira['pesada'], pressao['alta']),
            ctrl.Rule(quantidade['media'], pressao['media'])
        ]

        sistema = ctrl.ControlSystem(regras)
        simulador = ctrl.ControlSystemSimulation(sistema)

        simulador.input['quantidade'] = entrada_qtd
        simulador.input['sujeira'] = entrada_suj
        simulador.compute()

        resultados.append({
            'Função de Pertinência': tipo,
            'Método de Defuzzificação': metodo,
            'Pressão Recomendada': round(simulador.output['pressao'], 2)
        })

# Tabela comparativa
df_resultados = pd.DataFrame(resultados)
print(df_resultados)

# Gráfico
plt.figure(figsize=(10, 6))
for tipo in tipos:
    subset = df_resultados[df_resultados['Função de Pertinência'] == tipo]
    plt.plot(subset['Método de Defuzzificação'], subset['Pressão Recomendada'], marker='o', label=tipo)

plt.title("Comparação de métodos e funções de pertinência")
plt.xlabel("Método de Defuzzificação")
plt.ylabel("Pressão Recomendada (%)")
plt.legend(title="Tipo de Pertinência")
plt.grid(True)
plt.tight_layout()
plt.show()
