import schedule
import time
from fetch import get_genres, get_outliers, get_movie, get_tv

def job():
    print("Rodando Tarefa...")
    print("Obtendo gêneros...")
    get_genres()
    print("Obtendo destaques...")
    get_outliers()
    print("Obtendo filmes...")
    get_movie()
    print("Obtendo séries...")
    get_tv()

def test_job():
    print("Funcionando...")


schedule.every(10).seconds.do(test_job)
schedule.every().day.at("00:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)