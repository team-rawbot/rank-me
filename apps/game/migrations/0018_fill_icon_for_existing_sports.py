# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-20 13:00
from __future__ import unicode_literals

from django.db import migrations

def assign_icons(apps, schema_editor):

    Sport = apps.get_model('game', 'Sport')

    icons = {
        'table-tennis': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" enable-background="new 0 0 32 32" class="icon"><path d="M24.3 11.038l-13.3 13.3.7.7 13.3-13.3-.7-.7zM11.8 2.038c-3.3 0-5.9 1-7.5 2.9-1.6 1.9-2.3 4.7-2.3 7.9 0 6.7 5 12.8 11.8 12.8 1.7 0 3.1-.7 4.5-1.3.3-.1.6-.3.9-.3.3-.1.6 0 .6 0 1.1.4 2.3 1.8 3 3l1.2 2c.6 1.1 2.2 1.3 3.1.4l2.3-2.4c.9-.9.7-2.4-.4-3l-2-1.2c-.8-.5-1.8-1.2-2.4-1.9-.2-.2-.4-.5-.5-.7 0-.1-.1-.2-.1-.2v-.1c-.1-.2 0-.9.1-1.1.7-1.4 1.5-3.1 1.5-4.9 0-3.5-1.8-6.5-4.4-8.5-2.6-2.2-6-3.4-9.4-3.4zm0 1c3.1 0 6.3 1.1 8.8 3.1 2.4 1.9 4.1 4.6 4.1 7.8 0 1.6-.7 3.1-1.4 4.5-.3.5-.3 1.2-.1 1.8v.2c0 .1.1.2.2.3.1.2.3.6.6.9.7.9 1.8 1.7 2.7 2.2l2 1.2c.5.3.6 1.1.2 1.5l-2.3 2.3c-.4.4-1.2.3-1.5-.2l-1.2-2c-.8-1.3-1.9-2.9-3.5-3.5-.4-.1-.7-.1-1.1 0s-.8.2-1.2.4c-1.3.7-2.6 1.2-4 1.2-6.3 0-10.8-5.6-10.8-11.8 0-3.1.7-5.6 2.1-7.3 1.1-1.7 3.3-2.6 6.4-2.6zM10.4 4.038c-.3 0-.5.3-.4.6s.3.5.6.4c0 0 1.4-.1 1.9 0 .9.1 2.9.9 2.9.9.2.2.5.1.7-.1.2-.2.1-.5-.1-.7l-.2-.1s-1.9-.8-3.1-1c-.9-.1-2.2 0-2.3 0zM16.5 6.538c0 .3.2.5.5.5s.5-.2.5-.5-.2-.5-.5-.5-.5.2-.5.5zM11 12.038c-1.6 0-3 1.4-3 3s1.4 3 3 3 3-1.4 3-3-1.4-3-3-3zm0 1c1 0 2 1 2 2s-1 2-2 2-2-1-2-2 1-2 2-2z"/></svg>',
        'darts': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" enable-background="new 0 0 32 32" class="icon"><path d="M30.8 3.6c-.1-.1-.2-.1-.3-.1h-1.5c-.2 0-.5-.3-.5-.5v-1.5c0-.3-.2-.5-.5-.5h-.2l-.2.1-2.5 2.5-.1.4v1.5l.1.6-2.3 2.3c-2.4-2.1-5.6-3.4-8.8-3.4-3.4 0-6.8 1.4-9.2 3.8s-3.8 5.8-3.8 9.2 1.4 6.8 3.8 9.2 5.8 3.8 9.2 3.8 6.8-1.4 9.2-3.8 3.8-5.8 3.8-9.2c0-3.2-1.3-6.5-3.5-8.8l2.3-2.3.7.1h1.5c.1 0 .3-.1.3-.2l2.5-2.5c.2-.2.2-.5 0-.7zm-4.8 14.4c0 3.1-1.3 6.3-3.5 8.5s-5.4 3.5-8.5 3.5-6.3-1.3-8.5-3.5c-2.2-2.3-3.5-5.4-3.5-8.5s1.3-6.3 3.5-8.5 5.4-3.5 8.5-3.5c3 0 5.9 1.2 8.1 3.2l-2.9 2.9c-1.4-1.3-3.3-2.1-5.2-2.1-4.2 0-8 3.8-8 8s3.8 8 8 8 8-3.8 8-8c0-2-.8-3.8-2.1-5.2l2.9-2.9c2 2.2 3.2 5.1 3.2 8.1zm-9.5 0c0 1.3-1.2 2.5-2.5 2.5s-2.5-1.2-2.5-2.5 1.2-2.5 2.5-2.5c.5 0 .9.2 1.3.4l-1.2 1.2c-.2.2-.3.5-.1.7.2.2.5.3.7.1 0 0 .1 0 .1-.1l1.2-1.2c.3.4.5.9.5 1.4zm-.4-2.8c-.6-.4-1.3-.7-2.1-.7-1.9 0-3.5 1.6-3.5 3.5s1.6 3.5 3.5 3.5 3.5-1.6 3.5-3.5c0-.8-.3-1.5-.7-2.1l2.4-2.4c1.1 1.3 1.8 2.8 1.8 4.5 0 3.6-3.4 7-7 7s-7-3.4-7-7 3.4-7 7-7c1.6 0 3.2.7 4.5 1.8l-2.4 2.4zm11.7-9.2h-1.3c-.2 0-.5-.3-.5-.5v-1.3l1.5-1.5v.3c0 .8.7 1.5 1.5 1.5h.3l-1.5 1.5z"/></svg>',
        'table-football': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" enable-background="new 0 0 32 32" class="icon"><path d="M25.9 6.1c-1.3-1.3-2.9-2.3-4.6-3-.1-.1-.2-.1-.2-.1-1.6-.6-3.3-1-5.1-1-1.8 0-3.5.4-5.2 1-1.7.7-3.4 1.8-4.7 3.1-2.6 2.6-4.1 6.2-4.1 9.9s1.5 7.3 4.1 9.9 6.2 4.1 9.9 4.1 7.3-1.5 9.9-4.1 4.1-6.2 4.1-9.9-1.5-7.3-4.1-9.9zm1.5 16.1l-1.2-.2h-.30000000000000004l-3.8 1.4-2.8-3.8.1-.2 1-4v-.4l4.7-1.7 1.8 2.7c.2.2.3.4.6.5l1.1.5h.2c0 1.8-.5 3.6-1.4 5.2zm-17.5 1.2l-.1-.1-3.3-1.2c-.4-.1-.7-.1-.9-.1l-1 .2c-.9-1.6-1.4-3.4-1.6-5.2h.2l1.1-.5c.2-.1.4-.3.6-.5l1.8-2.7 4.7 1.7v.4l1 4 .1.2-2.6 3.8zm-3.8-15.8l.4.6c0 .1.1.2.1.2l-.2 3.6c0 .1 0 .1-.1.2l-2.1 3.1c0 .1-.1.1-.2.2l-1 .4c0-3 1.1-6 3.1-8.3zm6.4 7.5c0-.2.1-.4.2-.5l3-2c.2-.1.4-.1.6 0l3 2c.1.1.3.3.2.5l-1 4c0 .2-.3.4-.5.4h-4c-.2 0-.5-.2-.5-.4l-1-4zm13.1-6.8l.4-.6c1.9 2.3 3.1 5.3 3.1 8.3l-.9-.4c-.1 0-.2-.1-.2-.2l-2.1-3.1-.1-.2-.2-3.6c-.1-.1-.1-.2 0-.2zm-.4-1.5l-.5 1c-.1.2-.2.5-.2.8l.2 3.6v.2l-4.5 1.6-.3-.3-3-2-.3-.2v-5.6l3.3-.8c.3-.1.5-.2.7-.4l.6-.6c1.4.6 2.8 1.5 4 2.7zm-9.2-3.8c1.4 0 2.8.2 4.1.7l-.3.3c-.1.1-.2.1-.2.1l-3.5.9h-.2l-3.5-.9c-.1 0-.2-.1-.2-.1l-.3-.3c1.3-.4 2.7-.7 4.1-.7zm-5.1 1.1l.6.6c.2.2.4.3.7.4l3.3.8v5.7c-.1 0-.2.1-.3.2l-3 2-.3.3-4.6-1.7v-.2l.2-3.6c0-.3-.1-.5-.2-.8l-.5-1c1.2-1.2 2.6-2.1 4.1-2.7zm-5.8 19l.7-.1h.2l3.3 1.2.2.1 2.2 2.8c.1.1.1.1.1.2l.1 1c-1.9-.6-3.7-1.7-5.2-3.1-.5-.6-1.1-1.3-1.6-2.1zm7.9 5.5v-.2l-.1-1.2c0-.3-.2-.5-.3-.8l-1.9-2.4 2.7-3.8c.2.1.4.2.7.2h3.9c.3 0 .5-.1.7-.2l2.7 3.8-2.1 2.6c-.1.1-.1.2-.1.3l-.2 1.5v.2c-1 .2-2 .4-3 .4s-2-.1-3-.4zm12.2-3.4c-1.4 1.4-3.2 2.5-5.2 3.1l.1-1.1 2.4-3 3.6-1.3.8.1c-.5.9-1.1 1.6-1.7 2.2z"/></svg>',
        'video-game': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" enable-background="new 0 0 32 32" class="icon"><path d="M13.6 8.2h4.8l-2.4-3.8zM16 27.6l2.4-3.8h-4.8zM8.2 18.4v-4.8l-3.8 2.4zM23.8 18.4l3.8-2.4-3.8-2.4zM28.3 10.4h-6.6v-6.7c0-1.5-1.1-2.7-2.6-2.7h-6.1c-1.5 0-2.6 1.2-2.6 2.7v6.6h-6.7c-1.5 0-2.7 1.1-2.7 2.6v6.1c0 1.5 1.2 2.6 2.7 2.6h6.6v6.6c0 1.5 1.1 2.7 2.6 2.7h6.1c1.5 0 2.6-1.2 2.6-2.7v-6.6h6.6c1.5 0 2.7-1.1 2.7-2.6v-6.1c.1-1.5-1.1-2.5-2.6-2.5zm1.8 8.7c0 .8-1 1.6-1.8 1.6h-7.6v7.6c0 .8-.9 1.8-1.6 1.8h-6.1c-.8 0-1.6-1-1.6-1.8v-7.6h-7.7c-.8 0-1.8-.9-1.8-1.6v-6.1c0-.8 1-1.6 1.8-1.6h7.6v-7.7c0-.8.9-1.8 1.6-1.8h6.1c.8 0 1.6 1 1.6 1.8v7.6h7.6c.8 0 1.8.9 1.8 1.6v6.2z"/></svg>'
    }

    for slug, icon in icons.items():
        Sport.objects.filter(slug=slug).update(icon=icon)


def unassign_icons(apps, schema_editor):
    Sport = apps.get_model('game', 'Sport')

    Sport.objects.all().update(icon=None)


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0017_sport_icon'),
    ]

    operations = [
        migrations.RunPython(assign_icons, unassign_icons),
    ]
