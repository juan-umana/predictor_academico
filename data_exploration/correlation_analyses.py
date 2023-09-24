import numpy as np
import pandas as pd
import scipy.stats as ss
import seaborn as sns
import matplotlib.pyplot as plt

###### Correlation analyses for variables selection

## For continous variables

# Target as continous variable
target_contin = origin_data['target'].apply(lambda x: 1 if x == 'Graduate' else 0)
target_contin_df = pd.DataFrame({'target_contin' : target_contin})

# Continous predictors
contin_data = origin_data[['application_order','previous_qualification_(grade)',
                         'admission_grade','age_at_enrollment',
                         'curricular_units_1st_sem_(credited)',
                         'curricular_units_1st_sem_(enrolled)',
                         'curricular_units_1st_sem_(evaluations)',
                         'curricular_units_1st_sem_(approved)',
                         'curricular_units_1st_sem_(grade)',
                         'curricular_units_1st_sem_(without_evaluations)',
                         'curricular_units_2nd_sem_(credited)',
                         'curricular_units_2nd_sem_(enrolled)',
                         'curricular_units_2nd_sem_(evaluations)',
                         'curricular_units_2nd_sem_(approved)',
                         'curricular_units_2nd_sem_(grade)',
                         'curricular_units_2nd_sem_(without_evaluations)',
                         'unemployment_rate', 'inflation_rate', 'gdp']]

# Continous data
contin_data = contin_data.join(target_contin_df)

# Selecting target column
target_column = 'target_contin'

# Calculate the correlations
correlations = contin_data.corr()

# Sort correlations by absolute values with respect to the target column
contin_correlation_with_target = correlations[target_column].abs().sort_values(ascending=False)

print('Correlation results for continous data')
print(contin_correlation_with_target)

## For categorical variables

def cramers_v(x, y):
    confusion_matrix = pd.crosstab(x,y)
    chi2 = ss.chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2/n
    r,k = confusion_matrix.shape
    phi2corr = max(0, phi2-((k-1)*(r-1))/(n-1))
    rcorr = r-((r-1)**2)/(n-1)
    kcorr = k-((k-1)**2)/(n-1)
    return np.sqrt(phi2corr/min((kcorr-1),(rcorr-1)))

# from https://stackoverflow.com/a/46498792/5863503


categ_data = origin_data.drop(['application_order','previous_qualification_(grade)',
                         'admission_grade','age_at_enrollment',
                         'curricular_units_1st_sem_(credited)',
                         'curricular_units_1st_sem_(enrolled)',
                         'curricular_units_1st_sem_(evaluations)',
                         'curricular_units_1st_sem_(approved)',
                         'curricular_units_1st_sem_(grade)',
                         'curricular_units_1st_sem_(without_evaluations)',
                         'curricular_units_2nd_sem_(credited)',
                         'curricular_units_2nd_sem_(enrolled)',
                         'curricular_units_2nd_sem_(evaluations)',
                         'curricular_units_2nd_sem_(approved)',
                         'curricular_units_2nd_sem_(grade)',
                         'curricular_units_2nd_sem_(without_evaluations)',
                         'unemployment_rate', 'inflation_rate', 'gdp'],
                         axis = 1)

categ_data = categ_data.map(str)

cramers_v(categ_data,categ_data)




#print(origin_data['target'])


# # # Plot the correlations
# # plt.figure(figsize=(10, 6))
# # correlation_with_target.plot(kind='bar')
# # plt.title(f'Correlations with {target_column}')
# # plt.xlabel('Features')
# # plt.ylabel('Absolute Correlation')
# # plt.xticks(rotation=45)
# # plt.show()

# # # Print the sorted correlations
# # print(correlation_with_target)
