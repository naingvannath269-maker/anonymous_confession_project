from django.db import migrations, models


class Migration(migrations.Migration):

  dependencies = [
      ('confessions', '0002_reaction'),
  ]

  operations = [
      migrations.AddField(
          model_name='reaction',
          name='is_like',
          field=models.BooleanField(default=True),
      ),
  ]
