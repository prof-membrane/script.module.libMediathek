# -*- coding: utf-8 -*-
import urllib
import urllib2
import socket
import sys
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs
import re

from libMediathekUtils import clearString
#from libMediathek import get_params

icon = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path')+'/icon.png').decode('utf-8')
fanart = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path')+'/fanart.jpg').decode('utf-8')
translation = xbmcaddon.Addon(id='script.module.libMediathek').getLocalizedString


def addEntry(dict):	
	for key in dict:#sigh
		if isinstance(dict[key], unicode):
			dict[key] = dict[key].encode('utf-8')
	#xbmc.log(str(dict))
	if 'type' in dict and dict['type'] == 'nextPage':
		dict['name'] = translation(31040)
	if isinstance(dict["name"], unicode):
		dict["name"] = dict["name"].encode('utf-8')
	dict["name"] = clearString(dict["name"])
	if 'type' in dict and dict['type'] == 'date' and 'time' in dict:
		dict["name"] = '(' + dict["time"] + ') ' + dict["name"]
	#dict["name"] = '(' + dict["time"] + ') ' + dict["name"]
	#dict["name"] = dict["name"].replace('&amp;','&')
	#if hideAudioDisa:
	#	if 'Hörfassung' in dict["name"] or 'Audiodeskription' in dict["name"]:
	#		return False
			
	u = _buildUri(dict)
	ilabels = {
		"Title": clearString(dict.get('name','')),
		"Plot": clearString(dict.get('plot','')),
		"Plotoutline": clearString(dict.get('plot','')),
		"Duration": dict.get('duration',''),
		"Mpaa": dict.get('mpaa','')
		}
	ok=True
	liz=xbmcgui.ListItem(clearString(dict.get('name','')), iconImage="DefaultFolder.png", thumbnailImage=dict.get('thumb',icon))
	#liz.setInfo( type="Video", infoLabels={ "Title": clearString(dict.get('name','')) , "Plot": clearString(dict.get('plot','')) , "Plotoutline": clearString(dict.get('plot','')) , "Duration": dict.get('duration','') } )
	liz.setInfo( type="Video", infoLabels=ilabels)
	liz.setProperty('fanart_image',dict.get('fanart',dict.get('thumb',fanart)))
	xbmcplugin.setContent( handle=int( sys.argv[ 1 ] ), content="episodes" )
	if 'type' in dict and (dict['type'] == 'video' or dict['type'] == 'date'):
		liz.setProperty('IsPlayable', 'true')
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
	elif 'type' in dict and dict['type'] == 'nextPage':
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	else:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
		
	return ok
	
def addEntries(l,page=False):#TODO remove page
	lists = []
	ok = False
	for dict in l:
		for key in dict:#sigh
			if isinstance(dict[key], unicode):
				dict[key] = dict[key].encode('utf-8')
		#xbmc.log(str(dict))
		if 'type' in dict and dict['type'] == 'nextPage':
			dict['name'] = translation(31040)
			dict['mode'] = get_params()['mode']
		if isinstance(dict["name"], unicode):
			dict["name"] = dict["name"].encode('utf-8')
		dict["name"] = clearString(dict["name"])
		if 'type' in dict and dict['type'] == 'date' and 'airedtime' in dict:
			dict["name"] = '(' + str(dict["airedtime"]) + ') ' + dict["name"]
		elif 'type' in dict and dict['type'] == 'date' and 'time' in dict:
			dict["name"] = '(' + str(dict["date"]) + ') ' + dict["name"]
		#dict["name"] = dict["name"].replace('&amp;','&')
		#if hideAudioDisa:
		#	if 'Hörfassung' in dict["name"] or 'Audiodeskription' in dict["name"]:
		#		return False
				
		u = _buildUri(dict)
		ilabels = {
			"Title": clearString(dict.get('name','')),
			"Plot": clearString(dict.get('plot','')),
			"Plotoutline": clearString(dict.get('plot','')),
			"Duration": dict.get('duration',''),
			"Mpaa": dict.get('mpaa',''),
			"Aired": dict.get('aired',''),
			"Studio": dict.get('channel',''),
			}
		if 'episode' in dict: 
			ilabels['Episode'] = dict['episode']
		if 'Season' in dict: 
			ilabels['Season'] = dict['season']
		if 'tvshowtitle' in dict: 
			ilabels['tvshowtitle'] = dict['tvshowtitle']
			ilabels['tagline'] = dict['tvshowtitle']
			ilabels['album'] = dict['tvshowtitle']
		ok=True
		#liz=xbmcgui.ListItem(clearString(dict.get('name','')), iconImage="DefaultFolder.png", thumbnailImage=dict.get('thumb',icon))
		liz=xbmcgui.ListItem(clearString(dict.get('name','')))
		#liz.setInfo( type="Video", infoLabels={ "Title": clearString(dict.get('name','')) , "Plot": clearString(dict.get('plot','')) , "Plotoutline": clearString(dict.get('plot','')) , "Duration": dict.get('duration','') } )
		liz.setInfo( type="Video", infoLabels=ilabels)
		#if 'hasSubtitle' in dict:
		liz.addStreamInfo('subtitle', {'language': 'deu'})
		#if True:
			#liz.addStreamInfo('subtitle',{'language':'de'})
		#liz.setProperty('fanart_image',dict.get('fanart',dict.get('thumb',fanart)))
		#try:
		art = {}
		art['thumb'] = dict.get('thumb')
		art['landscape'] = dict.get('thumb')
		#art['poster'] = dict.get('thumb')
		art['fanart'] = dict.get('fanart',dict.get('thumb',fanart))
		art['icon'] = dict.get('channelLogo','')
		#art.append({'landscape': dict.get('thumb')})
		#art.append({'fanart': dict.get('fanart',dict.get('thumb',fanart))})
		#xbmc.log(str(art))
		liz.setArt(art)
		#except: pass
		if 'type' in dict:
			if dict.get('type',None) == 'video' or dict.get('type',None) == 'live' or dict.get('type',None) == 'date':
				xbmcplugin.setContent( handle=int( sys.argv[ 1 ] ), content="episodes" )
				liz.setProperty('IsPlayable', 'true')
				lists.append([u,liz,False])
			elif 'type' in dict and dict['type'] == 'nextPage':
				#lists.append([u,liz,True])
				lists.append([u,liz,True])
			elif dict['type'] == 'shows':
				#xbmcplugin.setContent( handle=int( sys.argv[ 1 ] ), content="episodes" )
				xbmcplugin.setContent( handle=int( sys.argv[ 1 ] ), content="tvshows" )
				lists.append([u,liz,True])
			else:
				xbmcplugin.setContent( handle=int( sys.argv[ 1 ] ), content="files" )
				lists.append([u,liz,True])
		else:
			#xbmcplugin.setContent( handle=int( sys.argv[ 1 ] ), content="files" )
			lists.append([u,liz,True])
	xbmcplugin.addDirectoryItems(int(sys.argv[1]), lists)
	#xbmcplugin.setContent( handle=int( sys.argv[ 1 ] ), content="episodes" )		
	return ok

def _buildUri(dict):
	u = dict.get('pluginpath',sys.argv[0])+'?'
	i = 0
	for key in dict.keys():
		if i > 0:
			u += '&'
		if isinstance(dict[key], basestring):
			dict[key] = dict[key]#.encode('utf8')
		else:
			dict[key] = str(dict[key])
		u += key + '=' + urllib.quote_plus(dict[key])
		i += 1
	return u
	

	
def get_params():
	param={}
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]= urllib.unquote_plus(splitparams[1])

	return param