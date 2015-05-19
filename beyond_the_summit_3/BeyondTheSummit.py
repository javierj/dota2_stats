

# Beyonf the Summit 3

import pandas as pd
import numpy as np
players = pd.read_csv("C:/code/workspaces/Python/dota2_stats/2661_players_data.csv", encoding='utf-8')
items = pd.read_csv("C:/code/workspaces/Python/dota2_stats/2661_items_data.csv", encoding='utf-8')
b_ps = pd.read_csv("C:/code/workspaces/Python/dota2_stats/2661_bans_and_picks_data.csv", encoding='utf-8')


## el jugador lleva una , en el nombre. Lo cmabio a mano, peor tendgo que modificar el parse
CParserError: Error tokenizing data. C error: Expected 20 fields in line 126, saw 21
1383610073,182325064,laopozuida,,Queen of Pain,Middle,Radiant,10,4,19,477,516,0,0.0,True,2221790,Vici Gaming Potential,1:02:52,2015-04-08T14:50:42+00:00,2661,The Summit 3

# pnc, la ardilla leprosa
1297648418,91539456,pnc, la ardi...,Ancient Apparition,Dire Jungle,Dire,1,3,2,34,212,0,0.0,False,1321909,Isurus Gaming HyperX,26:00,2015-03-06T03:02:07+00:00,2661,The Summit 3

#######################################

####################################
# Seleccionamos  los objetos inciiales de cada jugador
init_items = items[items['Time'].str.startswith("-")]
 
 # 7669 resultys
 
 Iron Branch               1573
Tango                     1414
Clarity                    750
Tango (Shared)             679
Boots of Speed             488
Healing Salve              447
Stout Shield               342
Observer Ward              322
Animal Courier             322
Ring of Protection         177
Sentry Ward                172
Wraith Band                144
Null Talisman              130
Town Portal Scroll         129
Magic Stick                118
Bottle                     105
Smoke of Deceit             97
Circlet                     56
Quelling Blade              48
Ring of Basilius            40
Poor Man's Shield           24
Orb of Venom                14
Mantle of Intelligence      12
Sage's Mask                 12
Ring of Regen               11
Slippers of Agility         10
Gauntlets of Strength        8
Dust of Appearance           8
Blades of Attack             6
Magic Wand                   3
Ring of Aquila               2
Gloves of Haste              2
Soul Ring                    2
Robe of the Magi             1
Bracer                       1

# 161 prtidso, 322 obsevee wards y 322 courriers
# Media d eiron branch por match:  1573/161 = 9.770186335403727

# Players distinsos: items['Player_id'].drop_duplicates() = 231

# Pero solo 172 Sentry Wards
# Ton de tangos: 161 x 2 x 5 = 1610 pero tengo 1573, la diferencia es
# 37, por lo que 37 jugadores de 1610 no compraron tangos.
# ¿Puedo saber los jugadore sy prtidos?
# ¿Pueso saber si alguien compró más d eun juegod e tangos d einicio?


############################################
# ¿Cuantos jugadores compraron más de un set de tangos al inicio?

tangos = init_items[init_items['Item']=="Tango"][['Match_id','Player_id','Item']]
tangos.groupby(['Match_id','Player_id']).count()
tmp = tangos.groupby(['Match_id','Player_id']).count().reset_index()
two_tangos = tmp[tmp['Item']>1]

# 41 jugadores compraron dos juegos de tangos.

two_tangos['Match_id'].drop_duplicates().count()

# En 35 partidos

############################################
# Media d etangos prestados por partido?



#######################################

###########
# Blink dagger más r´pida por partido

blinks = items[items['Item'] == "Blink Dagger"]
blinks.groupby(['Match_id']).min()


# Partidos sin blinkdagger
sin_id = blinks['Match_id'].drop_duplicates().tolist()
players[-players['Match_id'].isin(sin_id)]['Match_id'].drop_duplicates()
Out[16]: 
80      1385942777
250     1378748302
320     1374927532 -- Aquí hubo una blink
360     1373187082
860     1359955809
980     1355526089
1640    1471122762
1790    1482033310
1960    1476229078

# Esto no funciona bien
# eso es porque no tengo en items los objetos del match 1374927532
# y no los tengo porque dotabuff no tiene es ainformación y el mensaje de error de mi parser no para la ejecución.


# Blink dagger más rápida de todo el clasifixatorio
f_b = blinks.groupby(['Match_id']).min().reset_index()
f_b.min('Time')

f_b.sort('Time')

90   1362574521   44111721  Blink Dagger     06:18
2    1297648418   86726887  Blink Dagger     06:19
134  1378653789  123854991  Blink Dagger     06:40
32   1309618177    3940262  Blink Dagger     06:41
59   1353336855  110837826  Blink Dagger     06:51
101  1366467777   40209325  Blink Dagger     06:55

# La funcion min y max no funcionan bien con el campo time. Va a tocar convertirlos a fechas.
# Hay añgunos pocos datos que tienen el formato HH:MM:SS y la mayoría tiene el formato MM:SS
# Voy  ewscribir un función exclusiva de conversión.

def convert_time(s_time):
	import time
	format = "%M:%S" 
	if len(s_time.split(':')) > 2:
		format = "%H:%M:%S"
	return time.strptime(s_time, format) 

	# Funciona bien pero se visualiza d euna manera muy incómoda
# Tengo que mejorar la visualización

# Otra alternatoca

def convert_time(s_time):
	import time
	format = "2011.01.01 " 
	if len(s_time.split(':')) < 3 :
		format += "00:"
	return format + s_time 

	
# Con la segunda versión de la funciónd e conversión 
# funciona mucho mejor, pero sigue tratango los datos como cadenas

f_b['Datetime']=f_b['Time'].apply(convert_time)
f_b['Datetime'].min()

Out[6]: '2011.01.01 00:06:18'

f_b['Datetime']=f_b['Time'].apply(convert_time)
f_b['Datetime'].max()

Out[7]: '2011.01.01 01:28:20'

# Probemos con una tercera versión

def convert_time(s_time):
	import datetime
	time_ar = s_time.split(':') 
	if len(time_ar) < 3 :
		return datetime.datetime(2011, 1, 1, 0, int(time_ar[0]), int(time_ar[1]))
	return datetime.datetime(2011, 1, 1, int(time_ar[0]), int(time_ar[1]), int(time_ar[2]))
	
f_b['Datetime'].sum()
# No allow for this datatype

# Otra alternatoca

def convert_time(s_time):
	import time
	format = "2011.01.01 " 
	if len(s_time.split(':')) < 3 :
		format += "00:"
	return pd.Timestamp(format + s_time) 


f_b['Datetime']=f_b['Time'].apply(convert_time)
f_b['Datetime'].min()


Out[6]: Timestamp('2011-01-01 00:06:18')
# TypeError: reduction operation 'sum' not allowed for this dtype


# Vamos con los timedeltas

def convert_time(s_time):
	import datetime
	time_ar = s_time.split(':') 
	if len(time_ar) < 3 :
		return datetime.timedelta(hours=0, minutes=int(time_ar[0]), seconds=int(time_ar[1]))
	return datetime.timedelta(hours=int(time_ar[0]), minutes=int(time_ar[1]), seconds=int(time_ar[2]))

	
f_b['Timedelta']=f_b['Time'].apply(convert_time)
f_b['Timedelta'].min()

# Ahora sí que funciona la media
f_b['Timedelta'].mean()

f_b['Timedelta'].mean()
Out[11]: Timedelta('0 days 00:13:20.556962')


# ¿Cómo puedo calcular la media quitando todos los valores más altos?

# Pero no lo hacemos con f_b sino con blinks

b_tmp = blinks.copy()
b_tmp['Timedelta']=b_tmp['Time'].apply(convert_time)
f_b = b_tmp.groupby(['Match_id'])['Timedelta'].min().reset_index()

 f_b.sort('Timedelta')
Out[30]: 
       Match_id  Timedelta
90   1362574521   00:06:18
2    1297648418   00:06:19
134  1378653789   00:06:40
32   1309618177   00:06:41
59   1353336855   00:06:51
101  1366467777   00:06:55
58   1353149672   00:07:16
16   1303150892   00:07:28

# Y las que más tardaron

96   1364712133   00:23:44
177  1478468210   00:24:34
189  1481844063   00:25:54
40   1314082778   00:26:28
34   1311780934   00:27:29


# Y la media:
f_b.main()['Timedelta']

f_b.mean()['Timedelta']
Out[32]: Timedelta('0 days 00:12:27.161458')

####################################
# Analizar el lone druid de ee-sama
# ver la sveces que jugó dragon knight, dónde, contra quien y con qué reusltado.


dk = players[players['Hero'] == "Dragon Knight"]
dk['Position'].value_counts()

# Se ha jugado 4 veces y solo de mid.
# Ver las fechas
1641    2015-05-13T21:44:39+00:00
1662    2015-05-13T19:23:02+00:00
1671    2015-05-13T20:28:42+00:00
1731    2015-05-14T20:06:16+00:00
# Publicar algo sobre esto.


# Lista de ids de partidos
tmp = dk['Match_id'].tolist()

players[(players['Match_id'].isin(tmp)) and (players['Position'] == "Middle") and (players['Hero'] != "Dragon Knight")]

# ValueError: The truth value of a Series is ambiguous.

tmp1 = players[(players['Match_id'].isin(tmp))]
tmp2 = tmp1[tmp1['Position'] == "Middle"]
# Mejor cmabiar esta cond por que nos ea el team que jugó dk
tmp3 = tmp2[tmp2['Hero'] != "Dragon Knight"]

# Cada evz que ha jugado ha tenido enfrente a un heroe distinto, esta es la lista de heroes
# Por qué me salen 5 si solo ha jugado 4 veces ?
# Porque cuando lo jugó LGD, Zeus también lo tiene clasificado como mider 

 Hero      Team_name
Alchemist    Vici Gaming
1666  Queen of Pain  Evil Geniuses
1676   Ember Spirit  Evil Geniuses
1736         Kunkka    Not Today !

# Equipos que más reptiten gragon 

1641    Cloud9 G2A
1662    Cloud9 G2A
1671    Cloud9 G2A
1731    LGD-GAMING

# De las 4 partidas en que ha jugado DragonNight hasta ahora, 3 han sido de cloud9 y la restante, de LGD

# En sus 4 partidas en BeyondTheSummit, Dragon Knight siempre ha jugado mid y siempre ha tenido enrente a un heroe distinto.

# Los 4 heroes que se han enfrentado a Dragon Knight en sus 4 partidas son: Alchemist (Vici Gaming), Queen of Pain y Ember Spirit(EG) y Kunkka(NoT)

# Doubt is in the air. DK faced against: Alchemist (Vici Gaming), Queen of Pain y Ember Spirit(EG) y Kunkka(NoT)