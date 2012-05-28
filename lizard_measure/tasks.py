import logging
from celery.task import task
from lizard_task.task import task_logging
from lizard_measure.runner import run_sync_aquo


@task
@task_logging
def sync_aquo(data_set=None, username=None, taskname=None, loglevel=20):
    logger = logging.getLogger(taskname)
    logger.info("sync_aquo, dataset: %s" % data_set)
    logger.info("Start syncronization of domaintables.")

    run_sync_aquo(logger)
    
    logger.info('Finished')
