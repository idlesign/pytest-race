import sys
import logging
from threading import Thread, Event, Barrier
from collections import deque

import pytest


logger = logging.getLogger(__name__)


class RaceThread(Thread):

    def __init__(self, idx, target, events, barrier, args, timeout_interval=10):
        """
        :param int idx:
        :param callable target:
        :param tuple events: (event_start, event_fail, event_done)
        :param threading.Barrier barrier:
        :param int timeout_interval:
        """
        super(RaceThread, self).__init__()

        event_start, event_fail, event_done = events

        self.event_start = event_start
        self.event_fail = event_fail
        self.event_done = event_done
        self.target = target
        self.barrier = barrier
        self.args = args
        self.timeout_interval = timeout_interval

        self.setName('RaceThread %s' % idx)

    def run(self):
        thread_name = self.getName()
        logger.debug('%s waiting...', thread_name)
        self.barrier.wait()

        try:
            # event_start will be set when all other targets are bootstrapped.
            # If that does not happen within the timout interval, raise to
            # avoid a deadlock between main thread and worker threads.
            if not self.event_start.wait(self.timeout_interval):
                raise TimeoutError('%s timouted.', thread_name)

            self.target(**self.args)
            logger.debug('%s run succeed.', thread_name)
        except Exception:
            logger.debug('%s run failed.', thread_name)
            self.event_fail.exc_info = sys.exc_info()
            self.event_fail.set()
            raise

        finally:
            self.event_done.set()


@pytest.fixture
def start_race():
    """Starts a given callable in a given number of threads."""

    def actual_starter(threads_num, target, thread_args=None, barrier_timeout=10):
        """
        :param int threads_num:
        :param callable target:
        :param dict thread_args:
        :param int barrier_timeout:

        """
        event_start = Event()
        event_fail = Event()

        events_available = deque()
        # employ a barrier to synchronize workers and main thread - this means
        # that we need the number of workers + 1 as a wait condition.
        barrier = Barrier(threads_num + 1, timeout=barrier_timeout)

        logger.debug('Preparing clashing threads ...')

        thread_args_ = thread_args or {}
        thread_args = [{} for _ in range(threads_num)]

        for param_name, values in thread_args_.items():
            for idx, value in enumerate(values):
                thread_args[idx][param_name] = value

        for idx in range(1, threads_num+1):
            event_done = Event()
            events_available.appendleft(event_done)

            thread = RaceThread(
                idx,
                target,
                events=(event_start, event_fail, event_done),
                barrier=barrier,
                args=thread_args[idx - 1],
            )

            thread.start()

        logger.debug('Waiting for clashing threads to bootstrap ...')
        barrier.wait()

        logger.debug('All threads boostrapped. Starting clashing threads ...')
        event_start.set()

        while events_available:
            # Waiting for all threads to be done.
            event_done = events_available.pop()

            if event_done.is_set():
                if event_fail.is_set():
                    # Fail fast.
                    exc_info = event_fail.exc_info  # `exc_info` is used by `raise_from`
                    raise exc_info[1]

            else:
                events_available.appendleft(event_done)

        logger.debug('Clashing threads all done.')

    return actual_starter
