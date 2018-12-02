from selenium import webdriver
import os, time, pprint, json
from selenium.webdriver.common.keys import Keys
import datetime
import json

class reddit():
	def __init__(self,username, password, driver):
		self.username = username
		self.password = password
		self.login()
		self.post_dict = []

	def find_links(self):
		# xpath to all links that are stored in posts
		new = '//div[@class="content"]//div[@id="siteTable"]//div[@class][@id][@onclick]'
		elem = driver.find_elements_by_xpath(new)

		for e in elem:
			link = e.get_attribute('data-url')
			author = e.get_attribute('data-author')
			score = e.get_attribute('data-score')
			subreddit = e.get_attribute('data-subreddit')
			comments_url = e.get_attribute('data-permalink')
			comments_count = e.get_attribute('data-comments-count')
			post_id = e.get_attribute('id')[-6:]

			data = {'link':link, 'author':author, 'score':score, 'subreddit':subreddit,
				   'comments_url':comments_url, 'comments_count':comments_count, 'post_id':post_id}
			self.post_dict.append(data)


		return len(self.post_dict)

	def next_page(self):
		#path_to_button = '//span[@class="nextprev"]//span[@class="next-button//a"]' #//a[1]
		newpath = '//span[@class="nextprev"]//span[@class="next-button"]//a[1]'
		button = driver.find_element_by_xpath(newpath)

		#button = driver.find_element_by_class_name('next-button')
		button.click()

	def login(self):
		elem = driver.find_element_by_id('user_login')
		elem.send_keys(username)
		elem = driver.find_element_by_id('passwd_login')
		elem.send_keys(password)
		#elem = driver.find_elements_by_tag_name('button')
		elem.send_keys(Keys.RETURN)
		print('login attempt was made')

if __name__ == '__main__':
	s = time.time()
	chromedriver = "D:\Python\chromedriver"
	os.environ["webdriver.chrome.driver"] = chromedriver
	driver = webdriver.Chrome(chromedriver)
	driver.get('https://old.reddit.com/login?dest=https%3A%2F%2Fold.reddit.com%2Fuser%2Fme%2Fsaved')

	with open(r'D:\Python\reddit\saved post ripper\config.json', 'r') as f:
		data = json.load(f)
		username = data['username']
		password = data['password']


	time.sleep(2)
	usr = reddit(username,password, driver)
	usr.find_links()
	time.sleep(2)
	usr.next_page()
	time.sleep(2)
	increasing = True

	while increasing:
		prev_len = len(usr.post_dict)
		new_len = usr.find_links()
		print('increasing: %s' %(prev_len))

		try:
			usr.next_page()
			time.sleep(2)
		except Exception:
			break

	for i in usr.post_dict:
		pprint.pprint(i)
		print('\n\n')

	date = datetime.datetime.now().strftime('%B_%d_%Y.%H-%M-%S') + '.json'
	file_location = os.path.join(r'D:\Python\reddit\saved post ripper\rips', date)
	print(file_location)


	with open(file_location, 'w') as outfile:
		json.dump(usr.post_dict, outfile)
		print('file was saved')

	f = time.time()
	print('finished %s' % (f-s))
