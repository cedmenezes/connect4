import PySimpleGUI as sg
import numpy as np
from copy import deepcopy
import math
import pygame

'''
 Função de avaliação
'''
def funcaoAvaliacao(mat):
    pontuacaoJog1 =    max( avaliacaoHorizontal(mat, 'X'),
                                                avaliacaoVertical(mat, 'X'),
                                                avaliacaoDiagonalPrincipal(mat, 'X'),
                                                avaliacaoDiagonalSecundaria(mat, 'X') )
    pontuacaoJog2 =    max( avaliacaoHorizontal(mat, 'O'),
                                                avaliacaoVertical(mat, 'O'),
                                                avaliacaoDiagonalPrincipal(mat, 'O'),
                                                avaliacaoDiagonalSecundaria(mat, 'O') )
    if pontuacaoJog2 == 4: return -1000
    elif pontuacaoJog1 == 4: return 1000
    elif pontuacaoJog2 == 3: return -500
    elif pontuacaoJog1 == 3: return 500
    else: return pontuacaoJog1 - pontuacaoJog2

def pontuar(matString, jogador):
    if (jogador*4) in matString: return 4
    elif ' '+(jogador*3) in matString or (jogador*3)+' ' in matString: return 3
    elif ' '+(jogador*2) in matString or (jogador*2)+' ' in matString: return 2
    else: return 0

def avaliacaoHorizontal(mat, jogador):
    matString = ''
    for l in range(len(mat)):
        for c in range(len(mat[0])):
            matString += mat[l][c]
        matString += '\n'
    #print('String:', matString, sep='\n')
    return pontuar(matString, jogador)

def avaliacaoVertical(mat, jogador):
    matString = ''
    for c in range(len(mat[0])):
        for l in range(len(mat)):
            matString += mat[l][c]
        matString += '\n'
    #print('String:', matString, sep='\n')
    return pontuar(matString, jogador)

def avaliacaoDiagonalPrincipal(mat, jogador):
    matString = ''
    for x in range(len(mat)-1, 0, -1):
        l = x; c = 0
        while l<len(mat) and c<len(mat[0]):
            matString += mat[l][c]
            l+=1; c+=1
        matString += '\n'

    for x in range(len(mat[0])):
        l = 0; c = x
        while l<len(mat) and c<len(mat[0]):
            matString += mat[l][c]
            l+=1; c+=1
        matString += '\n'
    #print('String:', matString, sep='\n')
    return pontuar(matString, jogador)

def avaliacaoDiagonalSecundaria(mat, jogador):
    matString = ''
    for x in range(len(mat)-1, 0, -1):
        l = x; c = len(mat[0])-1
        while l<len(mat) and c>=0:
            matString += mat[l][c]
            l+=1; c-=1
        matString += '\n'

    for x in range(len(mat[0])-1, -1, -1):
        l = 0; c = x
        while l<len(mat) and c>=0:
            matString += mat[l][c]
            l+=1; c-=1
        matString += '\n'
    #print('String:', matString, sep='\n')
    return pontuar(matString, jogador)

'''
 Funções úteis
'''
def primeiraLinhaLivre(coluna, mat):
    return livre(len(mat)-1, coluna, mat)

def livre(linha, coluna, mat):
    if linha<0: return -1
    if mat[linha][coluna] == ' ': return linha
    return livre(linha-1, coluna, mat)

def outro(jogador):
    if jogador == 'X': return 'O'
    else: return 'X'

def gereSucessores(inicio, vez):
    suc = []
    for i in range(len(inicio[0])):
        linha = primeiraLinhaLivre(i, inicio)
        if linha >= 0:
            novaMat = deepcopy(inicio)
            novaMat[linha][i] = vez
            suc.append(novaMat)
        else:
            suc.append(None)
    return suc

'''
 Algoritmo Minimax
'''
def minimax (inicio, nivelDeDificuldade):
    _ , coluna = maxNo(inicio, 'X', nivelDeDificuldade)    # O computador quer maximizar seus pontos
    return coluna

def maxNo(inicio, vez, dificuldade):
    if dificuldade == 0:
        return funcaoAvaliacao(inicio), 0
    else:
        sucessores = gereSucessores(inicio, vez)
        pontos = []
        for i in range(len(sucessores)):
            if sucessores[i] == None: pontos.append(-math.inf) # jogada impossível
            else:
                ponto, indice = minNo( sucessores[i], outro(vez), dificuldade-1)
                pontos.append(ponto)
        return max(pontos), np.argmax(pontos)

def minNo(inicio, vez, dificuldade):
    if dificuldade == 0:
        return funcaoAvaliacao(inicio), 0
    else:
        sucessores = gereSucessores(inicio, vez)
        pontos = []
        for i in range(len(sucessores)):
            if sucessores[i] == None: pontos.append(math.inf) # jogada impossível
            else:
                ponto, indice = maxNo( sucessores[i], outro(vez), dificuldade-1)
                pontos.append(ponto)
        return min(pontos), np.argmin(pontos)

def toqueAudio(arquivo):
    pygame.mixer.init()
    my_sound = pygame.mixer.Sound(arquivo)
    my_sound.play()
    pygame.time.wait(int(my_sound.get_length() * 1000))


'''
 Jogo Connect4
'''
def main():
    mat = [[' ',' ',' ',' ',' ',' ',' '],
                [' ',' ',' ',' ',' ',' ',' '],
                [' ',' ',' ',' ',' ',' ',' '],
                [' ',' ',' ',' ',' ',' ',' '],
                [' ',' ',' ',' ',' ',' ',' '],
                [' ',' ',' ',' ',' ',' ',' '],
                [' ',' ',' ','X',' ',' ',' ']]

    face_angry = b'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'
    face_cool = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAN1wAADdcBQiibeAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAAXdEVYdEF1dGhvcgBMYXBvIENhbGFtYW5kcmVp35EaKgAAACl0RVh0RGVzY3JpcHRpb24AQmFzZWQgb2YgSmFrdWIgU3RlaW5lciBkZXNpZ26ghAVzAAAKIElEQVRYw5WXW4yd11XHf3t/t3Odc87cPOPLTGyPPY4zHTup40SRk9AKNbQPoChqQYhQkFCKgEhUQAQIqQSp9KURFUJB6QtIhJRSmrQkUZWoiVM5JKlTnNb4Fmdsx7e5nTkzcy7ffV94mGMYB0UuW1ra0vfw/X/7v9bWWltYa7n1EgL+UsCDco7YmWLUgYqzRk82ULZJbEa4TUFLwyc1YPtx6z/fGmBD/KVvzg9mywu/IqX5vOM6u3G8ISGcihEmksasaKU/1MJ5vlwffuGhx55ZBszPA3FLgGf/7FNTvrRPWT/4zK7paXvb/sPF6shu3NIw0i9j8hgVt4hWL3P13E+TC2dPijQKjylrv/zoV4+evhXExwJ858kZP48b3xBS/tbddx/wJ+971JF+EWsicDyEW0RIHxBYnYDOQRawecqVHz9n3jp2PFVZ+nzWSx577JmfRP8vgH/48wdGPK1fGav7++556JFiYcssJryALI8iK9sQQR3hlEC4gMWaFPIuJm5iojVEYYxs+TRvv/RccnGpdznV5hcf/9t3rv1cAM9++YFxPP3ezJ7tQ9NHHnZt2gRC3MZuZGUcURhEeGVwfARyw2GjsDrGpl101MR0rgEFcKqc+9G39X/8dK6da3v3Hz59/OLHAlSrw7cXCuLX7p4a+IN6baARVIdEWaxzz+wYhw4dZOe+adzKCKLYAK+CcHwQNwA0VkXYpE1n6To/O3GS4z85zYnT12h2Ja5N6fZ64dxC9M9K8S9ra82jNwHUarXfHxvf+sihT0wf2Ltre+O2qWkx1Kjiej7ziwvMvX+Sy1c+5L579/CbX/wsxdoYygxhrI/nRkjR4+rFizz9989z4sQc+/ftY2b2LsbHtoJRNFfWuTB3zs5dvNZ978zcucXm8tHO6uqfAohyvX4QZb6u0t7gzq1DB8a3jMhSuUSlFFAbbDA4OEilWsFYw8LyMp2wx5888RfUaqOsrDSZmNjNiy/+Iy+88AOG6lV2TU7gSEnYDWmttGi31wl7MWEUc31hyVxf7px2g3IXV/5Vu9V6xXWtvSdM40a95O21xsg0VzhRB9ep4YURQkjCOAIh2LFjJ7/zu0+QZglP/91TPPrFB3j7nWUe+qVfp17bwY9ef5mV1hrCWpI4Jooj0jQlibqkqUFiZdEXe3ppfM4X5U8Ar7ip1h8UgqAghSoKKcjCdVxKeFlCmno4DmjtIxzJlcsX+MbffI1cZcxdOEUaT/Pccy9z/MfHyJIIpTJUlmG1Jk8zkjgmTWLyLCOLQhASIYRfKAR1I8x5ADfp9U7t3D6srMpRaUJqBZ7nkiYJrisRwqB1hnQkJoZOu0WUxtx//xSz0wGDtYyzp9/l4OxdDNUnSeKYsLOOUgbXCxDA8NAo586eRmch5XJZKCvE9cXWawAS6H7uYMOZnazLUtFHaUOSJCRJTBiGhL0eYRgShT1WV1usry9y38EKj/3qDnR4ma8+cSdbhnLeeusorVaLrdsmmL79AAfuupdD99zP8MgY0vWRjovn++wZK4tP768CZP9zC7722weXdg2VR6+dP8W5lZz31zy6SuK5DtKR+IHEdR0mxny+8LktzM5sYWh0AM/zyHNNq9nhh8eu8b1Xl7m6lJJmBt9xKBQKdLohJZGxp56xd0gye+BO3pxrhU9990wFwAWQjlO/Y0eVfWnOzKhmIRW0MgcloVCCcsWl3vAYHy8xOSFo+D1klGEcibSGhqf4zAGP3bUKi4uS1dWUlVZOr7dOydFMVjTjBcMWXxPsqHFsruU/+YUZ/yv/eipzn/zSoZJvMFJIqk5Mbdhnry/JPRfleQQVj2IlwC35eCWJ9HNIQrRKEVJgrUHkhqqnuGObw/RgARVJ4p4k6Uk8leMrC4lGpDmR0TiQrKRqGJiXX/nmf8ZaGydOEzLr4lqDNYYkNTQCy4BnKUiNbxVSaWSaYeMUEyeYKMHEKSZNIM1wtMK3ioI0DHhQcgy9UCONwbWG3AjSPCPJjZ/ZyvpGEVprc6M67TAmFgFWGQIMUmte/a+YE3MJ3Y7CZAqb5pg0x6TZhnCcYqMUE2eYNMNmCpNr2p2MY6dj3jmfMViwOMZgtSYWPp0oQmljn/n3jQ7pAhht51thMlR2SlRViKc0gwXJfZMuP5zLeflkytYhj8kxn6ntBXZtC3BdiRUbreDKUsbZKwmXFzKWVnOsMjy41+HwToHMFEZpjDLEssxyO8FYs3yjF7gASovvXl/P9440qkE3adLINdaRlALJw7MB062AN85HHP1ZxEvvhmQahBS4UmCsRWlLwRVUAjg4WeYXpsvURBsbp1ilsbmmk0NSGeDSYqyU5vs3AVht/m25yx/HQ4WgrRyKuaYgFdIR2BT2jzjM3D5LK5Gcv7LE/EqHtU6ENpZC4DHSGGBybJCpyXGCbAXdmsMmOTbfSEmWG9raIZZFLq2kobZ8+/+04z96ZN+ZqSF9+1Q5op4sMBpYnIILgQ++i3BdnIFx3JFp3KG9SL+KkS5SOJi4Rd46T758Gt1ZQmqNTXPIckyiWE4Fa4Ux5roF3v6Qa//02qUJ2xd2b5BkRvzeByvyxZFiUBGijJP1GEYhrEBai9aWrHUVs3oN67yJ9aoIKcFadLyKNAZHWBxjEUphM4VNFasZrIsiHVvg3cu6l2r5uN00Bd00ET3+y9OvNYLoyF3j+JV4gUFPMxiA47kYz0FLByUlmRFoC8ZapAAB+BI8a3HNxnU1mWI1hVYu6ZW2cvxqri6tBie/9cblT26eiOT/Dt9CrK+nv7EUFdvnV41tuw2amaSZCKJYQZIj0xyZ5bi5wlU5Tm4QucJTGjfLkWkGcU6cKJYTQTOXdNwG7zdz5laCsBvxedFfNznQ/yAB5+EjE4cbJfeVvcNJac+goJC1qNqUsmspOxA4AiMFBoEVAoFFWhDGoIylp6CnBD18QneAC22Pd6+48VqYPfL6e4tvADmgb6RhM4ADBED5yMyWw7u2lJ4dq8aVO7cXnJKI8aImRWkpSfCkxRFseG9BW8iNIDEQGUHqVEiCBqcWrTkzb+MPl+IvnZhbeR2IgKQPYa21djOAuzHKUgbqI/XCvUf2D/91tSCGZ7ZZb/eWGk66ikzaSBXjfhQAB+UWMaVRFmOf43OhWuuq9jvn177easevAk2gB8R9APNRAAfwgSJQASaAw3u2DTx4x8TAp0qBCHaPV9yJkaIYrhXwHAnGIByXXGvaseXqamYvzHfz1mpPnb3affOD+c7bwHvA+8Ba34EUUNZac9MtEELIPoTXd6IKbAN2AhPbh8v7d4wUZ0Zq/pQUTkkIa31H6kwbiRVSGxO3utmlK83ozPVmeNbAPHAJuAKs98UzQN04/UcBblSm00+H16+JgU1R7++FcuAOlItuLUxVGMZqvX+yHtAGOpv2zcL6Ru4/9mXUB7kRzqZw+0B+H+6GY6Yfqi+UbBJTm17Jhr76Zr3/Bn/7nRMKs+hpAAAAAElFTkSuQmCC'
    vazio = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAOXHpUWHRSYXcgcHJvZmlsZSB0eXBlIGV4aWYAAHjarZlZchtJEkT/8xRzhNyX4+RqNjeY48/zLACiKMm6zboJESgWaokM9/DwKJn9v/8e8x9+QnHWxFRqbjlbfmKLzXc2qn1++n13Nt73++NfX/H3T/vN5wvPrsBneP6s+XX8e7/7XOD56GylLxeq8/XF+PmLFl/Xr98u9LpRUESKYr0u1F4XCv75wr0u0J9l2dxq+bqEsZ/P9V5JfX6N3s47J+X5+P53LGRvJe4TvN/BBcu7D/4JIOjXmdD5wvHuA9+wldlOod7970hIyO/yZL9EZb6j8tlyf9j/DZSQn/2GHT8nM38+f7vfpd8n39wUf7lzmJ87/7x//Mjv1yTfHJ9VzTn7WV2PmZTm16LeS7lbHDhIebinZV6F38R2ua/GqxrYO4F82WkHr+ma88ByXHTLdXfcvp/TTUKMfvvCp/cToLSvhuKbn8EaYaOXO76EFhZ4+TCBN7DXf2Jx977t3m66yo2X40jvuJgTFYze/o3XHy90jijvnK2fXBGXFwkJQ8jpnaMAxJ03j9JN8Pv1/Ue4BhBMN82VBXY7nkuM5F7cEo/CBTpwYOLzqTVX1usCpIh7J4KhAqKz2YXksrPF++Iceazg07lQ9SH6AQQuJb+I0scQMuBUr3tzTnH3WJ/8sxvNAohEMRWgaaGDVUTY4E+JFQ71FFJMKeVUUk0t9RxyzCnnXLLEr5dQYkkll1JqaaXXUGNNNddSq6mt9uZbQBxTy6202lrrnZt2rtw5u3NA78OPMOJII48y6mijT+gz40wzzzKrmW325VdY6MTKq6y62urbbai0404777LrbrsfqHbCiSedfMqpp53+Qc2ZB9ZfXn8fNfdGzV+kdGD5oMappbwv4SQnSZiBmI8OxIsQgNBemNnqYvRG0Akz21C2kDxRJoGznBADwbidT8d9sPuB3E+4mRj/EW7+jZwRdP8GckbQ/QG5X3H7DWpL3WbaYC5CKkMl1QbKj4O6r/yjJ/3pc3riPatsMrdmPiebzW3GIKZWNgGvs/dIfRZyE/Ycc2+XWkknrJRdKovqsimfkU51I6XZx2Kt6xje50Bu20laWD8tePJSz55nFP6eQd8OqnPsxK5Ty5kusNBeM7t6179q/NmnbJRmDiKkWYxj9Vl9WWBoU+E+cfaWqnsOtcev/cT0umTvJZky24q7j7rtYHUs26bAuYdw3weu3p0WBwz+JAAI6PJh/WTlZK4IrKa0Ng/L39OvlRWpEjo2K0NelNsuJ/GXn+b7DsLofa4SRj87FjqLb4MW8MpVycAFX3tYxbs9Rpm92JAWyS4DRKBbiWcSBoljZatRlBvF4zyulOrogLLshs9j5p4IfaaLSj9p7GkOCya3M7F8OlAeYUPuEQ9kgIeke9B3EgsvBJoGzA37tGX7IFExgCSUT8ckYmxJhAgEmZeb8VAGm1Kq0IaCO8KvIEcjiDZ8q/53oHwCz7HhuZZWlx/ZwXTxKlVQzUpU62OvBlcotBTaPp2WuwNKcxJXOFy4cJmH6wMbZP4ambG9KErRuxQ7GC/L9afP9sCMcq/plklQbaxE/kl4Qia6GN+WqJzJcN85D79H28jEyXSpnUnN4sIsYKU+xNrcDRlCP9bkEtlnKieuPlCjNQF7TkK44bB77kIvG4lOBAlCRxwSErlH6CNv0ytI5gIsOUeqEXlcOa6Sk5+xoI0xdAeimQJYkZSzkuz7Cv2orE9L4Ed1m572LnPRPcGX33YWm5sYz8iXoOI53+39SfsJro4pMDcgoQ8xORok/c3VpD/Q/c9nmYjByXB8oolz1ZqG24tC29wD7Vkx9U0SJW+ZHE3nSWRfseGYMkl1FGMn9bNA3sUtHeugPlDZ3Vlgnkg6sXSqeLg4qWiWPE3somwDFFg5HHwnk3XlSlLD5AuaxUbQT8KIDbpEggSHNzpUTqHP02G5cjT4jmOVcN1psbMv57Y6ymgoTJeUN6oDM1j3rhMNRyx3CbQXQufeuVFrxD6Xr2WQQxZp1Ur6krzGvMFMBL/0VZHhHb/xlSIgYGSEUAY1v1HpoJazxGEYQwyx5OGon91u9ZGglPfKngAS6HoEcdBWYeNc2SAhU4IAsIlJAoZMyAwn+6Cx7ryUuWV1cg5L73EemBsjpUbhkzto2UCN9DjpSq6uMwX2WW/2kDciWp48IQ6qhUDzTcOjFh2mzUxD1nXsyr1Ra7jcOlUUsm0UV27CMUChQnlGRIJeReWkzBVhswNfGnyQoA2SvYlOG2Z03PmKBwtRjhJOcT+JRNVmtlC7SlLWoy0NO0H1Z4yEWpN4WbQMugg1Qf9Lc1PvgOV3lr2oXrCze5DTI6GekPEhh2o6MiAsV7ZU03emN9MWXmFTlZ2YM12QsLZ0t5CMPbIaFcHtUXvB/9Q41g60H9iMKRixD5sJJhnfqIIGr4Axinr43tHLhpzigk0ShwrXA6WKMklUZheNMwpQYAVqRwimbzgRVfloJVEc7FNv0rCUb1xjSdw9bbe3yG4kgUtNCRrhcI/Ar0P8d204F0cA5GqFMtoMddZ06LuZGUpdGy2jiyaE7pGXfNE4MR4atFDIw7CwZ+s3eGwSTC05VAQRVjgYrgFjk5ydI8yCXVylohyGPBA0BqUOT4H5MSdlhZeYCx0f2KZTZUM6NUE7m1s2ZdP51Z02gkh5sZRk0MtgkZ3QpH8MJhAoUhlBMvaEw6Jkd05WSMmGbjsrsBtfWNU9EVkRUrBAf3IVK2k+KNACMsJmo2RqFmWgZsc9V6QKDwqBHb01ymrRoY2jv8459zWsMLKrHGgyCI4ddZEvUgJLB+IiPlRh2D0QMgXlJTGAt4OhZkNwVDfQUzdEWUgv5T2wwI0ZuKwRpOKUgcW2Vmk58aFZU3x4umVhdDUWSo2nXVJvyjLlCFyj6gb46+1Gh9x0NuxKZ3gmNw51V3EEsakFRwdVg5Rq0/QcpSQfjw8L3Jzszp0bVUzHXQettPuhD2tpOVx959dR/UiaObYw3AzOnjp4N6q0ka8g75gYICjVdlha4+TF0Oi3hgPLGzxzszL5pxmo/iiAcYcRfIJ46Ukol0oMHHKhhAuKiFVVbU0VTZM4qFkBSMfCu8jglx+5ACecNTqJJjraP32kRtiHT9t+DNLmHgACiWqWGwPjcUEblJerBknBaDXaH4ZqyrzFV/W8i6fiAaKdEptzl4uebwQTXs6AlqDsc1lDp2hWfY24IcU8cVu09RGsi0nMc47BIrNYRJQ54FNCq7AFctPVOLOYHCaFjsTuwXSxz9mOsBh4lByq05PmwhgYViNJG25KUq4NHZrsoJOne2TEP2M3k1i4YSOKRUpo2HlfI2nJkMXH57UP18YwV5DBpHOxokKgh4B3XnqAoOGAwHQocaP5rCnBXWyck3Y4jy5WGSQwZCadNWK1GctQ2li3EtyPuXUxrn4jWKUN64CDjqqykEtgxoAbUpC0GVzoWRR0/hkQkmkECTj8ULN1rlbLj0AZlKAOcQjUq8hZ2YXN8tcTOlVOoEz9NNAhCCBdlWbLnEr1XgmkFzhLy/FAw1hAe8iSviwtEvtuS4BUs2ESEw3SMYNCaTKDKOSt54feHuZaf8cOIsaHRIYS6gJbRILxatGTbMXj0BT+tuZJmydtWQ9R6O6avmCHer9D8HFo9XpkkPUoW5vDRvicvqgL/YEcadid3AtUyOyWKAZXcG5jM8DQEzicMoWhAFccDK90vYhjoh15WRCS1AxMLWQOwcZCkiZKOUewDzd0/B92C8TwbgnR0Ml4CHnb25gD8gTJy2LMgj5LRG6Pz0fS8G/M80QsvpUh18tKpeq4w61DHIHTDuk5+HAq2CK1DXPPzWelo1PeUDEjcpZlOq7RNTKw0gOZTimH8qkWkik8ZRbAGLwpX0qEVGdUg5VhH5cePAgX+iGKqikFwkjtoy5OT55Z1IkgZFdLmvqfzmverXe+nw7gOFWSLxeFKYdjENtjNZjOEKl0Fs5HjzbqugM2pRSZRRweHFlsfIXfFHpyGlEZvzuIN8+soRBpW0x3TC3caK+K1KLHqmoarHnuhBqTp/nYy8xUrNlqfBmKEV2Uduyspy5JEsdK9vwhPIZTGVfwNjPrMowFp1nclhzXfZDwzP5IHQpKaasQk1rv0RNYOYL7uMLiaq+JpbnRVJiObxfoadRB5jVf++bGTTweMGhMVOLZbjRwsea25hCMU/eE8OloJKJ/pUVu1EtQ552ZzyrSP9NN7uNSYUS40ECF++yG0p2GPSNcXObG0ZA65p5yXQLZwHdqnKEyxC88WRworn/kgQkJgSjoV53LPHMmHW/BMKc+oIdb+XmaRn7BUE2t04OOlnr/SnPew3jVQSegBRqdBPaNcZE780u7cXZHbZPZjc6TNI+qJKWJesOYL8ohyr0xgyc9wmCEkDIFBsuELR5l6OHZnSLTkvV3WIv1Y6i0LmmHNr5Om5RnNjonILTBcYK/uF/1oHTwypNOOJPkQT6K7hagwspHHlkW1S1NOgixM/J4oJQHLbcxJbqgCUYTxetJX4qLHZHilADWTi9DPstt7MrQ0B8ew46sw/UYmizZlOb79eQFIkcmDT2muradlgsHULOgPTBD5hE3gB+1wyzq58yi/9R45caWZu/qk/2Sk7txd7z4pq9vsp4jzeeU1ydGGNBRP9q8BFWTU6RzMDW1dd43VcOgdAvzI+rmUDbDoPlkUA8curSfCQwSOghZmJUYOWiw+z4KhK5HZhAlCGSIhiNezYLznmg2VG4a9ZIKh7No+ihc1QO6OyGToJg1BzCtIrL47bdS4hCUdKWrGgww+qKHDi2/R74e3PeHoQG5+GWXNseWRnRv3jv+4pnq86lGLbctjkNxGgY2f4CQiwa/WanFvp9sB/93nkw90X0Z/s8xqwHd/wGykMrSK7BCnwAAAYVpQ0NQSUNDIHByb2ZpbGUAAHicfZE9SMNAHMVfU6V+VBwsKOKQoTpZEBV11CoUoUKoFVp1MLn0C5o0JC0ujoJrwcGPxaqDi7OuDq6CIPgB4ubmpOgiJf4vKbSI8eC4H+/uPe7eAUKtyDSrbQzQ9LKZiEXFVHpVDLyiG/3owzQ6ZWYZc5IUh+f4uoePr3cRnuV97s/Ro2YsBvhE4llmmGXiDeKpzbLBeZ84xPKySnxOPGrSBYkfua64/MY557DAM0NmMjFPHCIWcy2stDDLmxrxJHFY1XTKF1Iuq5y3OGvFCmvck78wmNFXlrlOcwgxLGIJEkQoqKCAIsqI0KqTYiFB+1EP/6Djl8ilkKsARo4FlKBBdvzgf/C7Wys7Me4mBaNA+4ttfwwDgV2gXrXt72Pbrp8A/mfgSm/6SzVg5pP0alMLHwG928DFdVNT9oDLHWDgyZBN2ZH8NIVsFng/o29KA323QNea21tjH6cPQJK6it8AB4fASI6y1z3e3dHa279nGv39AJFjcrM+k3mmAAAPi2lUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4KPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNC40LjAtRXhpdjIiPgogPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgeG1sbnM6aXB0Y0V4dD0iaHR0cDovL2lwdGMub3JnL3N0ZC9JcHRjNHhtcEV4dC8yMDA4LTAyLTI5LyIKICAgIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIgogICAgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIKICAgIHhtbG5zOnBsdXM9Imh0dHA6Ly9ucy51c2VwbHVzLm9yZy9sZGYveG1wLzEuMC8iCiAgICB4bWxuczpHSU1QPSJodHRwOi8vd3d3LmdpbXAub3JnL3htcC8iCiAgICB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iCiAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyIKICAgIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIKICAgeG1wTU06RG9jdW1lbnRJRD0iZ2ltcDpkb2NpZDpnaW1wOjQzMzYzNWU2LTk3ZGQtNDI0Mi05YjliLTlhM2M3MTJlODQ1NSIKICAgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDozYTZmNTM3ZS1hNWRhLTQ1ZGQtYTEyMS1lMDdkMjBlNTQ4NGIiCiAgIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDo1M2QyZGVjNC00Njg2LTQyMjAtYmQxOC1iMGU4OTVkYTg1NzEiCiAgIEdJTVA6QVBJPSIyLjAiCiAgIEdJTVA6UGxhdGZvcm09IkxpbnV4IgogICBHSU1QOlRpbWVTdGFtcD0iMTYzNzY5NzQ5NzYyMjQ1MyIKICAgR0lNUDpWZXJzaW9uPSIyLjEwLjIyIgogICBkYzpGb3JtYXQ9ImltYWdlL3BuZyIKICAgdGlmZjpPcmllbnRhdGlvbj0iMSIKICAgeG1wOkNyZWF0b3JUb29sPSJHSU1QIDIuMTAiPgogICA8aXB0Y0V4dDpMb2NhdGlvbkNyZWF0ZWQ+CiAgICA8cmRmOkJhZy8+CiAgIDwvaXB0Y0V4dDpMb2NhdGlvbkNyZWF0ZWQ+CiAgIDxpcHRjRXh0OkxvY2F0aW9uU2hvd24+CiAgICA8cmRmOkJhZy8+CiAgIDwvaXB0Y0V4dDpMb2NhdGlvblNob3duPgogICA8aXB0Y0V4dDpBcnR3b3JrT3JPYmplY3Q+CiAgICA8cmRmOkJhZy8+CiAgIDwvaXB0Y0V4dDpBcnR3b3JrT3JPYmplY3Q+CiAgIDxpcHRjRXh0OlJlZ2lzdHJ5SWQ+CiAgICA8cmRmOkJhZy8+CiAgIDwvaXB0Y0V4dDpSZWdpc3RyeUlkPgogICA8eG1wTU06SGlzdG9yeT4KICAgIDxyZGY6U2VxPgogICAgIDxyZGY6bGkKICAgICAgc3RFdnQ6YWN0aW9uPSJzYXZlZCIKICAgICAgc3RFdnQ6Y2hhbmdlZD0iLyIKICAgICAgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDpjNzNiZWNiNS0wMDc5LTQ2ODUtYTI3Ni1jYTQ0MWQ4OThjMjAiCiAgICAgIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkdpbXAgMi4xMCAoTGludXgpIgogICAgICBzdEV2dDp3aGVuPSItMDM6MDAiLz4KICAgIDwvcmRmOlNlcT4KICAgPC94bXBNTTpIaXN0b3J5PgogICA8cGx1czpJbWFnZVN1cHBsaWVyPgogICAgPHJkZjpTZXEvPgogICA8L3BsdXM6SW1hZ2VTdXBwbGllcj4KICAgPHBsdXM6SW1hZ2VDcmVhdG9yPgogICAgPHJkZjpTZXEvPgogICA8L3BsdXM6SW1hZ2VDcmVhdG9yPgogICA8cGx1czpDb3B5cmlnaHRPd25lcj4KICAgIDxyZGY6U2VxLz4KICAgPC9wbHVzOkNvcHlyaWdodE93bmVyPgogICA8cGx1czpMaWNlbnNvcj4KICAgIDxyZGY6U2VxLz4KICAgPC9wbHVzOkxpY2Vuc29yPgogIDwvcmRmOkRlc2NyaXB0aW9uPgogPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgIAo8P3hwYWNrZXQgZW5kPSJ3Ij8+l9Xh7gAAAAZiS0dEAAAAAAAA+UO7fwAAAAlwSFlzAAAN1wAADdcBQiibeAAAAAd0SU1FB+ULFxM6EWE6nQQAAAAaSURBVFjD7cEBAQAAAIIg/69uSEABAAAA7wYQIAABl/dX1wAAAABJRU5ErkJggg=='

    layout = []
    for i in range(7):
        linha = []
        for j in range(7):
              if i==6 and j==3: linha.append(sg.Image(face_angry))
              else: linha.append(sg.Image(vazio))
        layout.append(linha)

    botoes = []
    for i in range(7):
        botoes.append(sg.Button(str(i), border_width=0, key=str(i)))
    layout.append(botoes)

    # Crio a janela
    window = sg.Window("Connect4", layout, margins=(60,40))

    # Aqui a gente cuida dos eventos
    while True:
        # aqui eu leio os eventos que talvez estejam ocorrendo
        evento, valores = window.read()
        # se você apertar o botão OK o programa finaliza
        if evento == sg.WIN_CLOSED:
            break
        else:
            coluna = int(evento)
            linha = primeiraLinhaLivre(coluna, mat)
            if linha < 0:
                print('Essa coluna está lotada. Tente outra.')
            else:
                mat[linha][coluna] = 'O'
                placar = funcaoAvaliacao(mat)
                layout[linha][coluna].update(face_cool)
                if placar > 0: print('Vantagem do COMPUTADOR')
                else: print('Vantagem do HUMANO')
                if placar <= -1000:
                    print('Parabéns, você ganhou!!')
                    sg.popup('Parabéns, você ganhou!!')
                    toqueAudio('applause.wav')
                    break
                # Jogada do computador
                coluna = minimax(mat, 4)    # grau de dificuldade 4
                linha = primeiraLinhaLivre(coluna, mat)
                if linha == -1:
                    print('Empate!!!!')
                    sg.popup('Empate!!!!')
                    break
                print('\nMinha jogada: COLUNA =', coluna, ', LINHA =', linha)
                mat[linha][coluna] = 'X'
                layout[linha][coluna].update(face_angry)
                placar = funcaoAvaliacao(mat)
                if placar > 0: print('Vantagem do COMPUTADOR')
                else: print('Vantagem do HUMANO')
                if placar >= 1000:
                    print('Patinho! Eu ganhei!!!!')
                    sg.popup('Patinho! Eu ganhei!!!!')
                    toqueAudio('applause.wav')
                    break

    #fecho a janela
    window.close()

main()
