# importações

from RPA.Browser.Selenium import Selenium
import time


# constantes

URL = "https://blaze-4.com/pt/games/mines?modal=auth&tab=login"



class rotina_principal:
    '''
        Comtempla todos os metodos usados para geração dos sinais a serem enviados para salas vip

        Arguments:
            None           
            
        Keyword Arguments:
            None
        Returns:
            {String} - String com a indicação de entrada
        See:
            funcao acionada: 
                None
            chamada pela funcao:
                None
    
    '''
    
    def __init__(self, url):
        self.browser_lib = Selenium()
        self.url = url


    def abre_site(self):
        self.browser_lib.open_available_browser(self.url)
        self.browser_lib.maximize_browser_window()
        time.sleep(5)

    def fecha_site(self):
        self.browser_lib.close_browser()


    def login(self):
        login_btn_path = "//button[normalize-space()='Entrar']"
        self.browser_lib.wait_until_page_contains_element(locator=login_btn_path)
        input_email_path = "//input[@name='username']"
        self.browser_lib.input_text(input_email_path, email)
        input_senha_path = "//input[@name='password']"
        self.browser_lib.input_text(input_senha_path, senha)
        self.browser_lib.click_element(login_btn_path)


    def main(self):
        self.abre_site()
        self.login()



if __name__ == "__main__":
    obj = rotina_principal(url=URL)
    obj.main()
