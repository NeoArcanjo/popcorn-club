from apscheduler.schedulers.blocking import BlockingScheduler
from popcorn_club.Spotify.models import updatePlaylists
from popcorn_club.Main.fetch import updateMedialists
import zoneinfo

scheduler = BlockingScheduler(timezone="America/Sao_Paulo")

# @scheduler.scheduled_job('interval', days=1)
scheduler.add_job(updateMedialists, trigger='interval', days=1)

# schedule updates for the TopTracks playlists
scheduler.add_job(updatePlaylists, trigger='interval', days=1)

scheduler.start()
