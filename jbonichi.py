#coding: utf-8
from __future__ import print_function, unicode_literals
try: raw_input
except NameError: raw_input = input
try: from lxml import etree as ET
except ImportError: import xml.etree.ElementTree as ET
import re, os, sys, codecs
from subprocess import call

#ファイル読み込み
def readxml():
    if len(sys.argv) > 1:
        path = os.path.expanduser(sys.argv[1].decode('utf-8'));
    else:
        print('引数にXMLファイルを指定してください')
        path = ""

    if not (path.endswith('.xml') and os.path.exists(path)):
        print('該当XMLファイルが見つからなかったため、デフォルトパス(日本語 - lojban.xml)を使用します')
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)).decode('utf-8'), '日本語 - lojban.xml')

    if not (path.endswith('.xml') and os.path.exists(path)):
        print('XMLファイルが見つからないため、変換を中止しました')
        exit()

    print(path)
    return ET.parse(path)


#項目印刷
def print_entry(valsi):
    word   = valsi.get('word')
    notes  = valsi.findtext('notes')
    rafsis = [x.text for x in valsi.iter('rafsi')]
    def print_index(index):
        print('<d:index d:value="'+index+'" d:title="'+word+'"/>')

    #項目名および検索キー
    print('<d:entry id="'+valsi.findtext('definitionid')+'" d:title="'+word+'">')
    print_index(word)

    if "'" in word:    #'をhへ（CAhAとか）
        print_index(word.replace("'","h"))

    if valsi.get('type') == 'gismu':    #rafsi各種
        print_index(word[0:4])
        for rafsi in rafsis:
            if rafsi != word:
                print_index(rafsi)

    if notes:    #訳語
        mean = re.search('・大意： (.*?) ',notes)
        if mean:
            print_index(mean.group(1))
    jps = valsi.findall('glossword') + valsi.findall('keyword')
    if jps:
        for jp in jps:
            jp.get('word')


    #本文
    print('<h1>'+word+'</h1>' )    #見出し（単語）
    print(end='<p>['+valsi.get('type'))    #品詞＆selma'o

    selmaho = valsi.findtext('selmaho')
    if selmaho:
        print(' ('+selmaho+')]<br/>')
    else:
        print(']<br/>')

    print(re.sub('\s*[；：]\s*','<br/>\n',re.sub('\$x_(\d)\$','x\g<1>',valsi.findtext('definition')))+'</p>')

    #付帯事項
    if notes:    #捕捉
        print('<p>')
        note = re.search('^(.*?)\s*(・|「[^／])',re.sub(u'\s*[；：]\s*','<br/>\n',notes))
        if note and note.group(1):
            print(note.group(1)+'<br/>')

        ex = re.search('(「[^」]+／.+?」(（.+）)?)*',notes).group(0)    #例文
        if ex:
            print(re.sub('(」|）)「','\g<1><br/>「',ex)+'<br/>')

        if rafsis:   #rafsi
            print('rafsi: '+', '.join(rafsis)+'<br/>')

        syno = re.findall('{(.+?)}',notes)
        if syno:    #関連語
            print(end='関連語: ')
            for s in syno:
                if s != syno[0]:
                    print(end=', ')
                print(end=s)
        print('</p>')

    print('</d:entry>\n')

###########ここから本体############
root = readxml()
os.chdir(os.path.dirname(os.path.abspath(__file__))) #このファイルと同じディレクトリに強制移動
sys.stdout = codecs.getwriter('utf_8')(open('MyDictionary.xml','w'))

print('<?xml version="1.0" encoding="UTF-8"?>\n<d:dictionary xmlns="http://www.w3.org/1999/xhtml" xmlns:d="http://www.apple.com/DTDs/DictionaryService-1.0.rng">')

for valsi in root.iter('valsi'):
    print_entry(valsi)

print('</d:dictionary>')

sys.stdout = sys.__stdout__
