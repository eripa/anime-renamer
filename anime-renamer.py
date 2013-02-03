#!/usr/bin/env python
#

import sys
import os
import re
import shutil
import tvdb_api
import ConfigParser

class AnimeEpisode():
	"""docstring for AnimeEpisode"""
	def __init__(self, file, tvdb, config):
		self.config = config
		self.filename = os.path.basename(file)
		self.location = os.path.dirname(file)
		self.filename_list = self.splitName(self.filename)
		self.group = self.getGroup()
		self.show_name = self.getShowName()
		self.episode = self.getEpisodeNumber()
		self.tvdb_metadata = tvdb[self.show_name]
		self.season_episode_name = self.generateSeasonEpisodeName()
		self.filler = self.isFiller()
		self.getRest()
		self.output_dir = self.getOutputDir()
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
		return self.filename_list[1].capitalize() + ' ' + self.filename_list[2].capitalize()

	def getEpisodeNumber(self):
		if self.filename_list[3] == '-':
			episode = self.filename_list[4]
		else:
			episode = self.filename_list[3]
		if 'v' in episode:
			return episode.split('v')[0]
		else:
			return episode

	def getOutputDir(self):
		if self.config.has_section(self.show_name.lower()):
			if self.config.has_option(self.show_name.lower(), 'output_dir'):
				return self.config.get(self.show_name.lower(), 'output_dir')
			else:
				return ""
		else:
			return ""

	def generateSeasonEpisodeName(self):
		if "-" in self.episode:
			lookup = self.episode.split('-')[0]
		else:
			lookup = self.episode
		seasons = [len(self.tvdb_metadata[x]) for x in self.tvdb_metadata.keys()]
		episode_dict, season_dict = self.genEpisodeAndSeasonDictionaries(seasons)
		try:
			episode = episode_dict[lookup]
		except KeyError as e:
			sys.exit('Episode (%s) seem to be too new, could not be found in episode dictionary, please update the script..' % lookup)
		episode_number = episode[episode.keys()[0]]
		if "-" in self.episode:
			double_episode_number = int(episode_number.split('E')[1])+1
			episode_number = "%sE%02d" % (episode_number, double_episode_number)
		return episode_number

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
		if self.config.has_section(self.show_name.lower()):
			if self.config.has_option(self.show_name.lower(), 'filler_episodes'):
				filler_episodes = [x.split('-') for x in self.config.get(self.show_name.lower(), 'filler_episodes').split(',')]
				for entry in filler_episodes:
					if len(entry) == 2:
						# a range
						fillers += range(int(entry[0]), int(entry[1])+1)
					else:
						# a single episode
						fillers += range(int(entry[0]), int(entry[0])+1)
				fillers = [str(x) for x in fillers]
		print fillers
		return episode in fillers

	def genEpisodeAndSeasonDictionaries(self, seasons):
		# skip index 0 as it contains only special episodes
		episodes = [x for x in xrange(1,sum(seasons[1:])+1)]
		season_dict = {}
		episode_dict = {}

		incr = 1
		episode_counter = episodes[0]
		while len(episodes) != 0:
			try:
				if len(season_dict[incr]): pass
			except:
				season_dict[incr] = []
			season_dict[incr].append(episode_counter)
			episode_dict[str(episodes[0])] = {incr: genEpisodeName(incr, episode_counter)}
			episodes.pop(0)
			if len(season_dict[incr]) == seasons[incr]:
			 	incr += 1
			 	episode_counter = 1
			else:
				episode_counter += 1
		return episode_dict, season_dict

	def __str__(self):
		ret_list = [self.show_name, self.season_episode_name, self.episode]
		ret_list += [self.format, self.group]
		if self.hash:
			ret_list.append(self.hash)
		if self.filler:
			ret_list.append('Filler')
		ret_list.append(self.extension)
		ret_string = ' '.join(ret_list[:2]) + ' - ' + ' '.join(ret_list[2:-1])
		return ret_string + '.' + ret_list[-1]

def getFiles(directories, config):
	extension_pattern = "|".join([ext+'$' for ext in config.get('global', 'file_extensions').split(',')])
	show_pattern = ".*("+"|".join([show.replace(' ', '.') for show in config.get('global', 'shows').split(',')]) + ").*"
	for dir in directories:
		dir =  os.path.abspath(dir)
		for root, dirs, files in os.walk(dir):
			for filename in [os.path.abspath(os.path.join(root, filename)) for filename in files if re.search(show_pattern, filename, flags=re.IGNORECASE) and re.search(extension_pattern, filename, flags=re.IGNORECASE)]:
				yield filename

def genEpisodeName(season, episode):
	return "S%02dE%02d" % (season, episode)

def main():
	if '--real' in sys.argv:
		real = True
		sys.argv.remove('--real')
	else:
		real = False

	config = ConfigParser.RawConfigParser()
	config.read('shows.cfg')



	tvdb = tvdb_api.Tvdb()
	file_names = [(AnimeEpisode(file=file, tvdb=tvdb, config=config)) for file in getFiles(sys.argv[1:], config=config)]

	for episode in file_names:
		to_dir = os.path.join(config.get('global', 'output_root'), episode.output_dir)
		if not os.path.isdir(to_dir):
			try:
				print 'Destination doesn\'t exist, try to create it..'
				os.makedirs(to_dir)
			except OSError as e:
				sys.exit(e)
		if real:
			print episode.filename, "->", episode.new_name, "->", to_dir
			shutil.move(os.path.join(episode.location, episode.filename), os.path.join(to_dir, episode.new_name))
		else:
			print episode.filename, "->", episode.new_name, "->", to_dir

if __name__ == '__main__':
	main()
