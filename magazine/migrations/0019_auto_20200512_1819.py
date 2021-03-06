# Generated by Django 3.0.5 on 2020-05-12 18:19

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('magazine', '0018_auto_20200225_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='magazinearticle',
            name='body',
            field=wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('pullquote', wagtail.core.blocks.BlockQuoteBlock())]),
        ),
    ]
