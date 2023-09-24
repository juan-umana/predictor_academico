import ucimlrepo
from ucimlrepo import fetch_ucirepo 

import numpy as np
import pandas as pd
import scipy.stats as ss
import seaborn as sns
import matplotlib.pyplot as plt

# fetch dataset 
predict_students_dropout_and_academic_success = fetch_ucirepo(id=697) 
  
# data (as pandas dataframes) 
predictors = predict_students_dropout_and_academic_success.data.features # All variables/predictors
academic_success = predict_students_dropout_and_academic_success.data.targets # Academic status

# Joined data
origin_data = predictors.join(academic_success)

# Set column names in snake_case
origin_data.columns = origin_data.columns.str.lower()
origin_data.columns = origin_data.columns.str.replace(' ', '_')

# Dictionaries
# Categorical variables
marital_status_dic = {1 : 'single', 2 : 'married', 3 : 'widower',
                       4 : 'divorced', 5 : 'facto union', 6 : 'legally separated'}
application_mode_dic = {1 : '1st phase : general contingent', 2 : 'Ordinance No. 612/93', 5 : '1st phase : special contingent (Azores Island)',
                        7 : 'Holders of other higher courses', 10 : 'Ordinance No. 854:B/99', 15 : 'International student (bachelor)',
                        16 : '1st phase : special contingent (Madeira Island)', 17 : '2nd phase : general contingent', 18 : '3rd phase : general contingent',
                        26 : 'Ordinance No. 533:A/99, item b2) (Different Plan)', 27 :' Ordinance No. 533:A/99, item b3 (Other Institution)',
                        39 : 'Over 23 years old', 42 : 'Transfer', 43 : 'Change of course', 44 : 'Technological specialization diploma holders',
                        51 : 'Change of institution/course', 53 : 'Short cycle diploma holders', 57 : 'Change of institution/course (International)'}
course_dic = {33 : 'Biofuel Production Technologies', 171 : 'Animation and Multimedia Design', 8014 : 'Social Service (evening attendance)', 9003 : 'Agronomy',
              9070 : 'Communication Design', 9085 : 'Veterinary Nursing', 9119 : 'Informatics Engineering', 9130 : 'Equinculture', 9147 : 'Management',
              9238 : 'Social Service', 9254 : 'Tourism', 9500 : 'Nursing', 9556 : 'Oral Hygiene', 9670 : 'Advertising and Marketing Management',
              9773 : 'Journalism and Communication', 9853 : 'Basic Education', 9991 : 'Management (evening attendance)'}
attendance_dic = {1 : 'daytime', 0 : 'evening'}
prev_qual_dic = {1 : 'Secondary education', 2 : 'Higher education - bachelors degree', 3 : 'Higher education - degree', 4 : 'Higher education - masters',
                 5 : 'Higher education - doctorate', 6 : 'Frequency of higher education', 9 : '12th year of schooling - not completed',
                 10 : '11th year of schooling - not completed', 12 : 'Other - 11th year of schooling', 14 : '10th year of schooling',
                 15 : '10th year of schooling - not completed', 19 : 'Basic education 3rd cycle (9th/10th/11th year) or equiv.',
                 38 : 'Basic education 2nd cycle (6th/7th/8th year) or equiv.', 39 : 'Technological specialization course', 40 : 'Higher education : degree (1st cycle)',
                 42 : 'Professional higher technical course', 43 : 'Higher education - master (2nd cycle)'}
nacionality_dic = {1 : 'Portuguese', 2 : 'German', 6 : 'Spanish', 11 : 'Italian', 13 : 'Dutch', 14 : 'English', 17 : 'Lithuanian', 21 : 'Angolan', 22 : 'Cape Verdean',
                   24 : 'Guinean', 25 : 'Mozambican', 26 : 'Santomean', 32 : 'Turkish', 41 : 'Brazilian', 62 : 'Romanian', 100 : 'Moldova (Republic of)', 101 : 'Mexican',
                   103 : 'Ukrainian', 105 : 'Russian', 108 : 'Cuban', 109 : 'Colombian'}
parent_education_dic = {1 : 'Secondary Education - 12th Year of Schooling or Eq.', 2 : 'Higher Education - Bachelors Degree', 3 : 'Higher Education - Degree',
                        4 : 'Higher Education - Masters', 5 : 'Higher Education - Doctorate', 6 : 'Frequency of Higher Education', 9 : '12th Year of Schooling - Not Completed',
                        10 : '11th Year of Schooling - Not Completed', 11 : '7th Year (Old)', 12 : 'Other - 11th Year of Schooling', 14 : '10th Year of Schooling',
                        18 : 'General commerce course', 19 : 'Basic Education 3rd Cycle (9th/10th/11th Year) or Equiv.', 22 : 'Technical-professional course',
                        26 : '7th year of schooling', 27 : '2nd cycle of the general high school course', 29 : '9th Year of Schooling - Not Completed', 30 : '8th year of schooling',
                        34 : 'Unknown', 35 : 'Cant read or write', 36 : 'Can read without having a 4th year of schooling', 37 : B'asic education 1st cycle (4th/5th year) or equiv.',
                        38 : 'Basic Education 2nd Cycle (6th/7th/8th Year) or Equiv.', 39 : 'Technological specialization course', 40 : 'Higher education - degree (1st cycle)',
                        41 : 'Specialized higher studies course', 42 : 'Professional higher technical course', 43 : 'Higher Education - Master (2nd cycle)', 44 : 'Higher Education - Doctorate (3rd cycle)'}
parent_occupation_dic = {0 : 'Student', 1 : 'Representatives of the Legislative Power and Executive Bodies, Directors, Directors and Executive Managers', 2 : 'Specialists in Intellectual and Scientific Activities',
                         3 : 'Intermediate Level Technicians and Professions', 4 : 'Administrative staff', 5 : 'Personal Services, Security and Safety Workers and Sellers',
                         6 : 'Farmers and Skilled Workers in Agriculture, Fisheries and Forestry', 7 : 'Skilled Workers in Industry, Construction and Craftsmen', 8 : 'Installation and Machine Operators and Assembly Workers',
                         9 : 'Unskilled Workers', 10 : 'Armed Forces Professions', 90 : 'Other Situation', 99 : '(blank)', 122 : 'Health professionals', 123 : 'teachers', 125 : 'Specialists in information and communication technologies (ICT)',
                         131 : 'Intermediate level science and engineering technicians and professions', 132 : 'Technicians and professionals, of intermediate level of health',
                         134 : 'Intermediate level technicians from legal, social, sports, cultural and similar services', 141 : 'Office workers, secretaries in general and data processing operators',
                         143 : 'Data, accounting, statistical, financial services and registry-related operators', 144 : 'Other administrative support staff', 151 : 'personal service workers', 152 : 'sellers',
                         153 : 'Personal care workers and the like', 171 : 'Skilled construction workers and the like, except electricians', 173 : 'Skilled workers in printing, precision instrument manufacturing, jewelers, artisans and the like',
                         175 : 'Workers in food processing, woodworking, clothing and other industries and crafts', 191 : 'cleaning workers', 192 : 'Unskilled workers in agriculture, animal production, fisheries and forestry',
                         193 : 'Unskilled workers in extractive industry, construction, manufacturing and transport', 194 : 'Meal preparation assistants'}
displaced_dic = {1 : 'yes', 0 : 'no'}
special_needs_dic = {1 : 'yes', 0 : 'no'}
debtor_dic = {1 : 'yes', 0 : 'no'}
tuition_uptodate_dic = {1 : 'yes', 0 : 'no'}
gender_dic = {1 : 'male', 0 : 'female'}
scholarship_dic = {1 : 'yes', 0 : 'no'}
international = {1 : 'yes', 0 : 'no'}

## Continous variables
# application_order_dic = Application order (between 0 - first choice; and 9 last choice)
# prev_qual_grade_dic = Grade of previous qualification (between 0 and 200)
# admission_grade = Admission grade (between 0 and 200)
# age = Age of studend at enrollment
# units_i_semester_credited/enrolled/evaluations/approved/wo_evaluation = number of units redited/enrolled/evaluations/approved/wo_evaluation in semester i
# units_i_semester_grade = Grade average in the ith semester (between 0 and 20)
# unemployment_rate
# inflation_rate
# GDP

## For continous variables

# Target as continous variable
target_contin = origin_data['target'].apply(lambda x: 1 if x == 'Graduate' else -1)
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

# TO DO
cramers_v(categ_data,origin_data['target'])

#explore : https://blog.knoldus.com/how-to-find-correlation-value-of-categorical-variables/