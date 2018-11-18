import json
import os
import pprint
import numpy
import pandas as pd
import time
import seaborn as sns
import matplotlib.pyplot as plt

# read config for path data
with open('config.json', 'r') as f:
	data = json.load(f)
	RIPS_FOLDER = data['RIPS_FOLDER']
	CHARTS_FOLDER = data['CHARTS_FOLDER']

def flatten_json():
	all_files = os.listdir(RIPS_FOLDER)
	total_data = {}
	for jsonfilename in all_files:
		with open(os.path.join(RIPS_FOLDER,jsonfilename), 'r') as f:
			list_of_dicts = json.load(f)
			for i in list_of_dicts:
				post_id = i['post_id']

				if post_id in total_data.keys():
					oldscore = total_data[post_id]['score']

					if oldscore is not None:
						oldscore = int(oldscore)
						new_score = int(i['score'])
						if new_score > oldscore:
							total_data[post_id]['score'] = int(i['score'])

				else:
					copy = dict(i)
					del copy['post_id']
					copy['comments_url'] = copy['comments_url'].encode('utf-8')
					if copy['score'] is not None:
						copy['score']= int(copy['score'])
					total_data[post_id] = copy
	return total_data

# object for making charts and stuff
class visualize:
	def __init__(data):
		self.data = data

	# plots the frequency of subreddits in the data
	def bar_chart():
		# get counts of all the unique elements in dataframe
		uniques = self.data['subreddit'].value_counts()
		# filter out DF for values > 5
		uniques = uniques[uniques > 0]
		# uniques = pd.DataFrame({'subreddit':uniques.index,'count':uniques.values}) # dataframe that was going to be passed to seaborn but used series instead
		sns.set_style('darkgrid')
		xdim, ydim = 20, 10
		fig, ax = plt.subplots(figsize=(xdim,ydim))
		# could not FOR THE LIFE OF ME figure out how to use seaborn here
		ax.bar(uniques.index,uniques.values,width=1)
		plt.xticks(rotation=90)
		# plt.show()
		plt.savefig(os.path.join(CHARTS_FOLDER,'chart_x_%s_y%s_time_%s.png' % (xdim, ydim, str(time.time())[-7:-1])), bbox_inches='tight',dpi=200)


	# this function will plot reddit activity for all posts with dates
	# it will have to interpolate dates for older posts
	def line_chart():
		pass
		# im thinking of calculating # of days in a 10 day inerval and
		# taking standard deviations. its its more than half SD
		# then add one to the mean of the days
		# because it would mean that that day was an older posts

if __name__ == '__main__':
	data = flatten_json()
	data = pd.DataFrame(data).T

	v = visualize()
	v.bar_chart()
