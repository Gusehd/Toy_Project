from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import urllib.request as req
from bs4 import BeautifulSoup
import random

#steam trending game random Recommendation - kor

#robots.txt
#Host: store.steampowered.com
#User-Agent: *
#Disallow: /share/
#Disallow: /news/externalpost/
#Disallow: /account/emailoptout/?*token=
#Disallow: /login/?*guestpasskey=
#Disallow: /join/?*redir=
#Disallow: /account/ackgift/
#Disallow: /email/
#Disallow: /widget/

game_category = {1:"&category=rogue_like_rogue_lite" , 2:"&category=rpg" , 3:"Action&tagid=19" ,
                 4:"Action%20Roguelike&tagid=42804" , 5:"&category=arcade_rhythm" , 6:"Beat%20%27em%20up&tagid=4158",
                 7:"&category=fighting_martial_arts", 8:"&category=action_fps" , 9:"&category=action_run_jump",
                 10:"&category=action_tps" , 11:"=&category=adventure_and_casual", 12:"Adventure&tagid=21",
                 13:"&category=adventure_rpg" , 14:"Casual&tagid=597" , 15:"Metroidvania&tagid=1628",
                 16:"&category=puzzle_matching" , 17:"&category=interactive_fiction" , 18:"Visual%20Novel&tagid=3799",
                 19:"Action%20RPG&tagid=4231" ,20:"JRPG&tagid=4434" , 21:"Party-Based%20RPG&tagid=10695",
                 22:"&category=rpg_strategy_tactics" , 23:"&category=rpg_turn_based" , 24:"Simulation&tagid=599" ,
                 25:"&category=sim_building_automation" , 26:"&category=sim_business_tycoon" , 27:"&category=sim_dating",
                 28:"&category=sim_farming_crafting" , 29:"&category=sim_life" , 30:"&category=sim_physics_sandbox",
                 31:"&category=sim_space_flight" , 32:"&category=strategy" , 33:"&category=strategy_card_board" ,
                 34:"&category=strategy_cities_settlements" ,35:"&category=strategy_grand_4x" , 36:"&category=strategy_military",
                 37:"RTS&tagid=1676" , 38:"Tower%20Defense&tagid=1645" , 39:"Turn-Based%20Strategy&tagid=1741" ,
                 40:"&category=sports_and_racing" , 41:"Sports&tagid=701" , 42:"&category=sports_fishing_hunting" ,
                 43:"&category=sports_individual" , 44:"Racing&tagid=699" , 45:"&category=racing_sim" ,
                 46:"&category=sports_sim" , 47:"&category=sports_team"}


tr_name = []
tr_url = []

def find_price(st):
    return st.find("₩")

def evalu(url_review):
    url = url_review.replace("\\", "")
    headers = req.Request(url, headers={"Accept-Language": "ko-KR"})
    code = req.urlopen(headers)
    soup = BeautifulSoup(code, "html.parser")

    review = soup.select("div.summary.column span.game_review_summary")
    date = soup.select("div.date")
    dev_n_pub = soup.select("div.summary.column > a")
    price1 = soup.select_one("div.discount_original_price")
    price2 = soup.select_one("div.game_purchase_price.price")
    if len(review) == 1:
        review_1 = str(review[0]).replace("user","명의").replace("reviews","리뷰").replace("Very","매우").replace("Positive"
                    ,"긍정적").replace("Mostly","대체로").replace("Mixed","복합적").replace("Negative","부정적").replace("Overwhelmingly","압도적으로")
        main_dialog.textBrowser.append("모든 평가 : " + review_1)
    elif len(review) >= 2:
        review_1 = str(review[0]).replace("user", "명의").replace("reviews", "리뷰").replace("Very", "매우").replace(
            "Positive", "긍정적").replace("Mostly", "대체로").replace("Mixed", "복합적").replace("Negative", "부정적").replace(
            "Overwhelmingly", "압도적으로")
        review_2 = str(review[1]).replace("user", "명의").replace("reviews", "리뷰").replace("Very", "매우").replace(
            "Positive", "긍정적").replace("Mostly", "대체로").replace("Mixed", "복합적").replace("Negative", "부정적").replace(
            "Overwhelmingly", "압도적으로")
        main_dialog.textBrowser.append("최근 평가 : " + review_1)
        main_dialog.textBrowser.append("모든 평가 : " + review_2)
    if len(date) != 0:
        date_str = str(date[0].string).replace(" Jan","일 1월").replace(" Feb","일 2월").replace(" Mar","일 3월").replace(" Apr","일 4월").replace(
            " May","일 5월").replace(" Jun","일 6월").replace(" Jul","일 7월").replace(" Aug","일 8월").replace(" Sep","일 9월").replace(" Oct","일 10월").replace(
            " Nov","일 11월").replace(" Dec","일 12월")
        main_dialog.textBrowser.append("출시 날짜 : " + date_str)
    if len(dev_n_pub) != 0:
        main_dialog.textBrowser.append("개발자 : " + dev_n_pub[0].string)
    if len(dev_n_pub) >= 2 :
        main_dialog.textBrowser.append("배급사 : " + dev_n_pub[1].string)
    if price1 != None:
        price1_idx = find_price(price1.get_text())
        if price1_idx == -1:
            main_dialog.textBrowser.append("가격 : 무료")
        else:
            main_dialog.textBrowser.append("가격 : " + price1.get_text()[price1_idx:price1_idx+10])
        #main_dialog.textBrowser.append("가격 : " + str(price1))
    else:
        price2_idx = find_price(price2.get_text())
        if price2_idx == -1:
            main_dialog.textBrowser.append("가격 : 무료")
        else:
            main_dialog.textBrowser.append("가격 : " + price2.get_text()[price2_idx:price2_idx + 10])
        #main_dialog.textBrowser.append("가격 : " + str(price2))



def search(idx, category):
    headers = req.Request(
        "https://store.steampowered.com/contenthub/querypaginated/category/NewReleases/render/?query=&start={}&count=15&cc=KR&l=english&v=4&tag={}".format(
            idx, category), headers={"Accept-Language": "ko-KR"})
    code = req.urlopen(headers)
    soup = BeautifulSoup(code, "html.parser")

    # gama name
    game_name = str(soup).replace("/div", "</div>")
    soup1 = BeautifulSoup(game_name, "html.parser")
    trending_name = soup1.findAll('div', attrs={'class': "\\\"tab_item_name\\\""})

    # game url
    game_url = str(soup).replace("\\r", "</a>")
    soup2 = BeautifulSoup(game_url, "html.parser")
    trending_url = soup2.findAll('a')

    for i,k in zip(trending_name,trending_url):
        main_dialog.textBrowser.append("게임 이름 : " + (i.string).replace("<\\", ""))
        tr_name.append((i.string).replace("<\\", ""))
        main_dialog.textBrowser.append("게임 url : " + k.get('href').replace("\\\"", ""))
        tr_url.append(k.get('href').replace("\\\"", ""))
        main_dialog.textBrowser.append("\n")

    main_dialog.textBrowser.append(" <== 현재 까지 검색된 게임의 개수 : " + str(len(tr_name)) + " 개 ( 한 페이지당 최대 15개 ) ===>\n")


ui_file = "./steam.ui"
class MainDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self,None)
        uic.loadUi(ui_file,self)
        self.initUI()
        self.setWindowTitle("스팀 인기 신제품 검색 및 랜덤 추천")

        self.pushButton.clicked.connect(self.btnclick)

    def btnclick(self):
        self.textBrowser.clear()
        global tr_name
        global tr_url

        tr_name = []
        tr_url = []

        game_cate_num = self.category_box.currentIndex()
        start_idx = self.startbox.currentIndex()
        end_idx = self.endbox.currentIndex()

        if start_idx > end_idx:
            self.textBrowser.setPlainText("페이지 범위 오류")
        else:
            for i in range(start_idx,end_idx+1):
                search((i  * 15),game_category[game_cate_num + 1])

        if len(tr_name) >= 5:
            self.textBrowser.append("\n"+"\n"+"==============================================================" +
                                    "\n"+"\n" + " < 검색 된 게임들 중 랜덤 추천 게임 > "+"\n"+"\n")
            random_list = random.sample(range(0, len(tr_name)), 5)
            for i in random_list:
                self.textBrowser.append("게임 이름 : " + tr_name[int(i)])
                evalu(tr_url[int(i)])
                self.textBrowser.append("게임 url : " + tr_url[int(i)])
                self.textBrowser.append("\n")
                self.textBrowser.append("\n")

        else:
            self.textBrowser.append("랜덤 추천 표본 부족")



    def initUI(self):
        self.category_box.setStyleSheet("QComboBox { combobox-popup: 0; font: 11pt;}")
        self.startbox.setStyleSheet("QComboBox { combobox-popup: 0; font: 11pt; }")
        self.endbox.setStyleSheet("QComboBox { combobox-popup: 0; font: 11pt; }")

        # 1:로그라이크 2:rpg , 3:액션 , 4:액션 로그라이크 5:아케이드 리듬: 6:비뎀업 7:격투 및 무술
        # 8 1인칭 슈팅 / 9 플랫포머 러너 / 10 3인칭 슈팅 / 11 어드벤쳐 캐주얼 / 12 어드벤쳐 / 13 어드벤쳐 알피지 /
        # 14 캐주얼 / 15 메트로배니아 / 16 퍼즐 / 17 풍부한 스토리 / 18 비주얼 노벨 / 19 액션 알피지 / 20 J알피지
        # 21 파티 기반 / 22 전략 롤플레잉 / 23 턴제 / 24 시물레이션 / 25 건설 및 자동화 / 26 사업 및 경영 / 27 연얘
        # 28 농업 및 제작 / 29 생활 및 몰입형 / 30 샌드박스 및 물리 / 31 우주 및 비행 / 32 전략 / 33 카드 및 보드
        # 34 도시 및 정착 / 35 대전략 및 4X / 36 군사 / 37 실시간 전략 / 38 타워 디펜스 / 39 턴제 전략 / 40 스포츠 및 레이싱
        # 41 모든 스포츠 / 42 낚시 및 사냥 / 43 개별 스포츠 / 44 레이싱 / 45 레이싱 시물레이션 / 46 스포츠 시물레이션
        # 47 팀 스포츠

        self.category_box.addItem("로그라이크")
        self.category_box.addItem("롤플레잉")
        self.category_box.addItem("액션")
        self.category_box.addItem("액션 로그라이크")
        self.category_box.addItem("아케이드 리듬")
        self.category_box.addItem("비뎀업")
        self.category_box.addItem("격투 및 무술")
        self.category_box.addItem("1인칭 슈팅")
        self.category_box.addItem("플랫포머 러너")
        self.category_box.addItem("3인칭 슈팅")
        self.category_box.addItem("어드벤쳐 캐주얼")
        self.category_box.addItem("어드벤쳐")
        self.category_box.addItem("어드벤쳐 알피지")
        self.category_box.addItem("캐주얼")
        self.category_box.addItem("메트로배니아")
        self.category_box.addItem("퍼즐")
        self.category_box.addItem("풍부한 스토리")
        self.category_box.addItem("비주얼 노벨")
        self.category_box.addItem("액션 RPG")
        self.category_box.addItem("JRPG")
        self.category_box.addItem("파티 기반")
        self.category_box.addItem("전략 롤플레잉")
        self.category_box.addItem("턴제")
        self.category_box.addItem("시물레이션")
        self.category_box.addItem("건설 및 자동화")
        self.category_box.addItem("사업 및 경영")
        self.category_box.addItem("연애")
        self.category_box.addItem("농업 및 제작")
        self.category_box.addItem("생활 및 몰입형")
        self.category_box.addItem("샌드박스 및 물리")
        self.category_box.addItem("우주 및 비행")
        self.category_box.addItem("전략")
        self.category_box.addItem("카드 및 보드")
        self.category_box.addItem("도시 및 정착")
        self.category_box.addItem("대전략 및 4X")
        self.category_box.addItem("군사")
        self.category_box.addItem("실시간 전략")
        self.category_box.addItem("타워 디펜스")
        self.category_box.addItem("턴제 전략")
        self.category_box.addItem("스포츠 및 레이싱")
        self.category_box.addItem("모든 스포츠")
        self.category_box.addItem("낚시 및 사냥 ")
        self.category_box.addItem("개별 스포츠")
        self.category_box.addItem("레이싱")
        self.category_box.addItem("레이싱 시물레이션")
        self.category_box.addItem("스포츠 시물레이션")
        self.category_box.addItem("팀 스포츠")

        for i in range(1,101):
            self.startbox.addItem(str(i))

        for i in range(1,101):
            self.endbox.addItem(str(i))


QApplication.setStyle("fusion")
app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()
sys.exit(app.exec_())