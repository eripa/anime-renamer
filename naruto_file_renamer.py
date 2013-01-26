#!/usr/bin/env python
#

import sys
import os
import re

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

class AnimeEpisode():
	"""docstring for AnimeEpisode"""
	def __init__(self, file):
		self.filename = os.path.basename(file)
		self.location = os.path.dirname(file)
		self.filename_list = self.splitName(self.filename)
		self.group = self.getGroup()
		self.show_name = self.getShowName()
		self.episode = self.getEpisodeNumber()
		self.filler = self.isFiller()
		self.getRest()
		self.new_name = str(self)

	def splitName(self, filename):
		if '_' in filename:
			split_name = filename.split('_')
		else:
			split_name = filename.split()
		return split_name
	
	def getGroup(self):
		return self.filename_list[0].translate(None, "[]")
	
	def getShowName(self):
		return self.filename_list[1].capitalize() + ' ' + self.filename_list[2].capitalize().replace('Shippuden', 'Shippuuden')

	def getEpisodeNumber(self):
		if self.filename_list[3] == '-':
			episode = self.filename_list[4]
		else:
			episode = self.filename_list[3]
		if 'v' in episode:
			return episode.split('v')[0]
		else:
			return episode

	def getRest(self):
		if self.filename_list[3] == '-':
			without_extension = self.filename_list[5].split('.')[0]
			self.extension = self.filename_list[5].split('.')[1]
		else:
			without_extension = self.filename_list[4].split('.')[0]
			self.extension = self.filename_list[4].split('.')[1]
		l = without_extension.translate(None, '[').split(']')[:-1]
		if len(l) is 1:
			self.format = l[0]
			self.hash = None
			self.other = None
		elif len(l) is 2:
			self.format = l[0]
			self.hash = l[1]
			self.other = None
		elif len(l) is 3:
			self.format = l[1]
			self.hash = l[2]
			self.other = l[0]
		else:
			self.format = None
			self.hash = None
			self.other = None
		if 'x' in self.format:
			self.format = self.format.split('x')[1] + "p"

	def isFiller(self):
		if '-' in self.episode:
			episode = self.episode.split('-')[0]
		else:
			episode = self.episode
		fillers = []
		for entry in filler_episodes:
			fillers += range(entry[0], entry[1]+1)
		fillers = [str(x) for x in fillers]
		return episode in fillers

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
		#print os.path.join(episode.location, episode.filename), os.path.join(to_dir, episode.new_name)

		

if __name__ == '__main__':
	main()