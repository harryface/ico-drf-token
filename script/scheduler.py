from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from script import distributor
from main.models import SiteConfiguration


site_config = SiteConfiguration.objects.filter(distributed=False).first()


def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(distributor.start, 'interval', minutes=2,
    #                   start_date=site_config.end_date, end_date=(site_config.end_date + timezone.timedelta(minutes=1)))
    scheduler.add_job(distributor.start, 'date', run_date=site_config.end_date)
    scheduler.start()