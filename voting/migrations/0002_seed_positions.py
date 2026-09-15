from django.db import migrations

POSITIONS = [
    "Head Prefect",
    "Head Boy",
    "Head Girl",
    "Sanitation Prefect",
    "Student Chaplain",
    "Sports/Entertainment Prefect",
]


def seed_positions(apps, schema_editor):
    Position = apps.get_model("voting", "Position")
    for order, name in enumerate(POSITIONS, start=1):
        Position.objects.create(id=order, name=name)


def remove_positions(apps, schema_editor):
    Position = apps.get_model("voting", "Position")
    Position.objects.filter(name__in=POSITIONS).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("voting", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_positions, remove_positions),
    ]
