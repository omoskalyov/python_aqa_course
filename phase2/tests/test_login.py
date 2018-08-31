#from src.fibonacci.fibonacci import generateFibonacci, errText
import requests


def test_login1():
    payload = {'username': 'Oleg_Moskalyov','password': 'Dizzy32768'}
    r = requests.post('http://jira.hillel.it:8080/rest/auth/1/session',json=payload)
    print(r.status_code)


