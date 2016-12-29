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
    mt.write('Month\tReleases\n')
    for m in MONTHS:
        mt.write(m+'\t'+str(month_dict[m])+'\n')
    mt.close

def write_announcements(announcements, year):
    exclude=('now', 'support', 'amazon', 'aws', 'adds', 'available', 'supports','available','announcing',
             'new', 'adds','introduces','announces','using')
    wc = open('wordcloud_'+year+'.txt','w')
    ann = open('announcements_'+year+'.txt','w')
    for a in announcements:
        a = a.encode('utf-8')
        ann.write(a+'\n')
        a = a.lower()
        for e in exclude: a = a.replace(e,'')
        wc.write(a+'\n')
    wc.close
    ann.close




if __name__ == "__main__":
    main(sys.argv[1:])