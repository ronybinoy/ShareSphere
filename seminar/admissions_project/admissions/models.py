from django.db import models


class AdmissionPrediction(models.Model):
    percentage_12th = models.FloatField()
    GRE_Score = models.FloatField()
    TOEFL_Score = models.FloatField()
    CGPA = models.FloatField()
    probability = models.FloatField()
    accuracy = models.FloatField()
    precision = models.FloatField()
    recall = models.FloatField()
    
    class Meta:
        app_label = 'admissions'
