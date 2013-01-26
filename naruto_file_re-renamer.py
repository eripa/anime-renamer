#!/usr/bin/env python
#

import sys
import os
import re
import shutil

match_pattern = 'naruto'
match_extensions = 'mkv$|mp4$'
filler_episodes = [[144,151],
				   [170,171],
				   [176,196],
				   [222,242],
				   [257,260],
				   [271,271],
				   [279,281],
				   [284,289],
				   [290,295]]
to_dir = os.path.join('/Volumes', 'Rukia', 'Anime', 'Naruto Shippuuden')

seasons = [0,
			32, #season 1
			21, #season 2
			18, #season 3
			17, #season 4
			24, #season 5
			31, #season 6
			8,  #season 7
			24, #season 8
			21, #season 9
			22, #season 10
			24, #season 11
			18, #season 12
			38 #season 13
			]

# KNOWN episode 220 maps to s11 e02

class AnimeEpisode():
	"""docstring for AnimeEpisode"""
	def __init__(self, file):
		self.filename = os.path.basename(file)
		self.location = os.path.dirname(file)
		self.filename_list = self.splitName(self.filename)
		self.show_name = self.getShowName()
		self.episode = self.getEpisodeNumber()
		self.getRest()
		self.new_name = str(self)

	def splitName(self, filename):
		if '_' in filename:
			split_name = filename.split('_')
		else:
			split_name = filename.split()
		return split_name
	
	def getShowName(self):
		return self.filename_list[0].capitalize() + ' ' + self.filename_list[1].capitalize().replace('Shippuden', 'Shippuuden')

	def getEpisodeNumber(self):
		if self.filename_list[2] == '220':
			return '%s %s' % ('s11e02', self.filename_list[2])
		else:
			return self.filename_list[2]

	def getRest(self):
		last_without_extension = [self.filename_list[-1].split('.')[0]]
		self.extension = self.filename_list[-1].split('.')[1]
		l = self.filename_list[4:-1] + last_without_extension
		if len(l) is 2:
			self.format = l[0]
			self.group = l[1]
			self.hash = None
			self.other = None
			self.filler = False
		elif len(l) is 3:
			self.format = l[0]
			self.group = l[1]
			self.hash = l[2]
			self.other = None
			self.filler = False
		elif len(l) is 4:
			self.format = l[0]
			self.group = l[1]
			self.hash = l[2]
			self.other = None
			self.filler = True
		else:
			self.format = None
			self.hash = None
			self.other = None
			self.group = None
			self.filler = None

	# def isFiller(self):
	# 	if '-' in self.episode:
	# 		episode = self.episode.split('-')[0]
	# 	else:
	# 		episode = self.episode
	# 	fillers = []
	# 	for entry in filler_episodes:
	# 		fillers += range(entry[0], entry[1]+1)
	# 	fillers = [str(x) for x in fillers]
	# 	return episode in fillers

	def __str__(self):
		ret_list = [self.show_name, self.episode]
		ret_list += [self.format, self.group]
		if self.hash:
			ret_list.append(self.hash)
		if self.filler:
			ret_list.append('Filler')
		ret_list.append(self.extension)
		ret_string = ' '.join(ret_list[:2]) + ' - ' + ' '.join(ret_list[2:-1])
		return ret_string + '.' + ret_list[-1]

def getFiles(directories):
	for dir in directories:
		dir =  os.path.abspath(dir)
		for root, dirs, files in os.walk(dir):
			for filename in [os.path.abspath(os.path.join(root, filename)) for filename in files if re.search(match_pattern, filename, flags=re.IGNORECASE) and re.search(match_extensions, filename, flags=re.IGNORECASE)]:
				yield filename

def main():
	if not os.path.isdir(to_dir):
		os.makedirs(to_dir)
	file_names = [(AnimeEpisode(file)) for file in getFiles(sys.argv[1:])]

	new_names = []
	for episode in file_names:
		print episode.new_name
		#shutil.move(os.path.join(episode.location, episode.filename), os.path.join(to_dir, episode.new_name))
		

if __name__ == '__main__':
	main()
