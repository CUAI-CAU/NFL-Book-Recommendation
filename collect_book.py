from selenium import webdriver
import time
import pandas as pd
browser = webdriver.Chrome('chromedriver')

datalist = []

browser.get("https://www.aladin.co.kr/shop/wbrowse.aspx?CID=50917") #알라딘 한국소설 페이지

for p in range(0,50):
    print(p)
    if p >= 1:
        p +=1
    if p <=10:
        p = p % 11
    else:
        p+=3
        if p % 12 < 2:
            continue
        p = p % 12
    time.sleep(1)
    for i in range(0,25):
        time.sleep(1)
        book_list = browser.find_elements_by_css_selector('.ss_book_box li .bo3') #책 목록
        book = book_list[i] #책 하나씩 클릭
        print(book.text)
        data = []
        data.append(book.text)
        book.send_keys('\n')

        book_author = browser.find_element_by_css_selector('.Ere_prod_titlewrap li .Ere_sub2_title') # 작가
        #print(book_author.text)
        data.append(book_author.text)

        book_published = browser.find_element_by_css_selector('.Ere_prod_titlewrap li:nth-child(3) a:nth-child(3)') # 출판사
        #print(book_published.text)
        data.append(book_published.text)

        book_subject = browser.find_element_by_css_selector('.conts_info_list2 b') # 장르
        print(book_subject.text)
        data.append(book_subject.text)

        for j in range(0,80): #js 모두 불러오기
            browser.execute_script("window.scrollTo({0}, {1})".format((200*j),(200*j+300)))

        time.sleep(1)
        browser.execute_script("window.scrollTo(9000, 0)")
        time.sleep(1)

        try:
            book_star = browser.find_element_by_css_selector('.star_list .score_box .num') # 별점
            print(book_star.text)
            data.append(book_star.text)
        except:
            data.append('')

        try:
            book_prefer_woman = browser.find_elements_by_css_selector('.analysis_box .tb_woman .per') # 구매자 분포(여자)

            prefer_w = []
            for i in range(6):
                prefer_w.append(float(book_prefer_woman[i].text[:-1]))
            #print(prefer_w)
            data.append(list(prefer_w))
        except:
            data.append([])

        try:
            book_prefer_man = browser.find_elements_by_css_selector('.analysis_box .tb_man .per') # 구매자 분포(남자)

            prefer_m = []
            for i in range(6):
                prefer_m.append(float(book_prefer_man[i].text[:-1]))
            #print(prefer_m)
            data.append(list(prefer_m))
        except:
            data.append([])

        # 테스트용 콘솔에 출력
        pypi = None
        
        datalist.append(data)
        # 뒤로가기
        browser.back()

    # 다음 페이지 클릭
    page_list = browser.find_elements_by_css_selector('.numoff')
    page = page_list[p]
    page.send_keys('\n')

print(datalist)
selectdata = pd.DataFrame(datalist, columns=['제목', '작가', '출판사', '장르', '별점', '구매자분포(여)', '구매자분포(남)'])

selectdata.to_excel("book.xlsx")
selectdata.to_csv("book.csv")