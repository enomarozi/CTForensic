from django.db import models

class ImageFile(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=255)
	size = models.CharField(max_length=20)
	format = models.CharField(max_length=6)

	class Meta:
		db_table = 'tb_image_forensics'