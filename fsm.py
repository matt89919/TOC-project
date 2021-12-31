from future.utils import text_to_native_str
from transitions.extensions import GraphMachine
import time
from utils import *
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'

key=''

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.machine.get_graph().draw('my_state_diagram.png', prog='dot')
        
    def start_to_menu(self, event):
        text = event.message.text
        if len(text) > 0:
            return 1

    def menu_to_intro(self, event):
        text = event.message.text
        return text.lower() == "intro"
    
    def intro_to_roast(self, event):
        text = event.message.text
        return text.lower() == "roast"
    
    def on_enter_roast(self, event):
        id=event.source.user_id
        print("on roast")
        url='https://blog.idrip.coffee/wp-content/uploads/2020/11/three_types_of_coffee_beans-1-1200x800.jpg'
        title='烘焙'
        uptext='咖啡又可以大略分成 淺焙 中焙 深焙 \n請選擇一種'
        labels=['淺焙','中焙','深焙','返回']
        texts=['l','m','d','go back']
        send_button_message(id,url,title,uptext,labels,texts)
        
    def roast_to_l(self, event):
        text = event.message.text
        return text.lower() == "l"
        
    def on_enter_l(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "淺烘焙\n\n常見於單一產地咖啡豆烘焙，此種烘焙舊稱為肉桂烘焙，因為其烘焙出的咖啡帶有肉桂皮的顏色，此烘焙度的咖啡具有較高酸度，有些具有果實般的甜味\n\n常見風味:果香、花香、酒香")
        time.sleep(7)
        self.go_back(event)
        
    def roast_to_m(self, event):
        text = event.message.text
        return text.lower() == "m"
        
    def on_enter_m(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "中烘焙\n\n咖啡較淺焙有著更深褐色的外觀，咖啡的油脂也可能在表面就看得到。此烘焙度的咖啡甜度較高，兼具醇厚度\n\n常見風味:堅果、巧克力、花生")
        time.sleep(7)
        self.go_back(event)
        
    def roast_to_d(self, event):
        text = event.message.text
        return text.lower() == "d"
        
    def on_enter_d(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "深烘焙\n\n咖啡豆呈現深黑色，並泛出油光，苦味濃烈，常見分為法式烘焙（French Roast），帶有苦巧克力的色澤。義式烘焙（Italian）則幾乎呈現黑色的外觀並且咖啡豆表面非常油。適合搭配牛奶飲用\n\n常見風味:巧克力、焦糖、榛果")
        time.sleep(7)
        self.go_back(event)
    
    def backto_intro(self, event):
        text = event.message.text
        return text.lower() == "go back"
    
    def intro_to_method(self, event):
        text = event.message.text
        return text.lower() == "method"
    
    def on_enter_method(self, event):
        id=event.source.user_id
        print("on method")
        url='https://static.wixstatic.com/media/e988c0_a950541906134ce9bcce5242e528bcca~mv2.jpg/v1/fill/w_800,h_450,al_c,q_90/e988c0_a950541906134ce9bcce5242e528bcca~mv2.jpg'
        title='咖啡處理法'
        uptext='常見的咖啡處理法有水洗、日曬、密處理，各有不同的特色\n點擊以查看各個處理法吧!'
        labels=['水洗','日曬','密處理','返回']
        texts=['washed','natural','honey','go back']
        send_button_message(id,url,title,uptext,labels,texts)
        
    def method_to_washed(self, event):
        text = event.message.text
        return text.lower() == "washed"
    
    def on_enter_washed(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "水洗處理法\n\n將篩選完的咖啡果經過去殼機將果皮、果肉等去除，剩下含有果膠層的咖啡豆會由咖啡本身的共生細菌，如：醋酸菌與乳酸菌等發酵12至24小時不等。這些菌株會消化咖啡豆外部的果膠層，進而產酸滲入咖啡豆中，讓咖啡豆的風味偏酸，後續再透過水洗方式處理，因此稱為水洗法。\n\n特色:酸值明亮、風味乾淨")
        time.sleep(5)
        self.go_back(event)
    
    def method_to_natural(self, event):
        text = event.message.text
        return text.lower() == "natural"
    
    def on_enter_natural(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "日曬處理法\n\n將篩選後的咖啡果實直接鋪在大廣場上，讓陽光曝曬個2至3週將咖啡果曬乾，曬乾的咖啡果再去除外殼就可以得到咖啡豆。日曬豆會黏附乾掉的果肉層與果膠層，因此咖啡豆的風味會更為豐富，嚐起來的味道也會偏向於甘甜。\n\n特色:常帶較重的水果味、發酵味，或是酒味")
        time.sleep(5)
        self.go_back(event)
    
    def method_to_honey(self, event):
        text = event.message.text
        return text.lower() == "honey"
    
    def on_enter_honey(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "密處理\n\n蜜處理法與日曬十分類似，差別在於蜜處理是將採收後的咖啡果實去除一定程度的果皮及果肉層，將除去果肉層的帶殼咖啡豆舖放在露台或曝曬桌上曝曬，藉由控制咖啡豆的曝曬時間、咖啡豆外殼上的果膠及果肉的量來控制發酵。隨著保留的果肉果膠層越多，風味也將更為複雜深沉，同時瑕疵風險也越高，市場上也漸漸有著不同的標示出現，由保留最少果膠果肉層的白蜜，到保留最多的黑蜜也因此而生。\n\n特色:風味介於日曬和水洗之間，果膠保留越多風味越接近日曬，反之則接近水洗")
        time.sleep(5)
        self.go_back(event)
        
    def country_to_africa(self, event):
        text = event.message.text
        return text.lower() == "africa"
    
    def on_enter_africa(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "非洲\n\n咖啡的發源地。雖然咖啡的商業種植在全球已有數百年的發展，時至今日非洲不知凡幾的野生咖啡品種依舊是咖啡研究者們心中最大的寶藏。非洲咖啡的普遍特點是濃郁的香氣以及迷人的果酸，其酸味亮度活潑令人振奮，但非洲咖啡的醇厚略顯單薄，甜味較不突出。\n\n代表國家:衣索比亞、肯亞、盧安達")
        time.sleep(5)
        self.go_back(event)
    
    def country_to_asia(self, event):
        text = event.message.text
        return text.lower() == "asia"
    
    def on_enter_asia(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "亞洲\n\n亞洲的咖啡，咖啡愛好者們的第一印象往往是渾厚沉穩。正因為亞洲咖啡厚重的特點，在製作意式拼配咖啡時，非常適合作為基底。亞洲的咖啡生豆處理一般採用濕法或半濕法的加工處理方式，生豆的豆型大多比較均勻，只是半濕法處理後的豆子顏色較暗。亞洲咖啡的普遍特點是風味厚重，甜味強烈圓潤，但香氣與明亮度略顯平淡。\n\n代表國家:印尼、蘇門答臘")
        time.sleep(5)
        self.go_back(event)
    
    def country_to_ca(self, event):
        text = event.message.text
        return text.lower() == "ca"
    
    def on_enter_ca(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "中南美洲\n\n中南美洲是世界上最大的咖啡產區，這裡的精品咖啡數不勝數。隨便拿哥倫比亞、瓜地馬拉或巴西一國為例，好咖啡就足以令人眼花繚亂。是什麼資源優勢使得中南美洲如此之好呢?1721年法國海軍軍官德-克利（Gabriel Mathieu de Clieu）歷經艱難險阻將第一棵咖啡樹苗從非洲帶到拉丁美洲的馬提尼克島（Martinique），這一切就是拉丁美洲咖啡種植的起源。因為當時的法國處於波旁王朝統治時期，拉丁美洲所種植的阿拉比卡咖啡就有了另一個時至今日在咖啡行業中聲名遐邇的名字「波旁」。如今波旁已經是阿拉比卡中咖啡的重要分支。拉丁美洲咖啡的整體風味以平衡而著稱，咖啡中所有的風味都可以在拉丁美洲咖啡中找到。\n\n代表國家:哥斯大黎加、哥倫比亞、巴西")
        time.sleep(5)
        self.go_back(event)
        
    def on_enter_aftercountry(self, event):
        id=event.source.user_id
        print("on after")
        url='https://img.shoplineapp.com/media/image_clips/5f5b32db2508075aa2848715/original.jpg?1599812314'
        title='查看更多'
        uptext='查看其他資訊或讓小幫手幫你沖一杯咖啡吧!\n若要回到主選單也可以哦'
        labels=['其他資訊','沖杯咖啡','回到主選單']
        texts=['intro','helper','menu']
        send_button_message(id,url,title,uptext,labels,texts)
        
    def after_to_intro(self, event):
        text = event.message.text
        return text.lower() == "intro"
    
    def after_to_helper(self, event):
        text = event.message.text
        return text.lower() == "helper"
    
    def after_to_menu(self, event):
        text = event.message.text
        return text.lower() == "menu"
    
    def intro_to_country(self, event):
        text = event.message.text
        return text.lower() == "country"
    
    def on_enter_country(self, event):
        id=event.source.user_id
        print("on country")
        url='https://lh3.googleusercontent.com/proxy/6XLJlYh1K_CtD8iW6oD2WK7dRdeW9RnpBIhquuDB0Gma45svP_f0vm83iePyEdw-TNZ4xyooc-Odle7gLR71WE3acg9ldviuGFov-6hL7hxi'
        title='咖啡產地'
        uptext='你知道嗎，每個地方生產的咖啡都有不同的味道哦!這裡粗略的以洲為單位介紹各洲不同的特色\n從選單中選擇吧!'
        labels=['非洲','中南美洲','亞洲','返回']
        texts=['africa','ca','asia','go back']
        send_button_message(id,url,title,uptext,labels,texts)

    def menu_to_helpermenu(self, event):
        text = event.message.text
        return text.lower() == "helpermenu"
    
    def menu_to_input(self, event):
        text = event.message.text
        return text.lower() == "web"
    
    def on_enter_input(self, event):
        id=event.source.user_id
        print("on input")
        url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTuYMJ0n5ac2edUKHL6fi91IHvq3V308Yut-A&usqp=CAU'
        title='看看鄉民們的討論吧'
        uptext='想看甚麼主題呢\n點選按鈕或直接輸入關鍵字'
        labels=['器材','情報','販售','返回']
        texts=['器材','情報','販售','go back']
        send_button_message(id,url,title,uptext,labels,texts)
        
    def backto_menu(self, event):
        text = event.message.text
        return text.lower() == "go back"

    def on_enter_intro(self, event):
        id=event.source.user_id
        print("on intro")
        url='https://cdn.imweb.me/thumbnail/20210904/b9bab80a82d20.jpg'
        title='精品咖啡'
        uptext='一杯美味的咖啡，從種植、後處理到烘焙都不能馬虎\n想從哪裡開始呢?'
        labels=['烘焙','處理法','產區','返回']
        texts=['roast','method','country','go back']
        send_button_message(id,url,title,uptext,labels,texts)   

    def on_enter_helpermenu(self, event):
        id=event.source.user_id
        print("on helpermenu")
        url='https://scontent.ftpe7-4.fna.fbcdn.net/v/t39.30808-6/248596293_3114593108762268_373844912436580825_n.jpg?_nc_cat=101&ccb=1-5&_nc_sid=8bfeb9&_nc_ohc=WGC26QQ9S6oAX_cZeMA&tn=TJv3KnU0CuAhyqG3&_nc_ht=scontent.ftpe7-4.fna&oh=00_AT-MX9QDyIXKsjLNusm2LKL5mLhIKA58iUFPWtjc9l_9_w&oe=61D437B7'
        title='沖煮小幫手'
        uptext='喜歡甚麼風味呢?\n讓小幫手選擇最適合的手法吧'
        labels=['偏酸','偏甜','其他','返回']
        texts=['mode1','mode2','mode3','go back']
        send_button_message(id,url,title,uptext,labels,texts)
        
    def on_enter_premode(self, event):    
        id=event.source.user_id
        print("on premode")
        url='https://scontent.ftpe7-4.fna.fbcdn.net/v/t39.30808-6/248596293_3114593108762268_373844912436580825_n.jpg?_nc_cat=101&ccb=1-5&_nc_sid=8bfeb9&_nc_ohc=WGC26QQ9S6oAX_cZeMA&tn=TJv3KnU0CuAhyqG3&_nc_ht=scontent.ftpe7-4.fna&oh=00_AT-MX9QDyIXKsjLNusm2LKL5mLhIKA58iUFPWtjc9l_9_w&oe=61D437B7'
        title='沖煮小幫手'
        uptext='在開始前，請先準備好20g的咖啡豆並研磨成咖啡粉以及手沖壺、濾杯'
        labels=['下一步','返回']
        texts=['ok','go back']
        send_button_message(id,url,title,uptext,labels,texts)
        
    def premode_to_helpermenu(self, event):
        text = event.message.text
        return text.lower() == "ok"
        
    def input_to_web(self, event):   
        global key
        key = event.message.text
        if key.lower()=="go back":
            return 0
        if len(key) > 0:
            return 1
        else :
            return 0
        
    def on_enter_web(self, event):
        print("start web scraping")
        global key
        if key.lower()=="all":
            key="["
        reply_token = event.reply_token
        msg=webscrape(key)
        if msg=='':
            msg='Nothing has found'
        send_text_message(reply_token, msg)
        time.sleep(4)
        self.go_back(event)

    def helpermenu_to_mode1(self, event):
        text = event.message.text
        return text.lower() == "mode1"
    
    def on_enter_mode1(self, event):
        print("start mode1")
        userid=event.source.user_id

        msg="注入30~40g的水進行悶蒸\n\n小幫手將幫您計時30秒開始下一段注水"
        reply_token = event.reply_token
        send_text_message(reply_token, msg)
        time.sleep(30)
        msg="從中心開始注水，緩慢繞圈\n由內向外再回到內圈\n重複此動作至180g\n\n小幫手將幫您計時40秒開始下一段注水"
        push_message(userid,msg)
        time.sleep(40)
        msg="中心定點注水至300g"
        push_message(userid,msg)
        time.sleep(2)
        msg="注水完成後沖煮即完成，享受美味的咖啡吧!"
        push_message(userid,msg)
        time.sleep(2)
        self.go_back(event)
 
    def helpermenu_to_mode2(self, event):
        text = event.message.text
        return text.lower() == "mode2"
    
    def on_enter_mode2(self, event):
        print("start mode2")
        userid=event.source.user_id

        msg="以中心繞至外圍再繞回中心注水至40g (注意不要沖煮到濾紙)\n\n小幫手將幫您計時45秒開始下一段注水"
        reply_token = event.reply_token
        send_text_message(reply_token, msg)
        time.sleep(45)
        msg="以相同手法注水至120g\n\n小幫手將幫您計時45秒開始下一段注水"
        push_message(userid,msg)
        time.sleep(45)
        msg="以相同手法注水至180g\n\n小幫手將幫您計時45秒開始下一段注水"
        push_message(userid,msg)
        time.sleep(45)
        msg="以相同手法注水至240g\n\n小幫手將幫您計時45秒開始下一段注水"
        push_message(userid,msg)
        time.sleep(45)
        msg="以相同手法注水至300g"
        push_message(userid,msg)
        time.sleep(2)
        msg="注水完成後沖煮即完成，享受美味的咖啡吧!"
        push_message(userid,msg)
        time.sleep(2)
        self.go_back(event)    
    
    def helpermenu_to_mode3(self, event):
        text = event.message.text
        return text.lower() == "mode3"
     
    def on_enter_mode3(self, event):
        print("start mode3")
        userid=event.source.user_id

        msg="注入30~40g的水進行悶蒸\n\n小幫手將幫您計時30秒開始下一段注水"
        reply_token = event.reply_token
        send_text_message(reply_token, msg)
        time.sleep(30)
        msg="以中心繞至外圍再繞回中心注水至300c.c，繞圈直徑至多約50元硬幣大小，水柱中等偏細、力道溫柔、講究細水長流，避免過多的粉層翻攪"
        push_message(userid,msg)
        time.sleep(2)
        msg="注水完成後沖煮即完成，享受美味的咖啡吧!"
        push_message(userid,msg)
        time.sleep(2)
        self.go_back(event)
           
    def on_enter_afterhelper(self, event):
        id=event.source.user_id
        print("on afterhelper")
        url='https://img.shoplineapp.com/media/image_clips/5f5b32db2508075aa2848715/original.jpg?1599812314'
        title='更多資訊'
        uptext='品嘗咖啡的同時，也來看看吧'
        labels=['看看手上的咖啡風味','看看鄉民討論','回到主選單']
        texts=['intro','web','menu']
        send_button_message(id,url,title,uptext,labels,texts)
           
    def afterhelper_to_intro(self, event):
        text = event.message.text
        return text.lower() == "intro"    
    
    def afterhelper_to_menu(self, event):
        text = event.message.text
        return text.lower() == "menu"   
    
    def afterhelper_to_web(self, event):
        text = event.message.text
        return text.lower() == "web"      
           
    def on_enter_menu(self, event):
        id=event.source.user_id
        print("on menu")
        url='https://scontent.ftpe7-4.fna.fbcdn.net/v/t39.30808-6/253761785_3111015685786677_4473771224163440542_n.jpg?_nc_cat=107&ccb=1-5&_nc_sid=e3f864&_nc_ohc=F0En4OfnM4QAX9gMVjz&_nc_ht=scontent.ftpe7-4.fna&oh=00_AT9YTab7VUgMzRIUYin097b-hGdHO5WfCq0QT3sTKZjDCA&oe=61D2D8C3'
        title='Menu'
        uptext='歡迎使用咖啡小幫手\n請選擇您想使用的功能'
        labels=['甚麼是精品咖啡','沖煮小幫手','看看鄉民都在討論甚麼吧']
        texts=['intro','helpermenu','web']
        send_button_message(id,url,title,uptext,labels,texts)
        #reply_token = event.reply_token
        #send_text_message(reply_token, "go back to menu")