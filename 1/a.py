from ChickenUtil import ChickenStore
from itertools import count

####################################################
brandName = 'kyochon'
base_url = 'https://m.7-eleven.co.kr:444/store/storeSearch1.asp'


####################################################
def getData():
    savedData = []  # 엑셀로 저장할 리스트

    for sido1 in range(1, 18):
        for sido2 in count():
            url = base_url
            url += '?sido1=' + str(sido1)
            url += '&sido2=' + str(sido2 + 1)
            #             print(url)

            chknStore = ChickenStore(brandName, url)
            soup = chknStore.getSoup()

            # 존재하지 않는 주소 : 서울시의 26번째 구
            if soup == None:
                break

            ultag = soup.find('ul', attrs={'class': 'list'})
            for myitem in ultag.findAll('a'):
                #                 print( myitem )
                #                 print('c' * 30)

                try:
                    store = myitem.span.strong.string
                    #                     print( store )
                    #                     print('c' * 30)

                    myhref = myitem['href']
                    myhref = myhref.replace("javascript:mapchange('", '')
                    #                     print( myhref )
                    #                     print('c' * 30)

                    quote = myhref.find("'")
                    address = myhref[0:quote]
                    #                 print('b' * 30)
                    imsi = address.split(' ')
                    sido = imsi[0]
                    gungu = imsi[1]

                    emlist = myitem.span.em.get_text(strip=True)
                    # print( '[' + emlist + ']')
                    # print('c' * 30)
                    savedData.append([brandName, store, sido, gungu, address])

                except Exception as err:
                    print(err)
                    break

    chknStore.save2Csv(savedData)

    print('a' * 30)


####################################################
print(brandName + ' 매장 크롤링 시작')
getData()
print(brandName + ' 매장 크롤링 끝')