from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from accounts.models import Profile

# Create your models here.

# TODO: add model for category to classify all projects using project category, can be multiple ie frontend, backend
# TODO: categorise language into frontend, backend etc


class Language(models.Model):
    name = models.CharField(max_length=140)

    def __str__(self):
        return self.name


class Framework(models.Model):
    STACK_CHOICES = (
        ('node-js', 'NodeJS'),
        ('python', 'Python'),
        ('android', 'Android'),
        ('angular', 'Angular'),
        ('php', 'PHP'),
    )
    ide_stack = models.CharField(max_length=140, default='node-js', choices=STACK_CHOICES)
    name = models.CharField(max_length=140)
    language = models.ForeignKey(Language, on_delete=models.DO_NOTHING)
    image =models.CharField(max_length=140,blank=True)

    def __str__(self):
        return self.name
class level(models.Model):
    name = models.CharField(max_length=140)
    language = models.ForeignKey(Language, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

class Devtype(models.Model):
    name = models.CharField(max_length=140)


    def __str__(self):
        return self.name

class Projecttype(models.Model):
    name = models.CharField(max_length=140)

    def __str__(self):
        return  self.name


class Project(models.Model):
    name = models.CharField(max_length=140,blank=True,null=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE,blank=True,null=True,default=1)
    brief = models.CharField(max_length=500, blank=True, null=True, )
    description = models.CharField(max_length=2000, blank=True, null=True, )
    level = models.CharField(max_length=200, blank=True, null=True, )
    concept = models.CharField(max_length=200, blank=True, null=True, )
    tags = models.CharField(max_length=900, null=True, blank=True)
    projectimage1 = models.CharField(max_length=500, blank=True, null=True, )
    projectimage2 = models.CharField(max_length=500, blank=True, null=True, )
    projectimage3 = models.CharField(max_length=500, blank=True, null=True, )
    projectimage4 = models.CharField(max_length=500, blank=True, null=True, )
    projectimage5 = models.CharField(max_length=500, blank=True, null=True, )
    projectimage6 = models.CharField(max_length=500, blank=True, null=True, )
    projectimage7 = models.CharField(max_length=500, blank=True, null=True, )
    projectimage8 = models.CharField(max_length=500, blank=True, null=True, )
    projectimage9 = models.CharField(max_length=500, blank=True, null=True, )
    projectimage10 = models.CharField(max_length=500, blank=True, null=True, )
    requirement1 = models.CharField(max_length=500, blank=True, null=True, )
    requirement2 = models.CharField(max_length=500, blank=True, null=True, )
    requirement3 = models.CharField(max_length=500, blank=True, null=True, )
    requirement4 = models.CharField(max_length=500, blank=True, null=True, )
    requirement5 = models.CharField(max_length=500, blank=True, null=True, )
    requirement6 = models.CharField(max_length=500, blank=True, null=True, )
    requirement7 = models.CharField(max_length=500, blank=True, null=True, )
    requirement8 = models.CharField(max_length=500, blank=True, null=True, )
    requirement9 = models.CharField(max_length=500, blank=True, null=True, )
    requirement10 = models.CharField(max_length=500, blank=True, null=True, )
    framework = models.ForeignKey(Framework, on_delete=False, null=True)
    devtype = models.ForeignKey(Devtype, on_delete=False, null=True)
    projecttype = models.ForeignKey(Projecttype, on_delete=False, null=True)
    hasvideo=models.BooleanField(default=False)
    duration = models.DurationField(default=timedelta(hours=2))
    project_template = models.URLField(blank=True, null=True)



    def __str__(self):
        return self.name
