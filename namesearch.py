from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import sys

def parsing_single_words():
	"""
		parsing all single words set to be tested
	"""
	f = open("single_word_base.txt", "r")
	single_name = []
	for buf in f:
		buf2 = buf.replace("\n","").split(",")

		for i in range(len(buf2)):
			if buf2[i] not in single_name:
				single_name.append(buf2[i])
	#print(len(single_name))
	return single_name

def count_name_score(family_name):
	"""
		透過family_name + words base 來計算名字的分數
		目前沒有support 單名
		找出的名字要符合總格大吉昌, 以及五格都是吉
	"""
	single_name = parsing_single_words()
	driver = webdriver.Chrome(ChromeDriverManager().install())

	report = open("save_score.txt", "w")
	report.close()

	#測試所有組合
	for i in range(len(single_name)):
		for j in range(len(single_name)):			
			if i != j:				
				driver.get("https://naming123.doitwell.tw/?lastname=" + family_name + "&middlename=" + single_name[i] + "&firstname=" + single_name[j]) #前往這個網址
				time.sleep(1.5)

				htmltext = driver.page_source
				nonBreakSpace = u'\xa0'
				htmltext = htmltext.replace(nonBreakSpace, ' ').replace("\n","")
				mybs = BeautifulSoup(htmltext, 'html.parser')

				five_comment = mybs.find_all("div", class_="span6")
				final_comment = mybs.find_all("div", class_="span1")
				final_condition = False
				for tag in final_comment:
					#print(tag.text)
					if "大吉昌" in tag.text:
						final_condition = True
						break
				#print(final_condition)
				if final_condition == False:
					continue
				
				badscore = 0
				tags = ""
				for tag in five_comment:
					score = tag.find_all("div", class_="forfive")		
					tags = tag.text + ","		
					for s in score:
						if "凶" in s.text:
							badscore = badscore + 1

				if badscore == 0:
					report = open("save_score.txt", "a")
					report.write(str(i)+","+str(j)+","+single_name[i]+single_name[j]+","+tags+"\n")
					report.close()
	driver.close()#關閉瀏覽器

if __name__ == "__main__":
	count_name_score(sys.argv[1])
