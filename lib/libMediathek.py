# -*- coding: utf-8 -*-
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib
import sys
import HTMLParser

html_parser = HTMLParser.HTMLParser()

hideAudioDisa = True
icon = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path')+'/icon.png').decode('utf-8')
fanart = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path')+'/fanart.jpg').decode('utf-8')
translation = xbmcaddon.Addon(id='script.module.libMediathek').getLocalizedString


def addEntry(dict):	
	
	if 'type' in dict and dict['type'] == 'nextPage':
		dict['name'] = translation(31040)
	if isinstance(dict["name"], unicode):
		dict["name"] = dict["name"].encode('utf-8')
	dict["name"] = cleanString(dict["name"])
	#dict["name"] = dict["name"].replace('&amp;','&')
	if hideAudioDisa:
		if 'Hörfassung' in dict["name"] or 'Audiodeskription' in dict["name"]:
			return False
			
	u = _buildUri(dict)
	ok=True
	liz=xbmcgui.ListItem(cleanString(dict.get('name','')), iconImage="DefaultFolder.png", thumbnailImage=dict.get('thumb',icon))
	liz.setInfo( type="Video", infoLabels={ "Title": cleanString(dict.get('name','')) , "Plot": cleanString(dict.get('plot','')) , "Plotoutline": cleanString(dict.get('plot','')) , "Duration": dict.get('duration','') } )
	liz.setProperty('fanart_image',dict.get('fanart',dict.get('thumb',fanart)))
	xbmcplugin.setContent( handle=int( sys.argv[ 1 ] ), content="episodes" )
	if 'type' in dict and dict['type'] == 'video':
		liz.setProperty('IsPlayable', 'true')
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
	else:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
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
	

def cleanString(s):
  s = s.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&#034;", "\"").replace("&#039;", "'").replace("&quot;", "\"").replace("&szlig;", "ß").replace("&ndash;", "-")
  s = s.replace("&Auml;", "Ä").replace("&Uuml;", "Ü").replace("&Ouml;", "Ö").replace("&auml;", "ä").replace("&uuml;", "ü").replace("&ouml;", "ö").replace("&eacute;", "é").replace("&egrave;", "è")
  s = s.replace("&#x00c4;","Ä").replace("&#x00e4;","ä").replace("&#x00d6;","Ö").replace("&#x00f6;","ö").replace("&#x00dc;","Ü").replace("&#x00fc;","ü").replace("&#x00df;","ß")
  s = s.replace("&apos;","'").strip()
  return s

	
def pvrCheckStartTimeIsComparable(a,b):
	n = abs(a-b)
	if n <= 15:
		return True
	else:
		return False
def pvrCheckIfMovie(name):
	if name.startswith("Fernsehfilm Deutschland"):
		return True
	else:
		return False
def pvrCheckDurationIsComparable(a,b,maxDeviation = 10):
	deviation = abs((a * 100) / b - 100)
	if deviation <= maxDeviation:
		return True
	else:
		return False

def pvrCheckNameIsComparable(a,b):
	if a == b:
		return True
	else:
		return _wordRatio(a,b)
	
def _wordRatio(a,b,maxRatio=0.7):
	xbmc.log(a)
	xbmc.log(b)
	i = 0
	aSplit = a.split(" ")
	bSplit = b.split(" ")
	for word in aSplit:
		if word in bSplit:
			i += 1
	ratio = i / len(aSplit) 
	if ratio >= maxRatio:
		return True
	else: return False