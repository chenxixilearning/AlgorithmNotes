"""
1、模拟：打印任务
2、构建模型：学生，打印队列，打印机
"""
import random

from queue import Queue


class Printer:
    def __init__(self, ppm: int) -> None:
        """
        初始化 打印速度，任务对象， 单个任务耗时时间
        :param ppm: 打印速度 每分钟5或10页
        """
        # 打印速度
        if ppm not in [5, 10]:
            raise Exception("打印速度参数设置失败")
        self.pageRate = ppm
        # 当前任务对象
        self.currentTask = None
        # 打印耗时
        self.timeRemaining = 0

    # 计时
    def tick(self) -> None:
        """
        任务执行倒计时  每次调用 self.timeRemaining 减一
        :return: None
        """
        if self.currentTask:
            self.timeRemaining -= 1
            if self.timeRemaining <= 0:
                self.currentTask = None

    # 任务状态
    def busy(self) -> bool:
        """
        打印机是否繁忙
        :return: True or False
        """
        return True if self.currentTask else False

    # 开始打印
    def startNext(self, new_task) -> None:  # 获取任务对象  获取执行时间
        """
        打印机开始新的任务
        :param new_task: 任务对象
        :return: None
        """
        self.timeRemaining = new_task.pages * 60 / self.pageRate
        self.currentTask = new_task


class Task:
    def __init__(self, time):
        self._timeStamp = time
        self._pages = random.randrange(1, 21)

    @property
    def pages(self):
        return self._pages

    @property
    def getStamp(self):
        return self._timeStamp

    def waitTime(self, current_time):
        return current_time - self._timeStamp


def simulation(num_seconds=3600, pages_per_minute=5, students=10, ones_max_print=2):
    lab_printer = Printer(pages_per_minute)
    print_queue = Queue()
    waiting_times = []

    for current_second in range(num_seconds):
        if newPrintTask(num_seconds, students, ones_max_print):
            new_task = Task(current_second)
            print_queue.put(new_task)

        if not lab_printer.busy() and not print_queue.empty():
            next_task = print_queue.get()
            waiting_times.append(next_task.waitTime(current_second))
            lab_printer.startNext(next_task)
        lab_printer.tick()
    average_wait = sum(waiting_times) / len(waiting_times)
    print("Average Wait %6.2f secs %3d tasks remaining." % (average_wait, print_queue.qsize()))


def newPrintTask(num_seconds, students, ones_max_print):
    print_with_second = num_seconds / (students * ones_max_print)
    num = random.randrange(1, print_with_second + 1)
    if num == print_with_second:
        return True
    else:
        return False


if __name__ == '__main__':
    for i in range(10):
        simulation()
