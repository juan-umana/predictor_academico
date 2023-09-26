library(tidyverse)
library(ggplot2)
library(ggsignif)
library(readr)

setwd("C:/Users/jd.umana10/Documents/GitHub/predictor_academico/data_viz")

origin_data <- read_delim("data.csv", delim = ";", 
                          escape_double = FALSE, trim_ws = TRUE)

colnames(origin_data) <- tolower(colnames(origin_data))
colnames(origin_data) <- str_replace(colnames(origin_data),' ','_')
colnames(origin_data) <- str_replace(colnames(origin_data),"'",'')

origin_data <- origin_data %>% mutate(targe_categ = ifelse(target == "Graduate",
                                                           "Success", "Fail"))

#### Unidades curriculares aprovadas en primer y segundo semestre ####

units_approved_1_plot <- ggplot(origin_data, aes(x = origin_data$targe_categ,
                                                 y = origin_data$`curricular_units 1st sem (approved)`)) + 
  geom_violin(aes(color=targe_categ), trim = TRUE) +
  labs(title = "Curricular units approved in 1st semester", y = "Number of units", x = "") + 
  theme_classic() +
  geom_signif(comparisons = list(c("Success", "Fail")),   
              map_signif_level=TRUE)

units_approved_2_plot <- ggplot(origin_data, aes(x = origin_data$targe_categ,
                                                 y = origin_data$`curricular_units 2nd sem (approved)`)) + 
  geom_violin(aes(color=targe_categ), trim = TRUE) +
  labs(title = "Curricular units approved in 2nd semester", y = "Number of units", x = "") + 
  theme_classic() +
  geom_signif(comparisons = list(c("Success", "Fail")),   
              map_signif_level=TRUE)

#### Calificación de las unidades curriculares en primer y segundo semestre ####

units_grade_1_plot <- ggplot(origin_data, aes(x = origin_data$targe_categ,
                                              y = origin_data$`curricular_units 1st sem (grade)`)) + 
  geom_violin(aes(color=targe_categ), trim = TRUE) +
  labs(title = "Grade units in 1st semester", y = "Grade", x = "") + 
  theme_classic() +
  geom_signif(comparisons = list(c("Success", "Fail")),   
              map_signif_level=TRUE)

units_grade_2_plot <- ggplot(origin_data, aes(x = origin_data$targe_categ,
                                              y = origin_data$`curricular_units 2nd sem (grade)`)) + 
  geom_violin(aes(color=targe_categ), trim = TRUE) +
  labs(title = "Grade units in 2nd semester", y = "Grade", x = "") + 
  theme_classic() +
  geom_signif(comparisons = list(c("Success", "Fail")),   
              map_signif_level=TRUE)

#### Cursos tomados por los estudiantes ####

course_plot <- ggplot(origin_data,aes(x = course)) + 
  theme_light() +
  labs(title = "Student course", y = "Count", x = "Course") +
  geom_histogram(data=subset(origin_data, targe_categ == 'Success'),fill = "green", alpha = 0.25) +
  geom_histogram(data=subset(origin_data, targe_categ == 'Fail'),fill = "red", alpha = 0.25)

#### Matrículas ####

tuition_plot <- ggplot(origin_data,aes(x = `tuition_fees up to date`)) + 
  theme_light() +
  labs(title = "Tuition", y = "Count", x = "Tuition") +
  geom_histogram(data=subset(origin_data, targe_categ == 'Success'),fill = "green", alpha = 0.25) +
  geom_histogram(data=subset(origin_data, targe_categ == 'Fail'),fill = "red", alpha = 0.25)

#### Scholarship ####

scholarship_plot <- ggplot(origin_data,aes(x = scholarship_holder)) + 
  theme_light() +
  labs(title = "Scholarship", y = "Count", x = "Scholarship") +
  geom_histogram(data=subset(origin_data, targe_categ == 'Success'),fill = "green", alpha = 0.25) +
  geom_histogram(data=subset(origin_data, targe_categ == 'Fail'),fill = "red", alpha = 0.25)

#### Application mode ####

application_plot <- ggplot(origin_data,aes(x = application_mode)) + 
  theme_light() +
  labs(title = "Application", y = "Count", x = "Application") +
  geom_histogram(data=subset(origin_data, targe_categ == 'Success'),fill = "green", alpha = 0.25) +
  geom_histogram(data=subset(origin_data, targe_categ == 'Fail'),fill = "red", alpha = 0.25)

#### Edad al momento de ingreso ####

age_plot <- ggplot(origin_data, aes(x = targe_categ, y = `age_at enrollment`)) + 
  geom_violin(aes(color=targe_categ), trim = TRUE) +
  labs(title = "Age at enrollment", y = "Age", x = "") + 
  theme_classic() +
  geom_signif(comparisons = list(c("Success", "Fail")),   
              map_signif_level=TRUE)

#### Unidades curriculares sin evaluación en primer y segundo semestre ####

units_woeval_1_plot <- ggplot(origin_data, aes(x = targe_categ, y = `curricular_units 1st sem (without evaluations)`)) + 
  geom_violin(aes(color=targe_categ), trim = TRUE) +
  labs(title = "Units without evaluation in 1st semester", y = "Number of units", x = "") + 
  theme_classic() +
  geom_signif(comparisons = list(c("Success", "Fail")),   
              map_signif_level=TRUE)

units_woeval_2_plot <- ggplot(origin_data, aes(x = targe_categ, y = `curricular_units 2nd sem (without evaluations)`)) + 
  geom_violin(aes(color=targe_categ), trim = TRUE) +
  labs(title = "Units without evaluation 2nd semester", y = "Number of units", x = "") + 
  theme_classic() +
  geom_signif(comparisons = list(c("Success", "Fail")),   
              map_signif_level=TRUE)

#### Tasa de inflación ####

inflation_plot <- ggplot(origin_data, aes(x = targe_categ, y = inflation_rate)) + 
  geom_violin(aes(color=targe_categ), trim = TRUE) +
  labs(title = "Inflation Rate", y = "Inflation rate", x = "") + 
  theme_classic() +
  geom_signif(comparisons = list(c("Success", "Fail")),   
              map_signif_level=TRUE)


