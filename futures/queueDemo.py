#
# 在執行緒之間傳送及接收一百萬個物件
#
from concurrent import futures
from concurrent.futures._base import (PENDING, RUNNING, CANCELLED, CANCELLED_AND_NOTIFIED, FINISHED, Future, wait)
#from Queue import Queue
import timeit
import sys

if sys.version_info > (3, 0):
    # Python 3 code in this block
    from queue import (Queue, Empty)
else:
    # Python 2 code in this block
    from Queue import (Queue, Empty)


def create_future(state=PENDING, exception=None, result=None):
    future = Future()
    future._state = state
    future._exception = exception
    future._result = result
    return future


PENDING_FUTURE = create_future(state=PENDING)
RUNNING_FUTURE = create_future(state=RUNNING)
CANCELLED_FUTURE = create_future(state=CANCELLED)
CANCELLED_AND_NOTIFIED_FUTURE = create_future(state=CANCELLED_AND_NOTIFIED)
EXCEPTION_FUTURE = create_future(state=FINISHED, exception=IOError())
SUCCESSFUL_FUTURE = create_future(state=FINISHED, result=42)

q = Queue()

QUEUE_BREAKER = {'IsStop': False}


def producer():
    print('producer enter')
    data = [x for x in range(1024)]
    index = 0
    timer_start = timeit.default_timer()
    for index in range(1000000):
        q.put(data)
    timer_end = timeit.default_timer()
    print('producer exit {} {} {}'.format(index + 1, len(data), (timer_end - timer_start)))
    return True


def consumer(num):
    count = 0
    total = 0
    print('consumer {} enter'.format(num))
    timer_start = timeit.default_timer()
    while True:
        if QUEUE_BREAKER['IsStop'] is False:
            try:
                res = q.get(timeout=1)
                count += 1
                total += len(res)
                if count >= 1000000:
                    print('break')
                    q.task_done()
                    break
            except Empty as e:
                print('{}'.format(repr(e)))
                break
            else:
                q.task_done()
    timer_end = timeit.default_timer()
    print('consumer {} exit {} {}'.format(num, count, (timer_end - timer_start)))
    return True


def main():
    worker = 1
    print('qsize {}'.format(q.qsize()))
    with futures.ThreadPoolExecutor(max_workers=worker + 1) as executor:
        th_producer = executor.submit(producer)
        wait(fs=[SUCCESSFUL_FUTURE, th_producer])
        consumers = []
        for index in range(worker):
            consumers.append(executor.submit(consumer, index))
        wait(fs=[SUCCESSFUL_FUTURE, consumers[0]])
        q.join()
        print('Queue is Empty')
        QUEUE_BREAKER['IsStop'] = True
        executor.shutdown(True)
        print('shutdown')

    print('main exit')
    return 0


if __name__ == '__main__':
    sys.exit(main())
