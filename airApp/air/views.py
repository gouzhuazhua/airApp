from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from .models import Steam_news as db_steam_news
from .models import Steam_apps as db_steam_apps
from .models import Steam_player_ownedgames as db_stem_player_ownedgames
from .models import Steam_player_rencentlyplaygames as db_steam_player_replayedgames
from .models import Steam_player_bans as db_steam_player_bans
from .models import Steam_player_summaries as db_steam_player_summaries
from .models import User as db_user
from .utils import filter_emoji

import requests
import json
import datetime
import uuid
import logging
import re


# Create your views here.
api_key = 'ED312A399410D07A1E811502C235B4A8'
api_steam_apps = 'https://api.steampowered.com/ISteamApps/GetAppList/v2/'
api_steam_news = 'https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/'
api_player_ownedgames = 'https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/'
api_plyaer_recentlyplayedgames = 'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/'
api_player_bans = 'https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/'
api_player_summaries = 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


def test(request):
    params_recentlyplayedgames_content = {'key': 'ED312A399410D07A1E811502C235B4A8',
                                          'steamid': '76561198076512211'}
    response_regames = requests.get(api_plyaer_recentlyplayedgames, params=params_recentlyplayedgames_content)
    dict_regames = json.loads(response_regames.text)['response']['games']
    for regame in dict_regames:
        logging.info(">>>>>>>>>>>>>>>" + str(regame['img_logo_url']))
    return JsonResponse(json.dumps(api_key), safe=False)


# api更新【steam app库】
def update_steam_apps(request):
    errors = []
    if request.method == 'POST' or request.method == 'GET':
        response_apps = requests.get(api_steam_apps)
        dict_apps = json.loads(response_apps.text)['applist']['apps']
        for app in dict_apps:
            db_steam_apps.objects.create(appid=int(app['appid']),
                                         appname=filter_emoji(str(app['name'])))
        return JsonResponse({'updatekey': 1, 'msg': 'Update air_steam_apps success.'}, safe=False)
    else:
        return JsonResponse({'updatekey': 0, 'msg': 'Method is not POST or GET.'}, safe=False)


# api更新【steam新闻】
def update_steam_news(request):
    if request.method == 'POST' or request.method == 'GET':
        params_content = {'key': 'ED312A399410D07A1E811502C235B4A8', 'appid': 578080, 'count': 3}
        response_news = requests.get(api_steam_news, params=params_content)
        dict_news = json.loads(response_news.text)['appnews']['newsitems']
        for news in dict_news:
            db_steam_news.objects.create(title=str(news['title']),
                                         url=str(news['url']),
                                         author=str(news['author']),
                                         contents=str(news['contents']),
                                         date=int(news['date']),
                                         appid=int(news['appid']))
        # db_steam_news(**json.loads(response_news.text)).save()
        return JsonResponse({'updatekey': 1, 'msg': 'Update air_steam_news success'}, safe=False)
    else:
        return JsonResponse({'updatekey': 0, 'msg': 'Method is not POST or GET.'}, safe=False)


# 注册
def register(request):
    errors = []
    username = None
    password = None
    password2 = None
    phone = None
    steamid = None
    compareflag = False
    if request.method == 'POST':
        if not request.POST.get('username'):
            errors.append('username cant be null.')
        else:
            username = request.POST.get('username')
        if not request.POST.get('password'):
            errors.append('password cant be null.')
        else:
            password = request.POST.get('password')
        if not request.POST.get('password2'):
            errors.append('password2 cant be null.')
        else:
            password2 = request.POST.get('password2')
        if not request.POST.get('phone'):
            errors.append('phone cant be null.')
        else:
            phone = request.POST.get('phone')
        if not request.POST.get('steamid'):
            errors.append('steamid cant be null.')
        else:
            steamid = request.POST.get('steamid')
        if password == password2:
            compareflag = True
        if username is not None and password is not None and password2 is not None and phone is not None and steamid is not None and compareflag:
            ban_id = uuid.uuid1()
            ownedgames_id = uuid.uuid1()
            re_id = uuid.uuid1()
            sum_id = uuid.uuid1()
            db_user.objects.create(username=username,
                                   password=password,
                                   phone=phone,
                                   steamid=steamid,
                                   ban_id=ban_id,
                                   ownedgames_id=ownedgames_id,
                                   re_id=re_id,
                                   sum_id=sum_id)

            PlayerApi.init_player_all(steamid, ban_id, ownedgames_id, re_id, sum_id)

            return JsonResponse({'registerkey': 1, 'msg': 'register success.'}, safe=False)
        else:
            return JsonResponse({'registerkey': 0, 'msg': errors}, safe=False)
    else:
        return JsonResponse({'registerkey': 3, 'msg': 'Method is not POST'}, safe=False)


# 登陆
def login(request):
    errors = []
    username = None
    password = None
    if request.method == 'POST':
        if not request.POST.get('username'):
            errors.append('username cant be null.')
        else:
            username = request.POST.get('username')
        if not request.POST.get('password'):
            errors.append('password cant be null.')
        else:
            password = request.POST.get('password')
        logging.info('>>>' + str(username) + '\t' + str(password))
        if username is not None and password is not None:
            user = db_user.objects.filter(username=username, password=password)
            # logging.info(">>>" + str(user[0].username))
            # user = auth.authenticate(username=username, password=password)
            if len(user) != 0:
                # auth.login(request, user)
                return JsonResponse({'loginkey': 1, 'msg': 'login success.'}, safe=False)
            else:
                errors.append('username or password error.')
                return JsonResponse({'loginkey': 0, 'msg': errors}, safe=False)
        else:
            return JsonResponse({'loginkey': 0, 'msg': errors}, safe=False)
    else:
        return JsonResponse({'loginkey': 3, 'msg': 'Method is not POST.'}, safe=False)


class PlayerApi:
    @staticmethod
    def init_player_api(steamid):
        params_ownedgames_content = {'key': 'ED312A399410D07A1E811502C235B4A8',
                                     'steamid': steamid,
                                     'include_appinfo': 1,
                                     'include_played_free_games': 1}
        params_bans_content = {'key': 'ED312A399410D07A1E811502C235B4A8',
                               'steamids': steamid}
        params_recentlyplayedgames_content = {'key': 'ED312A399410D07A1E811502C235B4A8',
                                              'steamid': steamid}
        params_plyaer_summaries_content = {'key': 'ED312A399410D07A1E811502C235B4A8',
                                           'steamids': steamid}

        response_ownedgames = requests.get(url=api_player_ownedgames, params=params_ownedgames_content)
        response_regames = requests.get(url=api_plyaer_recentlyplayedgames, params=params_recentlyplayedgames_content)
        response_bans = requests.get(url=api_player_bans, params=params_bans_content)
        response_summaries = requests.get(url=api_player_summaries, params=params_plyaer_summaries_content)
        return {'r_o': response_ownedgames, 'r_r': response_regames, 'r_b': response_bans, 'r_s': response_summaries}

    # 更新玩家【拥有游戏】、【部分游戏数据】、【玩家封禁】、【玩家信息】
    @staticmethod
    def init_player_all(steamid, ban_id, ownedgames_id, re_id, sum_id):
        response_init = PlayerApi.init_player_api(steamid)
        dict_ownedgames = json.loads(response_init['r_o'].text)['response']['games']
        for game in dict_ownedgames:
            db_stem_player_ownedgames.objects.create(ownedgames_id=ownedgames_id,
                                                     appid=int(game['appid']),
                                                     appname=str(game['name']),
                                                     playtime_forever=int(game['playtime_forever']),
                                                     img_icon_url=str(game['img_icon_url']),
                                                     img_logo_url=str(game['img_logo_url']))

        dict_regames = json.loads(response_init['r_r'].text)['response']['games']
        for regame in dict_regames:
            db_steam_player_replayedgames.objects.create(re_id=re_id,
                                                         appid=int(regame['appid']),
                                                         name=str(regame['name']),
                                                         playtime_2weeks=str(regame['playtime_2weeks']),
                                                         playtime_forever=int(regame['playtime_forever']),
                                                         img_icon_url=str(regame['img_icon_url']),
                                                         img_logo_url=str(regame['img_logo_url']))

        dict_bans = json.loads(response_init['r_b'].text)['players']
        db_steam_player_bans.objects.create(ban_id=ban_id,
                                            steamid=str(dict_bans[0]['SteamId']),
                                            communitybanned=str(dict_bans[0]['CommunityBanned']),
                                            vacbanned=str(dict_bans[0]['VACBanned']),
                                            dayssincelastban=int(dict_bans[0]['DaysSinceLastBan']),
                                            numberofvacbans=int(dict_bans[0]['NumberOfVACBans']),
                                            numberofgamebans=int(dict_bans[0]['NumberOfGameBans']),
                                            economyban=str(dict_bans[0]['EconomyBan']))

        dict_sum = json.loads(response_init['r_s'].text)['response']['players']
        db_steam_player_summaries.objects.create(sum_id=sum_id,
                                                 personname=str(dict_sum[0]['personaname']),
                                                 personstate=int(dict_sum[0]['personastate']),
                                                 lastlogoff=int(dict_sum[0]['lastlogoff']),
                                                 profileurl=str(dict_sum[0]['profileurl']),
                                                 avatar=str(dict_sum[0]['avatarfull']),
                                                 timecreate=int(dict_sum[0]['timecreated']),
                                                 loccode=str(dict_sum[0]['loccountrycode']))

    # 更新玩家信息
    @staticmethod
    def update_player(steamid, ban_id, ownedgames_id, re_id, sum_id):
        response_init = PlayerApi.init_player_api(steamid)
        dict_bans = json.loads(response_init['r_b'].text)['players']
        db_steam_player_bans.objects.filter(ban_id=ban_id).update(communitybanned=str(dict_bans[0]['CommunityBanned']),
                                                                  vacbanned=str(dict_bans[0]['VACBanned']),
                                                                  dayssincelastban=int(dict_bans[0]['DaysSinceLastBan']),
                                                                  numberofvacbans=int(dict_bans[0]['NumberOfVACBans']),
                                                                  numberofgamebans=int(dict_bans[0]['NumberOfGameBans']),
                                                                  economyban=str(dict_bans[0]['EconomyBan']))

        db_stem_player_ownedgames.objects.filter(ownedgames_id=ownedgames_id).delete()
        dict_ownedgames = json.loads(response_init['r_o'].text)['response']['games']
        for game in dict_ownedgames:
            db_stem_player_ownedgames.objects.create(ownedgames_id=ownedgames_id,
                                                     appid=int(game['appid']),
                                                     appname=str(game['name']),
                                                     playtime_forever=int(game['playtime_forever']),
                                                     img_icon_url=str(game['img_icon_url']),
                                                     img_logo_url=str(game['img_logo_url']))

        db_steam_player_replayedgames.objects.filter(re_id=re_id).delete()
        dict_regames = json.loads(response_init['r_r'].text)['response']['games']
        for regame in dict_regames:
            db_steam_player_replayedgames.objects.create(re_id=re_id,
                                                         appid=int(regame['appid']),
                                                         name=str(regame['name']),
                                                         playtime_2weeks=str(regame['playtime_2weeks']),
                                                         playtime_forever=int(regame['playtime_forever']),
                                                         img_icon_url=str(regame['img_icon_url']),
                                                         img_logo_url=str(regame['img_logo_url']))

        dict_sum = json.loads(response_init['r_s'].text)['response']['players']
        db_steam_player_summaries.objects.filter(sum_id=sum_id).update(personname=str(dict_sum[0]['personaname']),
                                                                       personstate=int(dict_sum[0]['personastate']),
                                                                       lastlogoff=int(dict_sum[0]['lastlogoff']),
                                                                       profileurl=str(dict_sum[0]['profileurl']),
                                                                       avatar=str(dict_sum[0]['avatarfull']),
                                                                       timecreate=int(dict_sum[0]['timecreated']),
                                                                       loccode=str(dict_sum[0]['loccountrycode']))


# 从数据库获取【steam新闻】
def get_steam_news_from_db(request):
    if request.method == 'POST' or request.method == 'GET':
        rs_news =db_steam_news.objects.all()[12:]
        news_list = []
        for r in rs_news:
            news = {}
            news['title'] = r.title
            news['author'] = r.author
            news['url'] = str(r.url)[:4] + str(r.url)[5:]
            news['contents'] = r.contents
            news['date'] = datetime.datetime.fromtimestamp(r.date).strftime("%Y-%m-%d %H:%M:%S")
            news['appid'] = r.appid
            if r.appid == 570:
                icon = '0bbb630d63262dd66d2fdd0f7d37e8661a410075'
            elif r.appid == 730:
                icon = '69f7ebe2735c366c65c0b33dae00e12dc40edbe4'
            elif r.appid == 578080:
                icon = '93d896e7d7a42ae35c1d77239430e1d90bc82cae'
            elif r.appid == 271590:
                icon = '1e72f87eb927fa1485e68aefaff23c7fd7178251'
            news['img_icon_url'] = 'http://cdn.steamstatic.com.8686c.com/steamcommunity/public/images/apps/' + str(r.appid) + '/' + icon + '.jpg'
            news_list.append(news)
        return JsonResponse(news_list, safe=False)
    else:
        return JsonResponse({'getkey': 0, 'msg': 'Method is not POST or GET.'}, safe=False)


# 从数据库中获取【我的游戏】
def get_player_ownedgames_from_db(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        rs_player = db_user.objects.filter(username=username)
        # 当请求【我的游戏】时更新该玩家资料
        PlayerApi.update_player(rs_player[0].steamid, rs_player[0].ban_id, rs_player[0].ownedgames_id, rs_player[0].re_id, rs_player[0].sum_id)
        rs_player_ownedgames = db_stem_player_ownedgames.objects.filter(ownedgames_id=rs_player[0].ownedgames_id)
        ownedgames = []
        for rpo in rs_player_ownedgames:
            ogame = {}
            ogame['appname'] = rpo.appname
            ogame['playtime_forever'] = rpo.playtime_forever
            ogame['img_icon_url'] = 'http://cdn.steamstatic.com.8686c.com/steamcommunity/public/images/apps/' + str(rpo.appid) + '/' + rpo.img_icon_url + '.jpg'
            ogame['img_logo_url'] = 'http://cdn.steamstatic.com.8686c.com/steamcommunity/public/images/apps/' + str(rpo.appid) + '/' + rpo.img_logo_url + '.jpg'
            ownedgames.append(ogame)
        return JsonResponse(ownedgames, safe=False)


# 从数据库中获取【我最近玩过的游戏】
def get_player_recentlygames_from_db(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        rs_player = db_user.objects.filter(username=username)
        rs_player_regames = db_steam_player_replayedgames.objects.filter(re_id=rs_player[0].re_id)
        regames = []
        for rpr in rs_player_regames:
            rgame = {}
            rgame['appname'] = rpr.name
            rgame['playtime_2weeks'] = rpr.playtime_2weeks
            rgame['img_icon_url'] = 'http://cdn.steamstatic.com.8686c.com/steamcommunity/public/images/apps/' + str(rpr.appid) + '/' + rpr.img_icon_url + '.jpg'
            rgame['img_logo_url'] = 'http://cdn.steamstatic.com.8686c.com/steamcommunity/public/images/apps/' + str(rpr.appid) + '/' + rpr.img_logo_url + '.jpg'
            regames.append(rgame)
        return JsonResponse(regames, safe=False)


# 根据username获取玩家封禁信息
def get_player_bansbyname_from_api(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        steamid = db_user.objects.filter(username=username)[0].steamid
        params_bans_content = {'key': 'ED312A399410D07A1E811502C235B4A8',
                               'steamids': steamid}

        response_bans = requests.get(url=api_player_bans, params=params_bans_content)
        bans_dict = json.loads(response_bans.text)['players']
        player_ban = {}
        player_ban['CommunityBanned'] = bans_dict[0]['CommunityBanned']
        player_ban['VACBanned'] = bans_dict[0]['VACBanned']
        player_ban['NumberOfVACBans'] = bans_dict[0]['NumberOfVACBans']
        player_ban['DaysSinceLastBan'] = bans_dict[0]['DaysSinceLastBan']
        player_ban['NumberOfGameBans'] = bans_dict[0]['NumberOfGameBans']
        player_ban['EconomyBan'] = bans_dict[0]['EconomyBan']
        return JsonResponse(player_ban, safe=False)


# 根据steamid获取玩家封禁信息
def get_player_bansbyid_from_api(request):
    if request.method == 'POST':
        steamid = request.POST.get('steamid')
        params_bans_content = {'key': 'ED312A399410D07A1E811502C235B4A8',
                               'steamids': steamid}

        response_bans = requests.get(url=api_player_bans, params=params_bans_content)
        bans_dict = json.loads(response_bans.text)['players']
        if len(bans_dict) == 0:
            return JsonResponse(0, safe=False)
        player_ban = {}
        player_ban['CommunityBanned'] = bans_dict[0]['CommunityBanned']
        player_ban['VACBanned'] = bans_dict[0]['VACBanned']
        player_ban['NumberOfVACBans'] = bans_dict[0]['NumberOfVACBans']
        player_ban['DaysSinceLastBan'] = bans_dict[0]['DaysSinceLastBan']
        player_ban['NumberOfGameBans'] = bans_dict[0]['NumberOfGameBans']
        player_ban['EconomyBan'] = bans_dict[0]['EconomyBan']
        return JsonResponse(player_ban, safe=False)


# 从数据库中获取玩家个人资料
def get_player_summaries_from_db(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        sum_id = db_user.objects.filter(username=username)[0].sum_id
        summaries = db_steam_player_summaries.objects.filter(sum_id=sum_id)[0]
        rs_summaries = {}
        rs_summaries['personname'] = summaries.personname
        rs_summaries['personstate'] = summaries.personstate
        rs_summaries['lastlogoff'] = datetime.datetime.fromtimestamp(summaries.lastlogoff).strftime("%Y-%m-%d %H:%M:%S")
        rs_summaries['profileurl'] = str(summaries.profileurl)[:4] + str(summaries.profileurl)[5:]
        rs_summaries['avatar'] = str(summaries.avatar)[:4] + str(summaries.avatar)[5:]
        rs_summaries['timecreate'] = datetime.datetime.fromtimestamp(summaries.timecreate).strftime("%Y-%m-%d %H:%M:%S")
        rs_summaries['loccode'] = summaries.loccode
        return JsonResponse(rs_summaries, safe=False)