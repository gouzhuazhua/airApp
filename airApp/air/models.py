from django.db import models


# Create your models here.
class Steam_apps(models.Model):
    appid = models.IntegerField()
    appname = models.CharField(max_length=225)
    easyname = models.CharField(max_length=225)


class Steam_news(models.Model):
    title = models.CharField(max_length=225)
    url = models.CharField(max_length=225)
    author = models.CharField(max_length=225)
    contents = models.CharField(max_length=225)
    date = models.IntegerField()
    appid = models.IntegerField()


class Steam_player_ownedgames(models.Model):
    ownedgames_id = models.CharField(max_length=225)
    appid = models.IntegerField()
    appname = models.CharField(max_length=225)
    playtime_forever = models.IntegerField()
    img_icon_url = models.CharField(max_length=225)
    img_logo_url = models.CharField(max_length=225)


class Steam_player_rencentlyplaygames(models.Model):
    re_id = models.CharField(max_length=225)
    appid = models.IntegerField()
    name = models.CharField(max_length=225)
    playtime_2weeks = models.IntegerField()
    playtime_forever = models.IntegerField()
    img_icon_url = models.CharField(max_length=225)
    img_logo_url = models.CharField(max_length=225)


class Steam_player_bans(models.Model):
    ban_id = models.CharField(max_length=225)
    steamid = models.CharField(max_length=225)
    communitybanned = models.CharField(max_length=225)
    vacbanned = models.CharField(max_length=225)
    numberofvacbans = models.IntegerField()
    dayssincelastban = models.IntegerField()
    numberofgamebans = models.IntegerField()
    economyban = models.CharField(max_length=225)


class Steam_player_summaries(models.Model):
    sum_id = models.CharField(max_length=225)
    personname = models.CharField(max_length=225)
    level = models.IntegerField()
    personstate = models.IntegerField()
    lastlogoff = models.IntegerField()
    profileurl = models.CharField(max_length=225)
    avatar = models.CharField(max_length=225)
    timecreate = models.IntegerField()
    loccode = models.CharField(max_length=225)


class User(models.Model):
    username = models.CharField(max_length=225)
    phone = models.CharField(max_length=225)
    password = models.CharField(max_length=225)
    steamid = models.CharField(max_length=225)
    isAdmin = models.IntegerField(default=0)
    ban_id = models.CharField(max_length=225)
    ownedgames_id = models.CharField(max_length=225)
    re_id = models.CharField(max_length=225)
    sum_id = models.CharField(max_length=225)
