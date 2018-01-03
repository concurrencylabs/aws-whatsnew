import sys, argparse, requests
from lxml import html


MONTHS = ['Jan','Feb','Mar', 'Apr', 'May', 'Jun', 'Jul','Aug','Sep','Oct','Nov','Dec']

def main (argv):

    parser = argparse.ArgumentParser()
    parser.add_argument('--year', help='', required=True)


    if len(sys.argv) == 1:
      parser.print_help()
      sys.exit(1)
    args = parser.parse_args()

    year = ''
    if args.year: year= args.year

    page = requests.get('https://aws.amazon.com/about-aws/whats-new/'+year+'/')
    tree = html.fromstring(page.content)

    #Reference: http://www.w3schools.com/xml/xpath_syntax.asp
    #Create word cloud using http://www.wordclouds.com/
    announcements = tree.xpath('//li[@class="directory-item text whats-new"]/h3/a/text()')
    dates = tree.xpath('//div[@class="date"]/text()')

    print 'Number of announcements: {}'.format(len(announcements))
    write_month_table(get_month_count(dates),year)
    write_announcements(announcements,year)

def get_month_count(dates):
    result = init_month_dict()
    for d in dates:
        for m in MONTHS:
          if m in d:result[m]+=1
    return result

def init_month_dict():
    result = {}
    for m in MONTHS: result[m]=0
    return result

def write_month_table(month_dict, year):
    mt = open('months_'+year+'.txt','w')
    mt.write('Month\tAnnouncements\n')
    for m in MONTHS:
        mt.write(m+'\t'+str(month_dict[m])+'\n')
    mt.close

def write_announcements(announcements, year):
    MIN_FREQUENCY = 10
    excludedict={'now':True, 'support':True, 'supports':True, 'amazon':True, 'aws':True, 'adds':True,
    			 'available':True, 'supports':True,'available':True,'announcing':True,
                'new':True, 'adds':True,'introduces':True,'announces':True,'using':True,
                'service':True, 'introducing':True, 'cloud':True, 'can':True, 'use':True,
                'and':True,'with':True,'is':True,'in':True, 'for':True, 'the':True, 'to':True,
                'an':True, 'on':True, 'you':True,'a':True, 'your':True,'of':True, 'are':True,
                'makes':True, 'offers':True,'updates':True}
        	
    wc = open('wordcloud_'+year+'.txt','w')
    ann = open('announcements_'+year+'.txt','w')
    worddict = {}

    #calculate word frequency
    for anntitle in announcements:
        for a in anntitle.split(' '):
          key = a.lower().encode('utf-8')    
    	  tmpCount = worddict.get(key,0)
    	  tmpCount += 1
    	  worddict[key]=tmpCount

    #find words that don't have a minimum frequency and add to the 'exclude' dict    	  
    for w in worddict.keys():
        if worddict[w] < MIN_FREQUENCY: excludedict[w]=True

    print("exclude dict:{}".format(excludedict))

    for anntitle in announcements:
        anntitle = anntitle.encode('utf-8')
        ann.write(a+'\n')
        for a in anntitle.lower().split(' '):
            if excludedict.get(a, False): pass
            else: wc.write(a+'\n')
    wc.close
    ann.close
    
    print(worddict)




if __name__ == "__main__":
    main(sys.argv[1:])