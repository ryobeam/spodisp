import sys
import time
from io import BytesIO 
import urllib.request
import pprint

import spotipy
import spotipy.util as util

import pygame
from pygame.locals import *
from PIL import Image


class Draw():

    def __init__(self):
        self.frame = 0

    def text(self, text, pos_xy, size, color):
        #pygame.draw.rect(screen, color, )
        font = pygame.font.SysFont('yugothicuisemibold', size)
        text = font.render(text, True, color)
        screen.blit(text, pos_xy)

    def draw(self):

        self.frame += 1
        pygame.display.update()


def draw_info(title, artist, album, albumart_url):
    px = 5
    py = 5
    image_width = 90

    def _read_image_fromurl(url):
        # URL から画像をバッファに読み込む
        buffer = Image.open(BytesIO(urllib.request.urlopen(url).read())).convert("RGB")
        image = pygame.image.fromstring(buffer.tobytes(), buffer.size, buffer.mode).convert()
        # 左隅の色で透明化
        #colorkey = image.get_at((0,0))
        #image.set_colorkey(colorkey, RLEACCEL)
        # 縮小
        img_small = pygame.transform.scale(image, (image_width, image_width)) 

        return img_small

    screen.fill((30,30,30))

    draw.text(title,  (px+image_width+10, py+10), 14, (250,250,250))
    draw.text(artist, (px+image_width+14, py+32), 12, (120,120,120))
    draw.text(album,  (px+image_width+14, py+50), 12, (120,120,120))
    image = _read_image_fromurl(albumart_url)
    screen.blit(image, (px,py))

class GetCurrentlyPlaying():

    def __init__(self, username, scope):
        self.username = username
        self.scope = scope
        self._token()

    def _token(self):
        self.token = util.prompt_for_user_token(self.username, self.scope)
        ### token = util.prompt_for_user_token(username,scope, client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)
        self.sp = spotipy.Spotify(auth=self.token)

    def song_info(self):
        try:
            results = self.sp.currently_playing()
        except spotipy.client.SpotifyException:
            self._token()
            results = self.sp.currently_playing()
        return results


# 初期化
scope = 'user-read-currently-playing'
username = 'K-O'
get_currently_playing = GetCurrentlyPlaying(username, scope)

draw = Draw()
is_end = False

# pygame の初期化
pygame.init()
screen = pygame.display.set_mode((400, 100))
pygame.display.set_caption(f'Spotify Now Playing [{username}]')    #

###import code
###code.InteractiveConsole(globals()).interact()

while not is_end:

    song_info = get_currently_playing.song_info()

    title  = song_info['item']['name']
    artist = song_info['item']['artists'][0]['name']
    album  = song_info['item']['album']['name']
    url    = song_info['item']['album']['images'][0]['url']
    #url   = 'https://i.scdn.co/image/ab67616d00001e02c249c673118e8f42450edc75'
    #print(r['is_playing'])
    #print(title,artist,album)

    draw_info(title, artist, album, url)
    draw.draw()

    for event in pygame.event.get():
            # 終了(ウインドウクローズ)
            if event.type == QUIT:
                is_end = True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    is_end = True

    pygame.time.wait(100)

pygame.quit()
sys.exit()
