from django.db import models

class InputNilai(models.Model):
	id = models.AutoField(primary_key=True)
	nilai = models.IntegerField()

	class Meta:
		db_table = 'setting_string'
