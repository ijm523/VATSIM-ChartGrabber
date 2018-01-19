from bs4 import BeautifulSoup
import urllib.request, urllib

dpapt = str(input('Departure airport ICAO: ')).upper()
dpurl = 'https://flightaware.com/resources/airport/' + dpapt + '/procedures'
#print(dpurl)

arapt = str(input('Arrival airport ICAO: ')).upper()
arurl = 'https://flightaware.com/resources/airport/' + arapt + '/procedures'

def weave(list1,list2):
    lijst = []
    i = 0
    while i < len(list1):
        try:
            lijst.append(list1[i])
            lijst.append(list2[i]) 
        except:
            pass
        i += 1
    return lijst


dppg = urllib.request.urlopen(dpurl)
dpsoup = BeautifulSoup(dppg, 'html.parser')

dplst = weave(dpsoup.find_all('tr', attrs={'class': 'smallrow1'}),dpsoup.find_all('tr', attrs={'class': 'smallrow2'}))
sidlst = []
cd1=0
for item in dplst:
    sublst1 = item.text.replace('\n',' ').split(maxsplit=1)
    sublist = [s.strip(' ') for s in sublst1]
#    print(sublist)
    if sublist[0] == 'Diagram':
        dpapdlnk = str('https://flightaware.com' + dplst[0].find('a').attrs['href'] + '/pdf')        
    if sublist[0] == 'DP':
        sidlst.append(sublist[1])
        cd2 = cd1
    else:
        cd1 += 1


arpg = urllib.request.urlopen(arurl)
arsoup = BeautifulSoup(arpg, 'html.parser')

arlst = weave(arsoup.find_all('tr', attrs={'class': 'smallrow1'}),arsoup.find_all('tr', attrs={'class': 'smallrow2'}))
starlst = []
applst = []
ca1 = 0
cap1 = 0
for item in arlst:
    sublst1 = item.text.replace('\n',' ').split(maxsplit=1)
    sublist = [s.strip(' ') for s in sublst1]
#    print(sublist)
    if sublist[0] == 'Diagram':
        arapdlnk = str('https://flightaware.com' + arlst[0].find('a').attrs['href'] + '/pdf')        
    if sublist[0] == 'STAR':
        starlst.append(sublist[1])
        ca2 = ca1
    else:
        ca1 += 1
    if sublist[0] == 'Approach':
        applst.append(sublist[1])
        cap2 = cap1
    else:
        cap1 += 1

i=1
print('-----------------------------')
for departure in sidlst:
    print(str(i)+'. '+departure)
    i += 1

sid = int(input('Select SID: '))
sidlnk = str('https://flightaware.com' + dplst[(sid+cd2)-1].find('a').attrs['href'] + '/pdf')
#print(sidlnk)

i=1
print('-----------------------------')
for arrival in starlst:
    print(str(i)+'. '+arrival)
    i += 1

star = int(input('Select STAR: '))
starlnk = str('https://flightaware.com' + arlst[(star+ca2)-1].find('a').attrs['href'] + '/pdf')
#print(starlnk)

i=1
print('-----------------------------')
for approach in applst:
    print(str(i)+'. '+approach)
    i += 1

app = int(input('Select approach: '))
applnk = str('https://flightaware.com' + arlst[(app+cap2)-1].find('a').attrs['href'] + '/pdf')
#print(starlnk)

print('Downloading charts...')
urllib.request.urlretrieve(dpapdlnk,'1 ' + dpapt + ' DIAGRAM.pdf')
urllib.request.urlretrieve(sidlnk,'2 ' + sidlst[sid-1] + '.pdf')
urllib.request.urlretrieve(starlnk,'3 ' + starlst[star-1] + '.pdf')
urllib.request.urlretrieve(applnk,str('4 ' + applst[app-1] + '.pdf').replace('/','-'))
urllib.request.urlretrieve(arapdlnk,'5 ' + arapt + ' DIAGRAM.pdf')
print('Done!')
