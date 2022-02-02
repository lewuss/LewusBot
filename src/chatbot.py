from twitchio.ext import commands
import api
import requests
from random import randint
import twitterapi
import datetime
import scrapesubs
import spotifyapi as spotify
import spotifykeys
import time
from datetime import date
import threading
import pymongo
import lolapi
import asyncio
import math
import glownaabusers as glowna

client = pymongo.MongoClient(
    f"mongodb+srv://twitchdata:{spotifykeys.mongodb_pw}@cluster0.qtyar.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.twitch.chatters
db_subs = client.twitchsubs.channels
db_vips = client.twitch.vips

xayopl_creation_date = date(2021, 7, 26)

cd = 15

yfl = ['youngmulti', 'xmerghani', '1wron3k', 'mrdzinold', 'mork', 'banduracartel']


def transform_minutes(total_minutes):
    days = math.floor(total_minutes / (24 * 60))
    leftover_minutes = total_minutes % (24 * 60)

    hours = math.floor(leftover_minutes / 60)
    mins = total_minutes - (days * 1440) - (hours * 60)

    return {'dni': days, 'godzin': hours, 'minut': mins}


class Bot(commands.Bot):
    messages = []
    bannable = []
    mods = {}
    tweeters = {}
    mod_count = {}
    queue = {}
    subs_count = {}
    instagrams = {}
    zajebanko = {}
    lol = {}
    drops = {}
    sr = {}
    streamerki = []
    spotfiy = ["lewus", "arquel", 'jvnioor_', '1wron3k', 'dziobano_']
    for user in spotfiy:
        sr[user] = False

    file = open("banned_words.txt", "r", encoding='UTF-8')
    for data in file:
        bannable.append(data.strip())
    ig_file = open('instagrams.txt', 'r', encoding='UTF-8')
    tt_file = open('twitteraccounts.txt', 'r', encoding='UTF-8')
    lol_accounts = open("lolaccounts.txt", "r", encoding='UTF-8')
    kobiety = open('kobiety.txt', 'r', encoding='UTF-8')
    for data in ig_file:
        line = data.strip().split(';')
        instagrams[line[0]] = line[1]
    for data in tt_file:
        line = data.strip().split(';')
        tweeters[line[0]] = line[1]
    for data in lol_accounts:
        line = data.strip().split(';')
        lol[line[0]] = line[1]
    for data in kobiety:
        streamerki.append(data.strip())
    random_mods_file = open('randombruce_mods.txt', 'r')
    random_mods = random_mods_file.read().split(', ')

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(token=api.oauth, prefix='$',
                         initial_channels=[])

    def refresh_queue(self, channel):
        current_song_id = spotify.get_current_track_id(channel)
        for song_id in list(self.queue):
            if song_id == current_song_id:
                break
            else:
                self.queue.pop(song_id)

    async def send_msg(self, msg, ctx):
        if any(ban_words in msg.lower().replace(" ", "") for ban_words in self.bannable):
            print('trigerred')
            await ctx.send(f"{ctx.message.author.name} - Bardzo nieładne słowo w wiadomości Sadeg")
        else:
            await ctx.send(msg)

    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        await self.join_channels(['lewus', 'vvarion', 'ben3kk', 'mokrysuchar', 'stazjaa', 'mork', "arquel",
                                  'bluealert', '1wron3k', 'xmerghani',
                                  'kozok', 'rajonesports', 'czekolad_',
                                  'youngmulti', 'sinmivak',
                                  'kasix', 'kaseko', 'franio'])
        print(f'Logged in as | {self.nick} to {self.connected_channels}')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return
        '''if message.author.name == message.channel.name and 'instream.ly/' in message.content:
            link = message.content.split()[-1]
            await message.channel.send(f"POLICE {link} POLICE "
                                       f"POLICE {link} POLICE")'''
        if any(ban_words in message.content.lower().replace(" ", "") for ban_words in self.bannable):
            await message.channel.send(f"/timeout {message.author.name} 30 NIE PISZ TAKICH BRZYDKICH SŁÓW")

        await self.handle_commands(message)

    @commands.command()
    async def vanish(self, ctx: commands.Context):
        await ctx.send(f'/timeout {ctx.author.name} 1')

    @commands.command()
    async def join(self, ctx: commands.Context):
        if ctx.author.name == 'lewus':
            print("JOINED")
            await self.join_channels(
                ['waxjan', 'IKacPRO', 'melonik', 'jaskol95', 'dziobano_', 'szymoool', 'bunny_marthy', 'dobrypt',
                 'xkaleson', 'wujabudyn', 'LuZack7', 'banduracartel', 'yuna', 'zahaczai', 'wheelchair_eboyxdddd'])
        else:
            await self.join_channels([ctx.author.name])

    @commands.command()
    @commands.cooldown(1, 5, commands.Bucket.user)
    async def ruletka(self, ctx: commands.Context):
        luck = randint(1, 4)
        if ctx.author.is_mod:
            await ctx.send("Masz moda nie da się w ciebie strzelic :tf:")
        else:
            if luck == 1:
                ban = randint(60, 10800)
                time = transform_minutes(ban / 60)
                time_msg = ''
                for k, v in time.items():
                    if v != 0:
                        time_msg += f'{math.floor(v)} {k} '
                time_msg = time_msg[:-1]
                await ctx.send(f'/timeout {ctx.author.name} {ban}')
                await self.send_msg(f'{ctx.author.name} umarł na {time_msg} Sadeg', ctx)
            else:
                await self.send_msg(ctx.author.name + " zyjesz", ctx)

    @commands.command()
    async def ban(self, ctx: commands.Context):
        words = ctx.message.content.split()
        users = api.get_all_chatters(ctx.channel.name)
        filtered = []
        for user in users:
            if user.startswith(words[1]):
                filtered.append(user)

        if ctx.author.is_mod:
            for user in filtered:
                await ctx.send("/ban " + user)

    @commands.command()
    async def unban(self, ctx: commands.Context):
        words = ctx.message.content.split()
        users = api.get_all_chatters(ctx.channel.name)
        filtered = []
        for user in users:
            if user.startswith(words[1]):
                filtered.append(user)

        if ctx.author.is_mod:
            for user in filtered:
                await ctx.send("/unban " + user)

    @commands.command()
    @commands.cooldown(1, 3, commands.Bucket.channel)
    async def ile(self, ctx: commands.Context):
        words = ctx.message.content.split()
        url = 'https://api.exchangerate-api.com/v4/latest/USD'
        if len(words) == 3:
            words.append('PLN')
        currency = words[2].upper()
        target_currency = words[3].upper()
        if words[1] in ['btc', 'bitcoin', 'vvarion'] and words[2] in ['btc', 'bitcoin', 'vvarion']:
            await ctx.send(f'Odpierdol sie od vvariona. On wcale nie jest btc milionerem.')
        try:
            amount = float(words[1].replace(',', '.'))
        except:
            amount = float(words[1])
        if amount < 0:
            await ctx.send("Ujemne pieniadze :tf:")
        else:
            if currency == 'ZŁ':
                currency = 'PLN'
            if target_currency == 'ZŁ':
                target_currency = 'PLN'
            rates = requests.get(url).json()['rates']
            price = round(amount / rates[currency] * rates[target_currency], 2)
            await ctx.send(f'{amount} {currency} to {price} {target_currency}')

    @commands.command()
    @commands.cooldown(1, 3, commands.Bucket.channel)
    async def kto(self, ctx: commands.Context):
        try:
            target_user = ctx.message.content.split()[1]
        except:
            target_user = ctx.channel.name
        if api.check_if_live(target_user):
            kto = sorted(api.who_is_watching_famous(target_user))
            users = ""
            for user in kto:
                users += user + ', '
            if users == "":
                users = "Nikt z listy nie "
            else:
                users = users[:-2]
            if len(users) < 480:
                await self.send_msg(f'lewusClap {users} oglada stream {target_user}', ctx)
            else:
                await self.send_msg(
                    f'{len(kto)} użytkowników oglada stream {target_user}. Tylu ich jest, że nie da się ich wypisać na czat. Sadge',
                    ctx)
        elif target_user == 'pytał' or target_user == 'pytal':
            await self.send_msg(f"Ty pytałeś dzbanie {ctx.author.name}", ctx)
        else:
            await self.send_msg(f'Sadeg {target_user} nie jest aktualnie na żywo.', ctx)

    @commands.command()
    @commands.cooldown(1, 3, commands.Bucket.channel)
    async def mentale(self, ctx: commands.Context):
        try:
            target_user = ctx.message.content.split()[1]
        except:
            target_user = ctx.channel.name
        if api.check_if_live(target_user):
            kto = sorted(api.who_is_watching_mental(target_user))
            users = ""
            for user in kto:
                users += user + ', '
            if users == "":
                users = "Nikt z mentali nie "
            else:
                users = users[:-2]
            if len(users) < 480:
                await self.send_msg(f'PogU {users} oglada stream {target_user}', ctx)
            else:
                await self.send_msg(
                    f'{len(kto)} użytkowników oglada stream {target_user}. Tylu ich jest, że nie da się ich wypisać na czat. Sadge',
                    ctx)
        elif target_user == 'pytał' or target_user == 'pytal':
            await self.send_msg(f"Ty pytałeś dzbanie {ctx.author.name}", ctx)
        else:
            await self.send_msg(f'Sadeg {target_user} nie jest aktualnie na żywo.', ctx)

    @commands.command()
    @commands.cooldown(1, 3, commands.Bucket.user)
    async def follow(self, ctx: commands.Context):
        words = ctx.message.content.split()
        await self.send_msg(api.check_if_x_follows_y(words[1], words[2]), ctx)

    @commands.command(name='chatters', aliases=['viewers'])
    @commands.cooldown(1, 3, commands.Bucket.user)
    async def chatters(self, ctx: commands.Context):
        words = ctx.message.content.split()
        try:
            channel_name = words[1]
        except:
            channel_name = ctx.channel.name
        try:
            viewers = api.get_viewers(channel_name)
            chatters_count = api.get_chatters(channel_name)
            if chatters_count < 0.5 * viewers:
                await self.send_msg(
                    f'Porvalo {channel_name.capitalize()}: {viewers} widzów, {chatters_count} chattersów Porvalo', ctx)
            else:
                await self.send_msg(f'{channel_name.capitalize()}: {viewers} widzów, {chatters_count} chattersów', ctx)
        except Exception as E:
            chatters_count = api.get_chatters(channel_name)
            await self.send_msg(f'{channel_name.capitalize()} jest offline. Chatters: {chatters_count} lewusSadge', ctx)

    @commands.command(name='ilexn', aliases=['Ilexn', "ILEXN"])
    @commands.cooldown(1, 3, commands.Bucket.user)
    async def ilexn(self, ctx: commands.Context):
        words = ctx.message.content.split()
        prefix = words[1]
        if len(words) == 2:
            channel_name = ctx.channel.name
        else:
            channel_name = words[2]
        chatters = api.get_all_chatters(channel_name)
        message = ''
        counter = 0
        for x in chatters:
            if x.startswith(prefix):
                counter += 1
                message += x + ', '
        if message == '':
            await self.send_msg(f"Nikt rozpoczynający się od {prefix} nie ogląda {channel_name}", ctx)
        elif len(message) > 400:
            await self.send_msg(
                f"{counter} użytkowników zaczynających się od {prefix} ogląda {channel_name}. Nie da się wypisać za dużo ich EZ",
                ctx)
        else:
            await self.send_msg(f"{message[:-2]} oglądają stream {channel_name}", ctx)

    @commands.command()
    @commands.cooldown(1, 3, commands.Bucket.user)
    async def help(self, ctx: commands.Context):
        if api.is_mod('lewusbot', ctx.channel.name):
            await ctx.send("Wszystkie komendy dostępne tutaj http://lewus.pl/ lewusHey ")
        else:
            await ctx.send("Wpisz se help na kanale gdzie bot ma moda np. u Lewusa lewusHey")

    @commands.command(name='mod', aliases=['mods'])
    @commands.cooldown(1, 3, commands.Bucket.user)
    async def mod(self, ctx: commands.Context):
        words = ctx.message.content.split()
        try:
            user = words[1]
        except:
            user = ctx.author.name
        if user not in self.mods:
            url = f'https://modlookup.3v.fi/api/user-v3/{user}'
            url_count = f'https://modlookup.3v.fi/api/user-totals/{user}'
            response = requests.get(url).json()
            response['channels'] = sorted(response['channels'], key=lambda k: k['views'], reverse=True)
            response_count = requests.get(url_count).json()
            self.mod_count[user] = response_count['total']
            tmp_mods = []
            for channel in response['channels']:
                tmp_mods.append(channel['name'])
            self.mods[user] = tmp_mods
            if 'randombrucetv' in tmp_mods:
                await ctx.send(f'/timeout {user} 60 mod Randombruca')
        if self.mod_count[user] == 0:
            await self.send_msg(f'Sadeg {user} nigdzie nie ma moda Sadge', ctx)
        elif self.mod_count[user] < 10:
            tmp_message = ", ".join(self.mods[user])
            await self.send_msg(f'PogU {user} ma moda u {tmp_message}', ctx)
        elif self.mod_count[user] < 100:
            tmp_message = ", ".join(self.mods[user][:10])
            await self.send_msg(f'PogU {user} ma moda na {self.mod_count[user]} kanałach. Największe to {tmp_message}',
                                ctx)
        elif self.mod_count[user] < 1000:
            await self.send_msg(f'VisLaud {user} ma moda na {self.mod_count[user]} kanałach.', ctx)
        else:
            await self.send_msg(f'MrDestructoid {user} ma moda na {self.mod_count[user]} kanałach i pewnie jest botem.',
                                ctx)

    @commands.command(name='last_ig', aliases=['zdjecie', 'fota', 'ig'])
    @commands.cooldown(1, 3, commands.Bucket.user)
    async def last_ig(self, ctx: commands.Context):
        if ctx.author.is_mod:
            link = api.get_last_ig_foto_instaloader(self.instagrams[ctx.channel.name])
            await ctx.send(f"Nowe foto na IG {link}")
        else:
            await ctx.send("Nie mam moda to nie wyślę Sadge")

    @commands.command()
    @commands.cooldown(1, 3, commands.Bucket.user)
    async def widzisz(self, ctx: commands.Context):
        if randint(0, 1):
            await self.send_msg(f'Widze Cię {ctx.author.name} Brek', ctx)
        else:
            await self.send_msg(f'Nie widze Cię {ctx.author.name} Sadeg', ctx)

    @commands.command(name="sr", aliases=["songrequest"])
    @commands.cooldown(1, 2, commands.Bucket.user)
    async def song_request(self, ctx: commands.Context):
        if (ctx.author.name == ctx.channel.name or ctx.author.name == "lewus") and ctx.channel.name in self.spotfiy:
            words = ctx.message.content.split()
            if words[1] == 'on':
                self.sr[ctx.channel.name] = True
                track_id, artist, title = spotify.get_current_track_data(ctx.channel.name)
                length = spotify.get_length(track_id, ctx.channel.name)
                self.queue[spotify.get_current_track_id(ctx.channel.name)] = spotify.Song(track_id, artist, title,
                                                                                          length, ctx.channel.name)
                await ctx.send('Song Request spotifyowy włączony')
            elif words[1] == 'off':
                self.sr[ctx.channel.name] = False
                self.queue.clear()
                await ctx.send('Song Request spotifyowy wyłączony')

    @commands.command()
    @commands.cooldown(1, 2, commands.Bucket.user)
    async def play(self, ctx: commands.Context):
        if ctx.channel.name in self.spotfiy and ctx.author.is_mod:
            spotify.play(ctx.channel.name)

    @commands.command()
    @commands.cooldown(1, 2, commands.Bucket.user)
    async def skip(self, ctx: commands.Context):
        if ctx.channel.name in self.spotfiy and ctx.author.is_mod:
            spotify.skip(ctx.channel.name)

    @commands.command(name="add_to_que", aliases=['add'])
    @commands.cooldown(1, 2, commands.Bucket.user)
    async def add_to_que(self, ctx: commands.Context):
        if ctx.channel.name in self.spotfiy and self.sr[ctx.channel.name]:
            artist, title, track_id = spotify.find_song(ctx.message.content[4:], ctx.channel.name)
            self.refresh_queue(ctx.channel.name)
            if any(x in f'{title} {artist}'.lower().split() for x in self.bannable):
                await ctx.send("lewusMrozon NIE WYSYŁAJ TAKICH PIOSENEK RASISTO lewusMrozon")
            elif track_id not in self.queue:
                length = spotify.get_length(track_id, ctx.channel.name)
                self.queue[track_id] = spotify.Song(track_id, artist, title, length, ctx.message.author.name)
                spotify.add_to_que(artist, title, track_id, ctx.channel.name)
                await self.send_msg(f"@{ctx.author.name} {artist} - {title} zostało dodane do kolejki", ctx)
            else:
                await self.send_msg(f"@{ctx.author.name} {artist} - {title} jest już w kolejce.", ctx)

    @commands.command()
    @commands.cooldown(1, 2, commands.Bucket.user)
    async def pause(self, ctx: commands.Context):
        if ctx.channel.name in self.spotfiy and ctx.author.is_mod:
            spotify.pause(ctx.channel.name)

    @commands.command(name='kiedy', aliases=['when'])
    @commands.cooldown(1, 2, commands.Bucket.user)
    async def kiedy(self, ctx: commands.Context):
        time = 0
        number_songs_before = 0
        if self.sr[ctx.channel.name]:
            for song in self.queue.values():
                if song.added_by == ctx.author.name:
                    if number_songs_before == 0:
                        await ctx.send("Twoja piosenka właśnie leci PogU")
                    else:
                        hours = int(datetime.datetime.fromtimestamp(time / 1000).strftime('%H')) - 1
                        minutes = int(datetime.datetime.fromtimestamp(time / 1000).strftime('%M'))
                        seconds = int(datetime.datetime.fromtimestamp(time / 1000).strftime('%S'))
                        await self.send_msg(
                            f"@{ctx.author.name} Twoja piosenka jest {number_songs_before + 1} w kolejce"
                            f"Będzie puszczona za {hours}h {minutes}min {seconds}s.", ctx)
                    return
                else:
                    time += song.length
                    number_songs_before += 1
            await ctx.send("Twojej piosenki nie ma w kolejce.")
        else:
            await ctx.send("Song Request jest wyłączony")

    @commands.command()
    @commands.cooldown(1, 2, commands.Bucket.user)
    async def volume(self, ctx: commands.Context):
        if ctx.channel.name in self.spotfiy and ctx.author.is_mod:
            words = ctx.message.content.split()
            try:
                level = words[1]
                if level[0] == '+':
                    level = int(level[1:]) + int(spotify.get_current_volume(ctx.channel.name))
                elif level[0] == '-':
                    level = int(spotify.get_current_volume(ctx.channel.name)) - int(level[1:])
                level = int(level)
                if level < 1:
                    level = 1
                elif level > 100:
                    level = 100
                spotify.change_volume(level, ctx.channel.name)
                await ctx.send(f'Spotify Volume changed to {level}')
            except Exception as e:
                print(e)
                await ctx.send(f'Current Volume - {spotify.get_current_volume()}.')

    @commands.command(name='song', aliases=['piosenka'])
    @commands.cooldown(1, 2, commands.Bucket.user)
    async def song(self, ctx: commands.Context):
        if ctx.channel.name in self.spotfiy:
            if spotify.get_current_playback_state(ctx.channel.name):
                track = spotify.get_current_track_name(ctx.channel.name)
                await self.send_msg(f'Aktualnie leci {track}', ctx)
            else:
                await ctx.send('Aktualnie nic nie leci.')

    @commands.command()
    @commands.cooldown(1, 2, commands.Bucket.user)
    async def top(self, ctx: commands.Context):
        words = ctx.message.content.split()
        if len(words) == 1:
            words.extend([100, 'pl'])
        elif len(words) == 2:
            words.append('pl')
        if len(words[2]) != 2:
            await self.send_msg(f'ZŁY KOD JĘZYKA @{ctx.author.name}', ctx)
        else:
            viewers = api.get_amount_of_viewers_from_top_streams(words[1], words[2])
            await self.send_msg(f'Top {words[1]} {words[2].upper()} ogląda łącznie {viewers} widzów.', ctx)

    @commands.command(name="lasttweet", aliases=['last_tweet', 'tweet'])
    @commands.cooldown(1, 2, commands.Bucket.user)
    async def last_tweet(self, ctx: commands.Context):
        if api.is_mod('lewusbot', ctx.channel.name) or api.is_vip('lewusbot', ctx.channel.name):
            words = ctx.message.content.split()
            if len(words) > 1:
                twitter_name = words[1]
            else:
                twitter_name = self.tweeters[ctx.channel.name]
            text, link = twitterapi.get_last_tweet(twitter_name)
            if twitterapi.get_followers_count(twitter_name) < 1000:
                return await self.send_msg(f'Pepega {twitter_name} ma mniej niż 1000 followersów.', ctx)
            if any(x in text.lower().split() for x in self.bannable):
                await ctx.send("NIE WYSYŁAJ TAKICH TWEETÓW RASISTO.")
            else:
                await self.send_msg(f'Ostatni tweet {twitter_name}: {text}. Link: {link}', ctx)
        else:
            await ctx.send("Nie mam tu moda/vipa Sadge")

    @commands.command(name="gdzie", aliases=['przesladowanie', 'where'])
    @commands.cooldown(1, 2, commands.Bucket.user)
    async def gdzie(self, ctx: commands.Context):
        user = ctx.message.content.split()[1].lower()
        if user in self.bannable:
            return await ctx.send("lewusMrozon OGARNIJ SIĘ. NIE MA KOGOŚ TAKIEGO. STOP BRZYDKICH SŁÓW lewusMrozon")
        user_info = api.user_info(user)
        if not user_info:
            return await self.send_msg(f"lewusSadge {user} - Nie istnieje taki użytkownik na twitchtv", ctx)
        else:
            user_inputted = user_info['data'][0]['display_name']
        result = db.find({'chatters': user})
        message = ''
        num_of_channels = 0
        for res in result:
            if res['name'].capitalize() not in message:
                message += f'{res["name"].capitalize()}, '
                num_of_channels += 1
        if message == '':
            await self.send_msg(f'lewusSadge {user_inputted} nie ogląda żadnego kanału Sadge', ctx)
        elif len(message) < 400:
            await self.send_msg(f'PepoG {user_inputted} ogląda kanały: {message[:-2]}.', ctx)
        else:
            await self.send_msg(f'PepoG {user_inputted} ogląda {num_of_channels} kanałów. '
                                f'Jest ich tyle, że na da się ich wypisać GG Sadge', ctx)

    @commands.command(name="subgifter", aliases=['gifter', 'gift'])
    @commands.cooldown(1, 5, commands.Bucket.user)
    async def subgifter(self, ctx: commands.Context):
        try:
            user = ctx.message.content.split()[1].lower()
        except:
            user = ctx.channel.name.lower()
        search = db_subs.find_one({'name': user})
        if search:
            gifters = {}
            for sub in search['subs']:
                if sub['gifter_name'] != '':
                    if sub['gifter_name'] in gifters.keys():
                        gifters[sub['gifter_name']] += 1
                    else:
                        gifters[sub['gifter_name']] = 1
            gifters = sorted(gifters.items(), key=lambda k: k[1], reverse=True)
            msg = ""
            i = 0
            for gifter in gifters:
                if i > 5:
                    return await self.send_msg(f'Lista aktualnych top gifterów. {msg}', ctx)
                msg += f'{gifter[0]}-{gifter[1]} PogU '
                i += 1
            return await self.send_msg(f'Lista aktualnych top gifterów. {msg}', ctx)
        else:
            await self.send_msg(
                f'Nie ma streamera w bazie, więc nie ma takich informacji Sadeg Musi on dać klucze do subów.', ctx)

    @commands.command(name="subs", aliases=['suby', 'subskrybenci'])
    @commands.cooldown(1, 5, commands.Bucket.user)
    async def subs(self, ctx: commands.Context):
        try:
            user = ctx.message.content.split()[1].lower()
        except:
            user = ctx.channel.name.lower()
        search = db_subs.find_one({'name': user})
        if search:
            gifted = 0
            tier3 = 0
            for sub in search['subs']:
                if sub['is_gift']:
                    gifted += 1
                if sub['tier'] == '3':
                    tier3 += 1
            if tier3 < 3:
                await self.send_msg(
                    f'{search["name"].capitalize()} ma {len(search["subs"])} subów z czego {gifted} to gifty.', ctx)
            else:
                await self.send_msg(
                    f'{search["name"].capitalize()} ma {len(search["subs"])} subów z czego {gifted} to gifty, a {tier3} jest tier3 PogU',
                    ctx)
        elif user in self.subs_count:
            if self.subs_count[user]:
                await self.send_msg(f'{user.capitalize()} ma {self.subs_count[user]} subów.', ctx)
            else:
                await self.send_msg(
                    f'Nie ma informacji na temat ilości subskrybentów {user.capitalize()}. Dawaj klucze Porvalo', ctx)
        elif api.user_info(user):
            subs_num = scrapesubs.get_subs_from_tracker(user)
            self.subs_count[user] = subs_num
            if subs_num:
                await self.send_msg(
                    f'{user.capitalize()} ma {subs_num} subów. Może być innacurate bo to dane z twitchtracker i streamer mógł kluczy nie updatwoać.',
                    ctx)
            else:
                await self.send_msg(
                    f'Nie ma informacji na temat ilości subskrybentów {user.capitalize()}. Dawaj klucze Porvalo', ctx)

    @commands.command(name="livegame", aliases=['gra', 'game'])
    @commands.cooldown(1, 5, commands.Bucket.user)
    async def livegame(self, ctx: commands.Context):
        try:
            user_name = ctx.message.content.split()[1]
        except:
            user_name = self.lol[ctx.channel.name]
        code, players = lolapi.get_players_from_live_game(user_name)
        if code == 200:
            message = ''
            for player in players:
                message += f'{player[0]}({player[1]}), '
            await self.send_msg(f'W grze {message[:-2]}.', ctx)
        elif code == 204:
            await self.send_msg(f'Sadge {user_name} nie jest aktualnie w grze.', ctx)
        elif code == 406:
            await self.send_msg(f'Taki gracz nie istnieje.', ctx)
        elif code == 402:
            await self.send_msg(f'Lewus nie zapłacił Porvalo', ctx)

    @commands.command(name="elo", aliases=['rank', 'lp'])
    @commands.cooldown(1, 5, commands.Bucket.user)
    async def elo(self, ctx: commands.Context):
        try:
            user_name = ctx.message.content.split()[1]
        except:
            user_name = self.lol[ctx.channel.name]
        message = lolapi.get_current_elo(user_name)
        await self.send_msg(f'Elo użytkownika {user_name} - konto {message}', ctx)

    @commands.command(name="whoingame", aliases=['bootcamp', 'ingame'])
    @commands.cooldown(1, 5, commands.Bucket.user)
    async def whoingame(self, ctx: commands.Context):
        players_ingame = lolapi.get_players_ingame()
        msg = ", ".join(players_ingame)
        await self.send_msg(f'Gracze w grze {msg}', ctx)

    @commands.command(name="stacked", aliases=['stackedgame', 'moststackedgame'])
    @commands.cooldown(1, 5, commands.Bucket.user)
    async def stackedgame(self, ctx: commands.Context):
        game = lolapi.get_most_stacked_game()
        msg = ", ".join(game)
        if len(game) > 2:
            await self.send_msg(f'Najlepsza gra do oglądania {msg}', ctx)
        else:
            await self.send_msg(f'Same nudziarskie gry.', ctx)

    @commands.command(name="konta", aliases=['acc', 'accs', 'konto'])
    @commands.cooldown(1, 5, commands.Bucket.user)
    async def konta(self, ctx: commands.Context):
        try:
            user_name = ctx.message.content.split()[1]
        except:
            user_name = self.lol[ctx.channel.name]
        accounts = lolapi.get_accounts(user_name)
        message = ', '.join(accounts)
        await self.send_msg(f'Konta gracza {user_name}: {message}.', ctx)

    @commands.command(name="opgg")
    @commands.cooldown(1, 5, commands.Bucket.user)
    async def opgg(self, ctx: commands.Context):
        if api.is_mod('lewusbot', ctx.channel.name) or api.is_vip('lewusbot', ctx.channel.name):
            try:
                user_name = ctx.message.content.split()[1]
            except:
                user_name = self.lol[ctx.channel.name]
            accounts = lolapi.get_accounts(user_name)
            if len(accounts) == 1:
                link = f'https://euw.op.gg/summoner/userName={accounts[0]}'
            else:
                link = "https://euw.op.gg/multi/query="
                for account in accounts:
                    link += account.replace(" ", "") + '%2C%20'
            await self.send_msg(f"OPGG gracza {user_name} {link}", ctx)
        else:
            await self.send_msg("Nie mam moda, nie moge wysłać Sadeg", ctx)

    @commands.command(name="czesi", aliases=['czech', 'czesiwgrze', 'cz'])
    @commands.cooldown(1, 5, commands.Bucket.user)
    async def czesi(self, ctx: commands.Context):
        try:
            user_name = ctx.message.content.split()[1]
        except:
            user_name = self.lol[ctx.channel.name]
        code, players = lolapi.get_czech_players(user_name)
        if code == 200:
            message = ''
            for player in players:
                message += f'{player[0]} - {player[1]}, '
            if message != '':
                await self.send_msg(f'POLICE W grze są reprezentaci Czech - {message[:-2]} POLICE', ctx)
            else:
                await self.send_msg("POLICE GRA WOLNA OD CZECHÓW EZ", ctx)
        elif code == 204:
            await self.send_msg(f'Sadge {user_name} nie jest aktualnie w grze.', ctx)
        elif code == 406:
            await ctx.send(f'Taki gracz nie istnieje.')
        elif code == 402:
            await ctx.send(f'Lewus nie zapłacił Porvalo')

    @commands.command(name="glowna", aliases=['frontpage'])
    @commands.cooldown(1, 10, commands.Bucket.user)
    async def glowna(self, ctx: commands.Context):
        glowna_names = []
        viewers_num = 0
        front = glowna.get_featured_streams()
        for user in front:
            # print(user['user_login'], user['viewers'], get_chatters(user['user_login']), user['priorityLevel'])
            viewers_num += (user['viewers'] - glowna.get_chatters(user['user_login']))
            glowna_names.append(user['user_login'])
            if user['priorityLevel'] < 3:
                return await self.send_msg(f'{user["user_login"]} ma astro promocje na głównej i zabiera wszystkich '
                                           f'{user["viewers"] - glowna.get_chatters(user["user_login"])} widzów.', ctx)

        msg = f"{', '.join(glowna_names)} są aktualnie na głównej. Główna daje aktualnie {viewers_num} dodatkowych widzów."
        await self.send_msg(msg, ctx)

    @commands.command(name="vips", aliases=['vip'])
    @commands.cooldown(1, 2, commands.Bucket.user)
    async def vip(self, ctx: commands.Context):
        try:
            user = ctx.message.content.split()[1].lower()
        except:
            user = ctx.author.name
        user_info = api.user_info(user)
        if not user_info:
            return await self.send_msg(f"Sadeg {user} - Nie istnieje taki użytkownik na twitchtv", ctx)
        else:
            user_inputted = user_info['data'][0]['display_name']
        result = db_vips.find({'vips': user})
        message = ''
        num_of_channels = 0
        for res in result:
            if res['login'].capitalize() not in message:
                message += f'{res["login"].capitalize()}, '
                num_of_channels += 1
        if message == '':
            await self.send_msg(f'Sadeg {user_inputted} nie ma nigdzie vipa Sadge', ctx)
        elif len(message) < 400:
            await self.send_msg(f'PogU {user_inputted} ma vipa na tych kanałach: {message[:-2]}.', ctx)
        else:
            await self.send_msg(f'PogO {user_inputted} ma tyle vipów {num_of_channels}. '
                                f'Jest ich tyle, że na da się ich wypisać GG Sadge', ctx)

    @commands.command(name="vipscount", aliases=['vipcount'])
    @commands.cooldown(1, 2, commands.Bucket.user)
    async def vipscount(self, ctx: commands.Context):
        try:
            user = ctx.message.content.split()[1].lower()
        except:
            user = ctx.channel.name
        user_info = api.user_info(user)
        if not user_info:
            return await self.send_msg(f"Sadeg {user} - Nie istnieje taki użytkownik na twitchtv", ctx)
        else:
            user_inputted = user_info['data'][0]['display_name']
        result = db_vips.find_one({'login': user})
        if result:
            return await self.send_msg(f'lewusDab {result["login"]} ma {result["vip_count"]} vipów.', ctx)
        else:
            return await self.send_msg('Nie ma tego kanału w bazie danych.', ctx)

    @commands.command(name="watchtime", aliases=['xayopl'])
    @commands.cooldown(1, 2, commands.Bucket.user)
    async def watchtime(self, ctx: commands.Context):
        if len(ctx.message.content.split()) == 1:
            user = ctx.author.name
            target_user = ctx.channel.name
        elif len(ctx.message.content.split()) == 2:
            target_user = ctx.channel.name
        else:
            user = ctx.message.content.split()[1].lower()
            target_user = ctx.message.content.split()[2].lower()
        url = f'https://xayo.pl/api/mostWatched/{user}'
        response = requests.get(url).json()

        for streamer in response:
            if streamer['streamer'] == target_user:
                time_min = streamer["count"] * 5
                time = transform_minutes(time_min)
                time_msg = ''
                for k, v in time.items():
                    if v != 0:
                        time_msg += f'{v} {k} '
                time_msg = time_msg[:-1]
                return await self.send_msg(
                    f'MrDestructoid {user} ogladał kanał {target_user} przez {time_msg}.', ctx)
        return await self.send_msg(f'MrDestructoid {user} nie oglądał w ogóle kanału {target_user}.', ctx)

    @commands.command(name="semp", aliases=['ileogladalkobiet'])
    @commands.cooldown(1, cd, commands.Bucket.user)
    async def semp(self, ctx: commands.Context):
        try:
            user = ctx.message.content.split()[1].lower()
        except:
            user = ctx.message.author.name.lower()
        url = f'https://xayo.pl/api/mostWatched/{user}'
        response = requests.get(url).json()
        time_all = 0
        time_female = 0
        for streamer in response:
            if streamer['streamer'] in self.streamerki:
                time_female += streamer['count'] * 5
            time_all += streamer['count'] * 5
        percentage = round(time_female / time_all * 100, 2)
        time = transform_minutes(time_female)
        time_msg = ''
        for k, v in time.items():
            if v != 0:
                time_msg += f'{v} {k} '
        time_msg = time_msg[:-1]
        if time_msg != '':
            return await self.send_msg(f"lewusSemp {user} oglądał streamerki przez {time_msg}, "
                                       f"co sprawia, że oglądał streamerki przez {percentage}% swojego czasu na PL Twitch.",
                                       ctx)
        return await self.send_msg(f"gachiBASS {user} nigdy nie oglądał żadnej polskiej streamerki GIGACHAD", ctx)

    @commands.command(name="ksiezniczki", aliases=['damy', 'topdupeczki', 'topsemp'])
    @commands.cooldown(1, cd, commands.Bucket.user)
    async def ksiezniczki(self, ctx: commands.Context):
        try:
            user = ctx.message.content.split()[1].lower()
        except:
            user = ctx.message.author.name.lower()
        url = f'https://xayo.pl/api/mostWatched/{user}'
        response = requests.get(url).json()
        num = 0
        fav_streamer = []
        for streamer in response:
            if streamer['streamer'] in self.streamerki and streamer['count'] > 12:
                num += 1
                fav_streamer.append(streamer['streamer'])
                if num == 3:
                    break
        if num > 0:
            return await self.send_msg(f'lewusSemp Ulubione streamerki {user}: {", ".join(fav_streamer)}.', ctx)
        return await self.send_msg(f'gachiBASS {user} nigdy nie oglądał żadnej polskiej streamerki GIGACHAD', ctx)

    @commands.command(name="watchtimeall", aliases=['watchalltime'])
    @commands.cooldown(1, cd, commands.Bucket.user)
    async def watchtimeall(self, ctx: commands.Context):
        try:
            user = ctx.message.content.split()[1].lower()
        except:
            user = ctx.message.author.name.lower()
        url = f'https://xayo.pl/api/mostWatched/{user}'
        response = requests.get(url).json()
        time_all = 0
        for streamer in response:
            time_all += streamer['count'] * 5
        today = date.today()
        datediff_min = ((today - xayopl_creation_date).days) * 24 * 60
        percentage = round(time_all * 100 / datediff_min, 2)
        time = transform_minutes(time_all)
        time_msg = ''
        for k, v in time.items():
            if v != 0:
                time_msg += f'{v} {k} '
        time_msg = time_msg[:-1]

        await self.send_msg(f'lewusDab {user} spedził {time_msg} na PL twitch od 26 lipca, '
                            f'co daje {percentage}% jego życia. ', ctx)

    @commands.command(name="pkt", aliases=['mastery', 'maestria', 'punkty'])
    @commands.cooldown(1, 2, commands.Bucket.user)
    async def pkt(self, ctx: commands.Context):
        args = ctx.message.content.split()
        accounts = []
        pkt_maestry = 0
        champion = args[1].lower()
        if len(args) == 2:
            user = self.lol[ctx.channel.name]
            accounts = lolapi.get_accounts(user)
            server = 'euw'
        elif 'euw' in args or 'EUW' in args or 'eune' in args or 'na' in args or 'kr' in args:
            server = args[2].upper()
            user = ''.join(args[3:])
            accounts.append(user)
        else:
            user = ''.join(args[2:])
            print(user)
            accounts = lolapi.get_accounts(user)
            server = 'euw'

        for account in accounts:
            id = lolapi.get_summoner_id(account, server)
            pkt_maestry += lolapi.get_mastery_points(id, champion, server)
        if user == 'lewus':
            id = lolapi.get_summoner_id('xwojteczek01pl', 'eune')
            pkt_maestry += lolapi.get_mastery_points(id, champion, 'eune')
        pkt_maestry = "{:,}".format(pkt_maestry)
        return await self.send_msg(f'Gracz {user} ma {pkt_maestry} punktów mastery na {champion.capitalize()}.', ctx)

    @commands.command(name="games", aliases=['wins', 'losses', 'gamesplayed'])
    @commands.cooldown(1, 2, commands.Bucket.user)
    async def games(self, ctx: commands.Context):
        try:
            target_user = ctx.message.content.split()[1]
        except:
            target_user = ctx.channel.name
        wins, loses = lolapi.get_played(target_user)
        await self.send_msg(
            f'Gracz {target_user} zagrał w tym sezonie {wins + loses} gier, W/L {wins}/{loses} - winratio - {round(wins * 100 / (wins + loses), 2)}%',
            ctx)

    @commands.command(name="chattersall", aliases=['allusers'])
    @commands.cooldown(1, 2, commands.Bucket.user)
    async def chattersall(self, ctx: commands.Context):
        try:
            country = ctx.message.content.split()[1]
        except:
            country = 'pl'
        chat_stats = db.find_one({'name': 'chat_stats'})
        if country == 'pl':
            await self.send_msg(
                f'Na polskim twitchu jest w tym momencie {chat_stats["num_pl_unique_chatters"]} unikalnych chattersów.',
                ctx)
        elif country == 'en':
            await self.send_msg(
                f'Na angielskim(top200) twitchu jest w tym momencie {chat_stats["num_en_unique_chatters"]} unikalnych chattersów.',
                ctx)
        else:
            await self.send_msg(
                f'Na polskim i angielskim(top200) twitchu jest w tym momencie {chat_stats["num_all_unique_chatters"]} unikalnych chattersów.',
                ctx)

    @commands.command(name="yfl", aliases=['yflwatchtime'])
    @commands.cooldown(1, 1, commands.Bucket.user)
    async def yfl(self, ctx: commands.Context):
        msg = ctx.message.content.split()
        if len(msg) == 1:
            user = ctx.message.author.name
        else:
            user = msg[1]
        url = f'https://xayo.pl/api/mostWatched/{user}'
        response = requests.get(url).json()
        time_all = 0
        yfl_time = 0
        for streamer in response:
            time_all += streamer['count'] * 5
            if streamer['streamer'] in yfl:
                yfl_time += streamer['count'] * 5
        ratio = yfl_time / time_all
        if ratio < 0.3:
            await self.send_msg(f'Sadeg {user} nie jest widzem yfl', ctx)
        elif ratio < 0.5:
            await self.send_msg(f'PogU {user} jest widzem yfl PogU', ctx)
        elif ratio > 0.5:
            await self.send_msg(f'PogU FIRE {user} jest giga koneserem yfl PogU FIRE', ctx)

    @commands.command(name="spam", aliases=['spammers'])
    @commands.cooldown(1, 1, commands.Bucket.user)
    async def spam(self, ctx: commands.Context):
        msg = ctx.message.content.split()[1:]
        msg = " ".join(msg)
        if ctx.author.name == 'lewus':
            for x in range(10):
                await ctx.send(msg)


if __name__ == "__main__":
    bot = Bot()
    bot.run()
