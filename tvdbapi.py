#!/usr/bin/python

import sys
import urllib
import urllib2
from xml.etree import ElementTree
from xml import etree
import zipfile
import os
from collections import Counter

def fetchSeasonsFromTheTVDB(tvdb_API_key, seriesname, language, verbose=False):
	api_url = 'http://www.thetvdb.com/api'
	get_series = api_url + '/GetSeries.php?seriesname=' + seriesname + '&language=' + language

	if verbose: print 'Looking up series detail for %s on TheTVDB.com (url: %s)' % (seriesname, get_series)
	requestURL = get_series
	root = ElementTree.parse(urllib.urlopen(requestURL)).getroot()

	series = root.findall('Series')
	for serie in series:
	    series_id = serie.find('seriesid').text

	try:
		series_id
	except NameError:
		sys.exit('nothing found for %s with language %s' % (seriesname, language))

	get_series_archive = api_url + '/' + tvdb_API_key + '/series/' + series_id + '/all/' + language + '.zip'

	if verbose: print 'Getting XML data.. (url: %s)' % (get_series_archive)

	f = urllib2.urlopen(get_series_archive)
	local_file = seriesname+' '+language+' xml.zip'
	with open(local_file, "wb") as tmp:
		tmp.write(f.read())

	zf = zipfile.ZipFile(local_file)

	for name in zf.namelist():
		if name == 'en.xml': 
			data = zf.read(name)
			root = ElementTree.fromstring(data)

	os.unlink(local_file)
	seasons = []
	seasons_tmp = []
	episodes = root.findall('Episode')
	for ep in episodes:
		seasons_tmp.append(ep.find('SeasonNumber').text)

	seasons_dict = Counter(seasons_tmp)
	for i in sorted([int(x) for x in seasons_dict.keys()]):
		seasons.append(seasons_dict[str(i)])

	if verbose: print seasons
	return seasons

