# -*- coding: utf-8 -*-
import sys
import logging
from threading import Thread, Event
from collections import deque
from time import sleep

import pytest


PY3 = sys.version_info[0] >= 3

logger = logging.getLogger(__name__)


class RaceThread(Thread):

    def __init__(self, idx, target, events, args):
        """
        :param int idx:
        :param callable target:
        :param tuple events: (event_start, event_fail, event_done)
        """
        super(RaceThread, self).__init__()

        event_start, event_fail, event_done = events

        self.event_start = event_start
        self.event_fail = event_fail
        self.event_done = event_done
        self.target = target
        self.args = args

        self.setName('RaceThread %s' % idx)

    def run(self):
        thread_name = self.getName()

        logger.debug('%s spawned.', thread_name)

        event_start = self.event_start

        while not event_start.is_set():
            if event_start.wait(1):
                logger.debug('%s waiting ...', thread_name)
                sleep(1)

            else:
                logger.debug('%s running ...', thread_name)

                try:
                    self.target(**self.args)
                    logger.debug('%s run succeed.', thread_name)

                except Exception:
                    logger.debug('%s run failed.', thread_name)
                    self.event_fail.exc_info = sys.exc_info()
                    self.event_fail.set()
                    raise

                finally:
                    self.event_done.set()
                    break


@pytest.fixture
def start_race():
    """Starts a given callable in a given number of threads."""

    def actual_starter(threads_num, target, thread_args=None):
        """
        :param int threads_num:
        :param callable target:
        :param dict thread_args:

        """
        event_start = Event()
        event_fail = Event()
        events_avaiable = deque()

        logger.debug('Preparing clashing threads ...')

        thread_args_ = thread_args or {}
        thread_args = [{} for _ in range(threads_num)]

        for param_name, values in thread_args_.items():
            for idx, value in enumerate(values):
                thread_args[idx][param_name] = value

        for idx in range(1, threads_num+1):
            event_done = Event()
            events_avaiable.appendleft(event_done)

            thread = RaceThread(
                idx, target,
                events=(event_start, event_fail, event_done),
                args=thread_args[idx - 1])

            thread.start()

        sleep(1)  # Probably is enough for all threads to bootstrap.

        logger.debug('Starting clashing threads ...')
        event_start.set()

        while events_avaiable:
            # Waiting for all threads to be done.
            event_done = events_avaiable.pop()

            if event_done.is_set():
                if event_fail.is_set():
                    # Fail fast.

                    exc_info = event_fail.exc_info  # `exc_info` is used by `raise_from`

                    # Now it's time for juggling to support `raise from`
                    # both in Python 2 and 3.
                    if PY3:
                        raise exc_info[1]
                    else:
                        exec('raise exc_info[0], exc_info[1], exc_info[2]', globals(), locals())
            else:
                events_avaiable.appendleft(event_done)

        logger.debug('Clashing threads all done.')

    return actual_starter
