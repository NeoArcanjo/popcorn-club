from apscheduler.schedulers.background import BackgroundScheduler
from popcorn_club.spotify.models import updatePlaylists
from popcorn_club.club.fetch import updateMedialists
print("Scheduler started")
scheduler = BackgroundScheduler()

# @scheduler.scheduled_job('interval', days=1)
scheduler.add_job(updateMedialists, trigger='interval', days=1)

# schedule updates for the TopTracks playlists
scheduler.add_job(updatePlaylists, trigger='interval', days=1)

@scheduler.scheduled_job('interval', seconds=10)
def printing():
    print("Rodando Tarefa...")
