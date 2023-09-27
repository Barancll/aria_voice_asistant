# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 23:45:56 2023

@author: bct
"""

import random
from gtts import gTTS
import pygame
import speech_recognition as sr
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os


class Aria:
    
    def __init__(self):
        self.ses_kaydi =None 
    
    
    def seslendirme(self, metin):
        metin_seslendirme = gTTS(text=metin, lang='tr')
        dosya = str(random.randint(0, 1000000000)) + ".mp3"
        metin_seslendirme.save(dosya)
        
        pygame.mixer.init()
        pygame.mixer.music.load(dosya)
        pygame.mixer.music.play()
        self.ses_kaydi = dosya
        
    def mikrofon(self):
        with sr.Microphone() as mic:
            print("Sizi dinliyorum...")
            listen = r.listen(mic)
            ses = ''
            
            try:
                ses = r.recognize_google(listen, language="tr-TR")
            except sr.UnknownValueError:
                self.seslendirme("Söylediğinizi anlayamadım lütfen tekrar eder misiniz")
            return ses
        
    def sesli_karsilik(self, gelen_Ses):
        if "merhaba" in gelen_Ses:
            self.seslendirme("merhaba ben aria size nasıl yardımcı olabilirim")
        
        elif "nasılsın" in gelen_Ses:
            self.seslendirme("ben bir yapay zekayım, duygularım yok")
        
        elif "müzik aç" in gelen_Ses or "video aç" in gelen_Ses:
            
            
            try:
                self.seslendirme("açmak istediğiniz şeyi söyler misiniz")
                cevap = self.mikrofon()
                
                url = "https://www.youtube.com/results?search_query=" + cevap
                tarayici = webdriver.Edge()
                tarayici.get(url)
                
                ilk_video=tarayici.find_element(By.XPATH,"//*[@id='video-title']/yt-formatted-string").click()
                
                time.sleep(5)
                
                self.seslendirme("istediğiniz içerik bu mu ")
                gelen_komut=self.mikrofon()
                if("hayır" in gelen_komut):
                    sayac=2
                    tarayici.back()
                    while (sayac<5):
                        diger_videolar=tarayici.find_element(By.XPATH, "//*[@id='contents']/ytd-video-renderer[{}]".format(sayac)).click()
                        time.sleep(7)
                        self.seslendirme("istediğiniz içerik bu mu")
                        komut=self.mikrofon()
                        if("evet" in komut):
                            self.seslendirme("iyi eğlenceler...")
                            break
                        else:
                            self.seslendirme("o zaman diğer içeriklere bakalım")
                            tarayici.back()
                            sayac+=1
                else:
                    self.seslendirme("iyi eğlenceler...")
                
            except:
                self.seslendirme("bir hata meydana geldi. lütfen daha sonra tekrar deneyiniz")
        
        elif(gelen_Ses in "google aç" or gelen_Ses in "arama yap"):
            self.seslendirme("neye göz atmak istersiniz")
            cevap=self.mikrofon()
            
            url="https://www.google.com.tr/search?q="+cevap
            self.seslendirme("{} ile ilgili bulduğum içerikler bunlar".format(cevap))
            tarayici=webdriver.Edge()
            tarayici.get(url)
            
            site=tarayici.find_element(By.XPATH,"//*[@id='search-result']/li[1]/div/div[2]").click()
            time.sleep(10) 
            tarayici.quit()
            
    def uyanma_fonk(self, gelen_Ses):
        if "hey arya" in gelen_Ses:
            self.seslendirme("merhaba ben arya sizin kişisel asistanınızım size nasıl yardımcı olabilirim.")
            ses = self.mikrofon()
            if ses != "":
                self.sesli_karsilik(ses)
                

# speech_recognition için bir tanımlama yapın
r = sr.Recognizer()
asistan = Aria()

while True:
    gelen_Ses = asistan.mikrofon().lower()
    if gelen_Ses != "":
        print(gelen_Ses)
        asistan.uyanma_fonk(gelen_Ses)

if asistan.ses_kaydi is not None:
        silme_suresi = 60  # Saniye cinsinden bekleme süresi (örnekte 30 saniye)
        time.sleep(silme_suresi)
        os.remove(asistan.ses_kaydi)
        asistan.ses_kaydi = None  # Kaydı temizle


