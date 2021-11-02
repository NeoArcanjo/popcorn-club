import schedule
from fetch import get_genres, get_outliers, get_movie, get_tv
from apscheduler.schedulers.background import BackgroundScheduler
import time

scheduler = BackgroundScheduler()

@scheduler.scheduled_job('interval', days=1)
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


@scheduler.scheduled_job('interval', seconds=10)
def job2():
    print("Rodando Tarefa...")

scheduler.start()
