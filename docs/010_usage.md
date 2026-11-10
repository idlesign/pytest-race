# Usage

You can use **start_race** fixture in your tests as follows:

```python
from time import sleep

ACCUMULATOR = 0  # This global var is race conditions prone.

def test_race(start_race):
    from random import randint

    def actual_test():
        global ACCUMULATOR

        increment = randint(1, 10000)

        accumulator = ACCUMULATOR
        sleep(1)  # Simulate some lag.
        ACCUMULATOR += increment

        # By that moment ACCUMULATOR should have been updated
        # by another thread. Let's try to prove it.

        # Using simple `assert` as usual for pytest.
        assert accumulator + increment == ACCUMULATOR

    # Let's run `actual_test` in 2 threads.
    start_race(threads_num=2, target=actual_test)
```

**start_race** accepts the following arguments:

* **threads_num** — number of threads to run simultaneously.
* **target** — actual test callable to run in threads.
