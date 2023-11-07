#%% Librerias
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination
from pgmpy.estimators import BayesianEstimator
from pgmpy.sampling import BayesianModelSampling
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from sklearn.metrics import accuracy_score, confusion_matrix
import pandas as pd
from sklearn.model_selection import train_test_split
import os
import numpy as np

#%% Red bayesiana para predecir el éxito académico

# Estructura de la red
model_success = BayesianNetwork([('debtor', 'tuition'), ('tuition', 'units_1_grade'), ('tuition', 'target'), ('gender', 'tuition'),
                                 ('units_1_approved', 'units_2_approved'), ('units_1_grade', 'units_2_grade'), ('units_1_grade', 'units_1_approved'),
                                 ('units_2_approved', 'target'), ('units_2_approved', 'scholarship')])

# Subir csv
data_model = pd.read_csv("C:/Users/jd.umana10/Documents/GitHub/predictor_academico_2/aprendizaje_estructura/data_model.csv")

# Dividir datos en train y test
X_train, X_test = train_test_split(data_model, stratify= data_model['target'], random_state=42)

# Emplear el módulo de ajuste de pgmpy para ajustar la CPDs del nuevo modelo
emv_success = MaximumLikelihoodEstimator(model = model_success, data = X_train)

# Obtener las CPDs ajustadas
cpds = emv_success.get_parameters()

print("Calculando cpds...")
cpdem_debtor = emv_success.estimate_cpd (node = 'debtor')
cpdem_tuition = emv_success.estimate_cpd (node = 'tuition')
cpdem_gender = emv_success.estimate_cpd (node = 'gender')
cpdem_scholarship = emv_success.estimate_cpd (node = 'scholarship')
cpdem_units_1_approved = emv_success.estimate_cpd (node = 'units_1_approved')
cpdem_units_1_grade = emv_success.estimate_cpd (node = 'units_1_grade')
cpdem_units_2_approved = emv_success.estimate_cpd (node = 'units_2_approved')
cpdem_units_2_grade = emv_success.estimate_cpd (node = 'units_2_grade')
cpdem_target = emv_success.estimate_cpd (node = 'target')

#Asociar las CPDs al modelo
model_success.add_cpds(cpdem_debtor,
                       cpdem_tuition,
                       cpdem_gender,
                       cpdem_scholarship,
                       cpdem_units_1_approved,
                       cpdem_units_1_grade,
                       cpdem_units_2_approved,
                       cpdem_units_2_grade,
                       cpdem_target)

#Revisar que el modelo esté completo
print("Modelo completo:",model_success.check_model())


# Crear un objeto de inferencia
inference = VariableElimination(model_success)

def make_predictions(inference):

    # Crear una lista para guardar las predicciones
    predictions = []

    for _, row in X_test.iterrows():

        # Crear un diccionario de evidencias con los datos de cada fila en datos de prueba
        evidence = {variable: row[variable] for variable in row.index if variable!='target'}
        # Realizar la inferencia para obtener la CPD de "success" dado la evidencia
        try:
            result = inference.query(variables=['target'], evidence=evidence)
        # Agregar la predicción a la lista de predicciones
            list_result = list(result.values)
            max_val = list_result.index(max(result.values))
            if max_val == 0:
                predictions.append('Dropout')
            elif max_val == 1:
                predictions.append('Enrolled')
            else:
                predictions.append('Graduate')
        except:
            predictions.append('NaN')

    # Obtener el ground truth para comparar las predicciones
    y_true = X_test['target'].tolist()

    # Calcular la exactitud del modelo
    accuracy = accuracy_score(y_true, predictions)
    print(f'Exactitud (Accuracy): {accuracy}')

    # Calcular la matriz de confusión
    confusion = confusion_matrix(y_true, predictions)

    # Extraer los valores de Verdaderos positivos, falsos positivos, falsos negativos y verdaderos negativos.
    # Se entiende como positivo haberse graduado, y negativo seguir matrículado o desertar
    t_drop, drop_as_enr, drop_as_grad, na_1, enr_as_drop, t_enr, enr_as_grad, na_2, grad_as_drop, grad_as_enr, t_grad, na_3, na_4, na_5, na_6, na_7 = confusion.ravel()
    true_positives = sum({t_grad})
    false_positives = sum({drop_as_grad, enr_as_grad})
    true_negatives = sum({t_drop, drop_as_enr, enr_as_drop, t_enr})
    false_negatives = sum({grad_as_drop, grad_as_enr})

    return true_positives, false_positives, true_negatives, false_negatives

if __name__ == "__main__":
    tp, fp, tn, fn = make_predictions(inference)
    print(f'Verdaderos Positivos: {tp}')
    print(f'Falsos Positivos: {fp}')
    print(f'Verdaderos Negativos: {tn}')
    print(f'Falsos Negativos: {fn}')


import pickle
filename='C:/Users/jd.umana10/Documents/GitHub/predictor_academico_2/aprendizaje_estructura/model.pkl'
with open(filename,'wb') as file:
    pickle.dump(model_success, file)
    file.close()