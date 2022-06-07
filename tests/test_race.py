pytest_plugins = 'pytester'


def test_race_fixture(testdir):

    testdir.makepyfile("""
        from time import sleep

        ACCUMULATOR = 0

        def test_race(start_race):
            from random import randint

            def actual_test():
                global ACCUMULATOR

                increment = randint(1, 10000)

                accumulator = ACCUMULATOR
                sleep(1)
                ACCUMULATOR += increment

                assert accumulator + increment == ACCUMULATOR

            start_race(threads_num=2, target=actual_test)
    """)

    result = testdir.runpytest('-v')

    assert result.ret == 1  # 1 - failure
    assert 'AssertionError' in result.stdout.str()
