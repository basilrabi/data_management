from os import name
from django.db import models
from flask import request
from pathlib import Path
import pandas as pd
import os

# Create your models here.

def filepath(instance, filename):
    filename = f"{instance.month}-{instance.year}.xlsx"
    return f"SAP_Upload/{instance.year}/{filename}"

class SapCostCenter(models.Model):

    def parser(instance, test_out):
        test_out = "water"
        return test_out


    month = models.CharField(max_length=32, null=True, blank=False)
    year = models.CharField(max_length=4, null=True, blank=False)
    test_field = parser
    Cost_Center_File = models.FileField(upload_to=filepath, null=True, blank=False)

class SapUpload(models.Model):

    month = models.CharField(max_length=32, null=True, blank=False)
    year = models.CharField(max_length=4, null=True, blank=False)
    file_loc = filepath
    fileup = models.FileField(upload_to=file_loc, null=True, blank=False)
