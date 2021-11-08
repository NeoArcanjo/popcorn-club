from apscheduler.schedulers.background import BackgroundScheduler
from popcorn_club.spotify.models import updatePlaylists
from popcorn_club.club.fetch import updateMedialists
from tzlocal import get_localzone
from datetime import datetime
import zoneinfo
SP = zoneinfo.ZoneInfo("America/Sao_Paulo")

scheduler = BackgroundScheduler()

# @scheduler.scheduled_job('interval', days=1)
scheduler.add_job(updateMedialists, trigger='interval', days=1)

# schedule updates for the TopTracks playlists
scheduler.add_job(updatePlaylists, trigger='interval', days=1)
