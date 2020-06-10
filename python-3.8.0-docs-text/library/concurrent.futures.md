
<!-- vim-markdown-toc GFM -->

* [`concurrent.futures` --- 启动并行任务 19]
	* [`concurrent.futures` 模块提供异步执行回调高层接口。 23]
	* [执行器对象 27]
		* [submit 33]
		* [map 46]
		* [shutdown 72]
	* [ThreadPoolExecutor 96]
	* [ProcessPoolExecutor 193]
	* [期程对象 267]
		* [class concurrent.futures.Future 272]
		* [future 测试方法  331]
	* [模块函数 369]
	* [Exception类 419]

<!-- vim-markdown-toc -->
## `concurrent.futures` --- 启动并行任务 19
> 3.2 新版功能.
> **源码:** Lib/concurrent/futures/thread.py 和Lib/concurrent/futures/process.py

### `concurrent.futures` 模块提供异步执行回调高层接口。 23
> 异步执行可以由 `ThreadPoolExecutor` 使用线程或由 `ProcessPoolExecutor`
使用单独的进程来实现。** 两者都是实现抽像类 `Executor` 定义的接口**。

### 执行器对象 27
1. 抽象类提供异步执行调用方法。要通过它的子类调用，而不是直接调用。
```
class concurrent.futures.Executor
```

#### submit 33
1. submit(fn, *args, **kwargs)

2. 调度可调用对象 *fn*，以 `fn(*args `**`kwargs)` 方式执行并返回
`Future` 对像代表可调用对象的执行。

3. eg
```
with ThreadPoolExecutor(max_workers=1) as executor:
	future = executor.submit(pow, 323, 1235)
	print(future.result())
```

#### map 46
1. map(func, *iterables, timeout=None, chunksize=1)

1. 类似于 `map(func, *iterables)` 除去：
	- 应立即收集 *iterables* 不要延迟再收集;

	- func 是异步执行的且对 func 的调用可以并发执行。

	- 如果 `__next__()` 已被调用且返回的结果在对 `Executor.map()`
	 的原始调用经过 *timeout* 秒后还不可用，则已返回的迭代器将引发
	 `concurrent.futures.TimeoutError`。 *timeout* 可以为 int 或
	 float 类型。 如果 *timeout* 未指定或为 `None`，则不限制等待时
	 间。

	- 如果 *func* 调用引发一个异常，当从迭代器中取回它的值时这个异
	常将被引发。

	- 使用 `ProcessPoolExecutor` 时，这个方法会将 *iterables* 分割
	任务块并作为独立的任务并提交到执行池中。这些块的大概数量可以
	由 *chunksize* 指定正整数设置。 
	
	- 对很长的迭代器来说，使用大的*chunksize* 值比默认值 1 能显著地提高性能。 
	- *chunksize* 对`ThreadPoolExecutor` 没有效果。

	- 在 3.5 版更改: 加入 *chunksize* 参数。

#### shutdown 72
1. shutdown(wait=True)

2. 当待执行的期程完成执行后向执行者发送信号，它就会释放正在使用
的任何资源。调用 `Executor.submit()`会在关闭后触发 `RuntimeError`。

3. 如果 *wait* 为 `True` 则**此方法只有在所有待执行的期程完成执行
且释放已分配的资源后才会返回**。 

4. 如果 *wait* 为 `False`，方法立即返回，所有待执行的期程完成执行后会释放已分
配的资源。 <font color=red>不管*wait* 的值是什么，整个 Python 程序将等到所有待执行的期程完成
执行后才退出</font>。

5. 如果使用 `with` 语句，你就可以避免显式调用这个方法，它将会停止 `Executor` 
(就好像 `Executor.shutdown()` 调用时 *wait* 设为 `True` 一样等待):
```
import shutil
with ThreadPoolExecutor(max_workers=4) as e:
	e.submit(shutil.copy, 'src1.txt', 'dest1.txt')
	e.submit(shutil.copy, 'src2.txt', 'dest2.txt')
	e.submit(shutil.copy, 'src3.txt', 'dest3.txt')
	e.submit(shutil.copy, 'src4.txt', 'dest4.txt')
```

### ThreadPoolExecutor 96
1. `ThreadPoolExecutor` 是 `Executor` 的子类，它使用线程池来异步执行调用

2. 当回调已关联了一个 `Future` 然后再等待另一个 `Future` 的结果时就会发生
死锁情况。 例如:
```
import time
def wait_on_b():
   time.sleep(5)
   print(b.result())  # b will never complete because it is waiting on a.
   return 5

   def wait_on_a():
       time.sleep(5)
       print(a.result())  # a will never complete because it is waiting on b.
       return 6


   executor = ThreadPoolExecutor(max_workers=2)
   a = executor.submit(wait_on_b)
   b = executor.submit(wait_on_a)

And:

   def wait_on_future():
       f = executor.submit(pow, 5, 2)
       # This will never complete because there is only one worker thread and
       # it is executing this function.
       print(f.result())

   executor = ThreadPoolExecutor(max_workers=1)
   executor.submit(wait_on_future)
```
3. <font color=green>所以使用ThreadPoolExecutor时,必须要显示的唤醒一个线程,否则没人使用codition.notify的话,
	即使只有一个任务,没有set result的话,也会陷入死锁.</font>

4. class ThreadPoolExecutor:
	1. class concurrent.futures.ThreadPoolExecutor(max_workers=None,
				thread_name_prefix='', initializer=None, initargs=())

	2. `Executor` 的一个子类，使用最多 *max_workers* 个线程的线程池来异步
	执行调用。

	3. 参数 
		- initializer 是在每个工作者线程开始处调用的一个可选可调用对象。

		- initargs 是传递给初始化器的元组参数。

		- 任何向池提交更多工作的尝试，initializer 都将引发一个异常，
		当前所有等待的工作都会引发一个`BrokenThreadPool`。

	4. 在 3.5 版更改: 如果 *max_workers* 为 `None` 或没有指定，将默认为机
	   器处理器的个数，假如 `ThreadPoolExecutor` 则重于 I/O 操作而不是 CPU
	   运算，那么可以乘以 `5`，同时工作线程的数量可以比
	   `ProcessPoolExecutor` 的数量高。

	5. 3.6 新版功能: 添加 *thread_name_prefix* 参数允许用户控制由线程池创
	   建的 `threading.Thread` 工作线程名称以方便调试。

	6. 在 3.7 版更改: 加入 *initializer* 和*initargs* 参数。

	7. 在 3.8 版更改: *max_workers* 的默认值已改为 `min(32, os.cpu_count()+ 4)`。 
	   这个默认值会保留至少 5 个工作线程用于 I/O 密集型任务。 它会
	   使用至多 32 个 CPU 核心用于 CPU 密集型任务并将释放 GIL。 它还会避免
	   在多核机器上隐式地使用非常大量的资源。现在 ThreadPoolExecutor 在启
	   动 *max_workers* 个工作线程之前也会重用空闲的工作线程。

5.  ThreadPoolExecutor 例子
```
import concurrent.futures
import urllib.request

URLS = ['http://www.foxnews.com/',
	   'http://www.cnn.com/',
	   'http://europe.wsj.com/',
	   'http://www.bbc.co.uk/',
	   'http://some-made-up-domain.com/']

# Retrieve a single page and report the URL and contents 174
def load_url(url, timeout):
   with urllib.request.urlopen(url, timeout=timeout) as conn:
	   return conn.read()

# We can use a with statement to ensure threads are cleaned up promptly 179
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
   # Start the load operations and mark each future with its URL
   future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
   for future in concurrent.futures.as_completed(future_to_url):
	   url = future_to_url[future]
	   try:
		   data = future.result()
	   except Exception as exc:
		   print('%r generated an exception: %s' % (url, exc))
	   else:
		   print('%r page is %d bytes' % (url, len(data)))
```

### ProcessPoolExecutor 193
1. `ProcessPoolExecutor` 是 `Executor` 的子类，它使用进程池来实现异步执行调用。 

2. `ProcessPoolExecutor` 使用 `multiprocessing` 回避 *Global
	Interpreter Lock* 但也意味着**只可以处理和返回可序列化的对象**。

3. `__main__` <font color=green>模块必须可以被工作者子进程导入</font>。这意味着
`ProcessPoolExecutor` **不可以工作在交互式解释器中**。

4. 从提交给 `ProcessPoolExecutor` 的回调中调用 `Executor` 或 `Future` 方法会<font color=red>导致死锁</font>。

5. class
	1. class concurrent.futures.ProcessPoolExecutor(max_workers=None, 
				mp_context=None, initializer=None, initargs=())

	2. 异步执行调用的 `Executor` 子类使用一个最多有 *max_workers* 个进程的进程池。 
	如果 *max_workers* 为 `None` 或未给出，它将**默认为机器的处理器个数**。 
	如果 *max_workers* 小于等于 `0`，则将引发 `ValueError`。
	在 Windows 上，*max_workers* 必须小于等于 `61`，否则将引发
	`ValueError`。 如果 *max_workers* 为 `None`，则所选择的默认最多为
	`61`，即使存在更多处理器。 
	
	3. *mp_context* 可以是一个多进程上下文或是None。 它将被用来启动工作者。 
	如果 *mp_context* 为 `None` 或未给出，将使用默认的多进程上下文。

	4. *initializer* 是在每个工作者进程开始处调用的一个可选可调用对象。
	*initargs* 是传递给初始化器的元组参数。任何向池提交更多工作的尝试，
	*initializer* 都将引发一个异常，当前所有等待的工作都会引发一个
	`BrokenProcessPool`。

	5. 在 3.3 版更改: 如果其中一个工作进程被突然终止，`BrokenProcessPool`
	就会马上触发。可预计的行为没有定义，但执行器上的操作或它的期程会被
	冻结或死锁。

	6. 在 3.7 版更改: 添加 *mp_context* 参数允许用户控制由进程池创建给工作
	者进程的开始方法 。加入 *initializer* 和*initargs* 参数。


6. ProcessPoolExecutor 例子
```
import concurrent.futures
import math

PRIMES = [
   112272535095293,
   112582705942171,
   112272535095293,
   115280095190773,
   115797848077099,
   1099726899285419]

def is_prime(n):
   if n < 2:
	   return False
   if n == 2:
	   return True
   if n % 2 == 0:
	   return False

   sqrt_n = int(math.floor(math.sqrt(n)))
   for i in range(3, sqrt_n + 1, 2):
	   if n % i == 0:
		   return False
   return True

def main():
   with concurrent.futures.ProcessPoolExecutor() as executor:
	   for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
		   print('%d is prime: %s' % (number, prime))

if __name__ == '__main__':
   main()
```

### 期程对象 267
1. Future 类将可调用对象封装为异步执行。**Future 实例由Executor.submit() 创建**。
map返回一个迭代器对象,不是future,而是在迭代器中的next方法中对future执行result.


#### class concurrent.futures.Future 272
> 将可调用对象封装为异步执行。`Future` 实例由 `Executor.submit()` 
创建，除非测试，不应直接创建。

1. cancel()

	尝试取消调用。 如果调用正在执行或已结束运行不能被取消则该方法
	将返回 `False`，否则调用会被取消并且该方法将返回 `True`。

2. cancelled()

	如果调用成功取消返回 `True`。

3. running()

	如果调用正在执行而且不能被取消那么返回``True``。

4. done()

	如果调用已被取消或正常结束那么返回 `True`。

5. result(timeout=None)

	1. 返回调用返回的值。如果调用还没完成那么这个方法将等待
	*timeout* 秒。如果在 *timeout* 秒内没有执行完成，
	`concurrent.futures.TimeoutError` 将会被触发。

	2. *timeout* 可以是整数或浮点数。如果 *timeout* 没有指定或为
	`None`，那么等待时间就没有限制。

	3. 如果 futrue 在完成前被取消则 `CancelledError` 将被触发。

	4. 如果调用引发了一个异常，这个方法也会引发同样的异常。

6. exception(timeout=None)

	1. 返回由调用引发的异常。如果调用还没完成那么这个方法将等待
	*timeout* 秒。如果在 *timeout* 秒内没有执行完成，
	`concurrent.futures.TimeoutError` 将会被触发。*timeout* 可以
	是整数或浮点数。

	2. 如果 *timeout* 没有指定或为 `None`，那么等待时间就没有限制。

	3. 如果 futrue 在完成前被取消则 `CancelledError` 将被触发。

	4. 如果调用正常完成那么返回 `None`。

7. add_done_callback(fn)

	1. 附加可调用 *fn* 到期程。当期程被取消或完成运行时，将会调用
	*fn*，**而这个期程将作为它唯一的参数**。

	2. 加入的可调用对象总被属于添加它们的进程中的线程按加入的顺序调
	用。如果可调用对象引发一个 `Exception` 子类，它会被记录下来并
	被忽略掉。如果可调用对象引发一个 `BaseException` 子类，这个行
	为没有定义。

	3. 如果期程已经完成或已取消，*fn* 会被立即调用。

#### future 测试方法  331
> 下面这些 `Future` 方法用于单元测试和 `Executor` 实现。

1. set_running_or_notify_cancel()

	1. 这个方法只可以在执行关联 `Future`  工作之前由 `Executor` 实现
调用或由单测试调用。

	2. 如果这个方法返回  `False` 那么 `Future` 已被取消，即
`Future.cancel()` 已被调用并返回 `True` 。**等待 `Future` 完成
(即通过 `as_completed()` 或 `wait()`) 的线程将被唤醒**。

	3. 如果这个方法返回 `True` 那么 `Future` 不会被取消并已将它变为
正在运行状态，也就是说调用 `Future.running()` 时将返回 *True*

	4. 这个方法只可以被调用一次并且不能在调用 `Future.set_result()`
或 `Future.set_exception()` 之后再调用。

	5. 这个函数是用来启动或者取消函数的,放置future阻塞的.

2. set_result(result)

	1. 设置将 `Future` 关联工作的结果给 *result* 。

	2. 这个方法只可以由 `Executor` 实现和单元测试使用。

	3. 在 3.8 版更改: 如果 `Future` 已经完成则此方法会引发
	`concurrent.futures.InvalidStateError`。

3. set_exception(exception)

	1. 设置 `Future` 关联工作的结果给 `Exception` *exception* 。

	2. 这个方法只可以由 `Executor` 实现和单元测试使用。

	3. 在 3.8 版更改: 如果 `Future` 已经完成则此方法会引发
	`concurrent.futures.InvalidStateError`。

### 模块函数 369
1. concurrent.futures.wait(fs, timeout=None, return_when=ALL_COMPLETED)

	1. 等待 *fs* 指定的 `Future` 实例队列（可能由不同的 `Executor` 实例创建）完成。 

	2. 返回一个由集合构成的具名  2 元组。 

		- 第一个集合名称为 `done`，包含在等待完成之前已完成的期程
		（包括正常结束或被取消的期程）。 

		- 第二个集合名称为 `not_done`，包含未完成的期程（包括挂起的或正在运行的期程）。

	3. *timeout* 可以用来控制返回前最大的等待秒数。 *timeout* 可以为 int
	或 float 类型。 如果 *timeout* 未指定或为 `None` ，则不限制等待时间

	4. *return_when* 指定此函数应在何时返回。它必须为以下常数之一:
	```
	+-------------------------------+------------------------------------------+
	| 常数                          | 描述                                     |
	|===============================|==========================================|
	| `FIRST_COMPLETED`             | 函数将在任意可等待对象结束或取消时返回。 |
	+-------------------------------+------------------------------------------+
	| `FIRST_EXCEPTION`             | 函数将在任意可等待对象因引发异常而结束时 |
	|                               | 返回。当没有引发任何异常时 它就相当于    |
	|                               | `ALL_COMPLETED`。                        |
	+-------------------------------+------------------------------------------+
	| `ALL_COMPLETED`               | 函数将在所有可等待对象结束或取消时返回。 |
	+-------------------------------+------------------------------------------+
	```

2. concurrent.futures.as_completed(fs, timeout=None)

	1. 返回一个包含 *fs* 所指定的 `Future` 实例（可能由不同的 `Executor`
	实例创建）的迭代器，这些实例会在完成时生成期程（包括正常结束或被取
	消的期程）。 
	
	2. 任何由 *fs* 所指定的重复期程将只被返回一次。 
	
	3. 任何在`as_completed()` 被调用之前完成的期程将优先被生成。 
	
	4. 如果`__next__()` 被调用并且在对 `as_completed()` 的原始调用 *timeout*
	秒之后结果仍不可用，则返回的迭代器将引发`concurrent.futures.TimeoutError`。 
	
	5. *timeout* 可以为整数或浮点数。
	如果 *timeout* 未指定或为 `None`，则不限制等待时间。

3. 参见:

	**PEP 3148** -- futures - 异步执行指令。该提案描述了Python标准库中包含的这个特性。

### Exception类 419
1. exception concurrent.futures.CancelledError

	future被取消时会触发。

2. exception concurrent.futures.TimeoutError

	future运算超出给定的超时数值时触发。

3. exception concurrent.futures.BrokenExecutor

	当执行器被某些原因中断而且不能用来提交或执行新任务时就会被引发派生
	于 `RuntimeError` 的异常类。

	3.7 新版功能.

4. exception concurrent.futures.InvalidStateError

	当某个操作在一个当前状态所不允许的 future 上执行时将被引发。
	3.8 新版功能.

5. exception concurrent.futures.thread.BrokenThreadPool

	当 `ThreadPoolExecutor` 中的其中一个工作者初始化失败时会引发派生于
	`BrokenExecutor` 的异常类。

	3.7 新版功能.

6. exception concurrent.futures.process.BrokenProcessPool

	当 `ThreadPoolExecutor` 中的其中一个工作者不完整终止时(比如，被外部
	杀死)会引发派生于 `BrokenExecutor` ( 原名 `RuntimeError` ) 的异常类

   3.3 新版功能.
