#!/usr/bin/python

from selenium.webdriver.chrome.options import Options
from xml.sax.saxutils import unescape
from selenium import webdriver
from shutil import copyfile
from time import sleep

import urllib.parse
import requests
import getopt
import html
import sys
import re
import os


def subsAvailable():
  source = requests.get('https://translate.google.com/').text
  subs = re.findall('data:\[\[\[(.*?)\]\]\]', source)[1]
  subs = re.sub('","', ' -> ', subs)
  subs = re.sub('["\[\]"]', '', subs)
  subs = re.sub(',', ', ', subs)
  subs = 'auto -> auto, ' + subs
  codes = re.findall(',\s(.*?)\s->', ', '+subs)
  return subs, codes

def isCode(i):
  if i in subsAvailable()[1]:
    return True
  return False

def options(argv):
  codeIn = 'auto'
  codeOut = 'es'
  backup = False

  try:
    opts, args = getopt.getopt(argv,"bhci:o:")
  except getopt.GetoptError:
    print('usage: subtitle.py -i <code> -o <code>')
    sys.exit(2)

  for opt, arg in opts:
    if opt == '-h':
      print('usage: subtitle.py -i <code> -o <code>')
      print('example: subtitle.py -i en -o es')
      print('\noptional arguments:')
      print('-c   Shows the languages supported by Google Translator')
      print('-i   input language code, default is auto')
      print('-o   output language code, default is es')
      print('-b   create a backup of the file')
      sys.exit(2)
    elif opt == "-c":
      print('Subtitles Available (code -> language):\n')
      print(subsAvailable()[0])
      sys.exit(2)
    elif opt in ("-i"):
      if isCode(arg):
        codeIn = arg
      else:
        print('Is not code ->', arg)
        print('usage: subtitle.py -c')
        print('Shows the languages supported by Google Translator')
    elif opt in ("-o"):
      if isCode(arg):
        if arg == 'auto':
          print('auto can\'t be output code')
          sys.exit(2)
        codeOut = arg
      else:
        print('Is not code ->', arg)
        print('usage: subtitle.py -c')
        print('Shows the languages supported by Google Translator')
    elif opt in ("-b"):
      backup = True

  return codeIn, codeOut, backup

def getSrt():
  files = []

  for f in os.listdir():
    if os.path.isfile(f):
      if os.path.splitext(f)[1].lower() == '.srt':
        files.append(f)

  return files

def copyF(fr):
  filename, ext = os.path.splitext(fr)
  copyfile(filename+ext, filename+'-backup'+ext)

def openBrowser():
  options = webdriver.ChromeOptions()
  options.add_experimental_option('excludeSwitches', ['enable-logging'])
  options.add_argument("--headless")  

  return webdriver.Chrome(executable_path=r"driver\chromedriver.exe", options=options)

def goToBrowser(s, i, o, driver):
  driver.get("https://translate.google.com/?sl="+i+"&tl="+o+"&text="+s+"&op=translate")

def pageLoading(driver):
  while 'data-original-language' not in driver.page_source:
    sleep(0.5)

def getSource(driver):
  return driver.page_source

def searchTranslate(source):
  return re.findall('data-language-name.*?data-text="([\s\S]+?)" data-crosslingual-hint=', source)[1]

def addTwoLines(fr):
  f = open(fr, 'r')
  lines = f.readlines()
  f.close()

  if lines[-1].strip() != '' and lines[-2].strip() != '':
    f = open(fr, 'a')
    f.write('\n\n')
    f.close()

def format(fr):
  content = []
  st = ''
  newLine = '\n'
  ing = 0

  addTwoLines(fr)

  f = open(fr, 'r')
  for l in f:
    if(re.search('^\d+$', l.splitlines()[0])):
      content.append(l.splitlines()[0])
      continue
    if(re.search('\d+:\d+:\d+,\d+', l.splitlines()[0])):
      content.append(l.splitlines()[0])
      continue
    if(l.splitlines()[0].strip() == ''):
      content.append(st)
      if(st.strip() != ''):
        content.append('')
      st = ''
      ing = 0
      continue
    if(ing > 0):
      st += newLine
    st += l.splitlines()[0]
    ing += 1
  f.close()

  return content

def getS5000(content):
  stringSend = ''
  segments = []

  for e in range(len(content)):
    if content[-1].strip() == '':
      content.pop()
    else:
      break

  for i in range(len(content)):
    if i % 2 == 0 and not content[i].isdigit():
      if(len(stringSend) + len(content[i]) < 5000):
        stringSend += content[i] + '\n\n'
        if i == len(content) - 1:
          segments.append(stringSend[:-2])
      else:
        segments.append(stringSend)
        stringSend = content[i] + '\n\n'

  return segments

def translate(segments, i, o):
  response = []

  driver = openBrowser()

  for k in range(len(segments)):
    goToBrowser(urllib.parse.quote(segments[k]), i, o, driver)
    pageLoading(driver)
    source = getSource(driver)
    res = searchTranslate(source)
    response += res.split('\n\n')
    percentage = (k+1) / len(segments)
    time_msg = "\rProgress: {0:.2%} ".format(percentage)
    sys.stdout.write(time_msg)
    sys.stdout.flush()
  print()

  closeDrive(driver)

  return response

def toFile(content, response, fr, cout):
  stringEnd = ''
  ind = 0

  for i in range(len(content)):
    if i % 2 == 0 and not content[i].isdigit():
      content[i] = response[ind] + '\n'
      ind += 1

  for e in content:
    stringEnd += html.unescape(e)
    if e.strip() != '':
      stringEnd += '\n'

  filename, ext = os.path.splitext(fr)

  f = open(filename+'-'+cout+ext, 'w', encoding="utf-8")
  f.write(stringEnd)
  f.close()

def closeDrive(driver):
  driver.quit()

def main():
  cin, cout, ba = options(sys.argv[1:])

  files = getSrt()

  for fr in files:
    print('Convert ->', fr)
    if ba:
      copyF(fr)
    addTwoLines(fr)
    content = format(fr)
    segments = getS5000(content)
    response = translate(segments, cin, cout)
    toFile(content, response, fr, cout)

if __name__ == "__main__":
  main()




