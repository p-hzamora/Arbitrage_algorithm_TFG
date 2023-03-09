import time
import re
import os
from threading import Thread  as Thread

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import requests

class KeyGenerator:
    __keys_path = os.path.join(os.getcwd(),'arbitrage','keys.txt')
    __btn_refrescar_correo= '//*[@id="maillist"]/div[1]/a[2]/label'
    __VISIBLE = True        
    __correo = ""
    __html = ""
    __create_keys_manually = False
    __X_POS = 0
    __key = None
        
    def decorator(funcion):
        def tipo(*args,**kargs):
            c = funcion(*args,**kargs)
            os.system('cls')
            print(f'Clave de acceso a API {c}')
            return c
        return tipo    
    
    @classmethod
    def clear(self):
        KeyGenerator.__correo = ""
        KeyGenerator.__html = ""
    
    @staticmethod
    @decorator
    def get_key_api():
        def buscar(html,tipo):
            if tipo == "id":
                search = By.ID
            elif tipo == "class":
                search = By.CLASS_NAME
            elif tipo == "xpath":
                search = By.XPATH
            elif tipo == "css_selector":
                search = By.CSS_SELECTOR
            return (search,html)    

        def clicking(driver,html, tipo ):
            search = buscar(html,tipo)
            wait = WebDriverWait(driver, 10)
            element = wait.until(
                EC.element_to_be_clickable(search)
            )
            element.click()

        def escribir(driver, busqueda, tipo, texto):
            search = buscar(busqueda,tipo)
            wait = WebDriverWait(driver, 10)
            element = wait.until(
                EC.presence_of_element_located(search)
            )
            if element.get_attribute('value') != "":
                element.clear()
            element.send_keys(texto)
        
        def wait_until_get_mail():
            '''
            return URL para obtener una clave valida
            '''
            def click_mssg():
                titulo = ''
                while titulo != 'Confirm Email Address':
                    try:
                        pulsar = driver_mail.find_element(By.XPATH, KeyGenerator.__btn_refrescar_correo)     
                        driver_mail.execute_script("arguments[0].click();",pulsar) 
                        obj = driver_mail.find_element(By.XPATH,'//*[@id="email_message_list"]/div/table/tbody/tr[2]/td[1]')
                        titulo = obj.text
                    except Exception:
                        continue
                    time.sleep(1)
                    obj.click()
                clicking(driver_mail,'//*[@id="email_message_list"]/div/table/tbody/tr[2]/td[1]/a','xpath')
                WebDriverWait(driver_mail,5).until(
                EC.frame_to_be_available_and_switch_to_it((By.XPATH,'//*[@id="page_2"]/div[1]/div[2]/div/div[3]/div[2]/iframe'))
                )
                while len(KeyGenerator.__html) == 0:
                    #obtenemos el link de donde obtendremos la clave
                    KeyGenerator.__html = driver_mail.find_element(By.XPATH,'/html/body').text

            def register_API_web():
                '''
                Registarse en la pagina web de cambio de divisas con HCAPTCHA.
                Una vez finalizado debe enviar un correo de confirmacion.
                '''
                URL = 'https://www.exchangerate-api.com/'
                #__________________OPEN WEB_____________________________    
                ser = Service(ChromeDriverManager().install())
                op = webdriver.ChromeOptions()
                op.add_experimental_option('excludeSwitches', ['enable-automation'])
                driver_key = webdriver.Chrome(  service = ser, options=op, )
                driver_key.get(URL)
                driver_key.set_window_rect(KeyGenerator.__X_POS , 0 , 1040, 900)
                escribir(driver_key,'//*[@id="index_hero_cta_email"]','xpath',KeyGenerator.__correo)
                clicking(driver_key, '//*[@id="index_hero_cta_button"]','xpath')
                escribir(driver_key,'//*[@id="pass"]','xpath',KeyGenerator.__correo)
                clicking(driver_key,'//*[@id="sign_up_cta_button"]','xpath')
                
                
                
                
                #Bypass HCaptcha is necessary def bypass_captcha()
                
                
                
                
                while len(KeyGenerator.__html) == 0:
                    continue
                driver_key.quit()
            
            URL = 'https://www.moakt.com/es'
            #__________________OPEN WEB_____________________________    
            s = Service(ChromeDriverManager().install())
            op = webdriver.ChromeOptions()
            if not KeyGenerator.__VISIBLE: op.add_argument('--headless')   #para evitar ver las paginas que se abren
            op.add_argument('--disable-gpu')    
            op.add_experimental_option('excludeSwitches', ['enable-automation'])
            op.add_experimental_option('useAutomationExtension', False)
            driver_mail = webdriver.Chrome( service = s, options=op)
            driver_mail.get(URL)
            clicking(driver_mail,'//*[@id="mailForm"]/form/input[2]','xpath')

            #Creamos un correo
            KeyGenerator.__correo = driver_mail.find_element(By.ID,'email-address').text
            
            hilo_click_mssg = Thread(target= click_mssg)
            hilo_click_mssg.start()
            register_API_web()

            driver_mail.quit()
            #devuelve URL de la pagina para verificar el correo electronico y obtener la pass
            return re.findall(r'https:.+',KeyGenerator.__html).pop() # el . coge todos los caracteres excepto nueva linea

        def get_key(html):
            '''
            Obtiene una clave para https://v6.exchangerate-api.com/v6/{key}/latest/USD y poder acceder a los datos
            return clave valida
            '''
            URL = html
            #__________________OPEN WEB_____________________________    
            clave = Service(ChromeDriverManager().install())
            op = webdriver.ChromeOptions()
            op.add_experimental_option('excludeSwitches', ['enable-automation'])
            if not KeyGenerator.__VISIBLE: op.add_argument('--headless')
            op.add_argument('--disable-gpu')
            driver_key_final = webdriver.Chrome( service = clave, options=op, )
            driver_key_final.get(URL)
            key = driver_key_final.find_element(By.XPATH,'/html/body/div/div/main/div[2]/div/div[1]/div/div/div/div/h4/strong').text
            driver_key_final.quit()
            return key

        #Comprobar en el archivo de texto si podemos usar algunas de las claves ya generadas
        with open(KeyGenerator.__keys_path, 'r') as kfile:
            all_keys = kfile.read().splitlines()
            temp = [el for el in all_keys[::] if el != '']
        with open(KeyGenerator.__keys_path, 'w') as kfile:
            if not KeyGenerator.__create_keys_manually or len(temp) == 0:
                kfile.seek(0)
                for key in temp:
                    if requests.get(f'https://v6.exchangerate-api.com/v6/{key}/latest/USD').status_code == 200:
                        kfile.writelines(f'\n{g}' for g in temp)
                        KeyGenerator.__key = key
                        return key
                    else:
                        del temp[temp.index(key)]
                        
                KeyGenerator.__html = wait_until_get_mail()
                clave = get_key(KeyGenerator.__html)
                temp.append(clave) 
                kfile.writelines(f'\n{g}' for g in temp)
                KeyGenerator.__key = clave
                return clave
                
            else:
                KeyGenerator.__html = wait_until_get_mail()
                clave = get_key(KeyGenerator.__html)
                temp.append(clave) 
                kfile.writelines(f'\n{g}' for g in temp)
                KeyGenerator.__key = clave
                return clave
   
    @classmethod
    def create_keys_manually(cls):
        KeyGenerator.__create_keys_manually = True
        cls.clear()
        return cls.get_key_api()
    
    @classmethod
    def url(cls):
        key = KeyGenerator.__key
        return f'https://v6.exchangerate-api.com/v6/{key}/latest/USD'
    
if "__main__" == __name__:
    key = KeyGenerator.create_keys_manually()
    a = KeyGenerator.url()
    print(a)