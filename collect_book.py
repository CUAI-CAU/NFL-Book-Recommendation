from selenium import webdriver
import time
import pandas as pd
import os, json

secret_file = os.path.join('', 'secrets.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    return secrets[setting]

id = get_secret('ID')
password = get_secret('PASSWORD')



browser = webdriver.Chrome('chromedriver')

datalist = []

browser.get("https://www.aladin.co.kr/shop/wbrowse.aspx?CID=50917") #알라딘 한국소설 페이지

#로그인
login = browser.find_element_by_css_selector('.set3m div a')
login.send_keys('\n')

id_input = browser.find_element_by_css_selector('#Email')
password_input = browser.find_element_by_css_selector('#Password')

id_input.send_keys(id)
password_input.send_keys(password)
login_button = browser.find_element_by_css_selector('.left1_right a')
login_button.send_keys('\n')

#다시 페이지로
browser.get("https://www.aladin.co.kr/shop/wbrowse.aspx?CID=50917") #알라딘 한국소설 페이지

for p in range(0,20):
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
            book_star_count_btn = browser.find_element_by_css_selector('.Ere_fs15 .Ere_fs16')
            book_star_count_btn.send_keys('\n')
            time.sleep(1)
            book_star_count_text = browser.find_element_by_css_selector('#divRankLayer > div > div.bt_list3 > a')
            book_star_count = list(filter(str.isdigit,book_star_count_text.text))
            book_star_count = ''.join(book_star_count)
            print(book_star.text, book_star_count)
            data.append(book_star.text)
            data.append(book_star_count)
        except:
            data.append('')
            data.append('')

        try:
            book_prefer_woman = browser.find_elements_by_css_selector('.analysis_box .tb_woman .per') # 구매자 분포(여자)

            prefer_w = []
            for i in range(6):
                prefer_w.append(float(book_prefer_woman[i].text[:-1]))
            #print(prefer_w)
            # data.append(list(prefer_w))
            for prefer in prefer_w:
                prefer = float(prefer)*10
                prefer = int(prefer)/100
                data.append(prefer)
        except:
            # data.append([])
            browser.back()
            continue

        try:
            book_prefer_man = browser.find_elements_by_css_selector('.analysis_box .tb_man .per') # 구매자 분포(남자)

            prefer_m = []
            for i in range(6):
                prefer_m.append(float(book_prefer_man[i].text[:-1]))
            #print(prefer_m)
            # data.append(list(prefer_m))
            for prefer in prefer_m:
                prefer = float(prefer)*10
                prefer = int(prefer)/100
                data.append(prefer)
        except:
            # data.append([])
            browser.back()
            continue
        
        try:
            for n in range(0,20): #책속에서 큰 더보기 버튼 클릭. 간혹 더보기가 안사라지는 페이지 존재
                try:
                    more_btn = browser.find_element_by_css_selector('#Underline3_more a')
                    more_btn.send_keys('\n')
                except:
                    break
            while True: # 책속에서 책 구절들 더보기로 가려진 것들 모두 펼치기
                try:
                    more_more_btn = browser.find_elements_by_css_selector('#Underline3Updates .Ere_sub_gray8.Ere_fs13')
                    time.sleep(1)
                    if len(more_more_btn) == 0:
                        break
                    for k, btn in enumerate(more_more_btn):
                        if k % 2 == 0:
                            btn.send_keys('\n')
                except:
                    break
            time.sleep(1)
            contents = browser.find_element_by_css_selector('#Underline3Updates')
            data.append(contents.text)
        except:
            browser.back()
            continue
        # 테스트용 콘솔에 출력
        pypi = None
        
        datalist.append(data)
        # 뒤로가기
        browser.back()

    # 다음 페이지 클릭
    try:
        page_list = browser.find_elements_by_css_selector('.numoff')
        page = page_list[p]
        page.send_keys('\n')
    except:
        continue

print(datalist)
selectdata = pd.DataFrame(datalist, columns=['제목', '작가', '출판사', '장르', '별점', '별점 수', '10대(여)','20대(여)','30대(여)','40대(여)','50대(여)','60대 이상(여)', '10대(남)', '20대(남)', '30대(남)', '40대(남)', '50대(남)','60대(남)','내용'])

selectdata.to_excel("book.xlsx")
selectdata.to_csv("book.csv")