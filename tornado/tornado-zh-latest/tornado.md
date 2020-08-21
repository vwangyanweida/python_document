# Tornado

## Tornado Web Server
1. ``Tornado 是一个Python web框架和异步网络库，起初由 FriendFeed 开发. 通过使用非阻塞网络I/O，
Tornado可以支撑上万级的连接，处理长连接, WebSockets ，和其他需要与每个用户保持长久连接的应用.

### Hello, world
1. 这是一个简单的Tornado的web应用:
````````
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

这个例子没有使用Tornado的任何异步特性;了解详情请看 simple chat room.

安装¶

自动安装:

pip install tornado

Tornado在 PyPI 列表中，可以使用 pip 或 easy_install 安装. 注意源码发布中包含的示例应用可能不会出
现在这种方式安装的代码中，所以你也可能希望通过下载一份源码包的拷贝来进行安装.

手动安装: 下载当前4.3版本:

tar xvzf tornado-4.3.tar.gz
cd tornado-4.3
python setup.py build
sudo python setup.py install

Tornado的源码托管在 hosted on GitHub.

Prerequisites: Tornado 4.3 运行在Python 2.6, 2.7, 和 3.2+ (对Python 2.6 和 3.2的支持是不推荐的并
将在下个版本中移除). 对Python 2的2.7.9或更新版强烈推荐提高对SSL支持. 另外Tornado的依赖包可能通过
pip or setup.py install 被自动安装, 下面这些可选包可能是有用的:

  • unittest2 是用来在Python 2.6上运行Tornado的测试用例的(更高版本的Python是不需要的)
  • concurrent.futures 是推荐配合Tornado使用的线程池并且可以支持
    tornado.netutil.ThreadedResolver 的用法. 它只在Python 2中被需要，Python 3已经包括了这个标准
    库.
  • pycurl 是在 tornado.curl_httpclient 中可选使用的.需要Libcurl 7.19.3.1 或更高版本;推荐使用
    7.21.1或更高版本.
  • Twisted 会在 tornado.platform.twisted 中使用.
  • pycares 是一个当线程不适用情况下的非阻塞DNS解决方案.
  • Monotime 添加对monotonic clock的支持,当环境中的时钟被频繁调整的时候，改善其可靠性. 在Python
    3.3中不再需要.

平台: Tornado可以运行在任何类Unix平台上,虽然为了最好的性能和可扩展性只有Linux(使用 epoll)和BSD
(使用 kqueue)是推荐的产品部署环境(尽管Mac OS X通过BSD发展来并且支持kqueue,但它的网络质量很差，所
以它只适合开发使用) Tornado也可以运行在Windows上，虽然它的配置不是官方支持的,同时也仅仅推荐开发
使用.

文档¶

这个文档同时也提供 PDF 和 Epub 格式.

用户指南¶

介绍¶

Tornado 是一个Python web框架和异步网络库起初由 FriendFeed 开发. 通过使用非阻塞网络I/O, Tornado
可以支持上万级的连接，处理长连接, WebSockets, 和其他需要与每个用户保持长久连接的应用.

Tornado 大体上可以被分为4个主要的部分:

  • web框架 (包括创建web应用的 RequestHandler 类，还有很多其他支持的类).
  • HTTP的客户端和服务端实现 (HTTPServer and AsyncHTTPClient).
  • 异步网络库 (IOLoop and IOStream), 为HTTP组件提供构建模块，也可以用来实现其他协议.
  • 协程库 (tornado.gen) 允许异步代码写的更直接而不用链式回调的方式.

Tornado web 框架和HTTP server 一起为 WSGI 提供了一个全栈式的选择. 在WSGI容器 (WSGIAdapter) 中使
用Tornado web框架或者使用Tornado HTTP server 作为一个其他WSGI框架(WSGIContainer)的容器,这样的组
合方式都是有局限性的. 为了充分利用Tornado的特性,你需要一起使用Tornado的web框架和HTTP server.

异步和非阻塞I/O¶

实时web功能需要为每个用户提供一个多数时间被闲置的长连接, 在传统的同步web服务器中，这意味着要为每
个用户提供一个线程, 当然每个线程的开销都是很昂贵的.

为了尽量减少并发连接造成的开销，Tornado使用了一种单线程事件循环的方式. 这就意味着所有的应用代码
都应该是异步非阻塞的, 因为在同一时间只有一个操作是有效的.

异步和非阻塞是非常相关的并且这两个术语经常交换使用,但它们不是完全相同的事情.

阻塞¶

一个函数在等待某些事情的返回值的时候会被阻塞. 函数被阻塞的原因有很多: 网络I/O,磁盘I/O,互斥锁等.
事实上每个函数在运行和使用CPU的时候都或多或少会被阻塞(举个极端的例子来说明为什么对待CPU阻塞要和
对待一般阻塞一样的严肃: 比如密码哈希函数 bcrypt, 需要消耗几百毫秒的CPU时间,这已经远远超过了一般
的网络或者磁盘请求时间了).

一个函数可以在某些方面阻塞在另外一些方面不阻塞.例如, tornado.httpclient 在默认的配置下,会在DNS解
析上面阻塞,但是在其他网络请求的时候不阻塞 (为了减轻这种影响，可以用 ThreadedResolver 或者是通过
正确配置 libcurl 用 tornado.curl_httpclient 来做). 在Tornado的上下文中,我们一般讨论网络I/O上下文
的阻塞,尽管各种阻塞已经被最小化.

异步¶

异步函数在会在完成之前返回，在应用中触发下一个动作之前通常会在后台执行一些工作(和正常的同步函数
在返回前就执行完所有的事情不同).这里列举了几种风格的异步接口:

  • 回调参数
  • 返回一个占位符 (Future, Promise, Deferred)
  • 传送给一个队列
  • 回调注册表 (POSIX信号)

不论使用哪种类型的接口, 按照定义异步函数与它们的调用者都有着不同的交互方式;也没有什么对调用者透
明的方式使得同步函数异步(类似 gevent 使用轻量级线程的系统性能虽然堪比异步系统,但它们并没有真正的
让事情异步).

例子¶

一个简单的同步函数:

from tornado.httpclient import HTTPClient

def synchronous_fetch(url):
    http_client = HTTPClient()
    response = http_client.fetch(url)
    return response.body

把上面的例子用回调参数重写的异步函数:

from tornado.httpclient import AsyncHTTPClient

def asynchronous_fetch(url, callback):
    http_client = AsyncHTTPClient()
    def handle_response(response):
        callback(response.body)
    http_client.fetch(url, callback=handle_response)

使用 Future 代替回调:

from tornado.concurrent import Future

def async_fetch_future(url):
    http_client = AsyncHTTPClient()
    my_future = Future()
    fetch_future = http_client.fetch(url)
    fetch_future.add_done_callback(
        lambda f: my_future.set_result(f.result()))
    return my_future

Future 版本明显更加复杂，但是 Futures 却是Tornado中推荐的写法因为它有两个主要的优势.首先是错误处
理更加一致,因为 Future.result 方法可以简单的抛出异常(相较于常见的回调函数接口特别指定错误处理),
而且 Futures 很适合和协程一起使用.协程会在后面深入讨论.这里是上面例子的协程版本,和最初的同步版本
很像:

from tornado import gen

@gen.coroutine
def fetch_coroutine(url):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)
    raise gen.Return(response.body)

raise gen.Return(response.body) 声明是在Python 2 (and 3.2)下人为执行的, 因为在其中生成器不允许返
回值.为了克服这个问题,Tornado的协程抛出一种特殊的叫 Return 的异常. 协程捕获这个异常并把它作为返
回值. 在Python 3.3和更高版本,使用 return response.body 有相同的结果.

协程¶

Tornado中推荐使用协程写异步代码. 协程使用了Python的 yield 关键字代替链式回调来将程序挂起和恢复执
行(像在 gevent 中出现的轻量级线程合作方式有时也被称为协程, 但是在Tornado中所有的协程使用明确的上
下文切换,并被称为异步函数).

使用协程几乎像写同步代码一样简单, 并且不需要浪费额外的线程. 它们还通过减少上下文切换来使并发编程
更简单 .

例子:

from tornado import gen

@gen.coroutine
def fetch_coroutine(url):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)
    # 在Python 3.3之前, 在generator中是不允许有返回值的
    # 必须通过抛出异常来代替.
    # 就像 raise gen.Return(response.body).
    return response.body

Python 3.5: async and await¶

Python 3.5 引入了 async 和 await 关键字(使用这些关键字的函数也被称为”原生协程”). 从Tornado 4.3,
你可以用它们代替 yield 为基础的协程. 只需要简单的使用 async def foo() 在函数定义的时候代替 
@gen.coroutine 装饰器, 用 await 代替yield. 本文档的其他部分会继续使用 yield 的风格来和旧版本的
Python兼容, 但是如果 async 和 await 可用的话，它们运行起来会更快:

async def fetch_coroutine(url):
    http_client = AsyncHTTPClient()
    response = await http_client.fetch(url)
    return response.body

await 关键字比 yield 关键字功能要少一些. 例如,在一个使用 yield 的协程中，你可以得到 Futures 列
表, 但是在原生协程中,你必须把列表用 tornado.gen.multi 包起来. 你也可以使用
tornado.gen.convert_yielded 来把任何使用 yield 工作的代码转换成使用 await 的形式.

虽然原生协程没有明显依赖于特定框架(例如它们没有使用装饰器,例如 tornado.gen.coroutine 或
asyncio.coroutine), 不是所有的协程都和其他的兼容. 有一个协程执行者(coroutine runner) 在第一个协
程被调用的时候进行选择, 然后被所有用 await 直接调用的协程共享. Tornado 的协程执行者(coroutine
runner)在设计上是多用途的,可以接受任何来自其他框架的awaitable对象; 其他的协程运行时可能有很多限
制(例如, asyncio 协程执行者不接受来自其他框架的协程). 基于这些原因,我们推荐组合了多个框架的应用
都使用Tornado的协程执行者来进行协程调度. 为了能使用Tornado来调度执行asyncio的协程, 可以使用
tornado.platform.asyncio.to_asyncio_future 适配器.

它是如何工作的¶

包含了 yield 关键字的函数是一个生成器(generator). 所有的生成器都是异步的; 当调用它们的时候,会返
回一个生成器对象,而不是一个执行完的结果. @gen.coroutine 装饰器通过 yield 表达式和生成器进行交流,
而且通过返回一个 Future 与协程的调用方进行交互.

下面是一个协程装饰器内部循环的简单版本:

# tornado.gen.Runner 简化的内部循环
def run(self):
    # send(x) makes the current yield return x.
    # It returns when the next yield is reached
    future = self.gen.send(self.next)
    def callback(f):
        self.next = f.result()
        self.run()
    future.add_done_callback(callback)

装饰器从生成器接收一个 Future 对象, 等待(非阻塞的)这个 Future 对象执行完成, 然后”解开(unwraps)”
这个 Future 对象，并把结果作为 yield 表达式的结果传回给生成器. 大多数异步代码从来不会直接接触
Future 类除非 Future 立即通过异步函数返回给 yield 表达式.

如何调用协程¶

协程一般不会抛出异常: 它们抛出的任何异常将被 Future 捕获直到它被得到. 这意味着用正确的方式调用协
程是重要的, 否则你可能有被忽略的错误:

@gen.coroutine
def divide(x, y):
    return x / y

def bad_call():
    # 这里应该抛出一个 ZeroDivisionError 的异常, 但事实上并没有
    # 因为协程的调用方式是错误的.
    divide(1, 0)

几乎所有的情况下, 任何一个调用协程的函数都必须是协程它自身, 并且在调用的时候使用 yield 关键字.
当你复写超类中的方法, 请参阅文档, 看看协程是否支持(文档应该会写该方法 “可能是一个协程” 或者 “可
能返回一个 Future ”):

@gen.coroutine
def good_call():
    # yield 将会解开 divide() 返回的 Future 并且抛出异常
    yield divide(1, 0)

有时你可能想要对一个协程”一劳永逸”而且不等待它的结果. 在这种情况下, 建议使用
IOLoop.spawn_callback, 它使得 IOLoop 负责调用. 如果它失败了, IOLoop 会在日志中把调用栈记录下来:

# IOLoop 将会捕获异常,并且在日志中打印栈记录.
# 注意这不像是一个正常的调用, 因为我们是通过
# IOLoop 调用的这个函数.
IOLoop.current().spawn_callback(divide, 1, 0)

最后, 在程序顶层, 如果 `.IOLoop` 尚未运行, 你可以启动 IOLoop, 执行协程,然后使用 IOLoop.run_sync
方法停止 IOLoop . 这通常被用来启动面向批处理程序的 main 函数:

# run_sync() 不接收参数,所以我们必须把调用包在lambda函数中.
IOLoop.current().run_sync(lambda: divide(1, 0))

协程模式¶

结合 callback¶

为了使用回调而不是 Future 与异步代码进行交互, 把调用包在 Task 中. 这将为你添加一个回调参数并且返
回一个可以yield的 Future :

@gen.coroutine
def call_task():
    # 注意这里没有传进来some_function.
    # 这里会被Task翻译成
    #   some_function(other_args, callback=callback)
    yield gen.Task(some_function, other_args)

调用阻塞函数¶

从协程调用阻塞函数最简单的方式是使用 ThreadPoolExecutor, 它将返回和协程兼容的 Futures

thread_pool = ThreadPoolExecutor(4)

@gen.coroutine
def call_blocking():
    yield thread_pool.submit(blocking_func, args)

并行¶

协程装饰器能识别列表或者字典对象中各自的 Futures, 并且并行的等待这些 Futures :

@gen.coroutine
def parallel_fetch(url1, url2):
    resp1, resp2 = yield [http_client.fetch(url1),
                          http_client.fetch(url2)]

@gen.coroutine
def parallel_fetch_many(urls):
    responses = yield [http_client.fetch(url) for url in urls]
    # 响应是和HTTPResponses相同顺序的列表

@gen.coroutine
def parallel_fetch_dict(urls):
    responses = yield {url: http_client.fetch(url)
                        for url in urls}
    # 响应是一个字典 {url: HTTPResponse}

交叉存取¶

有时候保存一个 Future 比立即yield它更有用, 所以你可以在等待之前执行其他操作:

@gen.coroutine
def get(self):
    fetch_future = self.fetch_next_chunk()
    while True:
        chunk = yield fetch_future
        if chunk is None: break
        self.write(chunk)
        fetch_future = self.fetch_next_chunk()
        yield self.flush()

循环¶

协程的循环是棘手的, 因为在Python中没有办法在 for 循环或者 while 循环 yield 迭代器,并且捕获yield
的结果. 相反,你需要将循环条件从访问结果中分离出来, 下面是一个使用 Motor 的例子:

import motor
db = motor.MotorClient().test

@gen.coroutine
def loop_example(collection):
    cursor = db.collection.find()
    while (yield cursor.fetch_next):
        doc = cursor.next_object()

在后台运行¶

PeriodicCallback 通常不使用协程. 相反,一个协程可以包含一个 while True: 循环并使用
tornado.gen.sleep:

@gen.coroutine
def minute_loop():
    while True:
        yield do_something()
        yield gen.sleep(60)

# Coroutines that loop forever are generally started with
# spawn_callback().
IOLoop.current().spawn_callback(minute_loop)

有时可能会遇到一个更复杂的循环. 例如, 上一个循环运行每次花费 60+N 秒, 其中 N 是 do_something()
花费的时间. 为了准确的每60秒运行,使用上面的交叉模式:

@gen.coroutine
def minute_loop2():
    while True:
        nxt = gen.sleep(60)   # 开始计时.
        yield do_something()  # 计时后运行.
        yield nxt             # 等待计时结束.

Queue 示例 - 一个并发网络爬虫¶

Tornado的 tornado.queues 模块实现了异步生产者/消费者模式的协程, 类似于通过Python 标准库的 queue
实现线程模式.

一个yield Queue.get 的协程直到队列中有值的时候才会暂停. 如果队列设置了最大长度 yield Queue.put
的协程直到队列中有空间才会暂停.

一个 Queue 从0开始对完成的任务进行计数. put 加计数; task_done 减少计数.

这里的网络爬虫的例子, 队列开始的时候只包含 base_url. 当一个worker抓取到一个页面它会解析链接并把
它添加到队列中, 然后调用 task_done 减少计数一次. 最后, 当一个worker抓取到的页面URL都是之前抓取到
过的并且队列中没有任务了. 于是worker调用 task_done 把计数减到0. 等待 join 的主协程取消暂停并且完
成.

import time
from datetime import timedelta

try:
    from HTMLParser import HTMLParser
    from urlparse import urljoin, urldefrag
except ImportError:
    from html.parser import HTMLParser
    from urllib.parse import urljoin, urldefrag

from tornado import httpclient, gen, ioloop, queues

base_url = 'http://www.tornadoweb.org/en/stable/'
concurrency = 10


@gen.coroutine
def get_links_from_url(url):
    """Download the page at `url` and parse it for links.

    Returned links have had the fragment after `#` removed, and have been made
    absolute so, e.g. the URL 'gen.html#tornado.gen.coroutine' becomes
    'http://www.tornadoweb.org/en/stable/gen.html'.
    """
    try:
        response = yield httpclient.AsyncHTTPClient().fetch(url)
        print('fetched %s' % url)

        html = response.body if isinstance(response.body, str) \
            else response.body.decode()
        urls = [urljoin(url, remove_fragment(new_url))
                for new_url in get_links(html)]
    except Exception as e:
        print('Exception: %s %s' % (e, url))
        raise gen.Return([])

    raise gen.Return(urls)


def remove_fragment(url):
    pure_url, frag = urldefrag(url)
    return pure_url


def get_links(html):
    class URLSeeker(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.urls = []

        def handle_starttag(self, tag, attrs):
            href = dict(attrs).get('href')
            if href and tag == 'a':
                self.urls.append(href)

    url_seeker = URLSeeker()
    url_seeker.feed(html)
    return url_seeker.urls


@gen.coroutine
def main():
    q = queues.Queue()
    start = time.time()
    fetching, fetched = set(), set()

    @gen.coroutine
    def fetch_url():
        current_url = yield q.get()
        try:
            if current_url in fetching:
                return

            print('fetching %s' % current_url)
            fetching.add(current_url)
            urls = yield get_links_from_url(current_url)
            fetched.add(current_url)

            for new_url in urls:
                # Only follow links beneath the base URL
                if new_url.startswith(base_url):
                    yield q.put(new_url)

        finally:
            q.task_done()

    @gen.coroutine
    def worker():
        while True:
            yield fetch_url()

    q.put(base_url)

    # Start workers, then wait for the work queue to be empty.
    for _ in range(concurrency):
        worker()
    yield q.join(timeout=timedelta(seconds=300))
    assert fetching == fetched
    print('Done in %d seconds, fetched %s URLs.' % (
        time.time() - start, len(fetched)))


if __name__ == '__main__':
    import logging
    logging.basicConfig()
    io_loop = ioloop.IOLoop.current()
    io_loop.run_sync(main)

Tornado web应用的结构¶

通常一个Tornado web应用包括一个或者多个 RequestHandler 子类, 一个可以将收到的请求路由到对应
handler的 Application 对象,和一个启动服务的 main() 函数.

一个最小的”hello world”例子就像下面这样:

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

Application 对象¶

Application 对象是负责全局配置的, 包括映射请求转发给处理程序的路由表.

路由表是 URLSpec 对象(或元组)的列表, 其中每个都包含(至少)一个正则表达式和一个处理类. 顺序问题;
第一个匹配的规则会被使用. 如果正则表达式包含捕获组, 这些组会被作为路径参数传递给处理函数的HTTP方
法. 如果一个字典作为 URLSpec 的第三个参数被传递, 它会作为初始参数传递给
RequestHandler.initialize. 最后 URLSpec 可能有一个名字 , 这将允许它被 RequestHandler.reverse_url
使用.

例如, 在这个片段中根URL / 映射到了 MainHandler , 像 /story/ 后跟着一个数字这种形式的URL被映射到
了 StoryHandler. 这个数字被传递(作为字符串)给 StoryHandler.get.

class MainHandler(RequestHandler):
    def get(self):
        self.write('<a href="%s">link to story 1</a>' %
                   self.reverse_url("story", "1"))

class StoryHandler(RequestHandler):
    def initialize(self, db):
        self.db = db

    def get(self, story_id):
        self.write("this is story %s" % story_id)

app = Application([
    url(r"/", MainHandler),
    url(r"/story/([0-9]+)", StoryHandler, dict(db=db), name="story")
    ])

Application 构造函数有很多关键字参数可以用于自定义应用程序的行为和使用某些特性(或者功能); 完整列
表请查看 Application.settings .

### RequestHandler 子类

Tornado web 应用程序的大部分工作是在 RequestHandler 子类下完成的. 处理子类的主入口点是一个命名为
处理HTTP方法的函数: get(), post(), 等等. 每个处理程序可以定义一个或者多个这种方法来处理不同的
HTTP动作. 如上所述, 这些方法将被匹配路由规则的捕获组对应的参数调用.

在处理程序中, 调用方法如 RequestHandler.render 或者 RequestHandler.write 产生一个响应. render()
通过名字加载一个 Template 并使用给定的参数渲染它. write() 被用于非模板基础的输出; 它接受字符串,
字节, 和字典(字典会被编码成JSON).

在 RequestHandler 中的很多方法的设计是为了在子类中复写和在整个应用中使用. 常用的方法是定义一个 
BaseHandler 类, 复写一些方法例如 write_error 和 get_current_user 然后子类继承使用你自己的 
BaseHandler 而不是 RequestHandler 在你所有具体的处理程序中.

#### 处理输入请求

处理请求的程序(request handler)可以使用 self.request 访问代表当前请求的对象. 通过
HTTPServerRequest 的类定义查看完整的属性列表.

使用HTML表单格式请求的数据会被解析并且可以在一些方法中使用, 例如 get_query_argument 和
get_body_argument.

class MyFormHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body><form action="/myform" method="POST">'
                   '<input type="text" name="message">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')

    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.write("You wrote " + self.get_body_argument("message"))

由于HTLM表单编码不确定一个标签的参数是单一值还是一个列表, RequestHandler 有明确的方法来允许应用
程序表明是否它期望接收一个列表. 对于列表, 使用 get_query_arguments 和 get_body_arguments 而不是
它们的单数形式.

通过一个表单上传的文件可以使用 self.request.files, 它遍历名字(HTML 标签 <input type="file"> 的
name)到一个文件列表. 每个文件都是一个字典的形式 {"filename":..., "content_type":..., "body":...}
. files 对象是当前唯一的如果文件上传是通过一个表单包装 (i.e. a multipart/form-data
Content-Type); 如果没用这种格式, 原生上传的数据可以调用 self.request.body 使用. 默认上传的文件是
完全缓存在内存中的; 如果你需要处理占用内存太大的文件可以看看 stream_request_body 类装饰器.

由于HTML表单编码格式的怪异 (e.g. 在单数和复数参数的含糊不清), Tornado 不会试图统一表单参数和其他
输入类型的参数. 特别是, 我们不解析JSON请求体. 应用程序希望使用JSON代替表单编码可以复写 prepare
来解析它们的请求:

def prepare(self):
    if self.request.headers["Content-Type"].startswith("application/json"):
        self.json_args = json.loads(self.request.body)
    else:
        self.json_args = None

#### 复写RequestHandler的方法

除了 get()/post()/等, 在 RequestHandler 中的某些其他方法被设计成了在必要的时候让子类重写. 在每个
请求中, 会发生下面的调用序列:

 1. 在每次请求时生成一个新的 RequestHandler 对象
 2. initialize() 被 Application 配置中的初始化参数被调用. initialize 通常应该只保存成员变量传递
    的参数; 它不可能产生任何输出或者调用方法, 例如 send_error.
 3. prepare() 被调用. 这在你所有处理子类共享的基类中是最有用的, 无论是使用哪种HTTP方法, prepare
    都会被调用. prepare 可能会产生输出; 如果它调用 finish (或者 redirect, 等), 处理会在这里结束.
 4. 其中一种HTTP方法被调用: get(), post(), put(), 等. 如果URL的正则表达式包含捕获组, 它们会被作
    为参数传递给这个方法.
 5. 当请求结束, on_finish() 方法被调用. 对于同步处理程序会在 get() (等)后立即返回; 对于异步处理
    程序,会在调用 finish() 后返回.

所有这样设计被用来复写的方法被记录在了 RequestHandler 的文档中. 其中最常用的一些被复写的方法包
括:

  • write_error - 输出对错误页面使用的HTML.
  • on_connection_close - 当客户端断开时被调用; 应用程序可以检测这种情况,并中断后续处理. 注意这
    不能保证一个关闭的连接及时被发现.
  • get_current_user - 参考用户认证
  • get_user_locale - 返回 Locale 对象给当前用户使用
  • set_default_headers - 可以被用来设置额外的响应头(例如自定义的 Server 头)

错误处理¶

如果一个处理程序抛出一个异常, Tornado会调用 RequestHandler.write_error 来生成一个错误页.
tornado.web.HTTPError 可以被用来生成一个指定的状态码; 所有其他的异常都会返回一个500状态.

默认的错误页面包含一个debug模式下的调用栈和另外一行错误描述 (e.g. “500: Internal Server Error”).
为了创建自定义的错误页面, 复写 RequestHandler.write_error (可能在一个所有处理程序共享的一个基类
里面). 这个方法可能产生输出通常通过一些方法, 例如 write 和 render. 如果错误是由异常引起的, 一个 
exc_info 将作为一个关键字参数传递(注意这个异常不能保证是 sys.exc_info 当前的异常, 所以 
write_error 必须使用 e.g. traceback.format_exception 代替 traceback.format_exc).

也可以在常规的处理方法中调用 set_status 代替 write_error 返回一个(自定义)响应来生成一个错误页面.
特殊的例外 tornado.web.Finish 在直接返回不方便的情况下能够在不调用 write_error 前结束处理程序.

对于404错误, 使用 default_handler_class Application setting. 这个处理程序会复写 prepare 而不是一
个更具体的方法, 例如 get() 所以它可以在任何HTTP方法下工作. 它应该会产生如上所说的错误页面: 要么
raise 一个 HTTPError(404) 要么复写 write_error, 或者调用 self.set_status(404) 或者在 prepare()
中直接生成响应.

重定向¶

这里有两种主要的方式让你可以在Tornado中重定向请求: RequestHandler.redirect 和使用
RedirectHandler.

你可以在一个 RequestHandler 的方法中使用 self.redirect() 把用户重定向到其他地方. 还有一个可选参
数 permanent 你可以使用它来表明这个重定向被认为是永久的. permanent 的默认值是 False, 这会生成一
个 302 Found HTTP响应状态码, 适合类似在用户的 POST 请求成功后的重定向. 如果 permanent 是true, 会
使用 301 Moved Permanently HTTP响应, 更适合 e.g. 在SEO友好的方法中把一个页面重定向到一个权威的
URL.

RedirectHandler 让你直接在你 Application 路由表中配置. 例如, 配置一个静态重定向:

app = tornado.web.Application([
    url(r"/app", tornado.web.RedirectHandler,
        dict(url="http://itunes.apple.com/my-app-id")),
    ])

RedirectHandler 也支持正则表达式替换. 下面的规则重定向所有以 /pictures/ 开始的请求用 /photos/ 前
缀代替:

app = tornado.web.Application([
    url(r"/photos/(.*)", MyPhotoHandler),
    url(r"/pictures/(.*)", tornado.web.RedirectHandler,
        dict(url=r"/photos/\1")),
    ])

不像 RequestHandler.redirect, RedirectHandler 默认使用永久重定向. 这是因为路由表在运行时不会改
变, 而且被认为是永久的. 当在处理程序中发现重定向的时候, 可能是其他可能改变的逻辑的结果. 用
RedirectHandler 发送临时重定向, 需要添加 permanent=False 到 RedirectHandler 的初始化参数.

异步处理¶

Tornado默认会同步处理: 当 get()/post() 方法返回, 请求被认为结束并且返回响应. 因为当一个处理程序
正在运行的时候其他所有请求都被阻塞, 任何需要长时间运行的处理都应该是异步的, 这样它就可以在非阻塞
的方式中调用它的慢操作了. 这个话题更详细的内容包含在异步和非阻塞I/O 中; 这部分是关于在
RequestHandler 子类中的异步技术的细节.

使用 coroutine 装饰器是做异步最简单的方式. 这允许你使用 yield 关键字执行非阻塞I/O, 并且直到协程
返回才发送响应. 查看协程了解更多细节.

在某些情况下, 协程不如回调为主的风格方便, 在这种情况下 tornado.web.asynchronous 装饰器可以用来代
替. 当使用这个装饰器的时候, 响应不会自动发送; 而请求将一直保持开放直到callback调用
RequestHandler.finish. 这需要应用程序确保这个方法被调用或者其他用户的浏览器简单的挂起.

这里是一个使用Tornado’s 内置的 AsyncHTTPClient 调用FriendFeed API的例子:

class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        http.fetch("http://friendfeed-api.com/v2/feed/bret",
                   callback=self.on_response)

    def on_response(self, response):
        if response.error: raise tornado.web.HTTPError(500)
        json = tornado.escape.json_decode(response.body)
        self.write("Fetched " + str(len(json["entries"])) + " entries "
                   "from the FriendFeed API")
        self.finish()

当 get() 返回, 请求还没有完成. 当HTTP客户端最终调用 on_response(), 这个请求仍然是开放的, 通过调
用 self.finish(), 响应最终刷到客户端.

为了方便对比, 这里有一个使用协程的相同的例子:

class MainHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        response = yield http.fetch("http://friendfeed-api.com/v2/feed/bret")
        json = tornado.escape.json_decode(response.body)
        self.write("Fetched " + str(len(json["entries"])) + " entries "
                   "from the FriendFeed API")

更多高级异步的示例, 请看 chat example application, 实现了一个使用长轮询(long polling) 的AJAX聊天
室. 长轮询的可能想要覆盖 on_connection_close() 来在客户端关闭连接之后进行清理(注意看方法的文档来
查看警告).

模板和UI¶

Tornado 包含一个简单,快速并灵活的模板语言. 本节介绍了语言以及相关的问题,比如国际化.

Tornado 也可以使用其他的Python模板语言, 虽然没有准备把这些系统整合到 RequestHandler.render 里面.
而是简单的将模板转成字符串并传递给 RequestHandler.write

配置模板¶

默认情况下, Tornado会在和当前 .py 文件相同的目录查找关联的模板文件. 如果想把你的模板文件放在不同
的目录中, 可以使用 template_path Application setting (或复写 RequestHandler.get_template_path 如
果你不同的处理函数有不同的模板路径).

为了从非文件系统位置加载模板, 实例化子类 tornado.template.BaseLoader 并为其在应用设置
(application setting)中配置 template_loader .

默认情况下编译出来的模板会被缓存; 为了关掉这个缓存也为了使(对目标的) 修改在重新加载后总是可见,
使用应用设置(application settings)中的 compiled_template_cache=False 或 debug=True.

模板语法¶

一个Tornado模板仅仅是用一些标记把Python控制序列和表达式嵌入 HTML(或者任意其他文本格式)的文件中:

<html>
   <head>
      <title>{{ title }}</title>
   </head>
   <body>
     <ul>
       {% for item in items %}
         <li>{{ escape(item) }}</li>
       {% end %}
     </ul>
   </body>
 </html>

如果你把这个目标保存为”template.html”并且把它放在你Python文件的相同目录下, 你可以使用下面的代码
渲染它:

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        items = ["Item 1", "Item 2", "Item 3"]
        self.render("template.html", title="My title", items=items)

Tornado模板支持控制语句(control statements) 和表达式(expressions). 控制语句被包在 {% 和 %} 中间,
e.g., {% if len(items) > 2 %}. 表达式被包在 {{ 和 }} 之间, e.g., {{ items[0] }}.

控制语句或多或少都和Python语句类似. 我们支持 if, for, while, 和 try, 这些都必须使用 {% end %} 来
标识结束. 我们也支持模板继承(template inheritance) 使用 extends 和 block 标签声明, 这些内容的详
细信息都可以在 tornado.template 中看到.

表达式可以是任意的Python表达式, 包括函数调用. 模板代码会在包含以下对象和函数的命名空间中执行 (注
意这个列表适用于使用 RequestHandler.render 和 render_string 渲染模板的情况. 如果你直接在
RequestHandler 之外使用 tornado.template 模块, 下面这些很多都不存在).

  • escape: tornado.escape.xhtml_escape 的别名
  • xhtml_escape: tornado.escape.xhtml_escape 的别名
  • url_escape: tornado.escape.url_escape 的别名
  • json_encode: tornado.escape.json_encode 的别名
  • squeeze: tornado.escape.squeeze 的别名
  • linkify: tornado.escape.linkify 的别名
  • datetime: Python datetime 模块
  • handler: 当前的 RequestHandler 对象
  • request: handler.request 的别名
  • current_user: handler.current_user 的别名
  • locale: handler.locale 的别名
  • _: handler.locale.translate 的别名
  • static_url: handler.static_url 的别名
  • xsrf_form_html: handler.xsrf_form_html 的别名
  • reverse_url: Application.reverse_url 的别名
  • 所有从 ui_methods 和 ui_modules Application 设置的条目
  • 任何传递给 render 或 render_string 的关键字参数

当你正在构建一个真正的应用, 你可能想要使用Tornado模板的所有特性, 尤其是目标继承. 阅读所有关于这
些特性的介绍在 tornado.template 部分 (一些特性, 包括 UIModules 是在 tornado.web 模块中实现的)

在引擎下, Tornado模板被直接转换为Python. 包含在你模板中的表达式会逐字的复制到一个代表你模板的
Python函数中. 我们不会试图阻止模板语言中的任何东西; 我们明确的创造一个高度灵活的模板系统, 而不是
有严格限制的模板系统. 因此, 如果你在模板表达式中随意填充(代码), 当你执行它的时候你也会得到各种随
机错误.

所有模板输出默认都会使用 tornado.escape.xhtml_escape 函数转义. 这个行为可以通过传递 autoescape=
None 给 Application 或者 tornado.template.Loader 构造器来全局改变, 对于一个模板文件可以使用 {% 
autoescape None %} 指令, 对于一个单一表达式可以使用 {% raw ...%} 来代替 {{ ... }}. 此外, 在每个
地方一个可选的转义函数名可以被用来代替 None.

注意, 虽然Tornado的自动转义在预防XSS漏洞上是有帮助的, 但是它并不能胜任所有的情况. 在某一位置出现
的表达式, 例如Javascript 或 CSS, 可能需要另外的转义. 此外, 要么是必须注意总是在可能包含不可信内
容的HTML中使用双引号和 xhtml_escape , 要么必须在属性中使用单独的转义函数 (参见 e.g. http://
wonko.com/post/html-escaping)

国际化¶

当前用户的区域设置(无论他们是否登录)总是可以通过在请求处理程序中使用 self.locale 或者在模板中使
用 locale 进行访问. 区域的名字 (e.g., en_US) 可以通过 locale.name 获得, 你可以翻译字符串通过
Locale.translate 方法. 模板也有一个叫做 _() 全局函数用来进行字符串翻译. 翻译函数有两种形式:

_("Translate this string")

是直接根据当前的区域设置进行翻译, 还有:

_("A person liked this", "%(num)d people liked this",
  len(people)) % {"num": len(people)}

是可以根据第三个参数的值来翻译字符串单复数的. 在上面的例子中, 如果 len(people) 是 1, 那么第一句
翻译将被返回, 其他情况第二句的翻译将会返回.

翻译最通用的模式四使用Python命名占位符变量(上面例子中的 %(num)d ) 因为占位符可以在翻译时变化.

这是一个正确的国际化模板:

<html>
   <head>
      <title>FriendFeed - {{ _("Sign in") }}</title>
   </head>
   <body>
     <form action="{{ request.path }}" method="post">
       <div>{{ _("Username") }} <input type="text" name="username"/></div>
       <div>{{ _("Password") }} <input type="password" name="password"/></div>
       <div><input type="submit" value="{{ _("Sign in") }}"/></div>
       {% module xsrf_form_html() %}
     </form>
   </body>
 </html>

默认情况下, 我们通过用户的浏览器发送的 Accept-Language 头来发现用户的区域设置. 如果我们没有发现
恰当的 Accept-Language 值, 我们会使用 en_US . 如果你让用户进行自己偏爱的区域设置, 你可以通过复写
RequestHandler.get_user_locale 来覆盖默认选择的区域:

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id: return None
        return self.backend.get_user_by_id(user_id)

    def get_user_locale(self):
        if "locale" not in self.current_user.prefs:
            # Use the Accept-Language header
            return None
        return self.current_user.prefs["locale"]

如果 get_user_locale 返回 None, 那我们(继续)依靠 Accept-Language 头(进行判断).

tornado.locale 模块支持两种形式加载翻译: 一种是用 gettext 和相关的工具的 .mo 格式, 还有一种是简
单的 .csv 格式. 应用程序在启动时通常会调用一次 tornado.locale.load_translations 或者
tornado.locale.load_gettext_translations 其中之一; 查看这些方法来获取更多有关支持格式的详细信
息..

你可以使用 tornado.locale.get_supported_locales() 得到你的应用所支持的区域(设置)列表. 用户的区域
是从被支持的区域中选择距离最近的匹配得到的. 例如, 如果用户的区域是 es_GT, 同时 es 区域是被支持
的, 请求中的 self.locale 将会设置为 es . 如果找不到距离最近的匹配项, 我们将会使用 en_US .

UI 模块¶

Tornado支持 UI modules 使它易于支持标准, 在你的应用程序中复用 UI组件. UI模块像是特殊的函数调用来
渲染你的页面上的组件并且它们可以包装自己的CSS和JavaScript.

例如, 如果你实现一个博客, 并且你想要有博客入口出现在首页和每篇博客页, 你可以实现一个 Entry 模块
来在这些页面上渲染它们. 首先, 为你的UI模块新建一个Python模块, e.g., uimodules.py:

class Entry(tornado.web.UIModule):
    def render(self, entry, show_comments=False):
        return self.render_string(
            "module-entry.html", entry=entry, show_comments=show_comments)

在你的应用设置中, 使用 ui_modules 配置, 告诉Tornado使用 uimodules.py

from . import uimodules

class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        entries = self.db.query("SELECT * FROM entries ORDER BY date DESC")
        self.render("home.html", entries=entries)

class EntryHandler(tornado.web.RequestHandler):
    def get(self, entry_id):
        entry = self.db.get("SELECT * FROM entries WHERE id = %s", entry_id)
        if not entry: raise tornado.web.HTTPError(404)
        self.render("entry.html", entry=entry)

settings = {
    "ui_modules": uimodules,
}
application = tornado.web.Application([
    (r"/", HomeHandler),
    (r"/entry/([0-9]+)", EntryHandler),
], **settings)

在一个模板中, 你可以使用 {% module %} 语法调用一个模块. 例如, 你可以调用 Entry 模块从 home.html:

{% for entry in entries %}
  {% module Entry(entry) %}
{% end %}

和 entry.html:

{% module Entry(entry, show_comments=True) %}

模块可以包含自定义的CSS和JavaScript函数, 通过复写 embedded_css, embedded_javascript, 
javascript_files, 或 css_files 方法:

class Entry(tornado.web.UIModule):
    def embedded_css(self):
        return ".entry { margin-bottom: 1em; }"

    def render(self, entry, show_comments=False):
        return self.render_string(
            "module-entry.html", show_comments=show_comments)

模块CSS和JavaScript将被加载(或包含)一次, 无论模块在一个页面上被使用多少次. CSS总是包含在页面的 
<head> 标签中, JavaScript 总是被包含在页面最底部的 </body> 标签之前.

当不需要额外的Python代码时, 一个模板文件本身可以作为一个模块. 例如, 先前的例子可以重写到下面的 
module-entry.html:

{{ set_resources(embedded_css=".entry { margin-bottom: 1em; }") }}
<!-- more template html... -->

这个被修改过的模块模块可以被引用:

{% module Template("module-entry.html", show_comments=True) %}

set_resources 函数只能在模板中通过 {% module Template(...) %} 才可用. 不像 {% include ... %} 指
令, 模板模块有一个明确的命名空间它们的包含模板-它们只能看到全局模板命名空间和它们自己的关键字参
数.

认证和安全¶

Cookies 和 secure cookies¶

你可以在用户浏览器中通过 set_cookie 方法设置 cookie:

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        if not self.get_cookie("mycookie"):
            self.set_cookie("mycookie", "myvalue")
            self.write("Your cookie was not set yet!")
        else:
            self.write("Your cookie was set!")

普通的cookie并不安全, 可以通过客户端修改. 如果你需要通过设置cookie, 例如来识别当前登录的用户, 就
需要给你的cookie签名防止伪造. Tornado 支持通过 set_secure_cookie 和 get_secure_cookie 方法对
cookie签名. 想要使用这些方法, 你需要在你创建应用的时候, 指定一个名为 cookie_secret 的密钥. 你可
以在应用的设置中以关键字参数的形式传递给应用程序:

application = tornado.web.Application([
    (r"/", MainHandler),
], cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__")

签名后的cookie除了时间戳和一个 HMAC 签名还包含编码后的cookie值. 如果cookie过期或者签名不匹配, 
get_secure_cookie 将返回 None 就像没有设置cookie一样. 上面例子的安全版本:

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        if not self.get_secure_cookie("mycookie"):
            self.set_secure_cookie("mycookie", "myvalue")
            self.write("Your cookie was not set yet!")
        else:
            self.write("Your cookie was set!")

Tornado的安全cookie保证完整性但是不保证机密性. 也就是说, cookie不能被修改但是它的内容对用户是可
见的. 密钥 cookie_secret 是一个对称的key, 而且必须保密–任何获得这个key的人都可以伪造出自己签名的
cookie.

默认情况下, Tornado的安全cookie过期时间是30天. 可以给 set_secure_cookie 使用 expires_days 关键字
参数同时 get_secure_cookie 设置 max_age_days 参数也可以达到效果. 这两个值分别通过这样(设置)你就
可以达到如下的效果, 例如大多数情况下有30天有效期的cookie, 但是对某些敏感操作(例如修改账单信息)你
可以使用一个较小的 max_age_days .

Tornado也支持多签名密钥, 使签名密钥轮换. 然后 cookie_secret 必须是一个以整数key版本作为key, 以相
对应的密钥作为值的字典. 当前使用的签名键必须是应用设置中 key_version 的集合. 不过字典中的其他key
都允许做 cookie签名验证, 如果当前key版本在cookie集合中.为了实现cookie更新, 可以通过
get_secure_cookie_key_version 查询当前key版本.

用户认证¶

当前已经通过认证的用户在每个请求处理函数中都可以通过 self.current_user 得到, 在每个模板中可以使
用 current_user 获得. 默认情况下, current_user 是 None.

为了在你的应用程序中实现用户认证, 你需要在你的请求处理函数中复写 get_current_user() 方法来判断当
前用户, 比如可以基于cookie的值. 这里有一个例子, 这个例子允许用户简单的通过一个保存在cookie中的特
殊昵称登录到应用程序中:

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)

class LoginHandler(BaseHandler):
    def get(self):
        self.write('<html><body><form action="/login" method="post">'
                   'Name: <input type="text" name="name">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')

    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/")

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", LoginHandler),
], cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__")

你可以使用 Python 装饰器(decorator) tornado.web.authenticated 要求用户登录. 如果请求方法带有这个
装饰器并且用户没有登录, 用户将会被重定向到 login_url (另一个应用设置). 上面的例子可以被重写:

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)

settings = {
    "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    "login_url": "/login",
}
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", LoginHandler),
], **settings)

如果你使用 authenticated 装饰 post() 方法并且用户没有登录, 服务将返回一个 403 响应. 
@authenticated 装饰器是 if not self.current_user: self.redirect() 的简写. 可能不适合非基于浏览器
的登录方案.

通过 Tornado Blog example application 可以看到一个使用用户验证(并且在MySQL数据库中存储用户数据)
的完整例子.

第三方用户验证¶

tornado.auth 模块实现了对一些网络上最流行的网站的身份认证和授权协议, 包括Google/Gmail, Facebook,
Twitter,和FriendFeed. 该模块包括通过这些网站登录用户的方法, 并在适用情况下允许访问该网站服务的方
法, 例如, 下载一个用户的地址簿或者在他们支持下发布一条Twitter信息.

这是个使用Google身份认证, 在cookie中保存Google的认证信息以供之后访问的示例处理程序:

class GoogleOAuth2LoginHandler(tornado.web.RequestHandler,
                               tornado.auth.GoogleOAuth2Mixin):
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument('code', False):
            user = yield self.get_authenticated_user(
                redirect_uri='http://your.site.com/auth/google',
                code=self.get_argument('code'))
            # Save the user with e.g. set_secure_cookie
        else:
            yield self.authorize_redirect(
                redirect_uri='http://your.site.com/auth/google',
                client_id=self.settings['google_oauth']['key'],
                scope=['profile', 'email'],
                response_type='code',
                extra_params={'approval_prompt': 'auto'})

查看 tornado.auth 模块的文档以了解更多细节.

跨站请求伪造(防护)¶

跨站请求伪造(Cross-site request forgery), 或 XSRF, 是所有web应用程序面临的一个主要问题. 可以通过
Wikipedia 文章来了解更多关于XSRF的细节.

普遍接受的预防XSRF攻击的方案是让每个用户的cookie都是不确定的值, 并且把那个cookie值在你站点的每个
form提交中作为额外的参数包含进来. 如果cookie 和form提交中的值不匹配, 则请求可能是伪造的.

Tornado内置XSRF保护. 你需要在你的应用设置中使用 xsrf_cookies 便可以在你的网站上使用:

settings = {
    "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    "login_url": "/login",
    "xsrf_cookies": True,
}
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", LoginHandler),
], **settings)

如果设置了 xsrf_cookies , Tornado web应用程序将会给所有用户设置 _xsrf cookie并且拒绝所有不包含一
个正确的 _xsrf 值的 POST, PUT, 或 DELETE 请求. 如果你打开这个设置, 你必须给所有通过 POST 请求的
form提交添加这个字段. 你可以使用一个特性的 UIModule xsrf_form_html() 来做这件事情, 这个方法在所
有模板中都是可用的:

<form action="/new_message" method="post">
  {% module xsrf_form_html() %}
  <input type="text" name="message"/>
  <input type="submit" value="Post"/>
</form>

如果你提交一个AJAX的 POST 请求, 你也需要在每个请求中给你的 JavaScript添加 _xsrf 值. 这是我们在
FriendFeed为了AJAX的 POST 请求使用的一个 jQuery 函数, 可以自动的给所有请求添加 _xsrf 值:

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

jQuery.postJSON = function(url, args, callback) {
    args._xsrf = getCookie("_xsrf");
    $.ajax({url: url, data: $.param(args), dataType: "text", type: "POST",
        success: function(response) {
        callback(eval("(" + response + ")"));
    }});
};

对于 PUT 和 DELETE 请求(除了不使用form编码(form-encoded) 参数的 POST 请求, XSRF token也会通过一
个 X-XSRFToken 的HTTP头传递. XSRF cookie 通常在使用 xsrf_form_html 会设置, 但是在不使用正规 form
的纯Javascript应用中, 你可能需要访问 self.xsrf_token 手动设置 (只读这个属性足够设置cookie了).

如果你需要自定义每一个处理程序基础的XSRF行为, 你可以复写 RequestHandler.check_xsrf_cookie(). 例
如, 如果你有一个没有使用 cookie验证的API, 你可能想禁用XSRF保护, 可以通过使 check_xsrf_cookie()
不做任何处理. 然而, 如果你支持基于cookie和非基于cookie的认证, 重要的是, 当前带有cookie认证的请求
究竟什么时候使用XSRF保护.

运行和部署¶

因为Tornado内置了自己的HTTPServer, 运行和部署它与其他Python web框架不太一样. 你需要写一个 main()
函数来启动服务, 而不是配置一个WSGI容器来运行你的应用:

def main():
    app = make_app()
    app.listen(8888)
    IOLoop.current().start()

if __name__ == '__main__':
    main()

配置你的操作系统或者进程管理器来运行这个程序以启动服务. 请注意, 增加每个进程允许打开的最大文件句
柄数是可能是必要的(为了避免”Too many open files” 的错误). 为了增加这个上限(例如设置为50000 ) 你
可以使用ulimit命令, 修改/etc/security/limits.conf 或者设置 minfds 在你的supervisord配置中.

进程和端口¶

由于Python的GIL(全局解释器锁), 为了充分利用多CPU的机器, 运行多个Python 进程是很有必要的. 通常,
最好是每个CPU运行一个进程.

Tornado包含了一个内置的多进程模式来一次启动多个进程. 这需要一个在main 函数上做点微小的改变:

def main():
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.bind(8888)
    server.start(0)  # forks one process per cpu
    IOLoop.current().start()

这是最简单的方式来启动多进程并让他们共享同样的端口, 虽然它有一些局限性. 首先, 每个子进程将有它自
己的IOLoop, 所以fork之前, 不接触全局 IOLoop实例是重要的(甚至是间接的). 其次, 在这个模型中, 很难
做到零停机 (zero-downtime)更新. 最后, 因为所有的进程共享相同的端口, 想单独监控它们就更加困难了.

对更复杂的部署, 建议启动独立的进程, 并让它们各自监听不同的端口. supervisord 的”进程组(process
groups)” 功能是一个很好的方式来安排这些. 当每个进程使用不同的端口, 一个外部的负载均衡器例如
HAProxy 或nginx通常需要对外向访客提供一个单一的地址.

运行在负载均衡器后面¶

当运行在一个负载均衡器例如nginx, 建议传递 xheaders=True 给 HTTPServer 的构造器. 这将告诉Tornado
使用类似 X-Real-IP 这样的HTTP头来获取用户的IP地址而不是把所有流量都认为来自于负载均衡器的IP地址.

这是一份原始的nginx配置文件, 在结构上类似于我们在FriendFeed所使用的配置. 这是假设nginx和Tornado
server运行在同一台机器上的, 并且四个 Tornado server正运行在8000 - 8003端口:

user nginx;
worker_processes 1;

error_log /var/log/nginx/error.log;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
    use epoll;
}

http {
    # Enumerate all the Tornado servers here
    upstream frontends {
        server 127.0.0.1:8000;
        server 127.0.0.1:8001;
        server 127.0.0.1:8002;
        server 127.0.0.1:8003;
    }

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    access_log /var/log/nginx/access.log;

    keepalive_timeout 65;
    proxy_read_timeout 200;
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    gzip on;
    gzip_min_length 1000;
    gzip_proxied any;
    gzip_types text/plain text/html text/css text/xml
               application/x-javascript application/xml
               application/atom+xml text/javascript;

    # Only retry if there was a communication error, not a timeout
    # on the Tornado server (to avoid propagating "queries of death"
    # to all frontends)
    proxy_next_upstream error;

    server {
        listen 80;

        # Allow file uploads
        client_max_body_size 50M;

        location ^~ /static/ {
            root /var/www;
            if ($query_string) {
                expires max;
            }
        }
        location = /favicon.ico {
            rewrite (.*) /static/favicon.ico;
        }
        location = /robots.txt {
            rewrite (.*) /static/robots.txt;
        }

        location / {
            proxy_pass_header Server;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Scheme $scheme;
            proxy_pass http://frontends;
        }
    }
}

静态文件和文件缓存¶

Tornado中, 你可以通过在应用程序中指定特殊的 static_path 来提供静态文件服务:

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    "login_url": "/login",
    "xsrf_cookies": True,
}
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", LoginHandler),
    (r"/(apple-touch-icon\.png)", tornado.web.StaticFileHandler,
     dict(path=settings['static_path'])),
], **settings)

这些设置将自动的把所有以 /static/ 开头的请求从static目录进行提供, e.g., http://localhost:8888/
static/foo.png 将会通过指定的static目录提供 foo.png 文件. 我们也自动的会从static目录提供 /
robots.txt 和 /favicon.ico (尽管它们并没有以 /static/ 前缀开始).

在上面的设置中, 我们明确的配置Tornado 提供 apple-touch-icon.png 文件从 StaticFileHandler 根下,
虽然文件在static文件目录中. (正则表达式捕获组必须告诉 StaticFileHandler 请求的文件名; 调用捕获组
把文件名作为方法的参数传递给处理程序.) 你可以做同样的事情 e.g. 从网站的根提供 sitemap.xml 文件.
当然, 你也可以通过在你的HTML中使用 <link /> 标签来避免伪造根目录的 apple-touch-icon.png .

为了改善性能, 通常情况下, 让浏览器主动缓存静态资源是个好主意, 这样浏览器就不会发送不必要的可能在
渲染页面时阻塞的 If-Modified-Since 或 Etag 请求了. Tornado使用静态内容版本(static content
versioning) 来支持此项功能.

为了使用这些功能, 在你的模板中使用 static_url 方法而不是直接在你的HTML中输入静态文件的URL:

<html>
   <head>
      <title>FriendFeed - {{ _("Home") }}</title>
   </head>
   <body>
     <div><img src="{{ static_url("images/logo.png") }}"/></div>
   </body>
 </html>

static_url() 函数将把相对路径翻译成一个URI类似于 /static/images/logo.png?v=aae54. 其中的 v 参数
是 logo.png 内容的哈希(hash), 并且它的存在使得Tornado服务向用户的浏览器发送缓存头, 这将使浏览器
无限期的缓存内容.

因为参数 v 是基于文件内容的, 如果你更新一个文件并重启服务, 它将发送一个新的 v 值, 所以用户的浏览
器将会自动的拉去新的文件. 如果文件的内容没有改变, 浏览器将会继续使用本地缓存的副本, 而不会从服务
器检查更新, 显著的提高了渲染性能.

在生产中, 你可能想提供静态文件通过一个更优的静态服务器, 比如 nginx . 你可以配置任何web服务器识别
通过 static_url() 提供的版本标签并相应的设置缓存头. 下面是我们在 FriendFeed 使用的nginx相关配置
的一部分:

location /static/ {
    root /var/friendfeed/static;
    if ($query_string) {
        expires max;
    }
 }

Debug模式和自动重载¶

如果传递 debug=True 配置给 Application 的构造函数, 应用程序将会运行在debug/开发模式. 在这个模式
下, 为了方便于开发的一些功能将被启用( 每一个也可以作为独立的标签使用; 如果它们都被专门指定, 那它
们都将获得独立的优先级):

  • autoreload=True: 应用程序将会观察它的源文件是否改变, 并且当任何文件改变的时候便重载它自己.
    这减少了在开发中需要手动重启服务的需求. 然而, 在debug模式下, 某些错误(例如import的时候有语法
    错误)会导致服务关闭, 并且无法自动恢复.
  • compiled_template_cache=False: 模板将不会被缓存.
  • static_hash_cache=False: 静态文件哈希 (被 static_url 函数使用) 将不会被缓存
  • serve_traceback=True: 当一个异常在 RequestHandler 中没有捕获, 将会生成一个包含调用栈信息的错
    误页.

自动重载(autoreload)模式和 HTTPServer 的多进程模式不兼容. 你不能给 HTTPServer.start 传递1以外的
参数(或者调用 tornado.process.fork_processes) 当你使用自动重载模式的时候.

debug模式的自动重载功能可作为一个独立的模块位于 tornado.autoreload. 以下两者可以结合使用, 在语法
错误之时提供额外的健壮性: 设置 autoreload=True 可以在app运行时检测文件修改, 还有启动 python -m 
tornado.autoreload myserver.py 来捕获任意语法错误或者其他的启动时错误.

重载会丢失任何Python解释器命令行参数(e.g. -u). 因为它使用 sys.executable 和 sys.argv 重新执行
Python. 此外, 修改这些变量将造成重载错误.

在一些平台(包括Windows 和Mac OSX 10.6之前), 进程不能被”原地”更新, 所以当检测到代码更新, 旧服务就
会退出然后启动一个新服务. 这已经被公知来混淆一些IDE.

WSGI和Google App Engine¶

Tornado通常是独立运行的, 不需要一个WSGI容器. 然而, 在一些环境中 (例如Google App Engine), 只运行
WSGI, 应用程序不能独立运行自己的服务. 在这种情况下, Tornado支持一个有限制的操作模式, 不支持异步
操作但允许一个Tornado’s功能的子集在仅WSGI环境中. 以下功能在WSGI 模式下是不支持的, 包括协程, 
@asynchronous 装饰器, AsyncHTTPClient, auth 模块和WebSockets.

你可以使用 tornado.wsgi.WSGIAdapter 把一个Tornado Application 转换成WSGI应用. 在这个例子中, 配置
你的WSGI容器发现 application 对象:

import tornado.web
import tornado.wsgi

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

tornado_app = tornado.web.Application([
    (r"/", MainHandler),
])
application = tornado.wsgi.WSGIAdapter(tornado_app)

查看 appengine example application 以了解AppEngine在Tornado上开发的完整功能.

web框架¶

tornado.web — RequestHandler 和 Application 类¶

tornado.web 提供了一种带有异步功能并允许它扩展到大量开放连接的简单的web 框架, 使其成为处理长连接
(long polling) 的一种理想选择.

这里有一个简单的”Hello, world”示例应用:

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()

查看用户指南以了解更多信息.

线程安全说明¶

一般情况下, 在 RequestHandler 中的方法和Tornado 中其他的方法不是线程安全的. 尤其是一些方法, 例如
write(), finish(), 和 flush() 要求只能从主线程调用. 如果你使用多线程, 那么在结束请求之前, 使用
IOLoop.add_callback 来把控制权传送回主线程是很重要的.

Request handlers¶

class tornado.web.RequestHandler(application, request, **kwargs)[源代码]¶

    HTTP请求处理的基类.

    子类至少应该是以下”Entry points” 部分中被定义的方法其中之一.

Entry points¶

RequestHandler.initialize()[源代码]¶

    子类初始化(Hook).

    作为url spec的第三个参数传递的字典, 将作为关键字参数提供给 initialize().

    例子:

    class ProfileHandler(RequestHandler):
        def initialize(self, database):
            self.database = database

        def get(self, username):
            ...

    app = Application([
        (r'/user/(.*)', ProfileHandler, dict(database=database)),
        ])

RequestHandler.prepare()[源代码]¶

    在每个请求的最开始被调用, 在 get/post/等方法之前.

    通过复写这个方法, 可以执行共同的初始化, 而不用考虑每个请求方法.

    异步支持: 这个方法使用 gen.coroutine 或 return_future 装饰器来使它异步( asynchronous 装饰器
    不能被用在 prepare). 如果这个方法返回一个 Future 对象, 执行将不再进行, 直到 Future 对象完成.

    3.1 新版功能: 异步支持.

RequestHandler.on_finish()[源代码]¶

    在一个请求结束后被调用.

    复写这个方法来执行清理, 日志记录等. 这个方法和 prepare 是相对应的. on_finish 可能不产生任何
    输出, 因为它是在响应被送到客户端后才被调用.

执行后面任何的方法 (统称为HTTP 动词(verb) 方法) 来处理相应的HTTP方法. 这些方法可以通过使用下面的
装饰器: gen.coroutine, return_future, 或 asynchronous 变成异步.

为了支持不再列表中的方法, 可以复写类变量 SUPPORTED_METHODS:

class WebDAVHandler(RequestHandler):
    SUPPORTED_METHODS = RequestHandler.SUPPORTED_METHODS + ('PROPFIND',)

    def propfind(self):
        pass

RequestHandler.get(*args, **kwargs)[源代码]¶

RequestHandler.head(*args, **kwargs)[源代码]¶

RequestHandler.post(*args, **kwargs)[源代码]¶

RequestHandler.delete(*args, **kwargs)[源代码]¶

RequestHandler.patch(*args, **kwargs)[源代码]¶

RequestHandler.put(*args, **kwargs)[源代码]¶

RequestHandler.options(*args, **kwargs)[源代码]¶

Input¶

RequestHandler.get_argument(name, default=[], strip=True)[源代码]¶

    返回指定的name参数的值.

    如果没有提供默认值, 那么这个参数将被视为是必须的, 并且当找不到这个参数的时候我们会抛出一个
    MissingArgumentError.

    如果一个参数在url上出现多次, 我们返回最后一个值.

    返回值永远是unicode.

RequestHandler.get_arguments(name, strip=True)[源代码]¶

    返回指定name的参数列表.

    如果参数不存在, 返回一个空列表.

    返回值永远是unicode.

RequestHandler.get_query_argument(name, default=[], strip=True)[源代码]¶

    从请求的query string返回给定name的参数的值.

    如果没有提供默认值, 这个参数将被视为必须的, 并且当找不到这个参数的时候我们会抛出一个
    MissingArgumentError 异常.

    如果这个参数在url中多次出现, 我们将返回最后一次的值.

    返回值永远是unicode.

    3.2 新版功能.

RequestHandler.get_query_arguments(name, strip=True)[源代码]¶

    返回指定name的参数列表.

    如果参数不存在, 将返回空列表.

    返回值永远是unicode.

    3.2 新版功能.

RequestHandler.get_body_argument(name, default=[], strip=True)[源代码]¶

    返回请求体中指定name的参数的值.

    如果没有提供默认值, 那么这个参数将被视为是必须的, 并且当找不到这个参数的时候我们会抛出一个
    MissingArgumentError.

    如果一个参数在url上出现多次, 我们返回最后一个值.

    返回值永远是unicode.

    3.2 新版功能.

RequestHandler.get_body_arguments(name, strip=True)[源代码]¶

    返回由指定请求体中指定name的参数的列表.

    如果参数不存在, 返回一个空列表.

    返回值永远是unicode.

    3.2 新版功能.

RequestHandler.decode_argument(value, name=None)[源代码]¶

    从请求中解码一个参数.

    这个参数已经被解码现在是一个字节字符串(byte string). 默认情况下, 这个方法会把参数解码成utf-8
    并且返回一个unicode字符串, 但是它可以被子类复写.

    这个方法既可以在 get_argument() 中被用作过滤器, 也可以用来从url 中提取值并传递给 get()/post
    ()/等.

    如果知道的话参数的name会被提供, 但也可能为None (e.g. 在url正则表达式中未命名的组).

RequestHandler.request¶

    tornado.httputil.HTTPServerRequest 对象包含附加的请求参数包括e.g. 头部和body数据.

RequestHandler.path_args¶

RequestHandler.path_kwargs¶

    path_args 和 path_kwargs 属性包含传递给 HTTP verb methods 的位置和关键字参数. 这些属性被设
    置, 在这些方法被调用之前, 所以这些值在 prepare 之间是可用的.

Output¶

RequestHandler.set_status(status_code, reason=None)[源代码]¶

    设置响应的状态码.

           • status_code (int) – 响应状态码. 如果 reason 是 None, 它必须存在于 httplib.responses
     参      .
    数:    • reason (string) – 用人类可读的原因短语来描述状态码. 如果是 None, 它会由来自
             httplib.responses 的reason填满.

RequestHandler.set_header(name, value)[源代码]¶

    给响应设置指定的头部和对应的值.

    如果给定了一个datetime, 我们会根据HTTP规范自动的对它格式化. 如果值不是一个字符串, 我们会把它
    转换成字符串. 之后所有头部的值都将用UTF-8 编码.

RequestHandler.add_header(name, value)[源代码]¶

    添加指定的响应头和对应的值.

    不像是 set_header, add_header 可以被多次调用来为相同的头返回多个值.

RequestHandler.clear_header(name)[源代码]¶

    清除输出头, 取消之前的 set_header 调用.

    注意这个方法不适用于被 add_header 设置了多个值的头.

RequestHandler.set_default_headers()[源代码]¶

    复写这个方法可以在请求开始的时候设置HTTP头.

    例如, 在这里可以设置一个自定义 Server 头. 注意在一般的请求过程流里可能不会实现你预期的效果,
    因为头部可能在错误处理(error handling)中被重置.

RequestHandler.write(chunk)[源代码]¶

    把给定块写到输出buffer.

    为了把输出写到网络, 使用下面的flush()方法.

    如果给定的块是一个字典, 我们会把它作为JSON来写同时会把响应头设置为 application/json. (如果你
    写JSON但是设置不同的 Content-Type, 可以调用set_header 在调用write()之后 ).

    注意列表不能转换为JSON 因为一个潜在的跨域安全漏洞. 所有的JSON 输出应该包在一个字典中. 更多细
    节参考 http://haacked.com/archive/2009/06/25/json-hijacking.aspx/ 和 https://github.com/
    facebook/tornado/issues/1009

RequestHandler.flush(include_footers=False, callback=None)[源代码]¶

    将当前输出缓冲区写到网络.

    callback 参数, 如果给定则可用于流控制: 它会在所有数据被写到 socket后执行. 注意同一时间只能有
    一个flush callback停留; 如果另一个flush在前一个flush的callback运行之前发生, 那么前一个
    callback 将会被丢弃.

    在 4.0 版更改: 现在如果没有给定callback, 会返回一个 Future 对象.

RequestHandler.finish(chunk=None)[源代码]¶

    完成响应, 结束HTTP 请求.

RequestHandler.render(template_name, **kwargs)[源代码]¶

    使用给定参数渲染模板并作为响应.

RequestHandler.render_string(template_name, **kwargs)[源代码]¶

    使用给定的参数生成指定模板.

    我们返回生成的字节字符串(以utf8). 为了生成并写一个模板作为响应, 使用上面的render().

RequestHandler.get_template_namespace()[源代码]¶

    返回一个字典被用做默认的模板命名空间.

    可以被子类复写来添加或修改值.

    这个方法的结果将与 tornado.template 模块中其他的默认值还有 render 或 render_string 的关键字
    参数相结合.

RequestHandler.redirect(url, permanent=False, status=None)[源代码]¶

    重定向到给定的URL(可以选择相对路径).

    如果指定了 status 参数, 这个值将作为HTTP状态码; 否则将通过 permanent 参数选择301 (永久) 或者
    302 (临时). 默认是 302 (临时重定向).

RequestHandler.send_error(status_code=500, **kwargs)[源代码]¶

    给浏览器发送给定的HTTP 错误码.

    如果 flush() 已经被调用, 它是不可能发送错误的, 所以这个方法将终止响应. 如果输出已经被写但尚
    未flush, 它将被丢弃并被错误页代替.

    复写 write_error() 来自定义它返回的错误页. 额外的关键字参数将被传递给 write_error.

RequestHandler.write_error(status_code, **kwargs)[源代码]¶

    复写这个方法来实现自定义错误页.

    write_error 可能调用 write, render, set_header,等来产生一般的输出.

    如果错误是由未捕获的异常造成的(包括HTTPError), 三个一组的 exc_info 将变成可用的通过 kwargs
    ["exc_info"]. 注意这个异常可能不是”当前(current)” 目的或方法的异常就像 sys.exc_info() 或 
    traceback.format_exc.

RequestHandler.clear()[源代码]¶

    重置这个响应的所有头部和内容.

RequestHandler.data_received(chunk)[源代码]¶

    实现这个方法来处理请求数据流.

    需要 stream_request_body 装饰器.

Cookies¶

RequestHandler.cookies¶

    self.request.cookies 的别名.

RequestHandler.get_cookie(name, default=None)[源代码]¶

    获取给定name的cookie值, 如果未获取到则返回默认值.

RequestHandler.set_cookie(name, value, domain=None, expires=None, path='/', expires_days=None, 
    **kwargs)[源代码]¶

    设置给定的cookie 名称/值还有其他给定的选项.

    另外的关键字参数在Cookie.Morsel直接设置. 参见 https://docs.python.org/2/library/cookie.html#
    morsel-objects 查看可用的属性.

RequestHandler.clear_cookie(name, path='/', domain=None)[源代码]¶

    删除给定名称的cookie.

    受cookie协议的限制, 必须传递和设置该名称cookie时候相同的path 和domain来清除这个cookie(但是这
    里没有方法来找出在服务端所使用的该cookie的值).

RequestHandler.clear_all_cookies(path='/', domain=None)[源代码]¶

    删除用户在本次请求中所有携带的cookie.

    查看 clear_cookie 方法来获取关于path和domain参数的更多信息.

    在 3.2 版更改: 添加 path 和 domain 参数.

RequestHandler.get_secure_cookie(name, value=None, max_age_days=31, min_version=None)[源代码]¶

    如果给定的签名过的cookie是有效的,则返回，否则返回None.

    解码后的cookie值作为字节字符串返回(不像 get_cookie ).

    在 3.2.1 版更改: 添加 min_version 参数. 引进cookie version 2; 默认版本 1 和 2 都可以接受.

RequestHandler.get_secure_cookie_key_version(name, value=None)[源代码]¶

    返回安全cookie(secure cookie)的签名key版本.

    返回的版本号是int型的.

RequestHandler.set_secure_cookie(name, value, expires_days=30, version=None, **kwargs)[源代码]¶

    给cookie签名和时间戳以防被伪造.

    你必须在你的Application设置中指定 cookie_secret 来使用这个方法. 它应该是一个长的, 随机的字节
    序列作为HMAC密钥来做签名.

    使用 get_secure_cookie() 方法来阅读通过这个方法设置的cookie.

    注意 expires_days 参数设置cookie在浏览器中的有效期, 并且它是独立于 get_secure_cookie 的 
    max_age_days 参数的.

    安全cookie(Secure cookies)可以包含任意字节的值, 而不只是unicode 字符串(不像是普通cookie)

    在 3.2.1 版更改: 添加 version 参数. 提出cookie version 2 并将它作为默认设置.

RequestHandler.create_signed_value(name, value, version=None)[源代码]¶

    产生用时间戳签名的字符串, 防止被伪造.

    一般通过set_secure_cookie 使用, 但对于无cookie使用来说就作为独立的方法来提供. 为了解码不作为
    cookie存储的值, 可以在 get_secure_cookie 使用可选的value参数.

    在 3.2.1 版更改: 添加 version 参数. 提出cookie version 2 并将它作为默认设置.

tornado.web.MIN_SUPPORTED_SIGNED_VALUE_VERSION = 1¶

    这个Tornado版本所支持的最旧的签名值版本.

    比这个签名值更旧的版本将不能被解码.

    3.2.1 新版功能.

tornado.web.MAX_SUPPORTED_SIGNED_VALUE_VERSION = 2¶

    这个Tornado版本所支持的最新的签名值版本.

    比这个签名值更新的版本将不能被解码.

    3.2.1 新版功能.

tornado.web.DEFAULT_SIGNED_VALUE_VERSION = 2¶

    签名值版本通过 RequestHandler.create_signed_value 产生.

    可通过传递一个 version 关键字参数复写.

    3.2.1 新版功能.

tornado.web.DEFAULT_SIGNED_VALUE_MIN_VERSION = 1¶

    可以被 RequestHandler.get_secure_cookie 接受的最旧的签名值.

    可通过传递一个 min_version 关键字参数复写.

    3.2.1 新版功能.

Other¶

RequestHandler.application¶

    为请求提供服务的 Application 对象

RequestHandler.check_etag_header()[源代码]¶

    针对请求的 If-None-Match 头检查 Etag 头.

    如果请求的ETag 匹配则返回 True 并将返回一个304. 例如:

    self.set_etag_header()
    if self.check_etag_header():
        self.set_status(304)
        return

    这个方法在请求结束的时候会被自动调用, 但也可以被更早的调用当复写了 compute_etag 并且想在请求
    完成之前先做一个 If-None-Match 检查. Etag 头应该在这个方法被调用前设置 (可以使用
    set_etag_header).

RequestHandler.check_xsrf_cookie()[源代码]¶

    确认 _xsrf cookie匹配 _xsrf 参数.

    为了预防cross-site请求伪造, 我们设置一个 _xsrf cookie和包含相同值的一个non-cookie字段在所有 
    POST 请求中. 如果这两个不匹配, 我们拒绝这个表单提交作为一个潜在的伪造请求.

    _xsrf 的值可以被设置为一个名为 _xsrf 的表单字段或在一个名为 X-XSRFToken 或 X-CSRFToken 的自
    定义 HTTP头部(后者被接受为了兼容Django).

    查看 http://en.wikipedia.org/wiki/Cross-site_request_forgery

    发布1.1.1 之前, 这个检查会被忽略如果当前的HTTP头部是 X-Requested-With: XMLHTTPRequest . 这个
    异常已被证明是不安全的并且已经被移除. 更多信息请查看 http://www.djangoproject.com/weblog/
    2011/feb/08/security/ http://weblog.rubyonrails.org/2011/2/8/
    csrf-protection-bypass-in-ruby-on-rails

    在 3.2.2 版更改: 添加cookie 2版本的支持. 支持版本1和2.

RequestHandler.compute_etag()[源代码]¶

    计算被用于这个请求的etag头.

    到目前为止默认使用输出内容的hash值.

    可以被复写来提供自定义的etag实现, 或者可以返回None来禁止 tornado 默认的etag支持.

RequestHandler.create_template_loader(template_path)[源代码]¶

    返回给定路径的新模板装载器.

    可以被子类复写. 默认返回一个在给定路径上基于目录的装载器, 使用应用程序的 autoescape 和 
    template_whitespace 设置. 如果应用设置中提供了一个 template_loader , 则使用它来替代.

RequestHandler.current_user¶

    返回请求中被认证的用户.

    可以使用以下两者之一的方式来设置:

      □ 子类可以复写 get_current_user(), 这将会在第一次访问 self.current_user 时自动被调用.
        get_current_user() 在每次请求时只会被调用一次, 并为将来访问做缓存:

        def get_current_user(self):
            user_cookie = self.get_secure_cookie("user")
            if user_cookie:
                return json.loads(user_cookie)
            return None

      □ 它可以被设置为一个普通的变量, 通常在来自被复写的 prepare():

        @gen.coroutine
        def prepare(self):
            user_id_cookie = self.get_secure_cookie("user_id")
            if user_id_cookie:
                self.current_user = yield load_user(user_id_cookie)

    注意 prepare() 可能是一个协程, 尽管 get_current_user() 可能不是, 所以如果加载用户需要异步操
    作后面的形式是必要的.

    用户对象可以是application选择的任意类型.

RequestHandler.get_browser_locale(default='en_US')[源代码]¶

    从 Accept-Language 头决定用户的位置.

    参考 http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.4

RequestHandler.get_current_user()[源代码]¶

    复写来实现获取当前用户, e.g., 从cookie得到.

    这个方法可能不是一个协程.

RequestHandler.get_login_url()[源代码]¶

    复写这个方法自定义基于请求的登陆URL.

    默认情况下, 我们使用application设置中的 login_url 值.

RequestHandler.get_status()[源代码]¶

    返回响应的状态码.

RequestHandler.get_template_path()[源代码]¶

    可以复写为每个handler指定自定义模板路径.

    默认情况下, 我们使用应用设置中的 template_path . 如果返回None则使用调用文件的相对路径加载模
    板.

RequestHandler.get_user_locale()[源代码]¶

    复写这个方法确定认证过的用户所在位置.

    如果返回了None , 我们退回选择 get_browser_locale().

    这个方法应该返回一个 tornado.locale.Locale 对象, 就像调用 tornado.locale.get("en") 得到的那
    样

RequestHandler.locale¶

    返回当前session的位置.

    通过 get_user_locale 来确定, 你可以复写这个方法设置获取locale的条件, e.g., 记录在数据库中的
    用户偏好, 或 get_browser_locale, 使用 Accept-Language 头部.

RequestHandler.log_exception(typ, value, tb)[源代码]¶

    复写来自定义未捕获异常的日志.

    默认情况下 HTTPError 的日志实例作为警告(warning)没有堆栈追踪(在 tornado.general logger), 其
    他作为错误(error)的异常带有堆栈追踪(在 tornado.application logger).

    3.1 新版功能.

RequestHandler.on_connection_close()[源代码]¶

    在异步处理中, 如果客户端关闭了连接将会被调用.

    复写这个方法来清除与长连接相关的资源. 注意这个方法只有当在异步处理连接被关闭才会被调用; 如果
    你需要在每个请求之后做清理, 请复写 on_finish 方法来代替.

    在客户端离开后, 代理可能会保持连接一段时间 (也可能是无限期), 所以这个方法在终端用户关闭他们
    的连接时可能不会被立即执行.

RequestHandler.require_setting(name, feature='this feature')[源代码]¶

    如果给定的app设置未定义则抛出一个异常.

RequestHandler.reverse_url(name, *args)[源代码]¶

    Application.reverse_url 的别名.

RequestHandler.set_etag_header()[源代码]¶

    设置响应的Etag头使用 self.compute_etag() 计算.

    注意: 如果 compute_etag() 返回 None 将不会设置头.

    这个方法在请求结束的时候自动调用.

RequestHandler.settings¶

    self.application.settings 的别名.

RequestHandler.static_url(path, include_host=None, **kwargs)[源代码]¶

    为给定的相对路径的静态文件返回一个静态URL.

    这个方法需要你在你的应用中设置 static_path (既你静态文件的根目录).

    这个方法返回一个带有版本的url (默认情况下会添加 ?v=<signature>), 这会允许静态文件被无限期缓
    存. 这可以被禁用通过传递 include_version=False (默认已经实现; 其他静态文件的实现不需要支持这
    一点, 但它们可能支持其他选项).

    默认情况下这个方法返回当前host的相对URL, 但是如果 include_host 为true则返回的将是绝对路径的
    URL. 如果这个处理函数有一个 include_host 属性, 该值将被所有的 static_url 调用默认使用, 而不
    需要传递 include_host 作为一个关键字参数.

RequestHandler.xsrf_form_html()[源代码]¶

    一个将被包含在所有POST表单中的HTML <input/> 标签.

    它定义了我们在所有POST请求中为了预防伪造跨站请求所检查的 _xsrf 的输入值. 如果你设置了 
    xsrf_cookies application设置, 你必须包含这个HTML 在你所有的HTML表单.

    在一个模板中, 这个方法应该使用 {% module xsrf_form_html() %} 这种方式调用

    查看上面的 check_xsrf_cookie() 了解更多信息.

RequestHandler.xsrf_token¶

    当前用户/会话的XSRF-prevention token.

    为了防止伪造跨站请求, 我们设置一个 ‘_xsrf’ cookie 并在所有POST 请求中包含相同的 ‘_xsrf’ 值作
    为一个参数. 如果这两个不匹配, 我们会把这个提交当作潜在的伪造请求而拒绝掉.

    查看 http://en.wikipedia.org/wiki/Cross-site_request_forgery

    在 3.2.2 版更改: 该xsrf token现在已经在每个请求都有一个随机mask这使得它可以简洁的把token包含
    在页面中是安全的. 查看 http://breachattack.com 浏览更多信息关于这个更改修复的问题. 旧(版本1)
    cookies 将被转换到版本2 当这个方法被调用除非 xsrf_cookie_version Application 被设置为1.

    在 4.3 版更改: 该 xsrf_cookie_kwargs Application 设置可能被用来补充额外的cookie 选项(将会直
    接传递给 set_cookie). 例如, xsrf_cookie_kwargs=dict(httponly=True, secure=True) 将设置 
    secure 和 httponly 标志在 _xsrf cookie.

应用程序配置¶

class tornado.web.Application(handlers=None, default_host='', transforms=None, **settings)[源代
    码]¶

    组成一个web应用程序的请求处理程序的集合.

    该类的实例是可调用的并且可以被直接传递给HTTPServer为应用程序提供服务:

    application = web.Application([
        (r"/", MainPageHandler),
    ])
    http_server = httpserver.HTTPServer(application)
    http_server.listen(8080)
    ioloop.IOLoop.current().start()

    这个类的构造器带有一个列表包含 URLSpec 对象或 (正则表达式, 请求类)元组. 当我们接收到请求, 我
    们按顺序迭代该列表并且实例化和请求路径相匹配的正则表达式所对应的第一个请求类. 请求类可以被指
    定为一个类对象或一个(完全有资格的)名字.

    每个元组可以包含另外的部分, 只要符合 URLSpec 构造器参数的条件. (在Tornado 3.2之前, 只允许包
    含两个或三个元素的元组).

    一个字典可以作为该元组的第三个元素被传递, 它将被用作处理程序构造器的关键字参数和 initialize
    方法. 这种模式也被用于例子中的 StaticFileHandler (注意一个 StaticFileHandler 可以被自动挂载
    连带下面的static_path设置):

    application = web.Application([
        (r"/static/(.*)", web.StaticFileHandler, {"path": "/var/www"}),
    ])

    我们支持虚拟主机通过 add_handlers 方法, 该方法带有一个主机正则表达式作为第一个参数:

    application.add_handlers(r"www\.myhost\.com", [
        (r"/article/([0-9]+)", ArticleHandler),
    ])

    你可以提供静态文件服务通过传递 static_path 配置作为关键字参数. 我们将提供这些文件从 /static/
    URI (这是可配置的通过 static_url_prefix 配置), 并且我们将提供 /favicon.ico 和 /robots.txt 从
    相同目录下. 一个 StaticFileHandler 的自定义子类可以被指定, 通过 static_handler_class 设置.

    settings¶

        传递给构造器的附加关键字参数保存在 settings 字典中, 并经常在文档中被称为”application
        settings”. Settings被用于自定义Tornado的很多方面(虽然在一些情况下, 更丰富的定制可能是通
        过在 RequestHandler 的子类中复写方法). 一些应用程序也喜欢使用 settings 字典作为使一些处
        理程序可以使用应用程序的特定设置的方法, 而无需使用全局变量. Tornado中使用的 Setting描述
        如下.

        一般设置(General settings):

          ☆ autoreload: 如果为 True, 服务进程将会在任意资源文件改变的时候重启, 正如 Debug模式和
            自动重载中描述的那样. 这个选项是Tornado 3.2中新增的; 在这之前这个功能是由 debug 设置
            控制的.
          ☆ debug: 一些调试模式设置的速记, 正如 Debug模式和自动重载中描述的那样. debug=True 设置
            等同于 autoreload=True, compiled_template_cache=False, static_hash_cache=False, 
            serve_traceback=True.
          ☆ default_handler_class 和 default_handler_args: 如果没有发现其他匹配则会使用这个处理
            程序; 使用这个来实现自定义404页面(Tornado 3.2新增).
          ☆ compress_response: 如果为 True, 以文本格式的响应将被自动压缩. Tornado 4.0新增.
          ☆ gzip: 不推荐使用的 compress_response 别名自从 Tornado 4.0.
          ☆ log_function: 这个函数将在每次请求结束的时候调用以记录结果(有一次参数, 该
            RequestHandler 对象). 默认实现是写入 logging 模块的根logger. 也可以通过复写
            Application.log_request 自定义.
          ☆ serve_traceback: 如果为true, 默认的错误页将包含错误信息的回溯. 这个选项是在Tornado
            3.2中新增的; 在此之前这个功能由 debug 设置控制.
          ☆ ui_modules 和 ui_methods: 可以被设置为 UIModule 或UI methods 的映射提供给模板. 可以
            被设置为一个模块, 字典, 或一个模块的列表和/或字典. 参见 UI 模块了解更多细节.

        认证和安全设置(Authentication and security settings):

          ☆ cookie_secret: 被 RequestHandler.get_secure_cookie 使用, set_secure_cookie 用来给
            cookies签名.
          ☆ key_version: 被requestHandler set_secure_cookie 使用一个特殊的key给cookie签名当 
            cookie_secret 是一个 key字典.
          ☆ login_url: authenticated 装饰器将会重定向到这个url 如果该用户没有登陆. 更多自定义特
            性可以通过复写 RequestHandler.get_login_url 实现
          ☆ xsrf_cookies: 如果true, 跨站请求伪造(防护) 将被开启.
          ☆ xsrf_cookie_version: 控制由该server产生的新XSRF cookie的版本. 一般应在默认情况下(这
            将是最高支持的版本), 但是可以被暂时设置为一个较低的值, 在版本切换之间. 在Tornado
            3.2.2 中新增, 这里引入了XSRF cookie 版本2.
          ☆ xsrf_cookie_kwargs: 可设置为额外的参数字典传递给 RequestHandler.set_cookie 为该XSRF
            cookie.
          ☆ twitter_consumer_key, twitter_consumer_secret, friendfeed_consumer_key, 
            friendfeed_consumer_secret, google_consumer_key, google_consumer_secret, 
            facebook_api_key, facebook_secret: 在 tornado.auth 模块中使用来验证各种APIs.

        模板设置:

          ☆ autoescape: 控制对模板的自动转义. 可以被设置为 None 以禁止转义, 或设置为一个所有输出
            都该传递过去的函数 name . 默认是 "xhtml_escape". 可以在每个模板中改变使用 {% 
            autoescape %} 指令.
          ☆ compiled_template_cache: 默认是 True; 如果是 False 模板将会在每次请求重新编译. 这个
            选项是Tornado 3.2中新增的; 在这之前这个功能由 debug 设置控制.
          ☆ template_path: 包含模板文件的文件夹. 可以通过复写 RequestHandler.get_template_path
            进一步定制
          ☆ template_loader: 分配给 tornado.template.BaseLoader 的一个实例自定义模板加载. 如果使
            用了此设置, 则 template_path 和 autoescape 设置都会被忽略. 可通过复写
            RequestHandler.create_template_loader 进一步定制.
          ☆ template_whitespace: 控制处理模板中的空格; 参见 tornado.template.filter_whitespace
            查看允许的值. 在Tornado 4.3中新增.

        静态文件设置:

          ☆ static_hash_cache: 默认为 True; 如果是 False 静态url将会在每次请求重新计算. 这个选项
            是Tornado 3.2中新增的; 在这之前这个功能由 debug 设置控制.
          ☆ static_path: 将被提供服务的静态文件所在的文件夹.
          ☆ static_url_prefix: 静态文件的Url前缀, 默认是 "/static/".
          ☆ static_handler_class, static_handler_args: 可设置成为静态文件使用不同的处理程序代替
            默认的 tornado.web.StaticFileHandler. static_handler_args, 如果设置, 应该是一个关键
            字参数的字典传递给处理程序的 initialize 方法.

    listen(port, address='', **kwargs)[源代码]¶

        为应用程序在给定端口上启动一个HTTP server.

        这是一个方便的别名用来创建一个 HTTPServer 对象并调用它的listen方法. HTTPServer.listen 不
        支持传递关键字参数给 HTTPServer 构造器. 对于高级用途 (e.g. 多进程模式), 不要使用这个方
        法; 创建一个 HTTPServer 并直接调用它的 TCPServer.bind/TCPServer.start 方法.

        注意在调用这个方法之后你仍然需要调用 IOLoop.current().start() 来启动该服务.

        返回 HTTPServer 对象.

        在 4.3 版更改: 现在返回 HTTPServer 对象.

    add_handlers(host_pattern, host_handlers)[源代码]¶

        添加给定的handler到我们的handler表.

        Host 模式将按照它们的添加顺序进行处理. 所有匹配模式将被考虑.

    reverse_url(name, *args)[源代码]¶

        返回名为 name 的handler的URL路径

        处理程序必须作为 URLSpec 添加到应用程序.

        捕获组的参数将在 URLSpec 的正则表达式被替换. 如有必要它们将被转换成string, 编码成utf8,及
        网址转义(url-escaped).

    log_request(handler)[源代码]¶

        写一个完成的HTTP 请求到日志中.

        默认情况下会写到python 根(root)logger. 要改变这种行为无论是子类应用和复写这个方法, 或者
        传递一个函数到应用的设置字典中作为 log_function.

class tornado.web.URLSpec(pattern, handler, kwargs=None, name=None)[源代码]¶

    指定URL和处理程序之间的映射.

    Parameters:

      □ pattern: 被匹配的正则表达式. 任何在正则表达式的group 都将作为参数传递给处理程序的get/
        post/等方法.
      □ handler: 被调用的 RequestHandler 子类.
      □ kwargs (optional): 将被传递给处理程序构造器的额外参数组成的字典.
      □ name (optional): 该处理程序的名称. 被 Application.reverse_url 使用.

    URLSpec 类在 tornado.web.url 名称下也是可用的.

装饰器(Decorators)¶

tornado.web.asynchronous(method)[源代码]¶

    用这个包装请求处理方法如果它们是异步的.

    这个装饰器适用于回调式异步方法; 对于协程, 使用 @gen.coroutine 装饰器而没有 @asynchronous.
    (这是合理的, 因为遗留原因使用两个装饰器一起来提供 @asynchronous 在第一个, 但是在这种情况下 
    @asynchronous 将被忽略)

    这个装饰器应仅适用于 HTTP verb methods; 它的行为是未定义的对于任何其他方法. 这个装饰器不会使
    一个方法异步; 它告诉框架该方法是异步(执行)的. 对于这个装饰器, 该方法必须(至少有时)异步的做一
    些事情这是有用的.

    如果给定了这个装饰器, 当方法返回的时候响应并没有结束. 它是由请求处理程序调用 self.finish()
    来结束该HTTP请求的. 没有这个装饰器, 请求会自动结束当 get() 或 post() 方法返回时. 例如:

    class MyRequestHandler(RequestHandler):
        @asynchronous
        def get(self):
           http = httpclient.AsyncHTTPClient()
           http.fetch("http://friendfeed.com/", self._on_download)

        def _on_download(self, response):
           self.write("Downloaded!")
           self.finish()

    在 3.1 版更改: 可以使用 @gen.coroutine 而不需 @asynchronous.

    在 4.3 版更改: 可以返回任何东西但 None 或者一个可yield的对象来自于被 @asynchronous 装饰的方
    法是错误的. 这样的返回值之前是默认忽略的.

tornado.web.authenticated(method)[源代码]¶

    使用这个装饰的方法要求用户必须登陆.

    如果用户未登陆, 他们将被重定向到已经配置的 login url.

    如果你配置login url带有查询参数, Tornado将假设你知道你正在做什么并使用它. 如果不是, 它将添加
    一个 next 参数这样登陆页就会知道一旦你登陆后将把你送到哪里.

tornado.web.addslash(method)[源代码]¶

    使用这个装饰器给请求路径中添加丢失的slash.

    例如, 使用了这个装饰器请求 /foo 将被重定向到 /foo/ . 你的请求处理映射应该使用正则表达式类似 
    r'/foo/?' 和使用装饰器相结合.

tornado.web.removeslash(method)[源代码]¶

    使用这个装饰器移除请求路径尾部的斜杠(slashes).

    例如, 使用了这个装饰器请求 /foo/ 将被重定向到 /foo . 你的请求处理映射应该使用正则表达式类似 
    r'/foo/*' 和使用装饰器相结合.

tornado.web.stream_request_body(cls)[源代码]¶

    适用于 RequestHandler 子类以开启流式body支持.

    这个装饰器意味着以下变化:

      □ HTTPServerRequest.body 变成了未定义, 并且body参数将不再被 RequestHandler.get_argument 所
        包含.
      □ RequestHandler.prepare 被调用当读到请求头而不是在整个请求体都被读到之后.
      □ 子类必须定义一个方法 data_received(self, data):, 这将被调用0次或多次当数据是可用状态时.
        注意如果该请求的body是空的, data_received 可能不会被调用.
      □ prepare 和 data_received 可能返回Futures对象(就像通过 @gen.coroutine, 在这种情况下下一个
        方法将不会被调用直到这些 futures完成.
      □ 常规的HTTP方法 (post, put, 等)将在整个body被读取后被调用.

    在 data_received 和asynchronous之间有一个微妙的互动 prepare: data_received 的第一次调用可能
    出现在任何地方在调用 prepare 已经返回或 yielded.

其他(Everything else)¶

exception tornado.web.HTTPError(status_code=500, log_message=None, *args, **kwargs)[源代码]¶

    一个将会成为HTTP错误响应的异常.

    抛出一个 HTTPError 是一个更方便的选择比起调用 RequestHandler.send_error 因为它自动结束当前的
    函数.

    为了自定义 HTTPError 的响应, 复写 RequestHandler.write_error.

          • status_code (int) – HTTP状态码. 必须列在 httplib.responses 之中除非给定了 reason 关
            键字参数.
    参    • log_message (string) – 这个错误将会被写入日志的信息(除非该 Application 是debug模式否
    数:     则不会展示给用户). 可能含有 %s-风格的占位符, 它将填补剩余的位置参数.
          • reason (string) – 唯一的关键字参数. HTTP “reason” 短语将随着 status_code 传递给状态
            行. 通常从 status_code, 自动确定但可以使用一个非标准的数字代码.

exception tornado.web.Finish[源代码]¶

    一个会结束请求但不会产生错误响应的异常.

    当一个 RequestHandler 抛出 Finish , 该请求将会结束(调用 RequestHandler.finish 如果该方法尚未
    被调用), 但是错误处理方法 (包括 RequestHandler.write_error)将不会被调用.

    如果 Finish() 创建的时候没有携带参数, 则会发送一个pending响应. 如果 Finish() 给定了参数, 则
    参数将会传递给 RequestHandler.finish().

    这是比复写 write_error 更加便利的方式用来实现自定义错误页 (尤其是在library代码中):

    if self.current_user is None:
        self.set_status(401)
        self.set_header('WWW-Authenticate', 'Basic realm="something"')
        raise Finish()

    在 4.3 版更改: 传递给 Finish() 的参数将被传递给 RequestHandler.finish.

exception tornado.web.MissingArgumentError(arg_name)[源代码]¶

    由 RequestHandler.get_argument 抛出的异常.

    这是 HTTPError 的一个子类, 所以如果是未捕获的400响应码将被用来代替500(并且栈追踪不会被记录到
    日志).

    3.1 新版功能.

class tornado.web.UIModule(handler)[源代码]¶

    一个在页面上可复用, 模块化的UI单元.

    UI模块经常执行附加的查询, 它们也可以包含额外的CSS和 JavaScript, 这些将包含在输出页面上, 在页
    面渲染的时候自动插入.

    UIModule的子类必须复写 render 方法.

    render(*args, **kwargs)[源代码]¶

        在子类中复写以返回这个模块的输出.

    embedded_javascript()[源代码]¶

        复写以返回一个被嵌入页面的JavaScript字符串.

    javascript_files()[源代码]¶

        复写以返回这个模块需要的JavaScript文件列表.

        如果返回值是相对路径, 它们将被传递给 RequestHandler.static_url; 否则会被原样使用.

    embedded_css()[源代码]¶

        复写以返回一个将被嵌入页面的CSS字符串.

    css_files()[源代码]¶

        复写以返回这个模块需要的CSS文件列表.

        如果返回值是相对路径, 它们将被传递给 RequestHandler.static_url; 否则会被原样使用.

    html_head()[源代码]¶

        复写以返回一个将被放入<head/>标签的HTML字符串.

    html_body()[源代码]¶

        复写以返回一个将被放入<body/>标签最后的HTML字符串.

    render_string(path, **kwargs)[源代码]¶

        渲染一个模板并且将它作为一个字符串返回.

class tornado.web.ErrorHandler(application, request, **kwargs)[源代码]¶

    为所有请求生成一个带有 status_code 的错误响应.

class tornado.web.FallbackHandler(application, request, **kwargs)[源代码]¶

    包装其他HTTP server回调的 RequestHandler .

    fallback是一个可调用的对象, 它接收一个 HTTPServerRequest, 诸如一个 Application 或
    tornado.wsgi.WSGIContainer. 这对于在相同server中同时使用 Tornado RequestHandlers 和WSGI是非
    常有用的. 用法:

    wsgi_app = tornado.wsgi.WSGIContainer(
        django.core.handlers.wsgi.WSGIHandler())
    application = tornado.web.Application([
        (r"/foo", FooHandler),
        (r".*", FallbackHandler, dict(fallback=wsgi_app),
    ])

class tornado.web.RedirectHandler(application, request, **kwargs)[源代码]¶

    将所有GET请求重定向到给定的URL.

    你需要为处理程序提供 url 关键字参数, e.g.:

    application = web.Application([
        (r"/oldpath", web.RedirectHandler, {"url": "/newpath"}),
    ])

class tornado.web.StaticFileHandler(application, request, **kwargs)[源代码]¶

    可以为一个目录提供静态内容服务的简单处理程序.

    StaticFileHandler 是自动配置的如果你传递了 static_path 关键字参数给 Application. 这个处理程
    序可以被自定义通过 static_url_prefix, static_handler_class, 和 static_handler_args 配置.

    为了将静态数据目录映射一个额外的路径给这个处理程序你可以在你应用程序中添加一行例如:

    application = web.Application([
        (r"/content/(.*)", web.StaticFileHandler, {"path": "/var/www"}),
    ])

    处理程序构造器需要一个 path 参数, 该参数指定了将被服务内容的本地根目录.

    注意在正则表达式的捕获组需要解析 path 参数的值给get()方法(不同于上面的构造器的参数); 参见
    URLSpec 了解细节.

    为了自动的提供一个文件例如 index.html 当一个目录被请求的时候, 设置 static_handler_args=dict
    (default_filename="index.html") 在你的应用程序设置中(application settings), 或添加 
    default_filename 作为你的 StaticFileHandler 的初始化参数.

    为了最大限度的提高浏览器缓存的有效性, 这个类支持版本化的url(默认情况下使用 ?v= 参数). 如果给
    定了一个版本, 我们指示浏览器无限期的缓存该文件. make_static_url (也可作为
    RequestHandler.static_url) 可以被用来构造一个版本化的url.

    该处理程序主要用户开发和轻量级处理文件服务; 对重型传输,使用专用的静态文件服务是更高效的(例如
    nginx或Apache). 我们支持HTTP Accept-Ranges 机制来返回部分内容(因为一些浏览器需要此功能是为了
    查找在HTML5音频或视频中).

    子类注意事项

    这个类被设计是可以让子类继承的, 但由于静态url是被类方法生成的而不是实例方法的方式, 继承模式
    有点不同寻常. 一定要使用 @classmethod 装饰器当复写一个类方法时. 实例方法可以使用 self.path 
    self.absolute_path, 和 self.modified 属性.

    子类应该只复写在本节讨论的方法; 复写其他方法很容易出错. 最重要的 StaticFileHandler.get 问题
    尤其严重, 由于与 compute_etag 还有其他方法紧密耦合.

    为了改变静态url生成的方式(e.g. 匹配其他服务或CDN), 复写 make_static_url, parse_url_path,
    get_cache_time, 和/或 get_version.

    为了代替所有与文件系统的相互作用(e.g. 从数据库提供静态内容服务), 复写 get_content,
    get_content_size, get_modified_time, get_absolute_path, 和 validate_absolute_path.

    在 3.1 版更改: 一些为子类设计的方法在Tornado 3.1 被添加.

    compute_etag()[源代码]¶

        设置 Etag 头基于static url版本.

        这允许高效的针对缓存版本的 If-None-Match 检查, 并发送正确的 Etag 给局部的响应(i.e. 相同
        的 Etag 为完整的文件).

        3.1 新版功能.

    set_headers()[源代码]¶

        设置响应的内容和缓存头.

        3.1 新版功能.

    should_return_304()[源代码]¶

        如果头部表明我们应该返回304则返回True.

        3.1 新版功能.

    classmethod get_absolute_path(root, path)[源代码]¶

        返回 path 相对于 root 的绝对路径.

        root 是这个 StaticFileHandler 配置的路径(在大多数情况下是 Application 的 static_path 设
        置).

        这个类方法可能在子类中被复写. 默认情况下它返回一个文件系统路径, 但其他字符串可以被使用,
        只要它们是独特的并且被子类复写的 get_content 理解.

        3.1 新版功能.

    validate_absolute_path(root, absolute_path)[源代码]¶

        验证并返回绝对路径.

        root 是 StaticFileHandler 配置的路径,并且 path 是 get_absolute_path 的结果.

        这是一个实例方法在请求过程中被调用, 所以它可能抛出 HTTPError 或者使用类似
        RequestHandler.redirect (返回None在重定向到停止进一步处理之后) 这种方法. 如果丢失文件将
        会生成404错误.

        这个方法可能在返回路径之前修改它, 但是注意任何这样的修改将不会被 make_static_url 理解.

        在实例方法, 这个方法的结果对 self.absolute_path 是可用的.

        3.1 新版功能.

    classmethod get_content(abspath, start=None, end=None)[源代码]¶

        检索位于所给定绝对路径的请求资源的内容.

        这个类方法可以被子类复写. 注意它的特征不同于其他可复写的类方法(没有 settings 参数); 这是
        经过深思熟虑的以确保 abspath 能依靠自己作为缓存键(cache key) .

        这个方法返回一个字节串或一个可迭代的字节串. 对于大文件后者是更优的选择因为它有助于减少内
        存碎片.

        3.1 新版功能.

    classmethod get_content_version(abspath)[源代码]¶

        返回给定路径资源的一个版本字符串.

        这个类方法可以被子类复写. 默认的实现是对文件内容的hash.

        3.1 新版功能.

    get_content_size()[源代码]¶

        检索给定路径中资源的总大小.

        这个方法可以被子类复写.

        3.1 新版功能.

        在 4.0 版更改: 这个方法总是被调用, 而不是仅在部分结果被请求时.

    get_modified_time()[源代码]¶

        返回 self.absolute_path 的最后修改时间.

        可以被子类复写. 应当返回一个 datetime 对象或None.

        3.1 新版功能.

    get_content_type()[源代码]¶

        返回这个请求使用的 Content-Type 头.

        3.1 新版功能.

    set_extra_headers(path)[源代码]¶

        为了子类给响应添加额外的头部

    get_cache_time(path, modified, mime_type)[源代码]¶

        复写来自定义缓存控制行为.

        返回一个正的秒数作为结果可缓存的时间的量或者返回0标记资源可以被缓存一个未指定的时间段(受
        浏览器自身的影响).

        默认情况下带有 v 请求参数的资源返回的缓存过期时间是10年.

    classmethod make_static_url(settings, path, include_version=True)[源代码]¶

        为给定路径构造一个的有版本的url.

        这个方法可以在子类中被复写(但是注意他是一个类方法而不是一个实例方法). 子类只需实现签名 
        make_static_url(cls, settings, path); 其他关键字参数可以通过 static_url 传递, 但这不是标
        准.

        settings 是 Application.settings 字典. path 是被请求的静态路径. 返回的url应该是相对于当
        前host的.

        include_version 决定生成的URL是否应该包含含有给定 path 相对应文件的hash版本查询字符串.

    parse_url_path(url_path)[源代码]¶

        将静态URL路径转换成文件系统路径.

        url_path 是由去掉 static_url_prefix 的URL组成. 返回值应该是相对于 static_path 的文件系统
        路径.

        这是逆 make_static_url .

    classmethod get_version(settings, path)[源代码]¶

        生成用于静态URL的版本字符串.

        settings 是 Application.settings 字典并且 path 是请求资源在文件系统中的相对位置. 返回值
        应该是一个字符串或 None 如果没有版本可以被确定.

        在 3.1 版更改: 这个方法之前建议在子类中复写; get_content_version 现在是首选因为它允许基
        类来处理结果的缓存.

tornado.template — 产生灵活的输出¶

一个简单的模板系统, 将模板编译成Python代码.

基本用法如下:

t = template.Template("<html>{{ myvalue }}</html>")
print t.generate(myvalue="XXX")

Loader 是一个从根目录加载模板并缓存编译过的模板的类:

loader = template.Loader("/home/btaylor")
print loader.load("test.html").generate(myvalue="XXX")

我们编译所有模板至原生的Python. 错误报告是目前... uh, 很有趣. 模板语法如下:

### base.html
<html>
  <head>
    <title>{% block title %}Default title{% end %}</title>
  </head>
  <body>
    <ul>
      {% for student in students %}
        {% block student %}
          <li>{{ escape(student.name) }}</li>
        {% end %}
      {% end %}
    </ul>
  </body>
</html>

### bold.html
{% extends "base.html" %}

{% block title %}A bolder title{% end %}

{% block student %}
  <li><span style="bold">{{ escape(student.name) }}</span></li>
{% end %}

与大多数其他模板系统不同, 我们没有在你的语句中可包含的表达式上放置任何约束. if 和 for 语句块完全
翻译成了Python, 所以你可以写复杂的表达式例如:

{% for student in [p for p in people if p.student and p.age > 23] %}
  <li>{{ escape(student.name) }}</li>
{% end %}

直接翻译成Python意味着你可以很简单的在表达式中使用函数, 就像在上面例子中的 escape() 函数. 你可以
把函数传递到你的模板中就像其他任何变量一样(在一个 RequestHandler 中, 复写
RequestHandler.get_template_namespace):

### Python code
def add(x, y):
   return x + y
template.execute(add=add)

### The template
{{ add(1, 2) }}

默认情况下我们提供了 escape(), url_escape(), json_encode(), 和 squeeze() 函数给所有模板.

典型的应用程序不会手动创建 Template 或 Loader 实例, 而是使用 tornado.web.RequestHandler 中的
render 和 render_string 方法, 这些方法自动的基于 template_path Application 设置加载模板.

以 _tt_ 为前缀命名的变量是模板系统保留的, 不应该被应用程序的代码使用.

语法参考¶

模板表达式被双花括号包围: {{ ... }}. 内容可以是任何python表达式, 会根据当前自动转义(autoescape)
设置被转义并且插入到输出. 其他模板指令使用 {% %}. 这些标签可以被转义作为 {{! 和 {%! 如果你需要在
输出中包含一个原义的 {{ 或 {% .

为了注释掉一段让它从输出中省略, 使用 {# ... #} 包住它.

{% apply *function* %}...{% end %}

    在 apply 和 end 之间应用一个函数到所有模板代码的输出:

    {% apply linkify %}{{name}} said: {{message}}{% end %}

    注意作为一个实现细节使用块会执行嵌套函数, 因此可能产生奇怪的相互作用, 包括通过 {% set %} 设
    置的变量, 或者在循环中使用 {% break %} 或 {% continue %} .

{% autoescape *function* %}

    为当前文件设置自动转义(autoescape)模式. 这不会影响其他文件, 即使是那些通过 {% include %} 引
    用的文件. 注意自动转义也可以全局设置, 在 Application 或 Loader 中.:

    {% autoescape xhtml_escape %}
    {% autoescape None %}

{% block *name* %}...{% end %}

    标明了一个已命名的, 可以使用 {% extends %} 被替换的块. 在父模板中的块将会被子模板中同名块的
    内容替换.:

    <!-- base.html -->
    <title>{% block title %}Default title{% end %}</title>

    <!-- mypage.html -->
    {% extends "base.html" %}
    {% block title %}My page title{% end %}

{% comment ... %}
    一个将会从模板的输出中移除的注释. 注意这里没有 {% end %} 标签; 该注释从 comment 这个词开始到
    %} 标签关闭.
{% extends *filename* %}
    从另一个模板继承. 使用 extends 的模板应该包含一个或多个 block 标签以替换父模板中的内容. 子模
    板内任何不包含在一个 block 标签中的内容都将被忽略. 例如, 参见 {% block %} 标签.
{% for *var* in *expr* %}...{% end %}
    和python的 for 语句一样. {% break %} 和 {% continue %} 可以用在循环里.
{% from *x* import *y* %}
    和python的 import 语句一样.
{% if *condition* %}...{% elif *condition* %}...{% else %}...{% end %}
    条件语句 - 输出第一个条件为true 的部分. ( elif 和 else 部分是可选的)
{% import *module* %}
    和python的 import 语句一样.
{% include *filename* %}
    包含另一个模板文件. 被包含的文件可以看到所有局部变量就像它被直接复制到了该 include 指令的位
    置( {% autoescape %} 指令是一个异常). 替代的, {% module Template(filename, **kwargs) %} 可能
    被用来包含另外的有独立命名空间的模板.
{% module *expr* %}

    渲染一个 UIModule. 该 UIModule 的输出没有转义:

    {% module Template("foo.html", arg=42) %}

    UIModules 是 tornado.web.RequestHandler 类(尤其是它的 render 方法)的一个方法, 并且当模板系统
    在其他上下文中使用时, 它将不工作.

{% raw *expr* %}
    输出给定表达式的结果并且不会转义.
{% set *x* = *y* %}
    设置一个局部变量.
{% try %}...{% except %}...{% else %}...{% finally %}...{% end %}
    和python的 try 语句一样.
{% while *condition* %}... {% end %}
    和python的 while 语句一样. {% break %} 和 {% continue %} 可以用在循环里.
{% whitespace *mode* %}
    为当前文件的剩余部分设置空白模式(whitespace mode) (或直到下一个 {% whitespace %} 指令). 参见
    filter_whitespace 查看可用参数. Tornado 4.3中新增.

Class reference¶

class tornado.template.Template(template_string, name="<string>", loader=None, 
    compress_whitespace=None, autoescape="xhtml_escape", whitespace=None)[源代码]¶

    编译模板.

    我们从给定的template_string编译到Python. 你可以使用generate() 用变量生成模板.

    构造一个模板.

          • template_string (str) – 模板文件的内容.
          • name (str) – 被加载的模板文件名(用于错误信息).
          • loader (tornado.template.BaseLoader) – BaseLoader 负责该模板, 用于解决 {% include %}
    参      和 {% extend %} 指令.
    数:   • compress_whitespace (bool) – 自从Tornado 4.3过时了. 如果为true, 相当于 whitespace=
            "single" , 如果为false, 相当于 whitespace="all" .
          • autoescape (str) – 在模板命名空间中的函数名, 默认情况下为 None 以禁用转义.
          • whitespace (str) – 一个指定处理whitespace 的字符串; 参见 filter_whitespace 了解可选
            项.

    在 4.3 版更改: 增加 whitespace 参数; 弃用 compress_whitespace.

    generate(**kwargs)[源代码]¶

        用给定参数生成此模板.

class tornado.template.BaseLoader(autoescape='xhtml_escape', namespace=None, whitespace=None)[源
    代码]¶

    模板加载器的基类.

    你必须使用一个模板加载器来使用模板的构造器例如 {% extends %} 和 {% include %}. 加载器在所有
    模板首次加载之后进行缓存.

    构造一个模板加载器.

          • autoescape (str) – 在模板命名空间中的函数名, 例如 “xhtml_escape”, 或默认情况下为 
    参      None 来禁用自动转义.
    数:   • namespace (dict) – 一个被加入默认模板命名空间中的字典或 None.
          • whitespace (str) – 一个指定模板中whitespace默认行为的字符串; 参见 filter_whitespace
            查看可选项. 默认是 “single” 对于 ”.html” 和 ”.js” 文件的结束, “all” 是为了其他文件.

    在 4.3 版更改: 添加 whitespace 参数.

    reset()[源代码]¶

        重置已编译模板的缓存.

    resolve_path(name, parent_path=None)[源代码]¶

        转化一个可能相对的路径为绝对路径(内部使用).

    load(name, parent_path=None)[源代码]¶

        加载一个模板.

class tornado.template.Loader(root_directory, **kwargs)[源代码]¶

    一个从单一根文件夹加载的模板加载器.

class tornado.template.DictLoader(dict, **kwargs)[源代码]¶

    一个从字典加载的模板加载器.

exception tornado.template.ParseError(message, filename, lineno)[源代码]¶

    抛出模板的语法错误.

    ParseError 实例有 filename 和 lineno 属性指出错误所在位置.

    在 4.3 版更改: 添加 filename 和 lineno 属性.

tornado.template.filter_whitespace(mode, text)[源代码]¶

    根据 mode 转换空白到 text .

    可用的模式有:

      □ all: 返回所有未更改的空白.
      □ single: 压缩连串的空白用一个空白字符代替, 保留换行符.
      □ oneline: 压缩所有空白到一个空格字符, 在这个过程中移除所有换行符.

    4.3 新版功能.

tornado.escape — 转义和字符串操作¶

HTML, JSON, URLs, 和其他(格式)的转义/非转义方法.

也包含一些其他的各种字符串操作函数.

转义函数¶

tornado.escape.xhtml_escape(value)[源代码]¶

    转义一个字符串使它在HTML 或XML 中有效.

    转义这些字符 <, >, ", ', 和 &. 当属性值使用转义字符串必须用引号括起来.

    在 3.2 版更改: 添加了单引号到转义字符串列表.

tornado.escape.xhtml_unescape(value)[源代码]¶

    反转义一个已经XML转义过的字符串.

tornado.escape.url_escape(value, plus=True)[源代码]¶

    返回一个给定值的URL 编码版本.

    如果 plus 为true (默认值), 空格将被表示为”+”而不是”%20”. 这是适当的为查询字符串, 但不是一个
    URL路径组件. 注意此默认设置和Python的urllib 模块是相反的.

    3.1 新版功能: 该 plus 参数

tornado.escape.url_unescape(value, encoding='utf-8', plus=True)[源代码]¶

    解码来自于URL 的给定值.

    该参数可以是一个字节或unicode 字符串.

    如果encoding 是None , 该结果将会是一个字节串. 否则, 该结果会是指定编码的unicode 字符串.

    如果 plus 是true (默认值), 加号将被解释为空格(文字加号必须被表示为”%2B”). 这是适用于查询字符
    串和form-encoded 的值, 但不是URL 的路径组件. 注意该默认设置和Python 的urllib 模块是相反的.

    3.1 新版功能: 该 plus 参数

tornado.escape.json_encode(value)[源代码]¶

    将给定的Python 对象进行JSON 编码.

tornado.escape.json_decode(value)[源代码]¶

    返回给定JSON 字符串的Python 对象.

Byte/unicode 转换¶

这些函数在Tornado自身中被广泛使用, 但不应该被大多数应用程序直接需要. 值得注意的是,许多这些功能的
复杂性来源于这样一个事实: Tornado 同时支持Python 2 和Python 3.

tornado.escape.utf8(value)[源代码]¶

    将字符串参数转换为字节字符串.

    如果该参数已经是一个字节字符串或None, 则原样返回. 否则它必须是一个unicode 字符串并且被编码成
    utf8.

tornado.escape.to_unicode(value)[源代码]¶

    将字符串参数转换为unicode 字符串.

    如果该参数已经是一个unicode 字符串或None, 则原样返回. 否则它必须是一个字节字符串并且被解码成
    utf8.

tornado.escape.native_str()¶

    转换一个byte 或unicode 字符串到 str 类型. 等价于 Python 2的 utf8 和Python 3的 to_unicode .

tornado.escape.to_basestring(value)[源代码]¶

    将字符串参数转换为basestring 的子类.

    在python2 中, 字节字符串和unicode 字符串几乎是可以互换的, 所以函数处理一个用户提供的参数与
    ascii 字符串常量相结合, 可以使用和应该返回用户提供的类型. 在python3 中, 这两个类型不可以互
    换, 所以这个方法必须转换字节字符串为unicode 字符串.

tornado.escape.recursive_unicode(obj)[源代码]¶

    伴随一个简单的数据结构, 转换字节字符串为unicode 字符串.

    支持列表, 元组, 和字典.

其他函数¶

tornado.escape.linkify(text, shorten=False, extra_params='', require_protocol=False,
    permitted_protocols=['http', 'https'])[源代码]¶

    转换纯文本为带有链接的HTML.

    例如: linkify("Hello http://tornadoweb.org!") 将返回 Hello <a href="http://tornadoweb.org">
    http://tornadoweb.org</a>!

    参数:

      □ shorten: 长url 将被缩短展示.

      □ 
        extra_params: 额外的文本中的链接标签, 或一个可调用的

            带有该链接作为一个参数并返回该额外的文本. e.g. linkify(text, extra_params='rel=
            "nofollow" class="external"'), 或:

            def extra_params_cb(url):
                if url.startswith("http://example.com"):
                    return 'class="internal"'
                else:
                    return 'class="external" rel="nofollow"'
            linkify(text, extra_params=extra_params_cb)

      □ 
        require_protocol: 只有链接url 包括一个协议. 如果这是False,

            例如www.facebook.com 这样的url 也将被linkified.

      □ 
        permitted_protocols: 协议的列表(或集合)应该被linkified,

            e.g. linkify(text, permitted_protocols=["http", "ftp", "mailto"]). 这是非常不安全的,
            包括协议, 比如 javascript.

tornado.escape.squeeze(value)[源代码]¶

    使用单个空格代替所有空格字符组成的序列.

tornado.locale — 国际化支持¶

生成本地化字符串的翻译方法.

要加载区域设置并生成一个翻译后的字符串:

user_locale = tornado.locale.get("es_LA")
print user_locale.translate("Sign out")

tornado.locale.get() 返回最匹配的语言环境, 不一定是你请求的特定的语言环境. 你可以用额外的参数来
支持多元化给 translate(), e.g.:

people = [...]
message = user_locale.translate(
    "%(list)s is online", "%(list)s are online", len(people))
print message % {"list": user_locale.list(people)}

如果 len(people) == 1 则选择第一个字符串, 否则选择第二个字符串.

应用程序应该调用 load_translations (它使用一个简单的CSV 格式) 或 load_gettext_translations (它通
过使用 gettext 和相关工具支持 .mo 格式) 其中之一. 如果没有方法被调用, Locale.translate 方法将会
直接的返回原本的字符串.

tornado.locale.get(*locale_codes)[源代码]¶

    返回给定区域代码的最近匹配.

    我们按顺序遍历所有给定的区域代码. 如果我们有一个确定的或模糊的匹配代码(e.g., “en” 匹配
    “en_US”), 则我们返回该区域. 否则我们移动到列表中的下一个代码.

    默认情况下我们返回 en_US 如果没有发现任何对指定区域的翻译. 你可以改变默认区域通过
    set_default_locale().

tornado.locale.set_default_locale(code)[源代码]¶

    设置默认区域.

    默认语言环境被假定为用于系统中所有的字符串的语言. 从磁盘加载的翻译是从默认的语言环境到目标区
    域的映射. 因此, 你不需要为默认的语言环境创建翻译文件.

tornado.locale.load_translations(directory, encoding=None)[源代码]¶

    从目录中的CSV 文件加载翻译.

    翻译是带有任意的Python 风格指定的占位符的字符串(e.g., My name is %(name)s) 及其相关翻译.

    该目录应该有以下形式的翻译文件 LOCALE.csv, e.g. es_GT.csv. 该CSV 文件应该有两列或三列: 字符
    串, 翻译, 和可选的多个指标. 复数的指标应该是”plural” 或 “singular” 其中之一. 一个给定的字符
    串可以同时有单数和复数形式. 例如 %(name)s liked this 可能有一个不同的动词组合, 这取决于 %
    (name)s 是一个名字还是一个名字列表. 在CSV文件里应该有两个针对于该字符串的行, 一个用指示器指
    示”singular” (奇数), 一个指示”plural” (复数). 对于没有动词的字符串，将改变翻译, 简单的使用
    ”unknown” 或空字符串 (或者不包括在所有列中的).

    这个文件默认使用 csv 模块的”excel”进行读操作. 这种格式在逗号后面不应该包含空格.

    如果没有给定 encoding 参数, 如果该文件包含一个 byte-order marker (BOM), 编码格式将会自动检测
    (在UTF-8 和UTF-16 之间), 如果没有BOM将默认为UTF-8.

    例如翻译 es_LA.csv:

    "I love you","Te amo"
    "%(name)s liked this","A %(name)s les gustó esto","plural"
    "%(name)s liked this","A %(name)s le gustó esto","singular"

    在 4.3 版更改: 添加 encoding 参数. 添加对BOM-based 的编码检测, UTF-16, 和 UTF-8-with-BOM.

tornado.locale.load_gettext_translations(directory, domain)[源代码]¶

    从 gettext 的区域树加载翻译

    区域树和系统的 /usr/share/locale 很类似, 例如:

    {directory}/{lang}/LC_MESSAGES/{domain}.mo

    让你的应用程序翻译有三步是必须的:

     1. 生成POT翻译文件:

        xgettext --language=Python --keyword=_:1,2 -d mydomain file1.py file2.html etc

     2. 合并现有的POT文件:

        msgmerge old.po mydomain.po > new.po

     3. 编译:

        msgfmt mydomain.po -o {directory}/pt_BR/LC_MESSAGES/mydomain.mo

tornado.locale.get_supported_locales()[源代码]¶

    返回所有支持的语言代码列表.

class tornado.locale.Locale(code, translations)[源代码]¶

    对象代表一个区域.

    在调用 load_translations 或 load_gettext_translations 之后, 调用 get 或 get_closest 以得到一
    个Locale对象.

    classmethod get_closest(*locale_codes)[源代码]¶

        返回给定区域代码的最近匹配.

    classmethod get(code)[源代码]¶

        返回给定区域代码的Locale.

        如果这个方法不支持, 我们将抛出一个异常.

    translate(message, plural_message=None, count=None)[源代码]¶

        返回给定信息在当前区域环境下的翻译.

        如果给定了 plural_message , 你也必须有提供 count. 当 count != 1 时, 我们返回 
        plural_message 并且当 count == 1 时, 我们返回给定消息的单数形式.

    format_date(date, gmt_offset=0, relative=True, shorter=False, full_format=False)[源代码]¶

        格式化给定的日期(应该是GMT时间).

        默认情况下, 我们返回一个相对时间(e.g., “2 minutes ago”). 你可以返回一个绝对日期字符串通
        过 relative=False 参数.

        你可以强制使用一个完整的格式化日期(“July 10, 1980”) 通过 full_format=True 参数.

        这个方法主要用于过去的日期. 对于将来的日期, 我们退回到全格式.

    format_day(date, gmt_offset=0, dow=True)[源代码]¶

        将给定日期格式化为一周的某一天.

        例如: “Monday, January 22”. 你可以移除星期几通过 dow=False.

    list(parts)[源代码]¶

        返回给定列表的一个由逗号分隔的部分.

        格式是, e.g., “A, B and C”, “A and B” 或者”A”当列表长度为1.

    friendly_number(value)[源代码]¶

        返回给定整数的一个由逗号分隔的字符串.

class tornado.locale.CSVLocale(code, translations)[源代码]¶

    区域设置使用tornado 的CSV翻译格式.

class tornado.locale.GettextLocale(code, translations)[源代码]¶

    使用 gettext 模块实现Locale.

    pgettext(context, message, plural_message=None, count=None)[源代码]¶

        允许为翻译设置上下文, 接受复数形式.

        使用示例:

        pgettext("law", "right")
        pgettext("good", "right")

        复数信息示例:

        pgettext("organization", "club", "clubs", len(clubs))
        pgettext("stick", "club", "clubs", len(clubs))

        为了使用上下文生成POT文件, 给第1步添加下面的选项到 load_gettext_translations 序列:

        xgettext [basic options] --keyword=pgettext:1c,2 --keyword=pgettext:1c,2,3

        4.2 新版功能.

tornado.websocket — 浏览器与服务器双向通信¶

WebSocket 协议的实现

WebSockets 允许浏览器和服务器之间进行双向通信

所有主流浏览器的现代版本都支持WebSockets(支持情况详见：http://caniuse.com/websockets)

该模块依照最新 WebSocket 协议 RFC 6455 实现.

在 4.0 版更改: 删除了对76 草案协议版本的支持.

class tornado.websocket.WebSocketHandler(application, request, **kwargs)[源代码]¶

    通过继承该类来创建一个基本的 WebSocket handler.

    重写 on_message 来处理收到的消息, 使用 write_message 来发送消息到客户端. 你也可以重写 open
    和 on_close 来处理连接打开和关闭这两个动作.

    有关JavaScript 接口的详细信息： http://dev.w3.org/html5/websockets/ 具体的协议： http://
    tools.ietf.org/html/rfc6455

    一个简单的 WebSocket handler 的实例：服务端直接返回所有收到的消息给客户端

    class EchoWebSocket(tornado.websocket.WebSocketHandler):
        def open(self):
            print("WebSocket opened")

        def on_message(self, message):
            self.write_message(u"You said: " + message)

        def on_close(self):
            print("WebSocket closed")

    WebSockets 并不是标准的 HTTP 连接. “握手”动作符合 HTTP 标准,但是在”握手”动作之后, 协议是基于
    消息的. 因此,Tornado 里大多数的 HTTP 工具对于这类 handler 都是不可用的. 用来通讯的方法只有
    write_message() , ping() , 和 close() . 同样的,你的 request handler 类里应该使用 open() 而不
    是 get() 或者 post()

    如果你在应用中将这个 handler 分配到 /websocket, 你可以通过如下代码实现:

    var ws = new WebSocket("ws://localhost:8888/websocket");
    ws.onopen = function() {
       ws.send("Hello, world");
    };
    ws.onmessage = function (evt) {
       alert(evt.data);
    };

    这个脚本将会弹出一个提示框 :”You said: Hello, world”

    浏览器并没有遵循同源策略(same-origin policy),相应的允许了任意站点使用 javascript 发起任意
    WebSocket 连接来支配其他网络.这令人惊讶,并且是一个潜在的安全漏洞,所以从 Tornado 4.0 开始
    WebSocketHandler 需要对希望接受跨域请求的应用通过重写.

    check_origin (详细信息请查看文档中有关该方法的部分)来进行设置. 没有正确配置这个属性,在建立
    WebSocket 连接时候很可能会导致 403 错误.

    当使用安全的 websocket 连接(wss://) 时, 来自浏览器的连接可能会失败,因为 websocket 没有地方输
    出 “认证成功” 的对话. 你在 websocket 连接建立成功之前,必须使用相同的证书访问一个常规的 HTML
    页面.

Event handlers¶

WebSocketHandler.open(*args, **kwargs)[源代码]¶

    当打开一个新的 WebSocket 时调用

    open 的参数是从 tornado.web.URLSpec 通过正则表达式获取的, 就像获取
    tornado.web.RequestHandler.get 的参数一样

WebSocketHandler.on_message(message)[源代码]¶

    处理在 WebSocket 中收到的消息

    这个方法必须被重写

WebSocketHandler.on_close()[源代码]¶

    当关闭该 WebSocket 时调用

    当连接被彻底关闭并且支持 status code 或 reason phtase 的时候, 可以通过 self.close_code 和 
    self.close_reason 这两个属性来获取它们

    在 4.0 版更改: Added close_code and close_reason attributes. 添加 close_code 和 close_reason
    这两个属性

WebSocketHandler.select_subprotocol(subprotocols)[源代码]¶

    当一个新的 WebSocket 请求特定子协议(subprotocols)时调用

    subprotocols 是一个由一系列能够被客户端正确识别出相应的子协议（subprotocols）的字符串构成的
    list . 这个方法可能会被重载,用来返回 list 中某个匹配字符串, 没有匹配到则返回 None. 如果没有
    找到相应的子协议,虽然服务端并不会自动关闭 WebSocket 连接,但是客户端可以选择关闭连接.

Output¶

WebSocketHandler.write_message(message, binary=False)[源代码]¶

    将给出的 message 发送到客户端

    message 可以是 string 或者 dict（将会被编码成 json ) 如果 binary 为 false, message 将会以
    utf8 的编码发送; 在 binary 模式下 message 可以是任何 byte string.

    如果连接已经关闭, 则会触发 WebSocketClosedError

    在 3.2 版更改: 添加了 WebSocketClosedError (在之前版本会触发 AttributeError)

    在 4.3 版更改: 返回能够被用于 flow control 的 Future.

WebSocketHandler.close(code=None, reason=None)[源代码]¶

    关闭当前 WebSocket

    一旦挥手动作成功,socket将会被关闭.

    code 可能是一个数字构成的状态码, 采用 RFC 6455 section 7.4.1. 定义的值.

    reason 可能是描述连接关闭的文本消息. 这个值被提给客户端,但是不会被 WebSocket 协议单独解释.

    在 4.0 版更改: Added the code and reason arguments.

Configuration¶

WebSocketHandler.check_origin(origin)[源代码]¶

    通过重写这个方法来实现域的切换

    参数 origin 的值来自 HTTP header 中的 Origin ,url 负责初始化这个请求. 这个方法并不是要求客户
    端不发送这样的 heder;这样的请求一直被允许（因为所有的浏览器实现的 websockets 都支持这个
    header ,并且非浏览器客户端没有同样的跨域安全问题.

    返回 True 代表接受,相应的返回 False 代表拒绝.默认拒绝除 host 外其他域的请求.

    这个是一个浏览器防止 XSS 攻击的安全策略,因为 WebSocket 允许绕过通常的同源策略以及不使用 CORS
    头.

    要允许所有跨域通信的话（这在 Tornado 4.0 之前是默认的）,只要简单的重写这个方法让它一直返回
    true 就可以了:

    def check_origin(self, origin):
        return True

    要允许所有所有子域下的连接,可以这样实现:

    def check_origin(self, origin):
        parsed_origin = urllib.parse.urlparse(origin)
        return parsed_origin.netloc.endswith(".mydomain.com")

    4.0 新版功能.

WebSocketHandler.get_compression_options()[源代码]¶

    重写该方法返回当前连接的 compression 选项

    如果这个方法返回 None (默认), compression 将会被禁用. 如果它返回 dict (即使是空
    的),compression 都会被开启. dict 的内容将会被用来控制 compression 所使用的内存和CPU.但是这类
    的设置现在还没有被实现.

    4.1 新版功能.

WebSocketHandler.set_nodelay(value)[源代码]¶

    为当前 stream 设置 no-delay

    在默认情况下, 小块数据会被延迟和/或合并以减少发送包的数量. 这在有些时候会因为 Nagle’s 算法和
    TCP ACKs 相互作用会造成 200-500ms 的延迟.在 WebSocket 连接已经建立的情况下,可以通过设置 
    self.set_nodelay(True) 来降低延迟（这可能会占用更多带宽）

    更多详细信息： BaseIOStream.set_nodelay.

    在 BaseIOStream.set_nodelay 查看详细信息.

    3.1 新版功能.

Other¶

WebSocketHandler.ping(data)[源代码]¶

    发送 ping 包到远端.

WebSocketHandler.on_pong(data)[源代码]¶

    当收到ping 包的响应时执行.

exception tornado.websocket.WebSocketClosedError[源代码]¶

    出现关闭连接错误触发.

    3.2 新版功能.

Client-side support¶

tornado.websocket.websocket_connect(url, io_loop=None, callback=None, connect_timeout=None, 
    on_message_callback=None, compression_options=None)[源代码]¶

    客户端 WebSocket 支持需要指定 url, 返回一个结果为 WebSocketClientConnection 的 Future 对象

    compression_options 作为 WebSocketHandler.get_compression_options 的返回值, 将会以同样的方式
    执行.

    这个连接支持两种类型的操作.在协程风格下,应用程序通常在一个循环里调用 read_message:

    conn = yield websocket_connect(url)
    while True:
        msg = yield conn.read_message()
        if msg is None: break
        # Do something with msg

    在回调风格下,需要传递 on_message_callback 到 websocket_connect 里. 在这两种风格里,一个内容是
    None 的 message 都标志着 WebSocket 连接已经.

    在 3.2 版更改: 允许使用 HTTPRequest 对象来代替 urls.

    在 4.1 版更改: 添加 compression_options 和 on_message_callback .

    不赞成使用 compression_options .

class tornado.websocket.WebSocketClientConnection(io_loop, request, on_message_callback=None, 
    compression_options=None)[源代码]¶

    WebSocket 客户端连接

    这个类不应当直接被实例化, 请使用 websocket_connect

    close(code=None, reason=None)[源代码]¶

        关闭 websocket 连接

        code 和 reason 的文档在 WebSocketHandler.close 下已给出.

        3.2 新版功能.

        在 4.0 版更改: 添加 code 和 reason 这两个参数

    write_message(message, binary=False)[源代码]¶

        发送消息到 websocket 服务器.

    read_message(callback=None)[源代码]¶

        读取来自 WebSocket 服务器的消息.

        如果在 WebSocket 初始化时指定了 on_message_callback ,那么这个方法永远不会返回消息

        如果连接已经关闭,返回结果会是一个结果是 message 的 future 对象或者是 None. 如果 future
        给出了回调参数, 这个参数将会在 future 完成时调用.

HTTP servers and clients¶

tornado.httpserver — 非阻塞 HTTP server¶

非阻塞，单线程 HTTP server。

典型的应用很少与 HTTPServer 类直接交互，除非在进程开始时开启server （尽管这经常间接的通过
tornado.web.Application.listen 来完成）。

在 4.0 版更改: 曾经在此模块中的 HTTPRequest 类已经被移到 tornado.httputil.HTTPServerRequest 。其
旧名称仍作为一个别名。

HTTP Server¶

class tornado.httpserver.HTTPServer(*args, **kwargs)[源代码]¶

    非阻塞，单线程 HTTP server。

    一个server可以由一个 HTTPServerConnectionDelegate 的子类定义，或者，为了向后兼容，由一个以
    HTTPServerRequest 为参数的callback定义。它的委托对象(delegate)通常是 tornado.web.Application
    。

    HTTPServer 默认支持keep-alive链接（对于HTTP/1.1自动开启，而对于HTTP/1.0，需要client发起 
    Connection: keep-alive 请求）。

    如果 xheaders 是 True ，我们支持 X-Real-Ip/X-Forwarded-For 和 X-Scheme/X-Forwarded-Proto 首
    部字段，他们将会覆盖所有请求的 remote IP 与 URI scheme/protocol 。当Tornado运行在反向代理或
    者负载均衡(load balancer)之后时，这些首部字段非常有用。如果Tornado运行在一个不设置任何一个支
    持的 xheaders 的SSL-decoding代理之后， protocol 参数也能设置为 https 。

    要使server可以服务于SSL加密的流量，需要把 ssl_option 参数设置为一个 ssl.SSLContext 对象。为
    了兼容旧版本的Python ssl_options 可能也是一个字典(dictionary)，其中包含传给 ssl.wrap_socket
    方法的关键字参数。:

    ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_ctx.load_cert_chain(os.path.join(data_dir, "mydomain.crt"),
                            os.path.join(data_dir, "mydomain.key"))
    HTTPServer(applicaton, ssl_options=ssl_ctx)

    HTTPServer 的初始化依照以下三种模式之一（初始化方法定义在 tornado.tcpserver.TCPServer ）：

     1. listen: 简单的单进程:

        server = HTTPServer(app)
        server.listen(8888)
        IOLoop.current().start()

        在很多情形下， tornado.web.Application.listen 可以用来避免显式的创建 HTTPServer 。

     2. bind/start: 简单的多进程:

        server = HTTPServer(app)
        server.bind(8888)
        server.start(0)  # Fork 多个子进程
        IOLoop.current().start()

        当使用这个接口时，一个 IOLoop 不能被传给 HTTPServer 的构造方法(constructor)。 start 将默
        认在单例 IOLoop 上开启server。

     3. add_sockets: 高级多进程:

        sockets = tornado.netutil.bind_sockets(8888)
        tornado.process.fork_processes(0)
        server = HTTPServer(app)
        server.add_sockets(sockets)
        IOLoop.current().start()

        add_sockets 接口更加复杂，但是，当fork发生的时候，它可以与
        tornado.process.fork_processes 一起使用来提供更好的灵活性。如果你想使用其他的方法，而不
        是 tornado.netutil.bind_sockets ，来创建监听socket， add_sockets 也可以被用在单进程
        server中。

    在 4.0 版更改: 增加了 decompress_request, chunk_size, max_header_size, 
    idle_connection_timeout, body_timeout, max_body_size 参数。支持 HTTPServerConnectionDelegate
    实例化为 request_callback 。

    在 4.1 版更改: HTTPServerConnectionDelegate.start_request 现在需要传入两个参数来调用 
    (server_conn, request_conn) （根据文档内容）而不是一个 (request_conn).

    在 4.2 版更改: HTTPServer 现在是 tornado.util.Configurable 的一个子类。

tornado.httpclient — 异步 HTTP 客户端¶

阻塞和非阻塞的 HTTP 客户端接口.

这个模块定义了一个被两种实现方式 simple_httpclient 和 curl_httpclient 共享的通用接口 . 应用程序
可以选择直接实例化相对应的实现类, 或使用本模块提供的 AsyncHTTPClient 类, 通过复写
AsyncHTTPClient.configure 方法来选择一种实现 .

默认的实现是 simple_httpclient, 这可以能满足大多数用户的需要 . 然而, 一些应用程序可能会因为以下
原因想切换到 curl_httpclient :

  • curl_httpclient 有一些 simple_httpclient 不具有的功能特性, 包括对 HTTP 代理和使用指定网络接
    口能力的支持.
  • curl_httpclient 更有可能与不完全符合 HTTP 规范的网站兼容, 或者与使用很少使用 HTTP 特性的网站
    兼容.
  • curl_httpclient 更快.
  • curl_httpclient 是 Tornado 2.0 之前的默认值.

注意, 如果你正在使用 curl_httpclient, 强力建议你使用最新版本的 libcurl 和 pycurl. 当前 libcurl
能被支持的最小版本是 7.21.1, pycurl 能被支持的最小版本是 7.18.2. 强烈建议你所安装的 libcurl 是和
异步 DNS 解析器 (threaded 或 c-ares) 一起构建的, 否则你可能会遇到各种请求超时的问题 (更多信息请
查看 http://curl.haxx.se/libcurl/c/curl_easy_setopt.html#CURLOPTCONNECTTIMEOUTMS 和
curl_httpclient.py 里面的注释).

为了选择 curl_httpclient, 只需要在启动的时候调用 AsyncHTTPClient.configure

AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")

HTTP 客户端接口¶

class tornado.httpclient.HTTPClient(async_client_class=None, **kwargs)[源代码]¶

    一个阻塞的 HTTP 客户端.

    提供这个接口是为了方便使用和测试; 大多数运行于 IOLoop 的应用程序会使用 AsyncHTTPClient 来替
    代它. 一般的用法就像这样

    http_client = httpclient.HTTPClient()
    try:
        response = http_client.fetch("http://www.google.com/")
        print response.body
    except httpclient.HTTPError as e:
        # HTTPError is raised for non-200 responses; the response
        # can be found in e.response.
        print("Error: " + str(e))
    except Exception as e:
        # Other errors are possible, such as IOError.
        print("Error: " + str(e))
    http_client.close()

    close()[源代码]¶

        关闭该 HTTPClient, 释放所有使用的资源.

    fetch(request, **kwargs)[源代码]¶

        执行一个请求, 返回一个 HTTPResponse 对象.

        该请求可以是一个 URL 字符串或是一个 HTTPRequest 对象. 如果它是一个字符串, 我们会使用任意
        关键字参数构造一个 HTTPRequest : HTTPRequest(request, **kwargs)

        如果在 fetch 过程中发生错误, 我们将抛出一个 HTTPError 除非 raise_error 关键字参数被设置
        为 False.

class tornado.httpclient.AsyncHTTPClient[源代码]¶

    一个非阻塞 HTTP 客户端.

    使用示例:

    def handle_request(response):
        if response.error:
            print "Error:", response.error
        else:
            print response.body

    http_client = AsyncHTTPClient()
    http_client.fetch("http://www.google.com/", handle_request)

    这个类的构造器有几个比较神奇的考虑: 它实际创建了一个基于特定实现的子类的实例, 并且该实例被作
    为一种伪单例重用 (每一个 IOLoop ). 使用关键字参数 force_instance=True 可以用来限制这种单例行
    为. 只有使用了 force_instance=True 时候, 才可以传递 io_loop 以外其他的参数给 AsyncHTTPClient
    构造器. 实现的子类以及它的构造器的参数可以通过静态方法 configure() 设置.

    所有 AsyncHTTPClient 实现都支持一个 defaults 关键字参数, 可以被用来设置默认 HTTPRequest 属性
    的值. 例如:

    AsyncHTTPClient.configure(
        None, defaults=dict(user_agent="MyUserAgent"))
    # or with force_instance:
    client = AsyncHTTPClient(force_instance=True,
        defaults=dict(user_agent="MyUserAgent"))

    在 4.1 版更改: io_loop 参数被废弃.

    close()[源代码]¶

        销毁该 HTTP 客户端, 释放所有被使用的文件描述符.

        因为 AsyncHTTPClient 对象透明重用的方式, 该方法在正常使用时并不需要 . close() 一般只有在
        IOLoop 也被关闭, 或在创建 AsyncHTTPClient 的时候使用了 force_instance=True 参数才需要.

        在 AsyncHTTPClient 调用 close() 方法后, 其他方法就不能被调用了.

    fetch(request, callback=None, raise_error=True, **kwargs)[源代码]¶

        执行一个请求, 并且异步的返回 HTTPResponse.

        request 参数可以是一个 URL 字符串也可以是一个 HTTPRequest 对象. 如果是一个字符串, 我们将
        使用全部的关键字参数一起构造一个 HTTPRequest 对象: HTTPRequest(request, **kwargs)

        这个方法返回一个结果为 HTTPResponse 的 Future 对象. 默认情况下, 如果该请求返回一个非 200
        的响应码, 这个 Future 将会抛出一个 HTTPError 错误. 相反, 如果 raise_error 设置为 False,
        则无论响应码如何, 都将返回该 response (响应).

        如果给定了 callback , 它将被 HTTPResponse 调用. 在回调接口中, HTTPError 不会自动抛出. 相
        反你必须检查该响应的 error 属性或者调用它的 rethrow 方法.

    classmethod configure(impl, **kwargs)[源代码]¶

        配置要使用的 AsyncHTTPClient 子类.

        AsyncHTTPClient() 实际上是创建一个子类的实例. 此方法可以使用一个类对象或此类的完全限定名
        称(或为 None 则使用默认的, SimpleAsyncHTTPClient) 调用.

        如果给定了额外的关键字参数, 它们将会被传递给创建的每个子类实例的构造函数. 关键字参数 
        max_clients 确定了可以在每个 IOLoop 上并行执行的 fetch() 操作的最大数量. 根据使用的实现
        类不同, 可能支持其他参数.

        例如:

        AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")

Request 对象¶

class tornado.httpclient.HTTPRequest(url, method='GET', headers=None, body=None, auth_username=
    None, auth_password=None, auth_mode=None, connect_timeout=None, request_timeout=None, 
    if_modified_since=None, follow_redirects=None, max_redirects=None, user_agent=None, use_gzip
    =None, network_interface=None, streaming_callback=None, header_callback=None, 
    prepare_curl_callback=None, proxy_host=None, proxy_port=None, proxy_username=None, 
    proxy_password=None, allow_nonstandard_methods=None, validate_cert=None, ca_certs=None, 
    allow_ipv6=None, client_key=None, client_cert=None, body_producer=None, expect_100_continue=
    False, decompress_response=None, ssl_options=None)[源代码]¶

    HTTP 客户端请求对象.

    除了 url 以外所有参数都是可选的.

          • url (string) – fetch 的 URL
          • method (string) – HTTP 方法, e.g. “GET” or “POST”
          • headers (HTTPHeaders 或 dict) – 额外的 HTTP 请求头
          • body – HTTP 请求体字符串 (byte 或 unicode; 如果是 unicode 则使用 utf-8 编码)
          • body_producer – 可以被用于延迟/异步请求体调用. 它可以被调用, 带有一个参数, 一个 
            write 函数, 并应该返回一个 Future 对象. 它应该在新的数据可用时调用 write 函数. write
            函数返回一个可用于流程控制的 Future 对象. 只能指定 body 和 body_producer 其中之一. 
            body_producer 不被 curl_httpclient 支持. 当使用 body_producer 时, 建议传递一个 
            Content-Length 头, 否则将使用其他的分块编码, 并且很多服务断不支持请求的分块编码.
            Tornado 4.0 新增
          • auth_username (string) – HTTP 认证的用户名
          • auth_password (string) – HTTP 认证的密码
          • auth_mode (string) – 认证模式; 默认是 “basic”. 所允许的值是根据实现方式定义的; 
            curl_httpclient 支持 “basic” 和 “digest”; simple_httpclient 只支持 “basic”
          • connect_timeout (float) – 初始化连接的超时时间
          • request_timeout (float) – 整个请求的超时时间
          • if_modified_since (datetime 或 float) – If-Modified-Since 头的时间戳
          • follow_redirects (bool) – 是否应该自动跟随重定向还是返回 3xx 响应?
          • max_redirects (int) – follow_redirects 的最大次数限制
          • user_agent (string) – User-Agent 头
          • decompress_response (bool) – 从服务器请求一个压缩过的响应, 在下载后对其解压缩. 默认
            是 True. Tornado 4.0 新增.
          • use_gzip (bool) – decompress_response 的别名从 Tornado 4.0 已弃用.
          • network_interface (string) – 请求所使用的网络接口. 只有 curl_httpclient ; 请看下面的
    参      备注.
    数:   • streaming_callback (callable) – 如果设置了, streaming_callback 将用它接收到的数据块
            执行, 并且 HTTPResponse.body 和 HTTPResponse.buffer 在最后的响应中将为空.
          • header_callback (callable) – 如果设置了, header_callback 将在接收到每行头信息时运行
            (包括第一行, e.g. HTTP/1.0 200 OK\r\n, 最后一行只包含 \r\n. 所有行都包含结尾的换行
            符). HTTPResponse.headers 在最终响应中将为空. 这与 streaming_callback 结合是最有用
            的, 因为它是在请求正在进行时访问头信息唯一的方法.
          • prepare_curl_callback (callable) – 如果设置, 将使用 pycurl.Curl 对象调用, 以允许应用
            程序进行额外的 setopt 调用.
          • proxy_host (string) – HTTP 代理主机名. 如果想要使用代理, proxy_host 和 proxy_port 必
            须设置; proxy_username 和 proxy_pass 是可选项. 目前只有 curl_httpclient 支持代理.
          • proxy_port (int) – HTTP 代理端口
          • proxy_username (string) – HTTP 代理用户名
          • proxy_password (string) – HTTP 代理密码
          • allow_nonstandard_methods (bool) – 允许 method 参数使用未知值?
          • validate_cert (bool) – 对于 HTTPS 请求, 是否验证服务器的证书?
          • ca_certs (string) – PEM 格式的 CA 证书的文件名, 或者默认为 None. 当与 
            curl_httpclient 一起使用时参阅下面的注释.
          • client_key (string) – 客户端 SSL key 文件名(如果有). 当与 curl_httpclient 一起使用时
            参阅下面的注释.
          • client_cert (string) – 客户端 SSL 证书的文件名(如果有). 当与 curl_httpclient 一起使
            用时参阅下面的注释.
          • ssl_options (ssl.SSLContext) – 用在 simple_httpclient (curl_httpclient 不支持) 的
            ssl.SSLContext 对象. 覆写 validate_cert, ca_certs, client_key, 和 client_cert.
          • allow_ipv6 (bool) – 当 IPv6 可用时是否使用? 默认是 true.
          • expect_100_continue (bool) – 如果为 true, 发送 Expect: 100-continue 头并在发送请求体
            前等待继续响应. 只被 simple_httpclient 支持.

    3.1 新版功能: auth_mode 参数.

    4.0 新版功能: body_producer 和 expect_100_continue 参数.

    4.2 新版功能: ssl_options 参数.

Response 对象¶

class tornado.httpclient.HTTPResponse(request, code, headers=None, buffer=None, effective_url=
    None, error=None, request_time=None, time_info=None, reason=None)[源代码]¶

    HTTP 响应对象.

    属性:

      □ request: HTTPRequest 对象
      □ code: HTTP 状态码数值, e.g. 200 或 404
      □ reason: 人类可读的, 对状态码原因的简短描述
      □ headers: tornado.httputil.HTTPHeaders 对象
      □ effective_url: 跟随重定向后资源的最后位置
      □ buffer: 响应体的 cStringIO 对象
      □ body: string 化的响应体 (从 self.buffer 的需求创建)
      □ error: 任何异常对象
      □ request_time: 请求开始到结束的时间(秒)
      □ time_info: 来自请求的诊断时间信息的字典. 可用数据可能会更改, 不过当前在用的时间信息是
        http://curl.haxx.se/libcurl/c/curl_easy_getinfo.html, 加上 queue, 这是通过等待在
        AsyncHTTPClient 的 max_clients 设置下的插槽引入的延迟(如果有的话).

    rethrow()[源代码]¶

        如果请求中有错误发生, 将抛出一个 HTTPError.

异常¶

exception tornado.httpclient.HTTPError(code, message=None, response=None)[源代码]¶

    一个 HTTP 请求失败后抛出的异常.

    属性:

      □ code - 整数的 HTTP 错误码, e.g. 404. 当没有接收到 HTTP 响应时将会使用 599 错误码, e.g.
        超时.
      □ response - 全部的 HTTPResponse 对象.

    注意如果 follow_redirects 为 False, 重定向将导致 HTTPErrors, 并且你可以通过 
    error.response.headers['Location'] 查看重定向的描述.

Command-line 接口¶

This module provides a simple command-line interface to fetch a url using Tornado’s HTTP client.
Example usage:

# Fetch the url and print its body
python -m tornado.httpclient http://www.google.com

# Just print the headers
python -m tornado.httpclient --print_headers --print_body=false http://www.google.com

Implementations¶

class tornado.simple_httpclient.SimpleAsyncHTTPClient[源代码]¶

    Non-blocking HTTP client with no external dependencies.

    This class implements an HTTP 1.1 client on top of Tornado’s IOStreams. Some features found
    in the curl-based AsyncHTTPClient are not yet supported. In particular, proxies are not
    supported, connections are not reused, and callers cannot select the network interface to be
    used.

    initialize(io_loop, max_clients=10, hostname_mapping=None, max_buffer_size=104857600, 
        resolver=None, defaults=None, max_header_size=None, max_body_size=None)[源代码]¶

        Creates a AsyncHTTPClient.

        Only a single AsyncHTTPClient instance exists per IOLoop in order to provide limitations
        on the number of pending connections. force_instance=True may be used to suppress this
        behavior.

        Note that because of this implicit reuse, unless force_instance is used, only the first
        call to the constructor actually uses its arguments. It is recommended to use the 
        configure method instead of the constructor to ensure that arguments take effect.

        max_clients is the number of concurrent requests that can be in progress; when this
        limit is reached additional requests will be queued. Note that time spent waiting in
        this queue still counts against the request_timeout.

        hostname_mapping is a dictionary mapping hostnames to IP addresses. It can be used to
        make local DNS changes when modifying system-wide settings like /etc/hosts is not
        possible or desirable (e.g. in unittests).

        max_buffer_size (default 100MB) is the number of bytes that can be read into memory at
        once. max_body_size (defaults to max_buffer_size) is the largest response body that the
        client will accept. Without a streaming_callback, the smaller of these two limits
        applies; with a streaming_callback only max_body_size does.

        在 4.2 版更改: Added the max_body_size argument.

class tornado.curl_httpclient.CurlAsyncHTTPClient(io_loop, max_clients=10, defaults=None)[源代
    码]¶

    libcurl-based HTTP client.

tornado.httputil — Manipulate HTTP headers and URLs¶

HTTP utility code shared by clients and servers.

This module also defines the HTTPServerRequest class which is exposed via
tornado.web.RequestHandler.request.

class tornado.httputil.HTTPHeaders(*args, **kwargs)[源代码]¶

    A dictionary that maintains Http-Header-Case for all keys.

    Supports multiple values per key via a pair of new methods, add() and get_list(). The
    regular dictionary interface returns a single value per key, with multiple values joined by
    a comma.

    >>> h = HTTPHeaders({"content-type": "text/html"})
    >>> list(h.keys())
    ['Content-Type']
    >>> h["Content-Type"]
    'text/html'

    >>> h.add("Set-Cookie", "A=B")
    >>> h.add("Set-Cookie", "C=D")
    >>> h["set-cookie"]
    'A=B,C=D'
    >>> h.get_list("set-cookie")
    ['A=B', 'C=D']

    >>> for (k,v) in sorted(h.get_all()):
    ...    print('%s: %s' % (k,v))
    ...
    Content-Type: text/html
    Set-Cookie: A=B
    Set-Cookie: C=D

    add(name, value)[源代码]¶

        Adds a new value for the given key.

    get_list(name)[源代码]¶

        Returns all values for the given header as a list.

    get_all()[源代码]¶

        Returns an iterable of all (name, value) pairs.

        If a header has multiple values, multiple pairs will be returned with the same name.

    parse_line(line)[源代码]¶

        Updates the dictionary with a single header line.

        >>> h = HTTPHeaders()
        >>> h.parse_line("Content-Type: text/html")
        >>> h.get('content-type')
        'text/html'

    classmethod parse(headers)[源代码]¶

        Returns a dictionary from HTTP header text.

        >>> h = HTTPHeaders.parse("Content-Type: text/html\r\nContent-Length: 42\r\n")
        >>> sorted(h.items())
        [('Content-Length', '42'), ('Content-Type', 'text/html')]

class tornado.httputil.HTTPServerRequest(method=None, uri=None, version='HTTP/1.0', headers=None
    , body=None, host=None, files=None, connection=None, start_line=None)[源代码]¶

    A single HTTP request.

    All attributes are type str unless otherwise noted.

    method¶

        HTTP request method, e.g. “GET” or “POST”

    uri¶

        The requested uri.

    path¶

        The path portion of uri

    query¶

        The query portion of uri

    version¶

        HTTP version specified in request, e.g. “HTTP/1.1”

    headers¶

        HTTPHeaders dictionary-like object for request headers. Acts like a case-insensitive
        dictionary with additional methods for repeated headers.

    body¶

        Request body, if present, as a byte string.

    remote_ip¶

        Client’s IP address as a string. If HTTPServer.xheaders is set, will pass along the real
        IP address provided by a load balancer in the X-Real-Ip or X-Forwarded-For header.

    在 3.1 版更改: The list format of X-Forwarded-For is now supported.

    protocol¶

        The protocol used, either “http” or “https”. If HTTPServer.xheaders is set, will pass
        along the protocol used by a load balancer if reported via an X-Scheme header.

    host¶

        The requested hostname, usually taken from the Host header.

    arguments¶

        GET/POST arguments are available in the arguments property, which maps arguments names
        to lists of values (to support multiple values for individual names). Names are of type
        str, while arguments are byte strings. Note that this is different from
        RequestHandler.get_argument, which returns argument values as unicode strings.

    query_arguments¶

        Same format as arguments, but contains only arguments extracted from the query string.

        3.2 新版功能.

    body_arguments¶

        Same format as arguments, but contains only arguments extracted from the request body.

        3.2 新版功能.

    files¶

        File uploads are available in the files property, which maps file names to lists of
        HTTPFile.

    connection¶

        An HTTP request is attached to a single HTTP connection, which can be accessed through
        the “connection” attribute. Since connections are typically kept open in HTTP/1.1,
        multiple requests can be handled sequentially on a single connection.

    在 4.0 版更改: Moved from tornado.httpserver.HTTPRequest.

    supports_http_1_1()[源代码]¶

        Returns True if this request supports HTTP/1.1 semantics.

        4.0 版后已移除: Applications are less likely to need this information with the
        introduction of HTTPConnection. If you still need it, access the version attribute
        directly.

    cookies¶

        A dictionary of Cookie.Morsel objects.

    write(chunk, callback=None)[源代码]¶

        Writes the given chunk to the response stream.

        4.0 版后已移除: Use request.connection and the HTTPConnection methods to write the
        response.

    finish()[源代码]¶

        Finishes this HTTP request on the open connection.

        4.0 版后已移除: Use request.connection and the HTTPConnection methods to write the
        response.

    full_url()[源代码]¶

        Reconstructs the full URL for this request.

    request_time()[源代码]¶

        Returns the amount of time it took for this request to execute.

    get_ssl_certificate(binary_form=False)[源代码]¶

        Returns the client’s SSL certificate, if any.

        To use client certificates, the HTTPServer’s ssl.SSLContext.verify_mode field must be
        set, e.g.:

        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_ctx.load_cert_chain("foo.crt", "foo.key")
        ssl_ctx.load_verify_locations("cacerts.pem")
        ssl_ctx.verify_mode = ssl.CERT_REQUIRED
        server = HTTPServer(app, ssl_options=ssl_ctx)

        By default, the return value is a dictionary (or None, if no client certificate is
        present). If binary_form is true, a DER-encoded form of the certificate is returned
        instead. See SSLSocket.getpeercert() in the standard library for more details. http://
        docs.python.org/library/ssl.html#sslsocket-objects

exception tornado.httputil.HTTPInputError[源代码]¶

    Exception class for malformed HTTP requests or responses from remote sources.

    4.0 新版功能.

exception tornado.httputil.HTTPOutputError[源代码]¶

    Exception class for errors in HTTP output.

    4.0 新版功能.

class tornado.httputil.HTTPServerConnectionDelegate[源代码]¶

    Implement this interface to handle requests from HTTPServer.

    4.0 新版功能.

    start_request(server_conn, request_conn)[源代码]¶

        This method is called by the server when a new request has started.

               • server_conn – is an opaque object representing the long-lived (e.g. tcp-level)
         参      connection.
        数:    • request_conn – is a HTTPConnection object for a single request/response
                 exchange.

        This method should return a HTTPMessageDelegate.

    on_close(server_conn)[源代码]¶

        This method is called when a connection has been closed.

        参数: server_conn – is a server connection that has previously been passed to 
              start_request.

class tornado.httputil.HTTPMessageDelegate[源代码]¶

    Implement this interface to handle an HTTP request or response.

    4.0 新版功能.

    headers_received(start_line, headers)[源代码]¶

        Called when the HTTP headers have been received and parsed.

         参    • start_line – a RequestStartLine or ResponseStartLine depending on whether this
        数:      is a client or server message.
               • headers – a HTTPHeaders instance.

        Some HTTPConnection methods can only be called during headers_received.

        May return a Future; if it does the body will not be read until it is done.

    data_received(chunk)[源代码]¶

        Called when a chunk of data has been received.

        May return a Future for flow control.

    finish()[源代码]¶

        Called after the last chunk of data has been received.

    on_connection_close()[源代码]¶

        Called if the connection is closed without finishing the request.

        If headers_received is called, either finish or on_connection_close will be called, but
        not both.

class tornado.httputil.HTTPConnection[源代码]¶

    Applications use this interface to write their responses.

    4.0 新版功能.

    write_headers(start_line, headers, chunk=None, callback=None)[源代码]¶

        Write an HTTP header block.

              • start_line – a RequestStartLine or ResponseStartLine.
        参    • headers – a HTTPHeaders instance.
        数:   • chunk – the first (optional) chunk of data. This is an optimization so that
                small responses can be written in the same call as their headers.
              • callback – a callback to be run when the write is complete.

        The version field of start_line is ignored.

        Returns a Future if no callback is given.

    write(chunk, callback=None)[源代码]¶

        Writes a chunk of body data.

        The callback will be run when the write is complete. If no callback is given, returns a
        Future.

    finish()[源代码]¶

        Indicates that the last body data has been written.

tornado.httputil.url_concat(url, args)[源代码]¶

    Concatenate url and arguments regardless of whether url has existing query parameters.

    args may be either a dictionary or a list of key-value pairs (the latter allows for multiple
    values with the same key.

    >>> url_concat("http://example.com/foo", dict(c="d"))
    'http://example.com/foo?c=d'
    >>> url_concat("http://example.com/foo?a=b", dict(c="d"))
    'http://example.com/foo?a=b&c=d'
    >>> url_concat("http://example.com/foo?a=b", [("c", "d"), ("c", "d2")])
    'http://example.com/foo?a=b&c=d&c=d2'

class tornado.httputil.HTTPFile[源代码]¶

    Represents a file uploaded via a form.

    For backwards compatibility, its instance attributes are also accessible as dictionary keys.

      □ filename
      □ body
      □ content_type

tornado.httputil.parse_body_arguments(content_type, body, arguments, files, headers=None)[源代
    码]¶

    Parses a form request body.

    Supports application/x-www-form-urlencoded and multipart/form-data. The content_type
    parameter should be a string and body should be a byte string. The arguments and files
    parameters are dictionaries that will be updated with the parsed contents.

tornado.httputil.parse_multipart_form_data(boundary, data, arguments, files)[源代码]¶

    Parses a multipart/form-data body.

    The boundary and data parameters are both byte strings. The dictionaries given in the
    arguments and files parameters will be updated with the contents of the body.

tornado.httputil.format_timestamp(ts)[源代码]¶

    Formats a timestamp in the format used by HTTP.

    The argument may be a numeric timestamp as returned by time.time, a time tuple as returned
    by time.gmtime, or a datetime.datetime object.

    >>> format_timestamp(1359312200)
    'Sun, 27 Jan 2013 18:43:20 GMT'

class tornado.httputil.RequestStartLine¶

    RequestStartLine(method, path, version)

    Create new instance of RequestStartLine(method, path, version)

    method¶

        Alias for field number 0

    path¶

        Alias for field number 1

    version¶

        Alias for field number 2

tornado.httputil.parse_request_start_line(line)[源代码]¶

    Returns a (method, path, version) tuple for an HTTP 1.x request line.

    The response is a collections.namedtuple.

    >>> parse_request_start_line("GET /foo HTTP/1.1")
    RequestStartLine(method='GET', path='/foo', version='HTTP/1.1')

class tornado.httputil.ResponseStartLine¶

    ResponseStartLine(version, code, reason)

    Create new instance of ResponseStartLine(version, code, reason)

    code¶

        Alias for field number 1

    reason¶

        Alias for field number 2

    version¶

        Alias for field number 0

tornado.httputil.parse_response_start_line(line)[源代码]¶

    Returns a (version, code, reason) tuple for an HTTP 1.x response line.

    The response is a collections.namedtuple.

    >>> parse_response_start_line("HTTP/1.1 200 OK")
    ResponseStartLine(version='HTTP/1.1', code=200, reason='OK')

tornado.httputil.split_host_and_port(netloc)[源代码]¶

    Returns (host, port) tuple from netloc.

    Returned port will be None if not present.

    4.1 新版功能.

tornado.http1connection – HTTP/1.x client/server implementation¶

Client and server implementations of HTTP/1.x.

4.0 新版功能.

class tornado.http1connection.HTTP1ConnectionParameters(no_keep_alive=False, chunk_size=None, 
    max_header_size=None, header_timeout=None, max_body_size=None, body_timeout=None, decompress
    =False)[源代码]¶

    Parameters for HTTP1Connection and HTTP1ServerConnection.

            • no_keep_alive (bool) – If true, always close the connection after one request.
            • chunk_size (int) – how much data to read into memory at once
            • max_header_size (int) – maximum amount of data for HTTP headers
    参数:   • header_timeout (float) – how long to wait for all headers (seconds)
            • max_body_size (int) – maximum amount of data for body
            • body_timeout (float) – how long to wait while reading body (seconds)
            • decompress (bool) – if true, decode incoming Content-Encoding: gzip

class tornado.http1connection.HTTP1Connection(stream, is_client, params=None, context=None)[源代
    码]¶

    Implements the HTTP/1.x protocol.

    This class can be on its own for clients, or via HTTP1ServerConnection for servers.

            • stream – an IOStream
            • is_client (bool) – client or server
    参数:   • params – a HTTP1ConnectionParameters instance or None
            • context – an opaque application-defined object that can be accessed as 
              connection.context.

    read_response(delegate)[源代码]¶

        Read a single HTTP response.

        Typical client-mode usage is to write a request using write_headers, write, and finish,
        and then call read_response.

        参数: delegate – a HTTPMessageDelegate

        Returns a Future that resolves to None after the full response has been read.

    set_close_callback(callback)[源代码]¶

        Sets a callback that will be run when the connection is closed.

        4.0 版后已移除: Use HTTPMessageDelegate.on_connection_close instead.

    detach()[源代码]¶

        Take control of the underlying stream.

        Returns the underlying IOStream object and stops all further HTTP processing. May only
        be called during HTTPMessageDelegate.headers_received. Intended for implementing
        protocols like websockets that tunnel over an HTTP handshake.

    set_body_timeout(timeout)[源代码]¶

        Sets the body timeout for a single request.

        Overrides the value from HTTP1ConnectionParameters.

    set_max_body_size(max_body_size)[源代码]¶

        Sets the body size limit for a single request.

        Overrides the value from HTTP1ConnectionParameters.

    write_headers(start_line, headers, chunk=None, callback=None)[源代码]¶

        Implements HTTPConnection.write_headers.

    write(chunk, callback=None)[源代码]¶

        Implements HTTPConnection.write.

        For backwards compatibility is is allowed but deprecated to skip write_headers and
        instead call write() with a pre-encoded header block.

    finish()[源代码]¶

        Implements HTTPConnection.finish.

class tornado.http1connection.HTTP1ServerConnection(stream, params=None, context=None)[源代码]¶

    An HTTP/1.x server.

            • stream – an IOStream
    参数:   • params – a HTTP1ConnectionParameters or None
            • context – an opaque application-defined object that is accessible as 
              connection.context

    close()[源代码]¶

        Closes the connection.

        Returns a Future that resolves after the serving loop has exited.

    start_serving(delegate)[源代码]¶

        Starts serving requests on this connection.

        参数: delegate – a HTTPServerConnectionDelegate

异步网络¶

tornado.ioloop — Main event loop¶

An I/O event loop for non-blocking sockets.

Typical applications will use a single IOLoop object, in the IOLoop.instance singleton. The
IOLoop.start method should usually be called at the end of the main() function. Atypical
applications may use more than one IOLoop, such as one IOLoop per thread, or per unittest case.

In addition to I/O events, the IOLoop can also schedule time-based events. IOLoop.add_timeout is
a non-blocking alternative to time.sleep.

IOLoop objects¶

class tornado.ioloop.IOLoop[源代码]¶

    A level-triggered I/O loop.

    We use epoll (Linux) or kqueue (BSD and Mac OS X) if they are available, or else we fall
    back on select(). If you are implementing a system that needs to handle thousands of
    simultaneous connections, you should use a system that supports either epoll or kqueue.

    Example usage for a simple TCP server:

    import errno
    import functools
    import tornado.ioloop
    import socket

    def connection_ready(sock, fd, events):
        while True:
            try:
                connection, address = sock.accept()
            except socket.error as e:
                if e.args[0] not in (errno.EWOULDBLOCK, errno.EAGAIN):
                    raise
                return
            connection.setblocking(0)
            handle_connection(connection, address)

    if __name__ == '__main__':
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setblocking(0)
        sock.bind(("", port))
        sock.listen(128)

        io_loop = tornado.ioloop.IOLoop.current()
        callback = functools.partial(connection_ready, sock)
        io_loop.add_handler(sock.fileno(), callback, io_loop.READ)
        io_loop.start()

    By default, a newly-constructed IOLoop becomes the thread’s current IOLoop, unless there
    already is a current IOLoop. This behavior can be controlled with the make_current argument
    to the IOLoop constructor: if make_current=True, the new IOLoop will always try to become
    current and it raises an error if there is already a current instance. If make_current=False
    , the new IOLoop will not try to become current.

    在 4.2 版更改: Added the make_current keyword argument to the IOLoop constructor.

Running an IOLoop¶

static IOLoop.current(instance=True)[源代码]¶

    Returns the current thread’s IOLoop.

    If an IOLoop is currently running or has been marked as current by make_current, returns
    that instance. If there is no current IOLoop, returns IOLoop.instance() (i.e. the main
    thread’s IOLoop, creating one if necessary) if instance is true.

    In general you should use IOLoop.current as the default when constructing an asynchronous
    object, and use IOLoop.instance when you mean to communicate to the main thread from a
    different one.

    在 4.1 版更改: Added instance argument to control the fallback to IOLoop.instance().

IOLoop.make_current()[源代码]¶

    Makes this the IOLoop for the current thread.

    An IOLoop automatically becomes current for its thread when it is started, but it is
    sometimes useful to call make_current explicitly before starting the IOLoop, so that code
    run at startup time can find the right instance.

    在 4.1 版更改: An IOLoop created while there is no current IOLoop will automatically become
    current.

static IOLoop.instance()[源代码]¶

    Returns a global IOLoop instance.

    Most applications have a single, global IOLoop running on the main thread. Use this method
    to get this instance from another thread. In most other cases, it is better to use current()
    to get the current thread’s IOLoop.

static IOLoop.initialized()[源代码]¶

    Returns true if the singleton instance has been created.

IOLoop.install()[源代码]¶

    Installs this IOLoop object as the singleton instance.

    This is normally not necessary as instance() will create an IOLoop on demand, but you may
    want to call install to use a custom subclass of IOLoop.

static IOLoop.clear_instance()[源代码]¶

    Clear the global IOLoop instance.

    4.0 新版功能.

IOLoop.start()[源代码]¶

    Starts the I/O loop.

    The loop will run until one of the callbacks calls stop(), which will make the loop stop
    after the current event iteration completes.

IOLoop.stop()[源代码]¶

    Stop the I/O loop.

    If the event loop is not currently running, the next call to start() will return
    immediately.

    To use asynchronous methods from otherwise-synchronous code (such as unit tests), you can
    start and stop the event loop like this:

    ioloop = IOLoop()
    async_method(ioloop=ioloop, callback=ioloop.stop)
    ioloop.start()

    ioloop.start() will return after async_method has run its callback, whether that callback
    was invoked before or after ioloop.start.

    Note that even after stop has been called, the IOLoop is not completely stopped until
    IOLoop.start has also returned. Some work that was scheduled before the call to stop may
    still be run before the IOLoop shuts down.

IOLoop.run_sync(func, timeout=None)[源代码]¶

    Starts the IOLoop, runs the given function, and stops the loop.

    The function must return either a yieldable object or None. If the function returns a
    yieldable object, the IOLoop will run until the yieldable is resolved (and run_sync() will
    return the yieldable’s result). If it raises an exception, the IOLoop will stop and the
    exception will be re-raised to the caller.

    The keyword-only argument timeout may be used to set a maximum duration for the function. If
    the timeout expires, a TimeoutError is raised.

    This method is useful in conjunction with tornado.gen.coroutine to allow asynchronous calls
    in a main() function:

    @gen.coroutine
    def main():
        # do stuff...

    if __name__ == '__main__':
        IOLoop.current().run_sync(main)

    在 4.3 版更改: Returning a non-None, non-yieldable value is now an error.

IOLoop.close(all_fds=False)[源代码]¶

    Closes the IOLoop, freeing any resources used.

    If all_fds is true, all file descriptors registered on the IOLoop will be closed (not just
    the ones created by the IOLoop itself).

    Many applications will only use a single IOLoop that runs for the entire lifetime of the
    process. In that case closing the IOLoop is not necessary since everything will be cleaned
    up when the process exits. IOLoop.close is provided mainly for scenarios such as unit tests,
    which create and destroy a large number of IOLoops.

    An IOLoop must be completely stopped before it can be closed. This means that IOLoop.stop()
    must be called and IOLoop.start() must be allowed to return before attempting to call
    IOLoop.close(). Therefore the call to close will usually appear just after the call to start
    rather than near the call to stop.

    在 3.1 版更改: If the IOLoop implementation supports non-integer objects for “file
    descriptors”, those objects will have their close method when all_fds is true.

I/O events¶

IOLoop.add_handler(fd, handler, events)[源代码]¶

    Registers the given handler to receive the given events for fd.

    The fd argument may either be an integer file descriptor or a file-like object with a fileno
    () method (and optionally a close() method, which may be called when the IOLoop is shut
    down).

    The events argument is a bitwise or of the constants IOLoop.READ, IOLoop.WRITE, and 
    IOLoop.ERROR.

    When an event occurs, handler(fd, events) will be run.

    在 4.0 版更改: Added the ability to pass file-like objects in addition to raw file
    descriptors.

IOLoop.update_handler(fd, events)[源代码]¶

    Changes the events we listen for fd.

    在 4.0 版更改: Added the ability to pass file-like objects in addition to raw file
    descriptors.

IOLoop.remove_handler(fd)[源代码]¶

    Stop listening for events on fd.

    在 4.0 版更改: Added the ability to pass file-like objects in addition to raw file
    descriptors.

Callbacks and timeouts¶

IOLoop.add_callback(callback, *args, **kwargs)[源代码]¶

    Calls the given callback on the next I/O loop iteration.

    It is safe to call this method from any thread at any time, except from a signal handler.
    Note that this is the only method in IOLoop that makes this thread-safety guarantee; all
    other interaction with the IOLoop must be done from that IOLoop‘s thread. add_callback() may
    be used to transfer control from other threads to the IOLoop‘s thread.

    To add a callback from a signal handler, see add_callback_from_signal.

IOLoop.add_callback_from_signal(callback, *args, **kwargs)[源代码]¶

    Calls the given callback on the next I/O loop iteration.

    Safe for use from a Python signal handler; should not be used otherwise.

    Callbacks added with this method will be run without any stack_context, to avoid picking up
    the context of the function that was interrupted by the signal.

IOLoop.add_future(future, callback)[源代码]¶

    Schedules a callback on the IOLoop when the given Future is finished.

    The callback is invoked with one argument, the Future.

IOLoop.add_timeout(deadline, callback, *args, **kwargs)[源代码]¶

    Runs the callback at the time deadline from the I/O loop.

    Returns an opaque handle that may be passed to remove_timeout to cancel.

    deadline may be a number denoting a time (on the same scale as IOLoop.time, normally
    time.time), or a datetime.timedelta object for a deadline relative to the current time.
    Since Tornado 4.0, call_later is a more convenient alternative for the relative case since
    it does not require a timedelta object.

    Note that it is not safe to call add_timeout from other threads. Instead, you must use
    add_callback to transfer control to the IOLoop‘s thread, and then call add_timeout from
    there.

    Subclasses of IOLoop must implement either add_timeout or call_at; the default
    implementations of each will call the other. call_at is usually easier to implement, but
    subclasses that wish to maintain compatibility with Tornado versions prior to 4.0 must use
    add_timeout instead.

    在 4.0 版更改: Now passes through *args and **kwargs to the callback.

IOLoop.call_at(when, callback, *args, **kwargs)[源代码]¶

    Runs the callback at the absolute time designated by when.

    when must be a number using the same reference point as IOLoop.time.

    Returns an opaque handle that may be passed to remove_timeout to cancel. Note that unlike
    the asyncio method of the same name, the returned object does not have a cancel() method.

    See add_timeout for comments on thread-safety and subclassing.

    4.0 新版功能.

IOLoop.call_later(delay, callback, *args, **kwargs)[源代码]¶

    Runs the callback after delay seconds have passed.

    Returns an opaque handle that may be passed to remove_timeout to cancel. Note that unlike
    the asyncio method of the same name, the returned object does not have a cancel() method.

    See add_timeout for comments on thread-safety and subclassing.

    4.0 新版功能.

IOLoop.remove_timeout(timeout)[源代码]¶

    Cancels a pending timeout.

    The argument is a handle as returned by add_timeout. It is safe to call remove_timeout even
    if the callback has already been run.

IOLoop.spawn_callback(callback, *args, **kwargs)[源代码]¶

    Calls the given callback on the next IOLoop iteration.

    Unlike all other callback-related methods on IOLoop, spawn_callback does not associate the
    callback with its caller’s stack_context, so it is suitable for fire-and-forget callbacks
    that should not interfere with the caller.

    4.0 新版功能.

IOLoop.time()[源代码]¶

    Returns the current time according to the IOLoop‘s clock.

    The return value is a floating-point number relative to an unspecified time in the past.

    By default, the IOLoop‘s time function is time.time. However, it may be configured to use
    e.g. time.monotonic instead. Calls to add_timeout that pass a number instead of a
    datetime.timedelta should use this function to compute the appropriate time, so they can
    work no matter what time function is chosen.

class tornado.ioloop.PeriodicCallback(callback, callback_time, io_loop=None)[源代码]¶

    Schedules the given callback to be called periodically.

    The callback is called every callback_time milliseconds. Note that the timeout is given in
    milliseconds, while most other time-related functions in Tornado use seconds.

    If the callback runs for longer than callback_time milliseconds, subsequent invocations will
    be skipped to get back on schedule.

    start must be called after the PeriodicCallback is created.

    在 4.1 版更改: The io_loop argument is deprecated.

    start()[源代码]¶

        Starts the timer.

    stop()[源代码]¶

        Stops the timer.

    is_running()[源代码]¶

        Return True if this PeriodicCallback has been started.

        4.1 新版功能.

Debugging and error handling¶

IOLoop.handle_callback_exception(callback)[源代码]¶

    This method is called whenever a callback run by the IOLoop throws an exception.

    By default simply logs the exception as an error. Subclasses may override this method to
    customize reporting of exceptions.

    The exception itself is not passed explicitly, but is available in sys.exc_info.

IOLoop.set_blocking_signal_threshold(seconds, action)[源代码]¶

    Sends a signal if the IOLoop is blocked for more than s seconds.

    Pass seconds=None to disable. Requires Python 2.6 on a unixy platform.

    The action parameter is a Python signal handler. Read the documentation for the signal
    module for more information. If action is None, the process will be killed if it is blocked
    for too long.

IOLoop.set_blocking_log_threshold(seconds)[源代码]¶

    Logs a stack trace if the IOLoop is blocked for more than s seconds.

    Equivalent to set_blocking_signal_threshold(seconds, self.log_stack)

IOLoop.log_stack(signal, frame)[源代码]¶

    Signal handler to log the stack trace of the current thread.

    For use with set_blocking_signal_threshold.

Methods for subclasses¶

IOLoop.initialize(make_current=None)[源代码]¶

IOLoop.close_fd(fd)[源代码]¶

    Utility method to close an fd.

    If fd is a file-like object, we close it directly; otherwise we use os.close.

    This method is provided for use by IOLoop subclasses (in implementations of IOLoop.close
    (all_fds=True) and should not generally be used by application code.

    4.0 新版功能.

IOLoop.split_fd(fd)[源代码]¶

    Returns an (fd, obj) pair from an fd parameter.

    We accept both raw file descriptors and file-like objects as input to add_handler and
    related methods. When a file-like object is passed, we must retain the object itself so we
    can close it correctly when the IOLoop shuts down, but the poller interfaces favor file
    descriptors (they will accept file-like objects and call fileno() for you, but they always
    return the descriptor itself).

    This method is provided for use by IOLoop subclasses and should not generally be used by
    application code.

    4.0 新版功能.

tornado.iostream — Convenient wrappers for non-blocking sockets¶

Utility classes to write to and read from non-blocking files and sockets.

Contents:

  • BaseIOStream: Generic interface for reading and writing.
  • IOStream: Implementation of BaseIOStream using non-blocking sockets.
  • SSLIOStream: SSL-aware version of IOStream.
  • PipeIOStream: Pipe-based IOStream implementation.

Base class¶

class tornado.iostream.BaseIOStream(io_loop=None, max_buffer_size=None, read_chunk_size=None, 
    max_write_buffer_size=None)[源代码]¶

    A utility class to write to and read from a non-blocking file or socket.

    We support a non-blocking write() and a family of read_*() methods. All of the methods take
    an optional callback argument and return a Future only if no callback is given. When the
    operation completes, the callback will be run or the Future will resolve with the data read
    (or None for write()). All outstanding Futures will resolve with a StreamClosedError when
    the stream is closed; users of the callback interface will be notified via
    BaseIOStream.set_close_callback instead.

    When a stream is closed due to an error, the IOStream’s error attribute contains the
    exception object.

    Subclasses must implement fileno, close_fd, write_to_fd, read_from_fd, and optionally
    get_fd_error.

    BaseIOStream constructor.

           • io_loop – The IOLoop to use; defaults to IOLoop.current. Deprecated since Tornado
             4.1.
     参    • max_buffer_size – Maximum amount of incoming data to buffer; defaults to 100MB.
    数:    • read_chunk_size – Amount of data to read at one time from the underlying transport;
             defaults to 64KB.
           • max_write_buffer_size – Amount of outgoing data to buffer; defaults to unlimited.

    在 4.0 版更改: Add the max_write_buffer_size parameter. Changed default read_chunk_size to
    64KB.

Main interface¶

BaseIOStream.write(data, callback=None)[源代码]¶

    Asynchronously write the given data to this stream.

    If callback is given, we call it when all of the buffered write data has been successfully
    written to the stream. If there was previously buffered write data and an old write
    callback, that callback is simply overwritten with this new callback.

    If no callback is given, this method returns a Future that resolves (with a result of None)
    when the write has been completed. If write is called again before that Future has resolved,
    the previous future will be orphaned and will never resolve.

    在 4.0 版更改: Now returns a Future if no callback is given.

BaseIOStream.read_bytes(num_bytes, callback=None, streaming_callback=None, partial=False)[源代
    码]¶

    Asynchronously read a number of bytes.

    If a streaming_callback is given, it will be called with chunks of data as they become
    available, and the final result will be empty. Otherwise, the result is all the data that
    was read. If a callback is given, it will be run with the data as an argument; if not, this
    method returns a Future.

    If partial is true, the callback is run as soon as we have any bytes to return (but never
    more than num_bytes)

    在 4.0 版更改: Added the partial argument. The callback argument is now optional and a
    Future will be returned if it is omitted.

BaseIOStream.read_until(delimiter, callback=None, max_bytes=None)[源代码]¶

    Asynchronously read until we have found the given delimiter.

    The result includes all the data read including the delimiter. If a callback is given, it
    will be run with the data as an argument; if not, this method returns a Future.

    If max_bytes is not None, the connection will be closed if more than max_bytes bytes have
    been read and the delimiter is not found.

    在 4.0 版更改: Added the max_bytes argument. The callback argument is now optional and a
    Future will be returned if it is omitted.

BaseIOStream.read_until_regex(regex, callback=None, max_bytes=None)[源代码]¶

    Asynchronously read until we have matched the given regex.

    The result includes the data that matches the regex and anything that came before it. If a
    callback is given, it will be run with the data as an argument; if not, this method returns
    a Future.

    If max_bytes is not None, the connection will be closed if more than max_bytes bytes have
    been read and the regex is not satisfied.

    在 4.0 版更改: Added the max_bytes argument. The callback argument is now optional and a
    Future will be returned if it is omitted.

BaseIOStream.read_until_close(callback=None, streaming_callback=None)[源代码]¶

    Asynchronously reads all data from the socket until it is closed.

    If a streaming_callback is given, it will be called with chunks of data as they become
    available, and the final result will be empty. Otherwise, the result is all the data that
    was read. If a callback is given, it will be run with the data as an argument; if not, this
    method returns a Future.

    Note that if a streaming_callback is used, data will be read from the socket as quickly as
    it becomes available; there is no way to apply backpressure or cancel the reads. If flow
    control or cancellation are desired, use a loop with read_bytes(partial=True) instead.

    在 4.0 版更改: The callback argument is now optional and a Future will be returned if it is
    omitted.

BaseIOStream.close(exc_info=False)[源代码]¶

    Close this stream.

    If exc_info is true, set the error attribute to the current exception from sys.exc_info (or
    if exc_info is a tuple, use that instead of sys.exc_info).

BaseIOStream.set_close_callback(callback)[源代码]¶

    Call the given callback when the stream is closed.

    This is not necessary for applications that use the Future interface; all outstanding 
    Futures will resolve with a StreamClosedError when the stream is closed.

BaseIOStream.closed()[源代码]¶

    Returns true if the stream has been closed.

BaseIOStream.reading()[源代码]¶

    Returns true if we are currently reading from the stream.

BaseIOStream.writing()[源代码]¶

    Returns true if we are currently writing to the stream.

BaseIOStream.set_nodelay(value)[源代码]¶

    Sets the no-delay flag for this stream.

    By default, data written to TCP streams may be held for a time to make the most efficient
    use of bandwidth (according to Nagle’s algorithm). The no-delay flag requests that data be
    written as soon as possible, even if doing so would consume additional bandwidth.

    This flag is currently defined only for TCP-based IOStreams.

    3.1 新版功能.

Methods for subclasses¶

BaseIOStream.fileno()[源代码]¶

    Returns the file descriptor for this stream.

BaseIOStream.close_fd()[源代码]¶

    Closes the file underlying this stream.

    close_fd is called by BaseIOStream and should not be called elsewhere; other users should
    call close instead.

BaseIOStream.write_to_fd(data)[源代码]¶

    Attempts to write data to the underlying file.

    Returns the number of bytes written.

BaseIOStream.read_from_fd()[源代码]¶

    Attempts to read from the underlying file.

    Returns None if there was nothing to read (the socket returned EWOULDBLOCK or equivalent),
    otherwise returns the data. When possible, should return no more than self.read_chunk_size
    bytes at a time.

BaseIOStream.get_fd_error()[源代码]¶

    Returns information about any error on the underlying file.

    This method is called after the IOLoop has signaled an error on the file descriptor, and
    should return an Exception (such as socket.error with additional information, or None if no
    such information is available.

Implementations¶

class tornado.iostream.IOStream(socket, *args, **kwargs)[源代码]¶

    Socket-based IOStream implementation.

    This class supports the read and write methods from BaseIOStream plus a connect method.

    The socket parameter may either be connected or unconnected. For server operations the
    socket is the result of calling socket.accept. For client operations the socket is created
    with socket.socket, and may either be connected before passing it to the IOStream or
    connected with IOStream.connect.

    A very simple (and broken) HTTP client using this class:

    import tornado.ioloop
    import tornado.iostream
    import socket

    def send_request():
        stream.write(b"GET / HTTP/1.0\r\nHost: friendfeed.com\r\n\r\n")
        stream.read_until(b"\r\n\r\n", on_headers)

    def on_headers(data):
        headers = {}
        for line in data.split(b"\r\n"):
           parts = line.split(b":")
           if len(parts) == 2:
               headers[parts[0].strip()] = parts[1].strip()
        stream.read_bytes(int(headers[b"Content-Length"]), on_body)

    def on_body(data):
        print(data)
        stream.close()
        tornado.ioloop.IOLoop.current().stop()

    if __name__ == '__main__':
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        stream = tornado.iostream.IOStream(s)
        stream.connect(("friendfeed.com", 80), send_request)
        tornado.ioloop.IOLoop.current().start()

    connect(address, callback=None, server_hostname=None)[源代码]¶

        Connects the socket to a remote address without blocking.

        May only be called if the socket passed to the constructor was not previously connected.
        The address parameter is in the same format as for socket.connect for the type of socket
        passed to the IOStream constructor, e.g. an (ip, port) tuple. Hostnames are accepted
        here, but will be resolved synchronously and block the IOLoop. If you have a hostname
        instead of an IP address, the TCPClient class is recommended instead of calling this
        method directly. TCPClient will do asynchronous DNS resolution and handle both IPv4 and
        IPv6.

        If callback is specified, it will be called with no arguments when the connection is
        completed; if not this method returns a Future (whose result after a successful
        connection will be the stream itself).

        In SSL mode, the server_hostname parameter will be used for certificate validation
        (unless disabled in the ssl_options) and SNI (if supported; requires Python 2.7.9+).

        Note that it is safe to call IOStream.write while the connection is pending, in which
        case the data will be written as soon as the connection is ready. Calling IOStream read
        methods before the socket is connected works on some platforms but is non-portable.

        在 4.0 版更改: If no callback is given, returns a Future.

        在 4.2 版更改: SSL certificates are validated by default; pass ssl_options=dict
        (cert_reqs=ssl.CERT_NONE) or a suitably-configured ssl.SSLContext to the SSLIOStream
        constructor to disable.

    start_tls(server_side, ssl_options=None, server_hostname=None)[源代码]¶

        Convert this IOStream to an SSLIOStream.

        This enables protocols that begin in clear-text mode and switch to SSL after some
        initial negotiation (such as the STARTTLS extension to SMTP and IMAP).

        This method cannot be used if there are outstanding reads or writes on the stream, or if
        there is any data in the IOStream’s buffer (data in the operating system’s socket buffer
        is allowed). This means it must generally be used immediately after reading or writing
        the last clear-text data. It can also be used immediately after connecting, before any
        reads or writes.

        The ssl_options argument may be either an ssl.SSLContext object or a dictionary of
        keyword arguments for the ssl.wrap_socket function. The server_hostname argument will be
        used for certificate validation unless disabled in the ssl_options.

        This method returns a Future whose result is the new SSLIOStream. After this method has
        been called, any other operation on the original stream is undefined.

        If a close callback is defined on this stream, it will be transferred to the new stream.

        4.0 新版功能.

        在 4.2 版更改: SSL certificates are validated by default; pass ssl_options=dict
        (cert_reqs=ssl.CERT_NONE) or a suitably-configured ssl.SSLContext to disable.

class tornado.iostream.SSLIOStream(*args, **kwargs)[源代码]¶

    A utility class to write to and read from a non-blocking SSL socket.

    If the socket passed to the constructor is already connected, it should be wrapped with:

    ssl.wrap_socket(sock, do_handshake_on_connect=False, **kwargs)

    before constructing the SSLIOStream. Unconnected sockets will be wrapped when
    IOStream.connect is finished.

    The ssl_options keyword argument may either be an ssl.SSLContext object or a dictionary of
    keywords arguments for ssl.wrap_socket

    wait_for_handshake(callback=None)[源代码]¶

        Wait for the initial SSL handshake to complete.

        If a callback is given, it will be called with no arguments once the handshake is
        complete; otherwise this method returns a Future which will resolve to the stream itself
        after the handshake is complete.

        Once the handshake is complete, information such as the peer’s certificate and NPN/ALPN
        selections may be accessed on self.socket.

        This method is intended for use on server-side streams or after using IOStream.start_tls
        ; it should not be used with IOStream.connect (which already waits for the handshake to
        complete). It may only be called once per stream.

        4.2 新版功能.

class tornado.iostream.PipeIOStream(fd, *args, **kwargs)[源代码]¶

    Pipe-based IOStream implementation.

    The constructor takes an integer file descriptor (such as one returned by os.pipe) rather
    than an open file object. Pipes are generally one-way, so a PipeIOStream can be used for
    reading or writing but not both.

Exceptions¶

exception tornado.iostream.StreamBufferFullError[源代码]¶

    Exception raised by IOStream methods when the buffer is full.

exception tornado.iostream.StreamClosedError(real_error=None)[源代码]¶

    Exception raised by IOStream methods when the stream is closed.

    Note that the close callback is scheduled to run after other callbacks on the stream (to
    allow for buffered data to be processed), so you may see this error before you see the close
    callback.

    The real_error attribute contains the underlying error that caused the stream to close (if
    any).

    在 4.3 版更改: Added the real_error attribute.

exception tornado.iostream.UnsatisfiableReadError[源代码]¶

    Exception raised when a read cannot be satisfied.

    Raised by read_until and read_until_regex with a max_bytes argument.

tornado.netutil — Miscellaneous network utilities¶

Miscellaneous network utility code.

tornado.netutil.bind_sockets(port, address=None, family=<AddressFamily.AF_UNSPEC: 0>, backlog=
    128, flags=None, reuse_port=False)[源代码]¶

    Creates listening sockets bound to the given port and address.

    Returns a list of socket objects (multiple sockets are returned if the given address maps to
    multiple IP addresses, which is most common for mixed IPv4 and IPv6 use).

    Address may be either an IP address or hostname. If it’s a hostname, the server will listen
    on all IP addresses associated with the name. Address may be an empty string or None to
    listen on all available interfaces. Family may be set to either socket.AF_INET or
    socket.AF_INET6 to restrict to IPv4 or IPv6 addresses, otherwise both will be used if
    available.

    The backlog argument has the same meaning as for socket.listen().

    flags is a bitmask of AI_* flags to getaddrinfo, like socket.AI_PASSIVE | 
    socket.AI_NUMERICHOST.

    resuse_port option sets SO_REUSEPORT option for every socket in the list. If your platform
    doesn’t support this option ValueError will be raised.

tornado.netutil.bind_unix_socket(file, mode=384, backlog=128)[源代码]¶

    Creates a listening unix socket.

    If a socket with the given name already exists, it will be deleted. If any other file with
    that name exists, an exception will be raised.

    Returns a socket object (not a list of socket objects like bind_sockets)

tornado.netutil.add_accept_handler(sock, callback, io_loop=None)[源代码]¶

    Adds an IOLoop event handler to accept new connections on sock.

    When a connection is accepted, callback(connection, address) will be run (connection is a
    socket object, and address is the address of the other end of the connection). Note that
    this signature is different from the callback(fd, events) signature used for IOLoop
    handlers.

    在 4.1 版更改: The io_loop argument is deprecated.

tornado.netutil.is_valid_ip(ip)[源代码]¶

    Returns true if the given string is a well-formed IP address.

    Supports IPv4 and IPv6.

class tornado.netutil.Resolver[源代码]¶

    Configurable asynchronous DNS resolver interface.

    By default, a blocking implementation is used (which simply calls socket.getaddrinfo). An
    alternative implementation can be chosen with the Resolver.configure class method:

    Resolver.configure('tornado.netutil.ThreadedResolver')

    The implementations of this interface included with Tornado are

      □ tornado.netutil.BlockingResolver
      □ tornado.netutil.ThreadedResolver
      □ tornado.netutil.OverrideResolver
      □ tornado.platform.twisted.TwistedResolver
      □ tornado.platform.caresresolver.CaresResolver

    resolve(host, port, family=<AddressFamily.AF_UNSPEC: 0>, callback=None)[源代码]¶

        Resolves an address.

        The host argument is a string which may be a hostname or a literal IP address.

        Returns a Future whose result is a list of (family, address) pairs, where address is a
        tuple suitable to pass to socket.connect (i.e. a (host, port) pair for IPv4; additional
        fields may be present for IPv6). If a callback is passed, it will be run with the result
        as an argument when it is complete.

    close()[源代码]¶

        Closes the Resolver, freeing any resources used.

        3.1 新版功能.

class tornado.netutil.ExecutorResolver[源代码]¶

    Resolver implementation using a concurrent.futures.Executor.

    Use this instead of ThreadedResolver when you require additional control over the executor
    being used.

    The executor will be shut down when the resolver is closed unless close_resolver=False; use
    this if you want to reuse the same executor elsewhere.

    在 4.1 版更改: The io_loop argument is deprecated.

class tornado.netutil.BlockingResolver[源代码]¶

    Default Resolver implementation, using socket.getaddrinfo.

    The IOLoop will be blocked during the resolution, although the callback will not be run
    until the next IOLoop iteration.

class tornado.netutil.ThreadedResolver[源代码]¶

    Multithreaded non-blocking Resolver implementation.

    Requires the concurrent.futures package to be installed (available in the standard library
    since Python 3.2, installable with pip install futures in older versions).

    The thread pool size can be configured with:

    Resolver.configure('tornado.netutil.ThreadedResolver',
                       num_threads=10)

    在 3.1 版更改: All ThreadedResolvers share a single thread pool, whose size is set by the
    first one to be created.

class tornado.netutil.OverrideResolver[源代码]¶

    Wraps a resolver with a mapping of overrides.

    This can be used to make local DNS changes (e.g. for testing) without modifying system-wide
    settings.

    The mapping can contain either host strings or host-port pairs.

tornado.netutil.ssl_options_to_context(ssl_options)[源代码]¶

    Try to convert an ssl_options dictionary to an SSLContext object.

    The ssl_options dictionary contains keywords to be passed to ssl.wrap_socket. In Python
    2.7.9+, ssl.SSLContext objects can be used instead. This function converts the dict form to
    its SSLContext equivalent, and may be used when a component which accepts both forms needs
    to upgrade to the SSLContext version to use features like SNI or NPN.

tornado.netutil.ssl_wrap_socket(socket, ssl_options, server_hostname=None, **kwargs)[源代码]¶

    Returns an ssl.SSLSocket wrapping the given socket.

    ssl_options may be either an ssl.SSLContext object or a dictionary (as accepted by
    ssl_options_to_context). Additional keyword arguments are passed to wrap_socket (either the
    SSLContext method or the ssl module function as appropriate).

tornado.tcpclient — IOStream connection factory¶

A non-blocking TCP connection factory.

class tornado.tcpclient.TCPClient(resolver=None, io_loop=None)[源代码]¶

    A non-blocking TCP connection factory.

    在 4.1 版更改: The io_loop argument is deprecated.

    connect(host, port, af=<AddressFamily.AF_UNSPEC: 0>, ssl_options=None, max_buffer_size=None)
        [源代码]¶

        Connect to the given host and port.

        Asynchronously returns an IOStream (or SSLIOStream if ssl_options is not None).

tornado.tcpserver — 基于 IOStream 的基础 TCP 服务¶

一个非阻塞, 单线程 TCP 服务.

class tornado.tcpserver.TCPServer(io_loop=None, ssl_options=None, max_buffer_size=None, 
    read_chunk_size=None)[源代码]¶

    一个非阻塞, 单线程的 TCP 服务.

    想要使用 TCPServer, 只需要定义一个子类, 复写 handle_stream 方法即可. 例如, 一个简单的 echo
    server 可以做如下定义:

    from tornado.tcpserver import TCPServer
    from tornado.iostream import StreamClosedError
    from tornado import gen

    class EchoServer(TCPServer):
        @gen.coroutine
        def handle_stream(self, stream, address):
            while True:
                try:
                    data = yield stream.read_until(b"\n")
                    yield stream.write(data)
                except StreamClosedError:
                    break

    为了使该服务提供 SSL 传输, 通过一个名为``ssl_options`` 的关键字参数传递进去 ssl.SSLContext
    对象即可. 为了兼容旧版本的 Python, ssl_options 也可以是一个字典, 作为`ssl.wrap_socket` 方法
    的关键字参数.:

    ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_ctx.load_cert_chain(os.path.join(data_dir, "mydomain.crt"),
                            os.path.join(data_dir, "mydomain.key"))
    TCPServer(ssl_options=ssl_ctx)

    TCPServer 初始化可以是以下三种模式之一:

     1. listen: 简单的单进程模式:

        server = TCPServer()
        server.listen(8888)
        IOLoop.current().start()

     2. bind/start: 简单的多进程模式:

        server = TCPServer()
        server.bind(8888)
        server.start(0)  # Forks multiple sub-processes
        IOLoop.current().start()

        当使用这个接口, IOLoop 一定不能被传递给 TCPServer 构造器. start 总是会在默认单一的
        IOLoop 上启动服务.

     3. add_sockets: 高级多进程模式:

        sockets = bind_sockets(8888)
        tornado.process.fork_processes(0)
        server = TCPServer()
        server.add_sockets(sockets)
        IOLoop.current().start()

        add_sockets 接口更加复杂, 但是它可以和 tornado.process.fork_processes 一起被使用, 当
        fork 发生的时候给你更多灵活性. add_sockets 也可以被用于单进程服务中, 如果你想要使用
        bind_sockets 以外的方式创建你监听的 socket.

    3.1 新版功能: max_buffer_size 参数.

    listen(port, address='')[源代码]¶

        开始在给定的端口接收连接.

        这个方法可能不只被调用一次, 可能会在多个端口上被调用多次. listen 方法将立即生效, 所以它
        没必要在 TCPServer.start 之后调用. 然而, 必须要启动 IOLoop 才可以.

    add_sockets(sockets)[源代码]¶

        使服务开始接收给定端口的连接.

        sockets 参数是一个 socket 对象的列表, 例如那些被 bind_sockets 所返回的对象. add_sockets
        通常和 tornado.process.fork_processes 相结合使用, 以便于在一个多进程服务初始化时提供更多
        控制.

    add_socket(socket)[源代码]¶

        单数版本的 add_sockets. 接受一个单一的 socket 对象.

    bind(port, address=None, family=<AddressFamily.AF_UNSPEC: 0>, backlog=128)[源代码]¶

        绑定该服务到指定的地址的指定端口上.

        要启动该服务, 调用 start. 如果你想要在一个单进程上运行该服务, 你可以调用 listen 作为顺序
        调用 bind 和 start 的一个快捷方式.

        address 参数可以是 IP 地址或者主机名. 如果它是主机名, 该服务将监听在和该名称有关的所有
        IP 地址上. 地址也可以是空字符串或者 None, 服务将监听所有可用的接口. family 可以被设置为
        socket.AF_INET 或 socket.AF_INET6 用来限定是 IPv4 或 IPv6 地址, 否则如果可用的话, 两者都
        将被使用.

        backlog 参数和 socket.listen 是相同含义.

        这个方法可能在 start 之前被调用多次来监听在多个端口或接口上.

    start(num_processes=1)[源代码]¶

        在 IOLoop 中启动该服务.

        默认情况下, 我们在该进程中运行服务, 并且不会 fork 出任何额外的子进程.

        如果 num_processes 为 None 或 <= 0, 我们检测这台机器上可用的核心数并 fork 相同数量的子进
        程. 如果给定了 num_processes 并且 > 1, 我们 fork 指定数量的子进程.

        因为我们使用进程而不是线程, 在任何服务代码之间没有共享内存.

        注意多进程模式和 autoreload 模块不兼容(或者是当 debug=True 时 tornado.web.Application 的
        autoreload=True 选项默认为 True). 当使用多进程模式时, 直到 TCPServer.start(n) 调用后, 才
        能创建或者引用 IOLoops .

    stop()[源代码]¶

        停止对新连接的监听.

        正在进行的请求可能仍然会继续在服务停止之后.

    handle_stream(stream, address)[源代码]¶

        通过复写这个方法以处理一个来自传入连接的新 IOStream .

        这个方法可能是一个协程; 如果是这样, 异步引发的任何异常都将被记录. 接受传入连接不会被该协
        程阻塞.

        如果这个 TCPServer 被配置为 SSL, handle_stream 将在 SSL 握手完成前被调用. 如果你需要验证
        客户端的证书或使用 NPN/ALPN 请使用 SSLIOStream.wait_for_handshake .

        在 4.2 版更改: 给这个方法添加了选项, 可以为协程.

协程和并发¶

tornado.gen — Simplify asynchronous code¶

tornado.gen is a generator-based interface to make it easier to work in an asynchronous
environment. Code using the gen module is technically asynchronous, but it is written as a
single generator instead of a collection of separate functions.

For example, the following asynchronous handler:

class AsyncHandler(RequestHandler):
    @asynchronous
    def get(self):
        http_client = AsyncHTTPClient()
        http_client.fetch("http://example.com",
                          callback=self.on_fetch)

    def on_fetch(self, response):
        do_something_with_response(response)
        self.render("template.html")

could be written with gen as:

class GenAsyncHandler(RequestHandler):
    @gen.coroutine
    def get(self):
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch("http://example.com")
        do_something_with_response(response)
        self.render("template.html")

Most asynchronous functions in Tornado return a Future; yielding this object returns its result.

You can also yield a list or dict of Futures, which will be started at the same time and run in
parallel; a list or dict of results will be returned when they are all finished:

@gen.coroutine
def get(self):
    http_client = AsyncHTTPClient()
    response1, response2 = yield [http_client.fetch(url1),
                                  http_client.fetch(url2)]
    response_dict = yield dict(response3=http_client.fetch(url3),
                               response4=http_client.fetch(url4))
    response3 = response_dict['response3']
    response4 = response_dict['response4']

If the singledispatch library is available (standard in Python 3.4, available via the
singledispatch package on older versions), additional types of objects may be yielded. Tornado
includes support for asyncio.Future and Twisted’s Deferred class when tornado.platform.asyncio
and tornado.platform.twisted are imported. See the convert_yielded function to extend this
mechanism.

在 3.2 版更改: Dict support added.

在 4.1 版更改: Support added for yielding asyncio Futures and Twisted Deferreds via 
singledispatch.

Decorators¶

tornado.gen.coroutine(func, replace_callback=True)[源代码]¶

    Decorator for asynchronous generators.

    Any generator that yields objects from this module must be wrapped in either this decorator
    or engine.

    Coroutines may “return” by raising the special exception Return(value). In Python 3.3+, it
    is also possible for the function to simply use the return value statement (prior to Python
    3.3 generators were not allowed to also return values). In all versions of Python a
    coroutine that simply wishes to exit early may use the return statement without a value.

    Functions with this decorator return a Future. Additionally, they may be called with a 
    callback keyword argument, which will be invoked with the future’s result when it resolves.
    If the coroutine fails, the callback will not be run and an exception will be raised into
    the surrounding StackContext. The callback argument is not visible inside the decorated
    function; it is handled by the decorator itself.

    From the caller’s perspective, @gen.coroutine is similar to the combination of 
    @return_future and @gen.engine.

    警告

    When exceptions occur inside a coroutine, the exception information will be stored in the
    Future object. You must examine the result of the Future object, or the exception may go
    unnoticed by your code. This means yielding the function if called from another coroutine,
    using something like IOLoop.run_sync for top-level calls, or passing the Future to
    IOLoop.add_future.

tornado.gen.engine(func)[源代码]¶

    Callback-oriented decorator for asynchronous generators.

    This is an older interface; for new code that does not need to be compatible with versions
    of Tornado older than 3.0 the coroutine decorator is recommended instead.

    This decorator is similar to coroutine, except it does not return a Future and the callback
    argument is not treated specially.

    In most cases, functions decorated with engine should take a callback argument and invoke it
    with their result when they are finished. One notable exception is the RequestHandler HTTP
    verb methods, which use self.finish() in place of a callback argument.

Utility functions¶

exception tornado.gen.Return(value=None)[源代码]¶

    Special exception to return a value from a coroutine.

    If this exception is raised, its value argument is used as the result of the coroutine:

    @gen.coroutine
    def fetch_json(url):
        response = yield AsyncHTTPClient().fetch(url)
        raise gen.Return(json_decode(response.body))

    In Python 3.3, this exception is no longer necessary: the return statement can be used
    directly to return a value (previously yield and return with a value could not be combined
    in the same function).

    By analogy with the return statement, the value argument is optional, but it is never
    necessary to raise gen.Return(). The return statement can be used with no arguments instead.

tornado.gen.with_timeout(timeout, future, io_loop=None, quiet_exceptions=())[源代码]¶

    Wraps a Future in a timeout.

    Raises TimeoutError if the input future does not complete before timeout, which may be
    specified in any form allowed by IOLoop.add_timeout (i.e. a datetime.timedelta or an
    absolute time relative to IOLoop.time)

    If the wrapped Future fails after it has timed out, the exception will be logged unless it
    is of a type contained in quiet_exceptions (which may be an exception type or a sequence of
    types).

    Currently only supports Futures, not other YieldPoint classes.

    4.0 新版功能.

    在 4.1 版更改: Added the quiet_exceptions argument and the logging of unhandled exceptions.

exception tornado.gen.TimeoutError[源代码]¶

    Exception raised by with_timeout.

tornado.gen.sleep(duration)[源代码]¶

    Return a Future that resolves after the given number of seconds.

    When used with yield in a coroutine, this is a non-blocking analogue to time.sleep (which
    should not be used in coroutines because it is blocking):

    yield gen.sleep(0.5)

    Note that calling this function on its own does nothing; you must wait on the Future it
    returns (usually by yielding it).

    4.1 新版功能.

tornado.gen.moment¶

    A special object which may be yielded to allow the IOLoop to run for one iteration.

    This is not needed in normal use but it can be helpful in long-running coroutines that are
    likely to yield Futures that are ready instantly.

    Usage: yield gen.moment

    4.0 新版功能.

class tornado.gen.WaitIterator(*args, **kwargs)[源代码]¶

    Provides an iterator to yield the results of futures as they finish.

    Yielding a set of futures like this:

    results = yield [future1, future2]

    pauses the coroutine until both future1 and future2 return, and then restarts the coroutine
    with the results of both futures. If either future is an exception, the expression will
    raise that exception and all the results will be lost.

    If you need to get the result of each future as soon as possible, or if you need the result
    of some futures even if others produce errors, you can use WaitIterator:

    wait_iterator = gen.WaitIterator(future1, future2)
    while not wait_iterator.done():
        try:
            result = yield wait_iterator.next()
        except Exception as e:
            print("Error {} from {}".format(e, wait_iterator.current_future))
        else:
            print("Result {} received from {} at {}".format(
                result, wait_iterator.current_future,
                wait_iterator.current_index))

    Because results are returned as soon as they are available the output from the iterator will
    not be in the same order as the input arguments. If you need to know which future produced
    the current result, you can use the attributes WaitIterator.current_future, or 
    WaitIterator.current_index to get the index of the future from the input list. (if keyword
    arguments were used in the construction of the WaitIterator, current_index will use the
    corresponding keyword).

    On Python 3.5, WaitIterator implements the async iterator protocol, so it can be used with
    the async for statement (note that in this version the entire iteration is aborted if any
    value raises an exception, while the previous example can continue past individual errors):

    async for result in gen.WaitIterator(future1, future2):
        print("Result {} received from {} at {}".format(
            result, wait_iterator.current_future,
            wait_iterator.current_index))

    4.1 新版功能.

    在 4.3 版更改: Added async for support in Python 3.5.

    done()[源代码]¶

        Returns True if this iterator has no more results.

    next()[源代码]¶

        Returns a Future that will yield the next available result.

        Note that this Future will not be the same object as any of the inputs.

tornado.gen.multi(children, quiet_exceptions=())[源代码]¶

    Runs multiple asynchronous operations in parallel.

    children may either be a list or a dict whose values are yieldable objects. multi() returns
    a new yieldable object that resolves to a parallel structure containing their results. If 
    children is a list, the result is a list of results in the same order; if it is a dict, the
    result is a dict with the same keys.

    That is, results = yield multi(list_of_futures) is equivalent to:

    results = []
    for future in list_of_futures:
        results.append(yield future)

    If any children raise exceptions, multi() will raise the first one. All others will be
    logged, unless they are of types contained in the quiet_exceptions argument.

    If any of the inputs are YieldPoints, the returned yieldable object is a YieldPoint.
    Otherwise, returns a Future. This means that the result of multi can be used in a native
    coroutine if and only if all of its children can be.

    In a yield-based coroutine, it is not normally necessary to call this function directly,
    since the coroutine runner will do it automatically when a list or dict is yielded. However,
    it is necessary in await-based coroutines, or to pass the quiet_exceptions argument.

    This function is available under the names multi() and Multi() for historical reasons.

    在 4.2 版更改: If multiple yieldables fail, any exceptions after the first (which is raised)
    will be logged. Added the quiet_exceptions argument to suppress this logging for selected
    exception types.

    在 4.3 版更改: Replaced the class Multi and the function multi_future with a unified
    function multi. Added support for yieldables other than YieldPoint and Future.

tornado.gen.multi_future(children, quiet_exceptions=())[源代码]¶

    Wait for multiple asynchronous futures in parallel.

    This function is similar to multi, but does not support YieldPoints.

    4.0 新版功能.

    在 4.2 版更改: If multiple Futures fail, any exceptions after the first (which is raised)
    will be logged. Added the quiet_exceptions argument to suppress this logging for selected
    exception types.

    4.3 版后已移除: Use multi instead.

tornado.gen.Task(func, *args, **kwargs)[源代码]¶

    Adapts a callback-based asynchronous function for use in coroutines.

    Takes a function (and optional additional arguments) and runs it with those arguments plus a
    callback keyword argument. The argument passed to the callback is returned as the result of
    the yield expression.

    在 4.0 版更改: gen.Task is now a function that returns a Future, instead of a subclass of
    YieldPoint. It still behaves the same way when yielded.

class tornado.gen.Arguments¶

    The result of a Task or Wait whose callback had more than one argument (or keyword
    arguments).

    The Arguments object is a collections.namedtuple and can be used either as a tuple (args, 
    kwargs) or an object with attributes args and kwargs.

tornado.gen.convert_yielded(yielded)[源代码]¶

    Convert a yielded object into a Future.

    The default implementation accepts lists, dictionaries, and Futures.

    If the singledispatch library is available, this function may be extended to support
    additional types. For example:

    @convert_yielded.register(asyncio.Future)
    def _(asyncio_future):
        return tornado.platform.asyncio.to_tornado_future(asyncio_future)

    4.1 新版功能.

tornado.gen.maybe_future(x)[源代码]¶

    Converts x into a Future.

    If x is already a Future, it is simply returned; otherwise it is wrapped in a new Future.
    This is suitable for use as result = yield gen.maybe_future(f()) when you don’t know whether
    f() returns a Future or not.

    4.3 版后已移除: This function only handles Futures, not other yieldable objects. Instead of
    maybe_future, check for the non-future result types you expect (often just None), and yield
    anything unknown.

Legacy interface¶

Before support for Futures was introduced in Tornado 3.0, coroutines used subclasses of
YieldPoint in their yield expressions. These classes are still supported but should generally
not be used except for compatibility with older interfaces. None of these classes are compatible
with native (await-based) coroutines.

class tornado.gen.YieldPoint[源代码]¶

    Base class for objects that may be yielded from the generator.

    4.0 版后已移除: Use Futures instead.

    start(runner)[源代码]¶

        Called by the runner after the generator has yielded.

        No other methods will be called on this object before start.

    is_ready()[源代码]¶

        Called by the runner to determine whether to resume the generator.

        Returns a boolean; may be called more than once.

    get_result()[源代码]¶

        Returns the value to use as the result of the yield expression.

        This method will only be called once, and only after is_ready has returned true.

class tornado.gen.Callback(key)[源代码]¶

    Returns a callable object that will allow a matching Wait to proceed.

    The key may be any value suitable for use as a dictionary key, and is used to match 
    Callbacks to their corresponding Waits. The key must be unique among outstanding callbacks
    within a single run of the generator function, but may be reused across different runs of
    the same function (so constants generally work fine).

    The callback may be called with zero or one arguments; if an argument is given it will be
    returned by Wait.

    4.0 版后已移除: Use Futures instead.

class tornado.gen.Wait(key)[源代码]¶

    Returns the argument passed to the result of a previous Callback.

    4.0 版后已移除: Use Futures instead.

class tornado.gen.WaitAll(keys)[源代码]¶

    Returns the results of multiple previous Callbacks.

    The argument is a sequence of Callback keys, and the result is a list of results in the same
    order.

    WaitAll is equivalent to yielding a list of Wait objects.

    4.0 版后已移除: Use Futures instead.

class tornado.gen.MultiYieldPoint(children, quiet_exceptions=())[源代码]¶

    Runs multiple asynchronous operations in parallel.

    This class is similar to multi, but it always creates a stack context even when no children
    require it. It is not compatible with native coroutines.

    在 4.2 版更改: If multiple YieldPoints fail, any exceptions after the first (which is
    raised) will be logged. Added the quiet_exceptions argument to suppress this logging for
    selected exception types.

    在 4.3 版更改: Renamed from Multi to MultiYieldPoint. The name Multi remains as an alias for
    the equivalent multi function.

    4.3 版后已移除: Use multi instead.

tornado.concurrent — Work with threads and futures¶

Utilities for working with threads and Futures.

Futures are a pattern for concurrent programming introduced in Python 3.2 in the
concurrent.futures package. This package defines a mostly-compatible Future class designed for
use from coroutines, as well as some utility functions for interacting with the
concurrent.futures package.

class tornado.concurrent.Future[源代码]¶

    Placeholder for an asynchronous result.

    A Future encapsulates the result of an asynchronous operation. In synchronous applications 
    Futures are used to wait for the result from a thread or process pool; in Tornado they are
    normally used with IOLoop.add_future or by yielding them in a gen.coroutine.

    tornado.concurrent.Future is similar to concurrent.futures.Future, but not thread-safe (and
    therefore faster for use with single-threaded event loops).

    In addition to exception and set_exception, methods exc_info and set_exc_info are supported
    to capture tracebacks in Python 2. The traceback is automatically available in Python 3, but
    in the Python 2 futures backport this information is discarded. This functionality was
    previously available in a separate class TracebackFuture, which is now a deprecated alias
    for this class.

    在 4.0 版更改: tornado.concurrent.Future is always a thread-unsafe Future with support for
    the exc_info methods. Previously it would be an alias for the thread-safe
    concurrent.futures.Future if that package was available and fall back to the thread-unsafe
    implementation if it was not.

    在 4.1 版更改: If a Future contains an error but that error is never observed (by calling 
    result(), exception(), or exc_info()), a stack trace will be logged when the Future is
    garbage collected. This normally indicates an error in the application, but in cases where
    it results in undesired logging it may be necessary to suppress the logging by ensuring that
    the exception is observed: f.add_done_callback(lambda f: f.exception()).

Consumer methods¶

Future.result(timeout=None)[源代码]¶

    If the operation succeeded, return its result. If it failed, re-raise its exception.

    This method takes a timeout argument for compatibility with concurrent.futures.Future but it
    is an error to call it before the Future is done, so the timeout is never used.

Future.exception(timeout=None)[源代码]¶

    If the operation raised an exception, return the Exception object. Otherwise returns None.

    This method takes a timeout argument for compatibility with concurrent.futures.Future but it
    is an error to call it before the Future is done, so the timeout is never used.

Future.exc_info()[源代码]¶

    Returns a tuple in the same format as sys.exc_info or None.

    4.0 新版功能.

Future.add_done_callback(fn)[源代码]¶

    Attaches the given callback to the Future.

    It will be invoked with the Future as its argument when the Future has finished running and
    its result is available. In Tornado consider using IOLoop.add_future instead of calling
    add_done_callback directly.

Future.done()[源代码]¶

    Returns True if the future has finished running.

Future.running()[源代码]¶

    Returns True if this operation is currently running.

Future.cancel()[源代码]¶

    Cancel the operation, if possible.

    Tornado Futures do not support cancellation, so this method always returns False.

Future.cancelled()[源代码]¶

    Returns True if the operation has been cancelled.

    Tornado Futures do not support cancellation, so this method always returns False.

Producer methods¶

Future.set_result(result)[源代码]¶

    Sets the result of a Future.

    It is undefined to call any of the set methods more than once on the same object.

Future.set_exception(exception)[源代码]¶

    Sets the exception of a Future.

Future.set_exc_info(exc_info)[源代码]¶

    Sets the exception information of a Future.

    Preserves tracebacks on Python 2.

    4.0 新版功能.

tornado.concurrent.run_on_executor(*args, **kwargs)[源代码]¶

    Decorator to run a synchronous method asynchronously on an executor.

    The decorated method may be called with a callback keyword argument and returns a future.

    The IOLoop and executor to be used are determined by the io_loop and executor attributes of 
    self. To use different attributes, pass keyword arguments to the decorator:

    @run_on_executor(executor='_thread_pool')
    def foo(self):
        pass

    在 4.2 版更改: Added keyword arguments to use alternative attributes.

tornado.concurrent.return_future(f)[源代码]¶

    Decorator to make a function that returns via callback return a Future.

    The wrapped function should take a callback keyword argument and invoke it with one argument
    when it has finished. To signal failure, the function can simply raise an exception (which
    will be captured by the StackContext and passed along to the Future).

    From the caller’s perspective, the callback argument is optional. If one is given, it will
    be invoked when the function is complete with Future.result() as an argument. If the
    function fails, the callback will not be run and an exception will be raised into the
    surrounding StackContext.

    If no callback is given, the caller should use the Future to wait for the function to
    complete (perhaps by yielding it in a gen.engine function, or passing it to
    IOLoop.add_future).

    Usage:

    @return_future
    def future_func(arg1, arg2, callback):
        # Do stuff (possibly asynchronous)
        callback(result)

    @gen.engine
    def caller(callback):
        yield future_func(arg1, arg2)
        callback()

    Note that @return_future and @gen.engine can be applied to the same function, provided 
    @return_future appears first. However, consider using @gen.coroutine instead of this
    combination.

tornado.concurrent.chain_future(a, b)[源代码]¶

    Chain two futures together so that when one completes, so does the other.

    The result (success or failure) of a will be copied to b, unless b has already been
    completed or cancelled by the time a finishes.

tornado.locks – 同步原语¶

4.2 新版功能.

使用和标准库提供给线程相似的同步原语协调协程.

(请注意, 这些原语不是线程安全的, 不能被用来代替标准库中的–它们是为了协调在单线程app中的Tornado协
程, 而不是为了在一个多线程 app中保护共享对象.)

Condition¶

class tornado.locks.Condition[源代码]¶

    允许一个或多个协程等待直到被通知的条件.

    就像标准的 threading.Condition, 但是不需要一个被获取和释放的底层锁.

    通过 Condition, 协程可以等待着被其他协程通知:

    from tornado import gen
    from tornado.ioloop import IOLoop
    from tornado.locks import Condition

    condition = Condition()

    @gen.coroutine
    def waiter():
        print("I'll wait right here")
        yield condition.wait()  # Yield a Future.
        print("I'm done waiting")

    @gen.coroutine
    def notifier():
        print("About to notify")
        condition.notify()
        print("Done notifying")

    @gen.coroutine
    def runner():
        # Yield two Futures; wait for waiter() and notifier() to finish.
        yield [waiter(), notifier()]

    IOLoop.current().run_sync(runner)

    I'll wait right here
    About to notify
    Done notifying
    I'm done waiting

    wait 有一个可选参数 timeout , 要不然是一个绝对的时间戳:

    io_loop = IOLoop.current()

    # Wait up to 1 second for a notification.
    yield condition.wait(timeout=io_loop.time() + 1)

    ...或一个 datetime.timedelta 相对于当前时间的一个延时:

    # Wait up to 1 second.
    yield condition.wait(timeout=datetime.timedelta(seconds=1))

    这个方法将抛出一个 tornado.gen.TimeoutError 如果在最后时间之前都没有通知.

    wait(timeout=None)[源代码]¶

        等待 notify.

        返回一个 Future 对象, 如果条件被通知则为 True , 或者在超时之后为 False .

    notify(n=1)[源代码]¶

        唤醒 n 个等待者(waiters) .

    notify_all()[源代码]¶

        唤醒全部的等待者(waiters) .

Event¶

class tornado.locks.Event[源代码]¶

    一个阻塞协程的事件直到它的内部标识设置为True.

    类似于 threading.Event.

    协程可以等待一个事件被设置. 一旦它被设置, 调用 yield event.wait() 将不会被阻塞除非该事件已经
    被清除:

    from tornado import gen
    from tornado.ioloop import IOLoop
    from tornado.locks import Event

    event = Event()

    @gen.coroutine
    def waiter():
        print("Waiting for event")
        yield event.wait()
        print("Not waiting this time")
        yield event.wait()
        print("Done")

    @gen.coroutine
    def setter():
        print("About to set the event")
        event.set()

    @gen.coroutine
    def runner():
        yield [waiter(), setter()]

    IOLoop.current().run_sync(runner)

    Waiting for event
    About to set the event
    Not waiting this time
    Done

    is_set()[源代码]¶

        如果内部标识是true将返回 True .

    set()[源代码]¶

        设置内部标识为 True. 所有的等待者(waiters)都被唤醒.

        一旦该标识被设置调用 wait 将不会阻塞.

    clear()[源代码]¶

        重置内部标识为 False.

        调用 wait 将阻塞直到 set 被调用.

    wait(timeout=None)[源代码]¶

        阻塞直到内部标识为true.

        返回一个Future对象, 在超时之后会抛出一个 tornado.gen.TimeoutError 异常.

Semaphore¶

class tornado.locks.Semaphore(value=1)[源代码]¶

    可以在阻塞之前获得固定次数的锁.

    一个信号量管理着代表 release 调用次数减去 acquire 的调用次数的计数器, 加一个初始值. 如果必要
    的话,`.acquire` 方法将会阻塞, 直到它可以返回, 而不使该计数器成为负值.

    信号量限制访问共享资源. 为了允许两个worker同时获得权限:

    from tornado import gen
    from tornado.ioloop import IOLoop
    from tornado.locks import Semaphore

    sem = Semaphore(2)

    @gen.coroutine
    def worker(worker_id):
        yield sem.acquire()
        try:
            print("Worker %d is working" % worker_id)
            yield use_some_resource()
        finally:
            print("Worker %d is done" % worker_id)
            sem.release()

    @gen.coroutine
    def runner():
        # Join all workers.
        yield [worker(i) for i in range(3)]

    IOLoop.current().run_sync(runner)

    Worker 0 is working
    Worker 1 is working
    Worker 0 is done
    Worker 2 is working
    Worker 1 is done
    Worker 2 is done

    Workers 0 和 1 允许并行运行, 但是worker 2将等待直到信号量被worker 0释放.

    acquire 是一个上下文管理器, 所以 worker 可以被写为:

    @gen.coroutine
    def worker(worker_id):
        with (yield sem.acquire()):
            print("Worker %d is working" % worker_id)
            yield use_some_resource()

        # Now the semaphore has been released.
        print("Worker %d is done" % worker_id)

    在 Python 3.5 中, 信号量自身可以作为一个异步上下文管理器:

    async def worker(worker_id):
        async with sem:
            print("Worker %d is working" % worker_id)
            await use_some_resource()

        # Now the semaphore has been released.
        print("Worker %d is done" % worker_id)

    在 4.3 版更改: 添加对 Python 3.5 async with 的支持.

    release()[源代码]¶

        增加counter 并且唤醒一个waiter.

    acquire(timeout=None)[源代码]¶

        递减计数器. 返回一个 Future 对象.

        如果计数器(counter)为0将会阻塞, 等待 release. 在超时之后 Future 对象将会抛出
        TimeoutError .

BoundedSemaphore¶

class tornado.locks.BoundedSemaphore(value=1)[源代码]¶

    一个防止release() 被调用太多次的信号量.

    如果 release 增加信号量的值超过初始值, 它将抛出 ValueError. 信号量通常是通过限制容量来保护资
    源, 所以一个信号量释放太多次是一个错误的标志.

    release()[源代码]¶

        增加counter 并且唤醒一个waiter.

    acquire(timeout=None)¶

        递减计数器. 返回一个 Future 对象.

        如果计数器(counter)为0将会阻塞, 等待 release. 在超时之后 Future 对象将会抛出
        TimeoutError .

Lock¶

class tornado.locks.Lock[源代码]¶

    协程的锁.

    一个Lock开始解锁, 然后它立即 acquire 锁. 虽然它是锁着的, 一个协程yield acquire 并等待, 直到
    另一个协程调用 release.

    释放一个没锁住的锁将抛出 RuntimeError.

    在所有Python 版本中 acquire 支持上下文管理协议:

    >>> from tornado import gen, locks
    >>> lock = locks.Lock()
    >>>
    >>> @gen.coroutine
    ... def f():
    ...    with (yield lock.acquire()):
    ...        # Do something holding the lock.
    ...        pass
    ...
    ...    # Now the lock is released.

    在Python 3.5, Lock 也支持异步上下文管理协议(async context manager protocol). 注意在这种情况
    下没有 acquire, 因为 async with 同时包含 yield 和 acquire (就像 threading.Lock):

    >>> async def f():
    ...    async with lock:
    ...        # Do something holding the lock.
    ...        pass
    ...
    ...    # Now the lock is released.

    在 3.5 版更改: 添加Python 3.5 的 async with 支持.

    acquire(timeout=None)[源代码]¶

        尝试锁. 返回一个Future 对象.

        返回一个Future 对象, 在超时之后将抛出 tornado.gen.TimeoutError .

    release()[源代码]¶

        Unlock.

        在队列中等待 acquire 的第一个 coroutine 获得锁.

        如果没有锁, 将抛出 RuntimeError.

tornado.queues – 协程的队列¶

4.2 新版功能.

Classes¶

Queue¶

class tornado.queues.Queue(maxsize=0)[源代码]¶

    协调生产者消费者协程.

    如果maxsize 是0(默认配置)意味着队列的大小是无限的.

    from tornado import gen
    from tornado.ioloop import IOLoop
    from tornado.queues import Queue

    q = Queue(maxsize=2)

    @gen.coroutine
    def consumer():
        while True:
            item = yield q.get()
            try:
                print('Doing work on %s' % item)
                yield gen.sleep(0.01)
            finally:
                q.task_done()

    @gen.coroutine
    def producer():
        for item in range(5):
            yield q.put(item)
            print('Put %s' % item)

    @gen.coroutine
    def main():
        # Start consumer without waiting (since it never finishes).
        IOLoop.current().spawn_callback(consumer)
        yield producer()     # Wait for producer to put all tasks.
        yield q.join()       # Wait for consumer to finish all tasks.
        print('Done')

    IOLoop.current().run_sync(main)

    Put 0
    Put 1
    Doing work on 0
    Put 2
    Doing work on 1
    Put 3
    Doing work on 2
    Put 4
    Doing work on 3
    Doing work on 4
    Done

    在Python 3.5, Queue 实现了异步迭代器协议, 所以 consumer() 可以被重写为:

    async def consumer():
        async for item in q:
            try:
                print('Doing work on %s' % item)
                yield gen.sleep(0.01)
            finally:
                q.task_done()

    在 4.3 版更改: 为Python 3.5添加 async for 支持 in Python 3.5.

    maxsize¶

        队列中允许的最大项目数.

    qsize()[源代码]¶

        当前队列中的项目数.

    put(item, timeout=None)[源代码]¶

        将一个项目放入队列中, 可能需要等待直到队列中有空间.

        返回一个Future对象, 如果超时会抛出 tornado.gen.TimeoutError .

    put_nowait(item)[源代码]¶

        非阻塞的将一个项目放入队列中.

        如果没有立即可用的空闲插槽, 则抛出 QueueFull.

    get(timeout=None)[源代码]¶

        从队列中删除并返回一个项目.

        返回一个Future对象, 当项目可用时resolve, 或者在超时后抛出 tornado.gen.TimeoutError .

    get_nowait()[源代码]¶

        非阻塞的从队列中删除并返回一个项目.

        如果有项目是立即可用的则返回该项目, 否则抛出 QueueEmpty.

    task_done()[源代码]¶

        表明前面排队的任务已经完成.

        被消费者队列使用. 每个 get 用来获取一个任务, 随后(subsequent) 调用 task_done 告诉队列正
        在处理的任务已经完成.

        如果 join 正在阻塞, 它会在所有项目都被处理完后调起; 即当每个 put 都被一个 task_done 匹
        配.

        如果调用次数超过 put 将会抛出 ValueError .

    join(timeout=None)[源代码]¶

        阻塞(block)直到队列中的所有项目都处理完.

        返回一个Future对象, 超时后会抛出 tornado.gen.TimeoutError 异常.

PriorityQueue¶

class tornado.queues.PriorityQueue(maxsize=0)[源代码]¶

    一个有优先级的 Queue 最小的最优先.

    写入的条目通常是元组, 类似 (priority number, data).

    from tornado.queues import PriorityQueue

    q = PriorityQueue()
    q.put((1, 'medium-priority item'))
    q.put((0, 'high-priority item'))
    q.put((10, 'low-priority item'))

    print(q.get_nowait())
    print(q.get_nowait())
    print(q.get_nowait())

    (0, 'high-priority item')
    (1, 'medium-priority item')
    (10, 'low-priority item')

LifoQueue¶

class tornado.queues.LifoQueue(maxsize=0)[源代码]¶

    一个后进先出(Lifo)的 Queue.

    from tornado.queues import LifoQueue

    q = LifoQueue()
    q.put(3)
    q.put(2)
    q.put(1)

    print(q.get_nowait())
    print(q.get_nowait())
    print(q.get_nowait())

    1
    2
    3

Exceptions¶

QueueEmpty¶

exception tornado.queues.QueueEmpty[源代码]¶

    当队列中没有项目时, 由 Queue.get_nowait 抛出.

QueueFull¶

exception tornado.queues.QueueFull[源代码]¶

    当队列为最大size时, 由 Queue.put_nowait 抛出.

tornado.process — Utilities for multiple processes¶

Utilities for working with multiple processes, including both forking the server into multiple
processes and managing subprocesses.

exception tornado.process.CalledProcessError[源代码]¶

    An alias for subprocess.CalledProcessError.

tornado.process.cpu_count()[源代码]¶

    Returns the number of processors on this machine.

tornado.process.fork_processes(num_processes, max_restarts=100)[源代码]¶

    Starts multiple worker processes.

    If num_processes is None or <= 0, we detect the number of cores available on this machine
    and fork that number of child processes. If num_processes is given and > 0, we fork that
    specific number of sub-processes.

    Since we use processes and not threads, there is no shared memory between any server code.

    Note that multiple processes are not compatible with the autoreload module (or the 
    autoreload=True option to tornado.web.Application which defaults to True when debug=True).
    When using multiple processes, no IOLoops can be created or referenced until after the call
    to fork_processes.

    In each child process, fork_processes returns its task id, a number between 0 and 
    num_processes. Processes that exit abnormally (due to a signal or non-zero exit status) are
    restarted with the same id (up to max_restarts times). In the parent process, fork_processes
    returns None if all child processes have exited normally, but will otherwise only exit by
    throwing an exception.

tornado.process.task_id()[源代码]¶

    Returns the current task id, if any.

    Returns None if this process was not created by fork_processes.

class tornado.process.Subprocess(*args, **kwargs)[源代码]¶

    Wraps subprocess.Popen with IOStream support.

    The constructor is the same as subprocess.Popen with the following additions:

      □ stdin, stdout, and stderr may have the value tornado.process.Subprocess.STREAM, which
        will make the corresponding attribute of the resulting Subprocess a PipeIOStream.
      □ A new keyword argument io_loop may be used to pass in an IOLoop.

    在 4.1 版更改: The io_loop argument is deprecated.

    set_exit_callback(callback)[源代码]¶

        Runs callback when this process exits.

        The callback takes one argument, the return code of the process.

        This method uses a SIGCHLD handler, which is a global setting and may conflict if you
        have other libraries trying to handle the same signal. If you are using more than one 
        IOLoop it may be necessary to call Subprocess.initialize first to designate one IOLoop
        to run the signal handlers.

        In many cases a close callback on the stdout or stderr streams can be used as an
        alternative to an exit callback if the signal handler is causing a problem.

    wait_for_exit(raise_error=True)[源代码]¶

        Returns a Future which resolves when the process exits.

        Usage:

        ret = yield proc.wait_for_exit()

        This is a coroutine-friendly alternative to set_exit_callback (and a replacement for the
        blocking subprocess.Popen.wait).

        By default, raises subprocess.CalledProcessError if the process has a non-zero exit
        status. Use wait_for_exit(raise_error=False) to suppress this behavior and return the
        exit status without raising.

        4.2 新版功能.

    classmethod initialize(io_loop=None)[源代码]¶

        Initializes the SIGCHLD handler.

        The signal handler is run on an IOLoop to avoid locking issues. Note that the IOLoop
        used for signal handling need not be the same one used by individual Subprocess objects
        (as long as the IOLoops are each running in separate threads).

        在 4.1 版更改: The io_loop argument is deprecated.

    classmethod uninitialize()[源代码]¶

        Removes the SIGCHLD handler.

与其他服务集成¶

tornado.auth — Third-party login with OpenID and OAuth¶

This module contains implementations of various third-party authentication schemes.

All the classes in this file are class mixins designed to be used with the
tornado.web.RequestHandler class. They are used in two ways:

  • On a login handler, use methods such as authenticate_redirect(), authorize_redirect(), and 
    get_authenticated_user() to establish the user’s identity and store authentication tokens to
    your database and/or cookies.
  • In non-login handlers, use methods such as facebook_request() or twitter_request() to use
    the authentication tokens to make requests to the respective services.

They all take slightly different arguments due to the fact all these services implement
authentication and authorization slightly differently. See the individual service classes below
for complete documentation.

Example usage for Google OAuth:

class GoogleOAuth2LoginHandler(tornado.web.RequestHandler,
                               tornado.auth.GoogleOAuth2Mixin):
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument('code', False):
            user = yield self.get_authenticated_user(
                redirect_uri='http://your.site.com/auth/google',
                code=self.get_argument('code'))
            # Save the user with e.g. set_secure_cookie
        else:
            yield self.authorize_redirect(
                redirect_uri='http://your.site.com/auth/google',
                client_id=self.settings['google_oauth']['key'],
                scope=['profile', 'email'],
                response_type='code',
                extra_params={'approval_prompt': 'auto'})

在 4.0 版更改: All of the callback interfaces in this module are now guaranteed to run their
callback with an argument of None on error. Previously some functions would do this while others
would simply terminate the request on their own. This change also ensures that errors are more
consistently reported through the Future interfaces.

Common protocols¶

These classes implement the OpenID and OAuth standards. They will generally need to be
subclassed to use them with any particular site. The degree of customization required will vary,
but in most cases overridding the class attributes (which are named beginning with underscores
for historical reasons) should be sufficient.

class tornado.auth.OpenIdMixin[源代码]¶

    Abstract implementation of OpenID and Attribute Exchange.

    Class attributes:

      □ _OPENID_ENDPOINT: the identity provider’s URI.

    authenticate_redirect(callback_uri=None, ax_attrs=['name', 'email', 'language', 'username'],
        callback=None)[源代码]¶

        Redirects to the authentication URL for this service.

        After authentication, the service will redirect back to the given callback URI with
        additional parameters including openid.mode.

        We request the given attributes for the authenticated user by default (name, email,
        language, and username). If you don’t need all those attributes for your app, you can
        request fewer with the ax_attrs keyword argument.

        在 3.1 版更改: Returns a Future and takes an optional callback. These are not strictly
        necessary as this method is synchronous, but they are supplied for consistency with
        OAuthMixin.authorize_redirect.

    get_authenticated_user(callback, http_client=None)[源代码]¶

        Fetches the authenticated user data upon redirect.

        This method should be called by the handler that receives the redirect from the
        authenticate_redirect() method (which is often the same as the one that calls it; in
        that case you would call get_authenticated_user if the openid.mode parameter is present
        and authenticate_redirect if it is not).

        The result of this method will generally be used to set a cookie.

    get_auth_http_client()[源代码]¶

        Returns the AsyncHTTPClient instance to be used for auth requests.

        May be overridden by subclasses to use an HTTP client other than the default.

class tornado.auth.OAuthMixin[源代码]¶

    Abstract implementation of OAuth 1.0 and 1.0a.

    See TwitterMixin below for an example implementation.

    Class attributes:

      □ _OAUTH_AUTHORIZE_URL: The service’s OAuth authorization url.
      □ _OAUTH_ACCESS_TOKEN_URL: The service’s OAuth access token url.
      □ _OAUTH_VERSION: May be either “1.0” or “1.0a”.
      □ _OAUTH_NO_CALLBACKS: Set this to True if the service requires advance registration of
        callbacks.

    Subclasses must also override the _oauth_get_user_future and _oauth_consumer_token methods.

    authorize_redirect(callback_uri=None, extra_params=None, http_client=None, callback=None)[源
        代码]¶

        Redirects the user to obtain OAuth authorization for this service.

        The callback_uri may be omitted if you have previously registered a callback URI with
        the third-party service. For some services (including Friendfeed), you must use a
        previously-registered callback URI and cannot specify a callback via this method.

        This method sets a cookie called _oauth_request_token which is subsequently used (and
        cleared) in get_authenticated_user for security purposes.

        Note that this method is asynchronous, although it calls RequestHandler.finish for you
        so it may not be necessary to pass a callback or use the Future it returns. However, if
        this method is called from a function decorated with gen.coroutine, you must call it
        with yield to keep the response from being closed prematurely.

        在 3.1 版更改: Now returns a Future and takes an optional callback, for compatibility
        with gen.coroutine.

    get_authenticated_user(callback, http_client=None)[源代码]¶

        Gets the OAuth authorized user and access token.

        This method should be called from the handler for your OAuth callback URL to complete
        the registration process. We run the callback with the authenticated user dictionary.
        This dictionary will contain an access_key which can be used to make authorized requests
        to this service on behalf of the user. The dictionary will also contain other fields
        such as name, depending on the service used.

    _oauth_consumer_token()[源代码]¶

        Subclasses must override this to return their OAuth consumer keys.

        The return value should be a dict with keys key and secret.

    _oauth_get_user_future(access_token, callback)[源代码]¶

        Subclasses must override this to get basic information about the user.

        Should return a Future whose result is a dictionary containing information about the
        user, which may have been retrieved by using access_token to make a request to the
        service.

        The access token will be added to the returned dictionary to make the result of
        get_authenticated_user.

        For backwards compatibility, the callback-based _oauth_get_user method is also
        supported.

    get_auth_http_client()[源代码]¶

        Returns the AsyncHTTPClient instance to be used for auth requests.

        May be overridden by subclasses to use an HTTP client other than the default.

class tornado.auth.OAuth2Mixin[源代码]¶

    Abstract implementation of OAuth 2.0.

    See FacebookGraphMixin or GoogleOAuth2Mixin below for example implementations.

    Class attributes:

      □ _OAUTH_AUTHORIZE_URL: The service’s authorization url.
      □ _OAUTH_ACCESS_TOKEN_URL: The service’s access token url.

    authorize_redirect(redirect_uri=None, client_id=None, client_secret=None, extra_params=None,
        callback=None, scope=None, response_type='code')[源代码]¶

        Redirects the user to obtain OAuth authorization for this service.

        Some providers require that you register a redirect URL with your application instead of
        passing one via this method. You should call this method to log the user in, and then
        call get_authenticated_user in the handler for your redirect URL to complete the
        authorization process.

        在 3.1 版更改: Returns a Future and takes an optional callback. These are not strictly
        necessary as this method is synchronous, but they are supplied for consistency with
        OAuthMixin.authorize_redirect.

    oauth2_request(url, callback, access_token=None, post_args=None, **args)[源代码]¶

        Fetches the given URL auth an OAuth2 access token.

        If the request is a POST, post_args should be provided. Query string arguments should be
        given as keyword arguments.

        Example usage:

        ..testcode:

        class MainHandler(tornado.web.RequestHandler,
                          tornado.auth.FacebookGraphMixin):
            @tornado.web.authenticated
            @tornado.gen.coroutine
            def get(self):
                new_entry = yield self.oauth2_request(
                    "https://graph.facebook.com/me/feed",
                    post_args={"message": "I am posting from my Tornado application!"},
                    access_token=self.current_user["access_token"])

                if not new_entry:
                    # Call failed; perhaps missing permission?
                    yield self.authorize_redirect()
                    return
                self.finish("Posted a message!")

        4.3 新版功能.

    get_auth_http_client()[源代码]¶

        Returns the AsyncHTTPClient instance to be used for auth requests.

        May be overridden by subclasses to use an HTTP client other than the default.

        4.3 新版功能.

Google¶

class tornado.auth.GoogleOAuth2Mixin[源代码]¶

    Google authentication using OAuth2.

    In order to use, register your application with Google and copy the relevant parameters to
    your application settings.

      □ Go to the Google Dev Console at http://console.developers.google.com
      □ Select a project, or create a new one.
      □ In the sidebar on the left, select APIs & Auth.
      □ In the list of APIs, find the Google+ API service and set it to ON.
      □ In the sidebar on the left, select Credentials.
      □ In the OAuth section of the page, select Create New Client ID.
      □ Set the Redirect URI to point to your auth handler
      □ Copy the “Client secret” and “Client ID” to the application settings as {“google_oauth”:
        {“key”: CLIENT_ID, “secret”: CLIENT_SECRET}}

    3.2 新版功能.

    get_authenticated_user(redirect_uri, code, callback)[源代码]¶

        Handles the login for the Google user, returning an access token.

        The result is a dictionary containing an access_token field ([among others](https://
        developers.google.com/identity/protocols/OAuth2WebServer#handlingtheresponse)). Unlike
        other get_authenticated_user methods in this package, this method does not return any
        additional information about the user. The returned access token can be used with
        OAuth2Mixin.oauth2_request to request additional information (perhaps from https://
        www.googleapis.com/oauth2/v2/userinfo)

        Example usage:

        class GoogleOAuth2LoginHandler(tornado.web.RequestHandler,
                                       tornado.auth.GoogleOAuth2Mixin):
            @tornado.gen.coroutine
            def get(self):
                if self.get_argument('code', False):
                    access = yield self.get_authenticated_user(
                        redirect_uri='http://your.site.com/auth/google',
                        code=self.get_argument('code'))
                    user = yield self.oauth2_request(
                        "https://www.googleapis.com/oauth2/v1/userinfo",
                        access_token=access["access_token"])
                    # Save the user and access token with
                    # e.g. set_secure_cookie.
                else:
                    yield self.authorize_redirect(
                        redirect_uri='http://your.site.com/auth/google',
                        client_id=self.settings['google_oauth']['key'],
                        scope=['profile', 'email'],
                        response_type='code',
                        extra_params={'approval_prompt': 'auto'})

Facebook¶

class tornado.auth.FacebookGraphMixin[源代码]¶

    Facebook authentication using the new Graph API and OAuth2.

    get_authenticated_user(redirect_uri, client_id, client_secret, code, callback, extra_fields=
        None)[源代码]¶

        Handles the login for the Facebook user, returning a user object.

        Example usage:

        class FacebookGraphLoginHandler(tornado.web.RequestHandler,
                                        tornado.auth.FacebookGraphMixin):
          @tornado.gen.coroutine
          def get(self):
              if self.get_argument("code", False):
                  user = yield self.get_authenticated_user(
                      redirect_uri='/auth/facebookgraph/',
                      client_id=self.settings["facebook_api_key"],
                      client_secret=self.settings["facebook_secret"],
                      code=self.get_argument("code"))
                  # Save the user with e.g. set_secure_cookie
              else:
                  yield self.authorize_redirect(
                      redirect_uri='/auth/facebookgraph/',
                      client_id=self.settings["facebook_api_key"],
                      extra_params={"scope": "read_stream,offline_access"})

    facebook_request(path, callback, access_token=None, post_args=None, **args)[源代码]¶

        Fetches the given relative API path, e.g., “/btaylor/picture”

        If the request is a POST, post_args should be provided. Query string arguments should be
        given as keyword arguments.

        An introduction to the Facebook Graph API can be found at http://developers.facebook.com
        /docs/api

        Many methods require an OAuth access token which you can obtain through
        authorize_redirect and get_authenticated_user. The user returned through that process
        includes an access_token attribute that can be used to make authenticated requests via
        this method.

        Example usage:

        ..testcode:

        class MainHandler(tornado.web.RequestHandler,
                          tornado.auth.FacebookGraphMixin):
            @tornado.web.authenticated
            @tornado.gen.coroutine
            def get(self):
                new_entry = yield self.facebook_request(
                    "/me/feed",
                    post_args={"message": "I am posting from my Tornado application!"},
                    access_token=self.current_user["access_token"])

                if not new_entry:
                    # Call failed; perhaps missing permission?
                    yield self.authorize_redirect()
                    return
                self.finish("Posted a message!")

        The given path is relative to self._FACEBOOK_BASE_URL, by default “https://
        graph.facebook.com”.

        This method is a wrapper around OAuth2Mixin.oauth2_request; the only difference is that
        this method takes a relative path, while oauth2_request takes a complete url.

        在 3.1 版更改: Added the ability to override self._FACEBOOK_BASE_URL.

Twitter¶

class tornado.auth.TwitterMixin[源代码]¶

    Twitter OAuth authentication.

    To authenticate with Twitter, register your application with Twitter at http://twitter.com/
    apps. Then copy your Consumer Key and Consumer Secret to the application settings 
    twitter_consumer_key and twitter_consumer_secret. Use this mixin on the handler for the URL
    you registered as your application’s callback URL.

    When your application is set up, you can use this mixin like this to authenticate the user
    with Twitter and get access to their stream:

    class TwitterLoginHandler(tornado.web.RequestHandler,
                              tornado.auth.TwitterMixin):
        @tornado.gen.coroutine
        def get(self):
            if self.get_argument("oauth_token", None):
                user = yield self.get_authenticated_user()
                # Save the user using e.g. set_secure_cookie()
            else:
                yield self.authorize_redirect()

    The user object returned by get_authenticated_user includes the attributes username, name, 
    access_token, and all of the custom Twitter user attributes described at https://
    dev.twitter.com/docs/api/1.1/get/users/show

    authenticate_redirect(callback_uri=None, callback=None)[源代码]¶

        Just like authorize_redirect, but auto-redirects if authorized.

        This is generally the right interface to use if you are using Twitter for single-sign
        on.

        在 3.1 版更改: Now returns a Future and takes an optional callback, for compatibility
        with gen.coroutine.

    twitter_request(path, callback=None, access_token=None, post_args=None, **args)[源代码]¶

        Fetches the given API path, e.g., statuses/user_timeline/btaylor

        The path should not include the format or API version number. (we automatically use JSON
        format and API version 1).

        If the request is a POST, post_args should be provided. Query string arguments should be
        given as keyword arguments.

        All the Twitter methods are documented at http://dev.twitter.com/

        Many methods require an OAuth access token which you can obtain through
        authorize_redirect and get_authenticated_user. The user returned through that process
        includes an ‘access_token’ attribute that can be used to make authenticated requests via
        this method. Example usage:

        class MainHandler(tornado.web.RequestHandler,
                          tornado.auth.TwitterMixin):
            @tornado.web.authenticated
            @tornado.gen.coroutine
            def get(self):
                new_entry = yield self.twitter_request(
                    "/statuses/update",
                    post_args={"status": "Testing Tornado Web Server"},
                    access_token=self.current_user["access_token"])
                if not new_entry:
                    # Call failed; perhaps missing permission?
                    yield self.authorize_redirect()
                    return
                self.finish("Posted a message!")

tornado.wsgi — Interoperability with other Python frameworks and servers¶

WSGI support for the Tornado web framework.

WSGI is the Python standard for web servers, and allows for interoperability between Tornado and
other Python web frameworks and servers. This module provides WSGI support in two ways:

  • WSGIAdapter converts a tornado.web.Application to the WSGI application interface. This is
    useful for running a Tornado app on another HTTP server, such as Google App Engine. See the
    WSGIAdapter class documentation for limitations that apply.
  • WSGIContainer lets you run other WSGI applications and frameworks on the Tornado HTTP
    server. For example, with this class you can mix Django and Tornado handlers in a single
    server.

Running Tornado apps on WSGI servers¶

class tornado.wsgi.WSGIAdapter(application)[源代码]¶

    Converts a tornado.web.Application instance into a WSGI application.

    Example usage:

    import tornado.web
    import tornado.wsgi
    import wsgiref.simple_server

    class MainHandler(tornado.web.RequestHandler):
        def get(self):
            self.write("Hello, world")

    if __name__ == "__main__":
        application = tornado.web.Application([
            (r"/", MainHandler),
        ])
        wsgi_app = tornado.wsgi.WSGIAdapter(application)
        server = wsgiref.simple_server.make_server('', 8888, wsgi_app)
        server.serve_forever()

    See the appengine demo for an example of using this module to run a Tornado app on Google
    App Engine.

    In WSGI mode asynchronous methods are not supported. This means that it is not possible to
    use AsyncHTTPClient, or the tornado.auth or tornado.websocket modules.

    4.0 新版功能.

class tornado.wsgi.WSGIApplication(handlers=None, default_host='', transforms=None, **settings)
    [源代码]¶

    A WSGI equivalent of tornado.web.Application.

    4.0 版后已移除: Use a regular Application and wrap it in WSGIAdapter instead.

Running WSGI apps on Tornado servers¶

class tornado.wsgi.WSGIContainer(wsgi_application)[源代码]¶

    Makes a WSGI-compatible function runnable on Tornado’s HTTP server.

    警告

    WSGI is a synchronous interface, while Tornado’s concurrency model is based on
    single-threaded asynchronous execution. This means that running a WSGI app with Tornado’s
    WSGIContainer is less scalable than running the same app in a multi-threaded WSGI server
    like gunicorn or uwsgi. Use WSGIContainer only when there are benefits to combining Tornado
    and WSGI in the same process that outweigh the reduced scalability.

    Wrap a WSGI function in a WSGIContainer and pass it to HTTPServer to run it. For example:

    def simple_app(environ, start_response):
        status = "200 OK"
        response_headers = [("Content-type", "text/plain")]
        start_response(status, response_headers)
        return ["Hello world!\n"]

    container = tornado.wsgi.WSGIContainer(simple_app)
    http_server = tornado.httpserver.HTTPServer(container)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.current().start()

    This class is intended to let other frameworks (Django, web.py, etc) run on the Tornado HTTP
    server and I/O loop.

    The tornado.web.FallbackHandler class is often useful for mixing Tornado and WSGI apps in
    the same server. See https://github.com/bdarnell/django-tornado-demo for a complete example.

    static environ(request)[源代码]¶

        Converts a tornado.httputil.HTTPServerRequest to a WSGI environment.

tornado.platform.asyncio — Bridge between asyncio and Tornado¶

Bridges between the asyncio module and Tornado IOLoop.

3.2 新版功能.

This module integrates Tornado with the asyncio module introduced in Python 3.4 (and available
as a separate download for Python 3.3). This makes it possible to combine the two libraries on
the same event loop.

Most applications should use AsyncIOMainLoop to run Tornado on the default asyncio event loop.
Applications that need to run event loops on multiple threads may use AsyncIOLoop to create
multiple loops.

注解

Tornado requires the add_reader family of methods, so it is not compatible with the
ProactorEventLoop on Windows. Use the SelectorEventLoop instead.

class tornado.platform.asyncio.AsyncIOMainLoop[源代码]¶

    AsyncIOMainLoop creates an IOLoop that corresponds to the current asyncio event loop (i.e.
    the one returned by asyncio.get_event_loop()). Recommended usage:

    from tornado.platform.asyncio import AsyncIOMainLoop
    import asyncio
    AsyncIOMainLoop().install()
    asyncio.get_event_loop().run_forever()

class tornado.platform.asyncio.AsyncIOLoop[源代码]¶

    AsyncIOLoop is an IOLoop that runs on an asyncio event loop. This class follows the usual
    Tornado semantics for creating new IOLoops; these loops are not necessarily related to the 
    asyncio default event loop. Recommended usage:

    from tornado.ioloop import IOLoop
    IOLoop.configure('tornado.platform.asyncio.AsyncIOLoop')
    IOLoop.current().start()

    Each AsyncIOLoop creates a new asyncio.EventLoop; this object can be accessed with the 
    asyncio_loop attribute.

tornado.platform.asyncio.to_tornado_future(asyncio_future)[源代码]¶

    Convert an asyncio.Future to a tornado.concurrent.Future.

    4.1 新版功能.

tornado.platform.asyncio.to_asyncio_future(tornado_future)[源代码]¶

    Convert a Tornado yieldable object to an asyncio.Future.

    4.1 新版功能.

    在 4.3 版更改: Now accepts any yieldable object, not just tornado.concurrent.Future.

tornado.platform.caresresolver — Asynchronous DNS Resolver using C-Ares¶

This module contains a DNS resolver using the c-ares library (and its wrapper pycares).

class tornado.platform.caresresolver.CaresResolver¶

    Name resolver based on the c-ares library.

    This is a non-blocking and non-threaded resolver. It may not produce the same results as the
    system resolver, but can be used for non-blocking resolution when threads cannot be used.

    c-ares fails to resolve some names when family is AF_UNSPEC, so it is only recommended for
    use in AF_INET (i.e. IPv4). This is the default for tornado.simple_httpclient, but other
    libraries may default to AF_UNSPEC.

tornado.platform.twisted — Bridges between Twisted and Tornado¶

Bridges between the Twisted reactor and Tornado IOLoop.

This module lets you run applications and libraries written for Twisted in a Tornado
application. It can be used in two modes, depending on which library’s underlying event loop you
want to use.

This module has been tested with Twisted versions 11.0.0 and newer.

Twisted on Tornado¶

class tornado.platform.twisted.TornadoReactor(io_loop=None)[源代码]¶

    Twisted reactor built on the Tornado IOLoop.

    TornadoReactor implements the Twisted reactor interface on top of the Tornado IOLoop. To use
    it, simply call install at the beginning of the application:

    import tornado.platform.twisted
    tornado.platform.twisted.install()
    from twisted.internet import reactor

    When the app is ready to start, call IOLoop.current().start() instead of reactor.run().

    It is also possible to create a non-global reactor by calling 
    tornado.platform.twisted.TornadoReactor(io_loop). However, if the IOLoop and reactor are to
    be short-lived (such as those used in unit tests), additional cleanup may be required.
    Specifically, it is recommended to call:

    reactor.fireSystemEvent('shutdown')
    reactor.disconnectAll()

    before closing the IOLoop.

    在 4.1 版更改: The io_loop argument is deprecated.

tornado.platform.twisted.install(io_loop=None)[源代码]¶

    Install this package as the default Twisted reactor.

    install() must be called very early in the startup process, before most other
    twisted-related imports. Conversely, because it initializes the IOLoop, it cannot be called
    before fork_processes or multi-process start. These conflicting requirements make it
    difficult to use TornadoReactor in multi-process mode, and an external process manager such
    as supervisord is recommended instead.

    在 4.1 版更改: The io_loop argument is deprecated.

Tornado on Twisted¶

class tornado.platform.twisted.TwistedIOLoop[源代码]¶

    IOLoop implementation that runs on Twisted.

    TwistedIOLoop implements the Tornado IOLoop interface on top of the Twisted reactor.
    Recommended usage:

    from tornado.platform.twisted import TwistedIOLoop
    from twisted.internet import reactor
    TwistedIOLoop().install()
    # Set up your tornado application as usual using `IOLoop.instance`
    reactor.run()

    Uses the global Twisted reactor by default. To create multiple TwistedIOLoops in the same
    process, you must pass a unique reactor when constructing each one.

    Not compatible with tornado.process.Subprocess.set_exit_callback because the SIGCHLD
    handlers used by Tornado and Twisted conflict with each other.

Twisted DNS resolver¶

class tornado.platform.twisted.TwistedResolver[源代码]¶

    Twisted-based asynchronous resolver.

    This is a non-blocking and non-threaded resolver. It is recommended only when threads cannot
    be used, since it has limitations compared to the standard getaddrinfo-based Resolver and
    ThreadedResolver. Specifically, it returns at most one result, and arguments other than host
    and family are ignored. It may fail to resolve when family is not socket.AF_UNSPEC.

    Requires Twisted 12.1 or newer.

    在 4.1 版更改: The io_loop argument is deprecated.

通用工具¶

tornado.autoreload — Automatically detect code changes in development¶

Automatically restart the server when a source file is modified.

Most applications should not access this module directly. Instead, pass the keyword argument 
autoreload=True to the tornado.web.Application constructor (or debug=True, which enables this
setting and several others). This will enable autoreload mode as well as checking for changes to
templates and static resources. Note that restarting is a destructive operation and any requests
in progress will be aborted when the process restarts. (If you want to disable autoreload while
using other debug-mode features, pass both debug=True and autoreload=False).

This module can also be used as a command-line wrapper around scripts such as unit test runners.
See the main method for details.

The command-line wrapper and Application debug modes can be used together. This combination is
encouraged as the wrapper catches syntax errors and other import-time failures, while debug mode
catches changes once the server has started.

This module depends on IOLoop, so it will not work in WSGI applications and Google App Engine.
It also will not work correctly when HTTPServer‘s multi-process mode is used.

Reloading loses any Python interpreter command-line arguments (e.g. -u) because it re-executes
Python using sys.executable and sys.argv. Additionally, modifying these variables will cause
reloading to behave incorrectly.

tornado.autoreload.start(io_loop=None, check_time=500)[源代码]¶

    Begins watching source files for changes.

    在 4.1 版更改: The io_loop argument is deprecated.

tornado.autoreload.wait()[源代码]¶

    Wait for a watched file to change, then restart the process.

    Intended to be used at the end of scripts like unit test runners, to run the tests again
    after any source file changes (but see also the command-line interface in main)

tornado.autoreload.watch(filename)[源代码]¶

    Add a file to the watch list.

    All imported modules are watched by default.

tornado.autoreload.add_reload_hook(fn)[源代码]¶

    Add a function to be called before reloading the process.

    Note that for open file and socket handles it is generally preferable to set the FD_CLOEXEC
    flag (using fcntl or tornado.platform.auto.set_close_exec) instead of using a reload hook to
    close them.

tornado.autoreload.main()[源代码]¶

    Command-line wrapper to re-run a script whenever its source changes.

    Scripts may be specified by filename or module name:

    python -m tornado.autoreload -m tornado.test.runtests
    python -m tornado.autoreload tornado/test/runtests.py

    Running a script with this wrapper is similar to calling tornado.autoreload.wait at the end
    of the script, but this wrapper can catch import-time problems like syntax errors that would
    otherwise prevent the script from reaching its call to wait.

tornado.log — Logging support¶

Logging support for Tornado.

Tornado uses three logger streams:

  • tornado.access: Per-request logging for Tornado’s HTTP servers (and potentially other
    servers in the future)
  • tornado.application: Logging of errors from application code (i.e. uncaught exceptions from
    callbacks)
  • tornado.general: General-purpose logging, including any errors or warnings from Tornado
    itself.

These streams may be configured independently using the standard library’s logging module. For
example, you may wish to send tornado.access logs to a separate file for analysis.

class tornado.log.LogFormatter(color=True, fmt='%(color)s[%(levelname)1.1s %(asctime)s %(module)
    s:%(lineno)d]%(end_color)s %(message)s', datefmt='%y%m%d %H:%M:%S', colors={40: 1, 10: 4, 
    20: 2, 30: 3})[源代码]¶

    Log formatter used in Tornado.

    Key features of this formatter are:

      □ Color support when logging to a terminal that supports it.
      □ Timestamps on every log line.
      □ Robust against str/bytes encoding problems.

    This formatter is enabled automatically by tornado.options.parse_command_line (unless 
    --logging=none is used).

          • color (bool) – Enables color support.
          • fmt (string) – Log message format. It will be applied to the attributes dict of log
    参      records. The text between %(color)s and %(end_color)s will be colored depending on
    数:     the level if color support is on.
          • colors (dict) – color mappings from logging level to terminal color code
          • datefmt (string) – Datetime format. Used for formatting (asctime) placeholder in 
            prefix_fmt.

    在 3.2 版更改: Added fmt and datefmt arguments.

tornado.log.enable_pretty_logging(options=None, logger=None)[源代码]¶

    Turns on formatted logging output as configured.

    This is called automatically by tornado.options.parse_command_line and
    tornado.options.parse_config_file.

tornado.log.define_logging_options(options=None)[源代码]¶

    Add logging-related flags to options.

    These options are present automatically on the default options instance; this method is only
    necessary if you have created your own OptionParser.

    4.2 新版功能: This function existed in prior versions but was broken and undocumented until
    4.2.

tornado.options — Command-line parsing¶

A command line parsing module that lets modules define their own options.

Each module defines its own options which are added to the global option namespace, e.g.:

from tornado.options import define, options

define("mysql_host", default="127.0.0.1:3306", help="Main user DB")
define("memcache_hosts", default="127.0.0.1:11011", multiple=True,
       help="Main user memcache servers")

def connect():
    db = database.Connection(options.mysql_host)
    ...

The main() method of your application does not need to be aware of all of the options used
throughout your program; they are all automatically loaded when the modules are loaded. However,
all modules that define options must have been imported before the command line is parsed.

Your main() method can parse the command line or parse a config file with either:

tornado.options.parse_command_line()
# or
tornado.options.parse_config_file("/etc/server.conf")

Command line formats are what you would expect (--myoption=myvalue). Config files are just
Python files. Global names become options, e.g.:

myoption = "myvalue"
myotheroption = "myothervalue"

We support datetimes, timedeltas, ints, and floats (just pass a type kwarg to define). We also
accept multi-value options. See the documentation for define() below.

tornado.options.options is a singleton instance of OptionParser, and the top-level functions in
this module (define, parse_command_line, etc) simply call methods on it. You may create
additional OptionParser instances to define isolated sets of options, such as for subcommands.

注解

By default, several options are defined that will configure the standard logging module when
parse_command_line or parse_config_file are called. If you want Tornado to leave the logging
configuration alone so you can manage it yourself, either pass --logging=none on the command
line or do the following to disable it in code:

from tornado.options import options, parse_command_line
options.logging = None
parse_command_line()

在 4.3 版更改: Dashes and underscores are fully interchangeable in option names; options can be
defined, set, and read with any mix of the two. Dashes are typical for command-line usage while
config files require underscores.

Global functions¶

tornado.options.define(name, default=None, type=None, help=None, metavar=None, multiple=False, 
    group=None, callback=None)[源代码]¶

    Defines an option in the global namespace.

    See OptionParser.define.

tornado.options.options¶

    Global options object. All defined options are available as attributes on this object.

tornado.options.parse_command_line(args=None, final=True)[源代码]¶

    Parses global options from the command line.

    See OptionParser.parse_command_line.

tornado.options.parse_config_file(path, final=True)[源代码]¶

    Parses global options from a config file.

    See OptionParser.parse_config_file.

tornado.options.print_help(file=sys.stderr)[源代码]¶

    Prints all the command line options to stderr (or another file).

    See OptionParser.print_help.

tornado.options.add_parse_callback(callback)[源代码]¶

    Adds a parse callback, to be invoked when option parsing is done.

    See OptionParser.add_parse_callback

exception tornado.options.Error[源代码]¶

    Exception raised by errors in the options module.

OptionParser class¶

class tornado.options.OptionParser[源代码]¶

    A collection of options, a dictionary with object-like access.

    Normally accessed via static functions in the tornado.options module, which reference a
    global instance.

    items()[源代码]¶

        A sequence of (name, value) pairs.

        3.1 新版功能.

    groups()[源代码]¶

        The set of option-groups created by define.

        3.1 新版功能.

    group_dict(group)[源代码]¶

        The names and values of options in a group.

        Useful for copying options into Application settings:

        from tornado.options import define, parse_command_line, options

        define('template_path', group='application')
        define('static_path', group='application')

        parse_command_line()

        application = Application(
            handlers, **options.group_dict('application'))

        3.1 新版功能.

    as_dict()[源代码]¶

        The names and values of all options.

        3.1 新版功能.

    define(name, default=None, type=None, help=None, metavar=None, multiple=False, group=None, 
        callback=None)[源代码]¶

        Defines a new command line option.

        If type is given (one of str, float, int, datetime, or timedelta) or can be inferred
        from the default, we parse the command line arguments based on the given type. If 
        multiple is True, we accept comma-separated values, and the option value is always a
        list.

        For multi-value integers, we also accept the syntax x:y, which turns into range(x, y) -
        very useful for long integer ranges.

        help and metavar are used to construct the automatically generated command line help
        string. The help message is formatted like:

        --name=METAVAR      help string

        group is used to group the defined options in logical groups. By default, command line
        options are grouped by the file in which they are defined.

        Command line option names must be unique globally. They can be parsed from the command
        line with parse_command_line or parsed from a config file with parse_config_file.

        If a callback is given, it will be run with the new value whenever the option is
        changed. This can be used to combine command-line and file-based options:

        define("config", type=str, help="path to config file",
               callback=lambda path: parse_config_file(path, final=False))

        With this definition, options in the file specified by --config will override options
        set earlier on the command line, but can be overridden by later flags.

    parse_command_line(args=None, final=True)[源代码]¶

        Parses all options given on the command line (defaults to sys.argv).

        Note that args[0] is ignored since it is the program name in sys.argv.

        We return a list of all arguments that are not parsed as options.

        If final is False, parse callbacks will not be run. This is useful for applications that
        wish to combine configurations from multiple sources.

    parse_config_file(path, final=True)[源代码]¶

        Parses and loads the Python config file at the given path.

        If final is False, parse callbacks will not be run. This is useful for applications that
        wish to combine configurations from multiple sources.

        在 4.1 版更改: Config files are now always interpreted as utf-8 instead of the system
        default encoding.

    print_help(file=None)[源代码]¶

        Prints all the command line options to stderr (or another file).

    add_parse_callback(callback)[源代码]¶

        Adds a parse callback, to be invoked when option parsing is done.

    mockable()[源代码]¶

        Returns a wrapper around self that is compatible with mock.patch.

        The mock.patch function (included in the standard library unittest.mock package since
        Python 3.3, or in the third-party mock package for older versions of Python) is
        incompatible with objects like options that override __getattr__ and __setattr__. This
        function returns an object that can be used with mock.patch.object to modify option
        values:

        with mock.patch.object(options.mockable(), 'name', value):
            assert options.name == value

tornado.stack_context — Exception handling across asynchronous callbacks¶

StackContext allows applications to maintain threadlocal-like state that follows execution as it
moves to other execution contexts.

The motivating examples are to eliminate the need for explicit async_callback wrappers (as in
tornado.web.RequestHandler), and to allow some additional context to be kept for logging.

This is slightly magic, but it’s an extension of the idea that an exception handler is a kind of
stack-local state and when that stack is suspended and resumed in a new context that state needs
to be preserved. StackContext shifts the burden of restoring that state from each call site
(e.g. wrapping each AsyncHTTPClient callback in async_callback) to the mechanisms that transfer
control from one context to another (e.g. AsyncHTTPClient itself, IOLoop, thread pools, etc).

Example usage:

@contextlib.contextmanager
def die_on_error():
    try:
        yield
    except Exception:
        logging.error("exception in asynchronous operation",exc_info=True)
        sys.exit(1)

with StackContext(die_on_error):
    # Any exception thrown here *or in callback and its descendants*
    # will cause the process to exit instead of spinning endlessly
    # in the ioloop.
    http_client.fetch(url, callback)
ioloop.start()

Most applications shouldn’t have to work with StackContext directly. Here are a few rules of
thumb for when it’s necessary:

  • If you’re writing an asynchronous library that doesn’t rely on a stack_context-aware library
    like tornado.ioloop or tornado.iostream (for example, if you’re writing a thread pool), use
    stack_context.wrap() before any asynchronous operations to capture the stack context from
    where the operation was started.
  • If you’re writing an asynchronous library that has some shared resources (such as a
    connection pool), create those shared resources within a with stack_context.NullContext():
    block. This will prevent StackContexts from leaking from one request to another.
  • If you want to write something like an exception handler that will persist across
    asynchronous calls, create a new StackContext (or ExceptionStackContext), and make your
    asynchronous calls in a with block that references your StackContext.

class tornado.stack_context.StackContext(context_factory)[源代码]¶

    Establishes the given context as a StackContext that will be transferred.

    Note that the parameter is a callable that returns a context manager, not the context
    itself. That is, where for a non-transferable context manager you would say:

    with my_context():

    StackContext takes the function itself rather than its result:

    with StackContext(my_context):

    The result of with StackContext() as cb: is a deactivation callback. Run this callback when
    the StackContext is no longer needed to ensure that it is not propagated any further (note
    that deactivating a context does not affect any instances of that context that are currently
    pending). This is an advanced feature and not necessary in most applications.

class tornado.stack_context.ExceptionStackContext(exception_handler)[源代码]¶

    Specialization of StackContext for exception handling.

    The supplied exception_handler function will be called in the event of an uncaught exception
    in this context. The semantics are similar to a try/finally clause, and intended use cases
    are to log an error, close a socket, or similar cleanup actions. The exc_info triple (type, 
    value, traceback) will be passed to the exception_handler function.

    If the exception handler returns true, the exception will be consumed and will not be
    propagated to other exception handlers.

class tornado.stack_context.NullContext[源代码]¶

    Resets the StackContext.

    Useful when creating a shared resource on demand (e.g. an AsyncHTTPClient) where the stack
    that caused the creating is not relevant to future operations.

tornado.stack_context.wrap(fn)[源代码]¶

    Returns a callable object that will restore the current StackContext when executed.

    Use this whenever saving a callback to be executed later in a different execution context
    (either in a different thread or asynchronously in the same thread).

tornado.stack_context.run_with_stack_context(context, func)[源代码]¶

    Run a coroutine func in the given StackContext.

    It is not safe to have a yield statement within a with StackContext block, so it is
    difficult to use stack context with gen.coroutine. This helper function runs the function in
    the correct context while keeping the yield and with statements syntactically separate.

    Example:

    @gen.coroutine
    def incorrect():
        with StackContext(ctx):
            # ERROR: this will raise StackContextInconsistentError
            yield other_coroutine()

    @gen.coroutine
    def correct():
        yield run_with_stack_context(StackContext(ctx), other_coroutine)

    3.1 新版功能.

tornado.testing — Unit testing support for asynchronous code¶

Support classes for automated testing.

  • AsyncTestCase and AsyncHTTPTestCase: Subclasses of unittest.TestCase with additional support
    for testing asynchronous (IOLoop based) code.
  • ExpectLog and LogTrapTestCase: Make test logs less spammy.
  • main(): A simple test runner (wrapper around unittest.main()) with support for the
    tornado.autoreload module to rerun the tests when code changes.

Asynchronous test cases¶

class tornado.testing.AsyncTestCase(methodName='runTest', **kwargs)[源代码]¶

    TestCase subclass for testing IOLoop-based asynchronous code.

    The unittest framework is synchronous, so the test must be complete by the time the test
    method returns. This means that asynchronous code cannot be used in quite the same way as
    usual. To write test functions that use the same yield-based patterns used with the
    tornado.gen module, decorate your test methods with tornado.testing.gen_test instead of
    tornado.gen.coroutine. This class also provides the stop() and wait() methods for a more
    manual style of testing. The test method itself must call self.wait(), and asynchronous
    callbacks should call self.stop() to signal completion.

    By default, a new IOLoop is constructed for each test and is available as self.io_loop. This
    IOLoop should be used in the construction of HTTP clients/servers, etc. If the code being
    tested requires a global IOLoop, subclasses should override get_new_ioloop to return it.

    The IOLoop‘s start and stop methods should not be called directly. Instead, use self.stop
    and self.wait. Arguments passed to self.stop are returned from self.wait. It is possible to
    have multiple wait/stop cycles in the same test.

    Example:

    # This test uses coroutine style.
    class MyTestCase(AsyncTestCase):
        @tornado.testing.gen_test
        def test_http_fetch(self):
            client = AsyncHTTPClient(self.io_loop)
            response = yield client.fetch("http://www.tornadoweb.org")
            # Test contents of response
            self.assertIn("FriendFeed", response.body)

    # This test uses argument passing between self.stop and self.wait.
    class MyTestCase2(AsyncTestCase):
        def test_http_fetch(self):
            client = AsyncHTTPClient(self.io_loop)
            client.fetch("http://www.tornadoweb.org/", self.stop)
            response = self.wait()
            # Test contents of response
            self.assertIn("FriendFeed", response.body)

    # This test uses an explicit callback-based style.
    class MyTestCase3(AsyncTestCase):
        def test_http_fetch(self):
            client = AsyncHTTPClient(self.io_loop)
            client.fetch("http://www.tornadoweb.org/", self.handle_fetch)
            self.wait()

        def handle_fetch(self, response):
            # Test contents of response (failures and exceptions here
            # will cause self.wait() to throw an exception and end the
            # test).
            # Exceptions thrown here are magically propagated to
            # self.wait() in test_http_fetch() via stack_context.
            self.assertIn("FriendFeed", response.body)
            self.stop()

    get_new_ioloop()[源代码]¶

        Creates a new IOLoop for this test. May be overridden in subclasses for tests that
        require a specific IOLoop (usually the singleton IOLoop.instance()).

    stop(_arg=None, **kwargs)[源代码]¶

        Stops the IOLoop, causing one pending (or future) call to wait() to return.

        Keyword arguments or a single positional argument passed to stop() are saved and will be
        returned by wait().

    wait(condition=None, timeout=None)[源代码]¶

        Runs the IOLoop until stop is called or timeout has passed.

        In the event of a timeout, an exception will be thrown. The default timeout is 5
        seconds; it may be overridden with a timeout keyword argument or globally with the 
        ASYNC_TEST_TIMEOUT environment variable.

        If condition is not None, the IOLoop will be restarted after stop() until condition()
        returns true.

        在 3.1 版更改: Added the ASYNC_TEST_TIMEOUT environment variable.

class tornado.testing.AsyncHTTPTestCase(methodName='runTest', **kwargs)[源代码]¶

    A test case that starts up an HTTP server.

    Subclasses must override get_app(), which returns the tornado.web.Application (or other
    HTTPServer callback) to be tested. Tests will typically use the provided self.http_client to
    fetch URLs from this server.

    Example, assuming the “Hello, world” example from the user guide is in hello.py:

    import hello

    class TestHelloApp(AsyncHTTPTestCase):
        def get_app(self):
            return hello.make_app()

        def test_homepage(self):
            response = self.fetch('/')
            self.assertEqual(response.code, 200)
            self.assertEqual(response.body, 'Hello, world')

    That call to self.fetch() is equivalent to

    self.http_client.fetch(self.get_url('/'), self.stop)
    response = self.wait()

    which illustrates how AsyncTestCase can turn an asynchronous operation, like 
    http_client.fetch(), into a synchronous operation. If you need to do other asynchronous
    operations in tests, you’ll probably need to use stop() and wait() yourself.

    get_app()[源代码]¶

        Should be overridden by subclasses to return a tornado.web.Application or other
        HTTPServer callback.

    fetch(path, **kwargs)[源代码]¶

        Convenience method to synchronously fetch a url.

        The given path will be appended to the local server’s host and port. Any additional
        kwargs will be passed directly to AsyncHTTPClient.fetch (and so could be used to pass 
        method="POST", body="...", etc).

    get_httpserver_options()[源代码]¶

        May be overridden by subclasses to return additional keyword arguments for the server.

    get_http_port()[源代码]¶

        Returns the port used by the server.

        A new port is chosen for each test.

    get_url(path)[源代码]¶

        Returns an absolute url for the given path on the test server.

class tornado.testing.AsyncHTTPSTestCase(methodName='runTest', **kwargs)[源代码]¶

    A test case that starts an HTTPS server.

    Interface is generally the same as AsyncHTTPTestCase.

    get_ssl_options()[源代码]¶

        May be overridden by subclasses to select SSL options.

        By default includes a self-signed testing certificate.

tornado.testing.gen_test(func=None, timeout=None)[源代码]¶

    Testing equivalent of @gen.coroutine, to be applied to test methods.

    @gen.coroutine cannot be used on tests because the IOLoop is not already running. @gen_test
    should be applied to test methods on subclasses of AsyncTestCase.

    Example:

    class MyTest(AsyncHTTPTestCase):
        @gen_test
        def test_something(self):
            response = yield gen.Task(self.fetch('/'))

    By default, @gen_test times out after 5 seconds. The timeout may be overridden globally with
    the ASYNC_TEST_TIMEOUT environment variable, or for each test with the timeout keyword
    argument:

    class MyTest(AsyncHTTPTestCase):
        @gen_test(timeout=10)
        def test_something_slow(self):
            response = yield gen.Task(self.fetch('/'))

    3.1 新版功能: The timeout argument and ASYNC_TEST_TIMEOUT environment variable.

    在 4.0 版更改: The wrapper now passes along *args, **kwargs so it can be used on functions
    with arguments.

Controlling log output¶

class tornado.testing.ExpectLog(logger, regex, required=True)[源代码]¶

    Context manager to capture and suppress expected log output.

    Useful to make tests of error conditions less noisy, while still leaving unexpected log
    entries visible. Not thread safe.

    The attribute logged_stack is set to true if any exception stack trace was logged.

    Usage:

    with ExpectLog('tornado.application', "Uncaught exception"):
        error_response = self.fetch("/some_page")

    在 4.3 版更改: Added the logged_stack attribute.

    Constructs an ExpectLog context manager.

           • logger – Logger object (or name of logger) to watch. Pass an empty string to watch
             the root logger.
     参    • regex – Regular expression to match. Any log entries on the specified logger that
    数:      match this regex will be suppressed.
           • required – If true, an exeption will be raised if the end of the with statement is
             reached without matching any log entries.

class tornado.testing.LogTrapTestCase(methodName='runTest')[源代码]¶

    A test case that captures and discards all logging output if the test passes.

    Some libraries can produce a lot of logging output even when the test succeeds, so this
    class can be useful to minimize the noise. Simply use it as a base class for your test case.
    It is safe to combine with AsyncTestCase via multiple inheritance (class MyTestCase
    (AsyncHTTPTestCase, LogTrapTestCase):)

    This class assumes that only one log handler is configured and that it is a StreamHandler.
    This is true for both logging.basicConfig and the “pretty logging” configured by
    tornado.options. It is not compatible with other log buffering mechanisms, such as those
    provided by some test runners.

    4.1 版后已移除: Use the unittest module’s --buffer option instead, or ExpectLog.

    Create an instance of the class that will use the named test method when executed. Raises a
    ValueError if the instance does not have a method with the specified name.

Test runner¶

tornado.testing.main(**kwargs)[源代码]¶

    A simple test runner.

    This test runner is essentially equivalent to unittest.main from the standard library, but
    adds support for tornado-style option parsing and log formatting.

    The easiest way to run a test is via the command line:

    python -m tornado.testing tornado.test.stack_context_test

    See the standard library unittest module for ways in which tests can be specified.

    Projects with many tests may wish to define a test script like tornado/test/runtests.py.
    This script should define a method all() which returns a test suite and then call
    tornado.testing.main(). Note that even when a test script is used, the all() test suite may
    be overridden by naming a single test on the command line:

    # Runs all tests
    python -m tornado.test.runtests
    # Runs one test
    python -m tornado.test.runtests tornado.test.stack_context_test

    Additional keyword arguments passed through to unittest.main(). For example, use 
    tornado.testing.main(verbosity=2) to show many test details as they are run. See http://
    docs.python.org/library/unittest.html#unittest.main for full argument list.

Helper functions¶

tornado.testing.bind_unused_port(reuse_port=False)[源代码]¶

    Binds a server socket to an available port on localhost.

    Returns a tuple (socket, port).

tornado.testing.get_unused_port()[源代码]¶

    Returns a (hopefully) unused port number.

    This function does not guarantee that the port it returns is available, only that a series
    of get_unused_port calls in a single process return distinct ports.

    Use 版后已移除: bind_unused_port instead, which is guaranteed to find an unused port.

tornado.testing.get_async_test_timeout()[源代码]¶

    Get the global timeout setting for async tests.

    Returns a float, the timeout in seconds.

    3.1 新版功能.

tornado.util — General-purpose utilities¶

Miscellaneous utility functions and classes.

This module is used internally by Tornado. It is not necessarily expected that the functions and
classes defined here will be useful to other applications, but they are documented here in case
they are.

The one public-facing part of this module is the Configurable class and its configure method,
which becomes a part of the interface of its subclasses, including AsyncHTTPClient, IOLoop, and
Resolver.

class tornado.util.ObjectDict[源代码]¶

    Makes a dictionary behave like an object, with attribute-style access.

class tornado.util.GzipDecompressor[源代码]¶

    Streaming gzip decompressor.

    The interface is like that of zlib.decompressobj (without some of the optional arguments,
    but it understands gzip headers and checksums.

    decompress(value, max_length=None)[源代码]¶

        Decompress a chunk, returning newly-available data.

        Some data may be buffered for later processing; flush must be called when there is no
        more input data to ensure that all data was processed.

        If max_length is given, some input data may be left over in unconsumed_tail; you must
        retrieve this value and pass it back to a future call to decompress if it is not empty.

    unconsumed_tail¶

        Returns the unconsumed portion left over

    flush()[源代码]¶

        Return any remaining buffered data not yet returned by decompress.

        Also checks for errors such as truncated input. No other methods may be called on this
        object after flush.

tornado.util.import_object(name)[源代码]¶

    Imports an object by name.

    import_object(‘x’) is equivalent to ‘import x’. import_object(‘x.y.z’) is equivalent to
    ‘from x.y import z’.

    >>> import tornado.escape
    >>> import_object('tornado.escape') is tornado.escape
    True
    >>> import_object('tornado.escape.utf8') is tornado.escape.utf8
    True
    >>> import_object('tornado') is tornado
    True
    >>> import_object('tornado.missing_module')
    Traceback (most recent call last):
        ...
    ImportError: No module named missing_module

tornado.util.errno_from_exception(e)[源代码]¶

    Provides the errno from an Exception object.

    There are cases that the errno attribute was not set so we pull the errno out of the args
    but if someone instantiates an Exception without any args you will get a tuple error. So
    this function abstracts all that behavior to give you a safe way to get the errno.

class tornado.util.Configurable[源代码]¶

    Base class for configurable interfaces.

    A configurable interface is an (abstract) class whose constructor acts as a factory function
    for one of its implementation subclasses. The implementation subclass as well as optional
    keyword arguments to its initializer can be set globally at runtime with configure.

    By using the constructor as the factory method, the interface looks like a normal class,
    isinstance works as usual, etc. This pattern is most useful when the choice of
    implementation is likely to be a global decision (e.g. when epoll is available, always use
    it instead of select), or when a previously-monolithic class has been split into specialized
    subclasses.

    Configurable subclasses must define the class methods configurable_base and
    configurable_default, and use the instance method initialize instead of __init__.

    classmethod configurable_base()[源代码]¶

        Returns the base class of a configurable hierarchy.

        This will normally return the class in which it is defined. (which is not necessarily
        the same as the cls classmethod parameter).

    classmethod configurable_default()[源代码]¶

        Returns the implementation class to be used if none is configured.

    initialize()[源代码]¶

        Initialize a Configurable subclass instance.

        Configurable classes should use initialize instead of __init__.

        在 4.2 版更改: Now accepts positional arguments in addition to keyword arguments.

    classmethod configure(impl, **kwargs)[源代码]¶

        Sets the class to use when the base class is instantiated.

        Keyword arguments will be saved and added to the arguments passed to the constructor.
        This can be used to set global defaults for some parameters.

    classmethod configured_class()[源代码]¶

        Returns the currently configured class.

class tornado.util.ArgReplacer(func, name)[源代码]¶

    Replaces one value in an args, kwargs pair.

    Inspects the function signature to find an argument by name whether it is passed by position
    or keyword. For use in decorators and similar wrappers.

    get_old_value(args, kwargs, default=None)[源代码]¶

        Returns the old value of the named argument without replacing it.

        Returns default if the argument is not present.

    replace(new_value, args, kwargs)[源代码]¶

        Replace the named argument in args, kwargs with new_value.

        Returns (old_value, args, kwargs). The returned args and kwargs objects may not be the
        same as the input objects, or the input objects may be mutated.

        If the named argument was not found, new_value will be added to kwargs and None will be
        returned as old_value.

tornado.util.timedelta_to_seconds(td)[源代码]¶

    Equivalent to td.total_seconds() (introduced in python 2.7).

常见问题¶

  • Why isn’t this example with time.sleep() running in parallel?
  • My code is asynchronous, but it’s not running in parallel in two browser tabs.

Why isn’t this example with time.sleep() running in parallel?¶

Many people’s first foray into Tornado’s concurrency looks something like this:

class BadExampleHandler(RequestHandler):
    def get(self):
        for i in range(5):
            print(i)
            time.sleep(1)

Fetch this handler twice at the same time and you’ll see that the second five-second countdown
doesn’t start until the first one has completely finished. The reason for this is that
time.sleep is a blocking function: it doesn’t allow control to return to the IOLoop so that
other handlers can be run.

Of course, time.sleep is really just a placeholder in these examples, the point is to show what
happens when something in a handler gets slow. No matter what the real code is doing, to achieve
concurrency blocking code must be replaced with non-blocking equivalents. This means one of
three things:

 1. Find a coroutine-friendly equivalent. For time.sleep, use tornado.gen.sleep instead:

    class CoroutineSleepHandler(RequestHandler):
        @gen.coroutine
        def get(self):
            for i in range(5):
                print(i)
                yield gen.sleep(1)

    When this option is available, it is usually the best approach. See the Tornado wiki for
    links to asynchronous libraries that may be useful.

 2. Find a callback-based equivalent. Similar to the first option, callback-based libraries are
    available for many tasks, although they are slightly more complicated to use than a library
    designed for coroutines. These are typically used with tornado.gen.Task as an adapter:

    class CoroutineTimeoutHandler(RequestHandler):
        @gen.coroutine
        def get(self):
            io_loop = IOLoop.current()
            for i in range(5):
                print(i)
                yield gen.Task(io_loop.add_timeout, io_loop.time() + 1)

    Again, the Tornado wiki can be useful to find suitable libraries.

 3. Run the blocking code on another thread. When asynchronous libraries are not available,
    concurrent.futures.ThreadPoolExecutor can be used to run any blocking code on another
    thread. This is a universal solution that can be used for any blocking function whether an
    asynchronous counterpart exists or not:

    executor = concurrent.futures.ThreadPoolExecutor(8)

    class ThreadPoolHandler(RequestHandler):
        @gen.coroutine
        def get(self):
            for i in range(5):
                print(i)
                yield executor.submit(time.sleep, 1)

See the Asynchronous I/O chapter of the Tornado user’s guide for more on blocking and
asynchronous functions.

My code is asynchronous, but it’s not running in parallel in two browser tabs.¶

Even when a handler is asynchronous and non-blocking, it can be surprisingly tricky to verify
this. Browsers will recognize that you are trying to load the same page in two different tabs
and delay the second request until the first has finished. To work around this and see that the
server is in fact working in parallel, do one of two things:

  • Add something to your urls to make them unique. Instead of http://localhost:8888 in both
    tabs, load http://localhost:8888/?x=1 in one and http://localhost:8888/?x=2 in the other.
  • Use two different browsers. For example, Firefox will be able to load a url even while that
    same url is being loaded in a Chrome tab.

版本记录¶

What’s new in Tornado 4.3¶

Nov 6, 2015¶

Highlights¶

  • The new async/await keywords in Python 3.5 are supported. In most cases, async def can be
    used in place of the @gen.coroutine decorator. Inside a function defined with async def, use
    await instead of yield to wait on an asynchronous operation. Coroutines defined with async/
    await will be faster than those defined with @gen.coroutine and yield, but do not support
    some features including Callback/Wait or the ability to yield a Twisted Deferred. See the
    users’ guide for more.
  • The async/await keywords are also available when compiling with Cython in older versions of
    Python.

Deprecation notice¶

  • This will be the last release of Tornado to support Python 2.6 or 3.2. Note that PyPy3 will
    continue to be supported even though it implements a mix of Python 3.2 and 3.3 features.

Installation¶

  • Tornado has several new dependencies: ordereddict on Python 2.6, singledispatch on all
    Python versions prior to 3.4 (This was an optional dependency in prior versions of Tornado,
    and is now mandatory), and backports_abc>=0.4 on all versions prior to 3.5. These
    dependencies will be installed automatically when installing with pip or setup.py install.
    These dependencies will not be required when running on Google App Engine.
  • Binary wheels are provided for Python 3.5 on Windows (32 and 64 bit).

tornado.auth¶

  • New method OAuth2Mixin.oauth2_request can be used to make authenticated requests with an
    access token.
  • Now compatible with callbacks that have been compiled with Cython.

tornado.autoreload¶

  • Fixed an issue with the autoreload command-line wrapper in which imports would be
    incorrectly interpreted as relative.

tornado.curl_httpclient¶

  • Fixed parsing of multi-line headers.
  • allow_nonstandard_methods=True now bypasses body sanity checks, in the same way as in 
    simple_httpclient.
  • The PATCH method now allows a body without allow_nonstandard_methods=True.

tornado.gen¶

  • WaitIterator now supports the async for statement on Python 3.5.
  • @gen.coroutine can be applied to functions compiled with Cython. On python versions prior to
    3.5, the backports_abc package must be installed for this functionality.
  • Multi and multi_future are deprecated and replaced by a unified function multi.

tornado.httpclient¶

  • tornado.httpclient.HTTPError is now copyable with the copy module.

tornado.httpserver¶

  • Requests containing both Content-Length and Transfer-Encoding will be treated as an error.

tornado.httputil¶

  • HTTPHeaders can now be pickled and unpickled.

tornado.ioloop¶

  • IOLoop(make_current=True) now works as intended instead of raising an exception.
  • The Twisted and asyncio IOLoop implementations now clear current() when they exit, like the
    standard IOLoops.
  • IOLoop.add_callback is faster in the single-threaded case.
  • IOLoop.add_callback no longer raises an error when called on a closed IOLoop, but the
    callback will not be invoked.

tornado.iostream¶

  • Coroutine-style usage of IOStream now converts most errors into StreamClosedError, which has
    the effect of reducing log noise from exceptions that are outside the application’s control
    (especially SSL errors).
  • StreamClosedError now has a real_error attribute which indicates why the stream was closed.
    It is the same as the error attribute of IOStream but may be more easily accessible than the
    IOStream itself.
  • Improved error handling in read_until_close.
  • Logging is less noisy when an SSL server is port scanned.
  • EINTR is now handled on all reads.

tornado.locale¶

  • tornado.locale.load_translations now accepts encodings other than UTF-8. UTF-16 and UTF-8
    will be detected automatically if a BOM is present; for other encodings load_translations
    has an encoding parameter.

tornado.locks¶

  • Lock and Semaphore now support the async with statement on Python 3.5.

tornado.log¶

  • A new time-based log rotation mode is available with --log_rotate_mode=time, 
    --log-rotate-when, and log-rotate-interval.

tornado.netutil¶

  • bind_sockets now supports SO_REUSEPORT with the reuse_port=True argument.

tornado.options¶

  • Dashes and underscores are now fully interchangeable in option names.

tornado.queues¶

  • Queue now supports the async for statement on Python 3.5.

tornado.simple_httpclient¶

  • When following redirects, streaming_callback and header_callback will no longer be run on
    the redirect responses (only the final non-redirect).
  • Responses containing both Content-Length and Transfer-Encoding will be treated as an error.

tornado.template¶

  • tornado.template.ParseError now includes the filename in addition to line number.
  • Whitespace handling has become more configurable. The Loader constructor now has a 
    whitespace argument, there is a new template_whitespace Application setting, and there is a
    new {% whitespace %} template directive. All of these options take a mode name defined in
    the tornado.template.filter_whitespace function. The default mode is single, which is the
    same behavior as prior versions of Tornado.
  • Non-ASCII filenames are now supported.

tornado.testing¶

  • ExpectLog objects now have a boolean logged_stack attribute to make it easier to test
    whether an exception stack trace was logged.

tornado.web¶

  • The hard limit of 4000 bytes per outgoing header has been removed.
  • StaticFileHandler returns the correct Content-Type for files with .gz, .bz2, and .xz
    extensions.
  • Responses smaller than 1000 bytes will no longer be compressed.
  • The default gzip compression level is now 6 (was 9).
  • Fixed a regression in Tornado 4.2.1 that broke StaticFileHandler with a path of /.
  • tornado.web.HTTPError is now copyable with the copy module.
  • The exception Finish now accepts an argument which will be passed to the method
    RequestHandler.finish.
  • New Application setting xsrf_cookie_kwargs can be used to set additional attributes such as 
    secure or httponly on the XSRF cookie.
  • Application.listen now returns the HTTPServer it created.

tornado.websocket¶

  • Fixed handling of continuation frames when compression is enabled.

What’s new in Tornado 4.2.1¶

Jul 17, 2015¶

Security fix¶

  • This release fixes a path traversal vulnerability in StaticFileHandler, in which files whose
    names started with the static_path directory but were not actually in that directory could
    be accessed.

What’s new in Tornado 4.2¶

May 26, 2015¶

Backwards-compatibility notes¶

  • SSLIOStream.connect and IOStream.start_tls now validate certificates by default.
  • Certificate validation will now use the system CA root certificates instead of certifi when
    possible (i.e. Python 2.7.9+ or 3.4+). This includes IOStream and simple_httpclient, but not
    curl_httpclient.
  • The default SSL configuration has become stricter, using ssl.create_default_context where
    available on the client side. (On the server side, applications are encouraged to migrate
    from the ssl_options dict-based API to pass an ssl.SSLContext instead).
  • The deprecated classes in the tornado.auth module, GoogleMixin, FacebookMixin, and 
    FriendFeedMixin have been removed.

New modules: tornado.locks and tornado.queues¶

These modules provide classes for coordinating coroutines, merged from Toro.

To port your code from Toro’s queues to Tornado 4.2, import Queue, PriorityQueue, or LifoQueue
from tornado.queues instead of from toro.

Use Queue instead of Toro’s JoinableQueue. In Tornado the methods join and task_done are
available on all queues, not on a special JoinableQueue.

Tornado queues raise exceptions specific to Tornado instead of reusing exceptions from the
Python standard library. Therefore instead of catching the standard queue.Empty exception from
Queue.get_nowait, catch the special tornado.queues.QueueEmpty exception, and instead of catching
the standard queue.Full from Queue.get_nowait, catch tornado.queues.QueueFull.

To port from Toro’s locks to Tornado 4.2, import Condition, Event, Semaphore, BoundedSemaphore,
or Lock from tornado.locks instead of from toro.

Toro’s Semaphore.wait allowed a coroutine to wait for the semaphore to be unlocked without
acquiring it. This encouraged unorthodox patterns; in Tornado, just use acquire.

Toro’s Event.wait raised a Timeout exception after a timeout. In Tornado, Event.wait raises
tornado.gen.TimeoutError.

Toro’s Condition.wait also raised Timeout, but in Tornado, the Future returned by Condition.wait
resolves to False after a timeout:

@gen.coroutine
def await_notification():
    if not (yield condition.wait(timeout=timedelta(seconds=1))):
        print('timed out')
    else:
        print('condition is true')

In lock and queue methods, wherever Toro accepted deadline as a keyword argument, Tornado names
the argument timeout instead.

Toro’s AsyncResult is not merged into Tornado, nor its exceptions NotReady and AlreadySet. Use a
Future instead. If you wrote code like this:

from tornado import gen
import toro

result = toro.AsyncResult()

@gen.coroutine
def setter():
    result.set(1)

@gen.coroutine
def getter():
    value = yield result.get()
    print(value)  # Prints "1".

Then the Tornado equivalent is:

from tornado import gen
from tornado.concurrent import Future

result = Future()

@gen.coroutine
def setter():
    result.set_result(1)

@gen.coroutine
def getter():
    value = yield result
    print(value)  # Prints "1".

tornado.autoreload¶

  • Improved compatibility with Windows.
  • Fixed a bug in Python 3 if a module was imported during a reload check.

tornado.concurrent¶

  • run_on_executor now accepts arguments to control which attributes it uses to find the IOLoop
    and executor.

tornado.curl_httpclient¶

  • Fixed a bug that would cause the client to stop processing requests if an exception occurred
    in certain places while there is a queue.

tornado.escape¶

  • xhtml_escape now supports numeric character references in hex format (&#x20;)

tornado.gen¶

  • WaitIterator no longer uses weak references, which fixes several garbage-collection-related
    bugs.
  • tornado.gen.Multi and tornado.gen.multi_future (which are used when yielding a list or dict
    in a coroutine) now log any exceptions after the first if more than one Future fails
    (previously they would be logged when the Future was garbage-collected, but this is more
    reliable). Both have a new keyword argument quiet_exceptions to suppress logging of certain
    exception types; to use this argument you must call Multi or multi_future directly instead
    of simply yielding a list.
  • multi_future now works when given multiple copies of the same Future.
  • On Python 3, catching an exception in a coroutine no longer leads to leaks via 
    Exception.__context__.

tornado.httpclient¶

  • The raise_error argument now works correctly with the synchronous HTTPClient.
  • The synchronous HTTPClient no longer interferes with IOLoop.current().

tornado.httpserver¶

  • HTTPServer is now a subclass of tornado.util.Configurable.

tornado.httputil¶

  • HTTPHeaders can now be copied with copy.copy and copy.deepcopy.

tornado.ioloop¶

  • The IOLoop constructor now has a make_current keyword argument to control whether the new
    IOLoop becomes IOLoop.current().
  • Third-party implementations of IOLoop should accept **kwargs in their initialize methods and
    pass them to the superclass implementation.
  • PeriodicCallback is now more efficient when the clock jumps forward by a large amount.

tornado.iostream¶

  • SSLIOStream.connect and IOStream.start_tls now validate certificates by default.
  • New method SSLIOStream.wait_for_handshake allows server-side applications to wait for the
    handshake to complete in order to verify client certificates or use NPN/ALPN.
  • The Future returned by SSLIOStream.connect now resolves after the handshake is complete
    instead of as soon as the TCP connection is established.
  • Reduced logging of SSL errors.
  • BaseIOStream.read_until_close now works correctly when a streaming_callback is given but 
    callback is None (i.e. when it returns a Future)

tornado.locale¶

  • New method GettextLocale.pgettext allows additional context to be supplied for gettext
    translations.

tornado.log¶

  • define_logging_options now works correctly when given a non-default options object.

tornado.process¶

  • New method Subprocess.wait_for_exit is a coroutine-friendly version of
    Subprocess.set_exit_callback.

tornado.simple_httpclient¶

  • Improved performance on Python 3 by reusing a single ssl.SSLContext.
  • New constructor argument max_body_size controls the maximum response size the client is
    willing to accept. It may be bigger than max_buffer_size if streaming_callback is used.

tornado.tcpserver¶

  • TCPServer.handle_stream may be a coroutine (so that any exceptions it raises will be
    logged).

tornado.util¶

  • import_object now supports unicode strings on Python 2.
  • Configurable.initialize now supports positional arguments.

tornado.web¶

  • Key versioning support for cookie signing. cookie_secret application setting can now contain
    a dict of valid keys with version as key. The current signing key then must be specified via
    key_version setting.
  • Parsing of the If-None-Match header now follows the RFC and supports weak validators.
  • Passing secure=False or httponly=False to RequestHandler.set_cookie now works as expected
    (previously only the presence of the argument was considered and its value was ignored).
  • RequestHandler.get_arguments now requires that its strip argument be of type bool. This
    helps prevent errors caused by the slightly dissimilar interfaces between the singular and
    plural methods.
  • Errors raised in _handle_request_exception are now logged more reliably.
  • RequestHandler.redirect now works correctly when called from a handler whose path begins
    with two slashes.
  • Passing messages containing % characters to tornado.web.HTTPError no longer causes broken
    error messages.

tornado.websocket¶

  • The on_close method will no longer be called more than once.
  • When the other side closes a connection, we now echo the received close code back instead of
    sending an empty close frame.

What’s new in Tornado 4.1¶

Feb 7, 2015¶

Highlights¶

  • If a Future contains an exception but that exception is never examined or re-raised (e.g. by
    yielding the Future), a stack trace will be logged when the Future is garbage-collected.
  • New class tornado.gen.WaitIterator provides a way to iterate over Futures in the order they
    resolve.
  • The tornado.websocket module now supports compression via the “permessage-deflate”
    extension. Override WebSocketHandler.get_compression_options to enable on the server side,
    and use the compression_options keyword argument to websocket_connect on the client side.
  • When the appropriate packages are installed, it is possible to yield asyncio.Future or
    Twisted Defered objects in Tornado coroutines.

Backwards-compatibility notes¶

  • HTTPServer now calls start_request with the correct arguments. This change is
    backwards-incompatible, afffecting any application which implemented
    HTTPServerConnectionDelegate by following the example of Application instead of the
    documented method signatures.

tornado.concurrent¶

  • If a Future contains an exception but that exception is never examined or re-raised (e.g. by
    yielding the Future), a stack trace will be logged when the Future is garbage-collected.
  • Future now catches and logs exceptions in its callbacks.

tornado.curl_httpclient¶

  • tornado.curl_httpclient now supports request bodies for PATCH and custom methods.
  • tornado.curl_httpclient now supports resubmitting bodies after following redirects for
    methods other than POST.
  • curl_httpclient now runs the streaming and header callbacks on the IOLoop.
  • tornado.curl_httpclient now uses its own logger for debug output so it can be filtered more
    easily.

tornado.gen¶

  • New class tornado.gen.WaitIterator provides a way to iterate over Futures in the order they
    resolve.
  • When the singledispatch library is available (standard on Python 3.4, available via pip 
    install singledispatch on older versions), the convert_yielded function can be used to make
    other kinds of objects yieldable in coroutines.
  • New function tornado.gen.sleep is a coroutine-friendly analogue to time.sleep.
  • gen.engine now correctly captures the stack context for its callbacks.

tornado.httpclient¶

  • tornado.httpclient.HTTPRequest accepts a new argument raise_error=False to suppress the
    default behavior of raising an error for non-200 response codes.

tornado.httpserver¶

  • HTTPServer now calls start_request with the correct arguments. This change is
    backwards-incompatible, afffecting any application which implemented
    HTTPServerConnectionDelegate by following the example of Application instead of the
    documented method signatures.
  • HTTPServer now tolerates extra newlines which are sometimes inserted between requests on
    keep-alive connections.
  • HTTPServer can now use keep-alive connections after a request with a chunked body.
  • HTTPServer now always reports HTTP/1.1 instead of echoing the request version.

tornado.httputil¶

  • New function tornado.httputil.split_host_and_port for parsing the netloc portion of URLs.
  • The context argument to HTTPServerRequest is now optional, and if a context is supplied the 
    remote_ip attribute is also optional.
  • HTTPServerRequest.body is now always a byte string (previously the default empty body would
    be a unicode string on python 3).
  • Header parsing now works correctly when newline-like unicode characters are present.
  • Header parsing again supports both CRLF and bare LF line separators.
  • Malformed multipart/form-data bodies will always be logged quietly instead of raising an
    unhandled exception; previously the behavior was inconsistent depending on the exact error.

tornado.ioloop¶

  • The kqueue and select IOLoop implementations now report writeability correctly, fixing flow
    control in IOStream.
  • When a new IOLoop is created, it automatically becomes “current” for the thread if there is
    not already a current instance.
  • New method PeriodicCallback.is_running can be used to see whether the PeriodicCallback has
    been started.

tornado.iostream¶

  • IOStream.start_tls now uses the server_hostname parameter for certificate validation.
  • SSLIOStream will no longer consume 100% CPU after certain error conditions.
  • SSLIOStream no longer logs EBADF errors during the handshake as they can result from nmap
    scans in certain modes.

tornado.options¶

  • parse_config_file now always decodes the config file as utf8 on Python 3.
  • tornado.options.define more accurately finds the module defining the option.

tornado.platform.asyncio¶

  • It is now possible to yield asyncio.Future objects in coroutines when the singledispatch
    library is available and tornado.platform.asyncio has been imported.
  • New methods tornado.platform.asyncio.to_tornado_future and to_asyncio_future convert between
    the two libraries’ Future classes.

tornado.platform.twisted¶

  • It is now possible to yield Deferred objects in coroutines when the singledispatch library
    is available and tornado.platform.twisted has been imported.

tornado.tcpclient¶

  • TCPClient will no longer raise an exception due to an ill-timed timeout.

tornado.tcpserver¶

  • TCPServer no longer ignores its read_chunk_size argument.

tornado.testing¶

  • AsyncTestCase has better support for multiple exceptions. Previously it would silently
    swallow all but the last; now it raises the first and logs all the rest.
  • AsyncTestCase now cleans up Subprocess state on tearDown when necessary.

tornado.web¶

  • The asynchronous decorator now understands concurrent.futures.Future in addition to
    tornado.concurrent.Future.
  • StaticFileHandler no longer logs a stack trace if the connection is closed while sending the
    file.
  • RequestHandler.send_error now supports a reason keyword argument, similar to
    tornado.web.HTTPError.
  • RequestHandler.locale now has a property setter.
  • Application.add_handlers hostname matching now works correctly with IPv6 literals.
  • Redirects for the Application default_host setting now match the request protocol instead of
    redirecting HTTPS to HTTP.
  • Malformed _xsrf cookies are now ignored instead of causing uncaught exceptions.
  • Application.start_request now has the same signature as
    HTTPServerConnectionDelegate.start_request.

tornado.websocket¶

  • The tornado.websocket module now supports compression via the “permessage-deflate”
    extension. Override WebSocketHandler.get_compression_options to enable on the server side,
    and use the compression_options keyword argument to websocket_connect on the client side.
  • WebSocketHandler no longer logs stack traces when the connection is closed.
  • WebSocketHandler.open now accepts *args, **kw for consistency with RequestHandler.get and
    related methods.
  • The Sec-WebSocket-Version header now includes all supported versions.
  • websocket_connect now has a on_message_callback keyword argument for callback-style use
    without read_message().

What’s new in Tornado 4.0.2¶

Sept 10, 2014¶

Bug fixes¶

  • Fixed a bug that could sometimes cause a timeout to fire after being cancelled.
  • AsyncTestCase once again passes along arguments to test methods, making it compatible with
    extensions such as Nose’s test generators.
  • StaticFileHandler can again compress its responses when gzip is enabled.
  • simple_httpclient passes its max_buffer_size argument to the underlying stream.
  • Fixed a reference cycle that can lead to increased memory consumption.
  • add_accept_handler will now limit the number of times it will call accept per IOLoop
    iteration, addressing a potential starvation issue.
  • Improved error handling in IOStream.connect (primarily for FreeBSD systems)

What’s new in Tornado 4.0.1¶

Aug 12, 2014¶

  • The build will now fall back to pure-python mode if the C extension fails to build for any
    reason (previously it would fall back for some errors but not others).
  • IOLoop.call_at and IOLoop.call_later now always return a timeout handle for use with
    IOLoop.remove_timeout.
  • If any callback of a PeriodicCallback or IOStream returns a Future, any error raised in that
    future will now be logged (similar to the behavior of IOLoop.add_callback).
  • Fixed an exception in client-side websocket connections when the connection is closed.
  • simple_httpclient once again correctly handles 204 status codes with no content-length
    header.
  • Fixed a regression in simple_httpclient that would result in timeouts for certain kinds of
    errors.

What’s new in Tornado 4.0¶

July 15, 2014¶

Highlights¶

  • The tornado.web.stream_request_body decorator allows large files to be uploaded with limited
    memory usage.
  • Coroutines are now faster and are used extensively throughout Tornado itself. More methods
    now return Futures, including most IOStream methods and RequestHandler.flush.
  • Many user-overridden methods are now allowed to return a Future for flow control.
  • HTTP-related code is now shared between the tornado.httpserver, tornado.simple_httpclient
    and tornado.wsgi modules, making support for features such as chunked and gzip encoding more
    consistent. HTTPServer now uses new delegate interfaces defined in tornado.httputil in
    addition to its old single-callback interface.
  • New module tornado.tcpclient creates TCP connections with non-blocking DNS, SSL handshaking,
    and support for IPv6.

Backwards-compatibility notes¶

  • tornado.concurrent.Future is no longer thread-safe; use concurrent.futures.Future when
    thread-safety is needed.
  • Tornado now depends on the certifi package instead of bundling its own copy of the Mozilla
    CA list. This will be installed automatically when using pip or easy_install.
  • This version includes the changes to the secure cookie format first introduced in version
    3.2.1, and the xsrf token change in version 3.2.2. If you are upgrading from an earlier
    version, see those versions’ release notes.
  • WebSocket connections from other origin sites are now rejected by default. To accept
    cross-origin websocket connections, override the new method WebSocketHandler.check_origin.
  • WebSocketHandler no longer supports the old draft 76 protocol (this mainly affects Safari
    5.x browsers). Applications should use non-websocket workarounds for these browsers.
  • Authors of alternative IOLoop implementations should see the changes to IOLoop.add_handler
    in this release.
  • The RequestHandler.async_callback and WebSocketHandler.async_callback wrapper functions have
    been removed; they have been obsolete for a long time due to stack contexts (and more
    recently coroutines).
  • curl_httpclient now requires a minimum of libcurl version 7.21.1 and pycurl 7.18.2.
  • Support for RequestHandler.get_error_html has been removed; override
    RequestHandler.write_error instead.

Other notes¶

  • The git repository has moved to https://github.com/tornadoweb/tornado. All old links should
    be redirected to the new location.
  • An announcement mailing list is now available.
  • All Tornado modules are now importable on Google App Engine (although the App Engine
    environment does not allow the system calls used by IOLoop so many modules are still
    unusable).

tornado.auth¶

  • Fixed a bug in .FacebookMixin on Python 3.
  • When using the Future interface, exceptions are more reliably delivered to the caller.

tornado.concurrent¶

  • tornado.concurrent.Future is now always thread-unsafe (previously it would be thread-safe if
    the concurrent.futures package was available). This improves performance and provides more
    consistent semantics. The parts of Tornado that accept Futures will accept both Tornado’s
    thread-unsafe Futures and the thread-safe concurrent.futures.Future.
  • tornado.concurrent.Future now includes all the functionality of the old TracebackFuture
    class. TracebackFuture is now simply an alias for Future.

tornado.curl_httpclient¶

  • curl_httpclient now passes along the HTTP “reason” string in response.reason.

tornado.gen¶

  • Performance of coroutines has been improved.
  • Coroutines no longer generate StackContexts by default, but they will be created on demand
    when needed.
  • The internals of the tornado.gen module have been rewritten to improve performance when
    using Futures, at the expense of some performance degradation for the older YieldPoint
    interfaces.
  • New function with_timeout wraps a Future and raises an exception if it doesn’t complete in a
    given amount of time.
  • New object moment can be yielded to allow the IOLoop to run for one iteration before
    resuming.
  • Task is now a function returning a Future instead of a YieldPoint subclass. This change
    should be transparent to application code, but allows Task to take advantage of the
    newly-optimized Future handling.

tornado.http1connection¶

  • New module contains the HTTP implementation shared by tornado.httpserver and 
    tornado.simple_httpclient.

tornado.httpclient¶

  • The command-line HTTP client (python -m tornado.httpclient $URL) now works on Python 3.
  • Fixed a memory leak in AsyncHTTPClient shutdown that affected applications that created many
    HTTP clients and IOLoops.
  • New client request parameter decompress_response replaces the existing use_gzip parameter;
    both names are accepted.

tornado.httpserver¶

  • tornado.httpserver.HTTPRequest has moved to tornado.httputil.HTTPServerRequest.
  • HTTP implementation has been unified with tornado.simple_httpclient in
    tornado.http1connection.
  • Now supports Transfer-Encoding: chunked for request bodies.
  • Now supports Content-Encoding: gzip for request bodies if decompress_request=True is passed
    to the HTTPServer constructor.
  • The connection attribute of HTTPServerRequest is now documented for public use; applications
    are expected to write their responses via the HTTPConnection interface.
  • The HTTPServerRequest.write and HTTPServerRequest.finish methods are now deprecated. (
    RequestHandler.write and RequestHandler.finish are not deprecated; this only applies to the
    methods on HTTPServerRequest)
  • HTTPServer now supports HTTPServerConnectionDelegate in addition to the old request_callback
    interface. The delegate interface supports streaming of request bodies.
  • HTTPServer now detects the error of an application sending a Content-Length error that is
    inconsistent with the actual content.
  • New constructor arguments max_header_size and max_body_size allow separate limits to be set
    for different parts of the request. max_body_size is applied even in streaming mode.
  • New constructor argument chunk_size can be used to limit the amount of data read into memory
    at one time per request.
  • New constructor arguments idle_connection_timeout and body_timeout allow time limits to be
    placed on the reading of requests.
  • Form-encoded message bodies are now parsed for all HTTP methods, not just POST, PUT, and 
    PATCH.

tornado.httputil¶

  • HTTPServerRequest was moved to this module from tornado.httpserver.
  • New base classes HTTPConnection, HTTPServerConnectionDelegate, and HTTPMessageDelegate
    define the interaction between applications and the HTTP implementation.

tornado.ioloop¶

  • IOLoop.add_handler and related methods now accept file-like objects in addition to raw file
    descriptors. Passing the objects is recommended (when possible) to avoid a
    garbage-collection-related problem in unit tests.
  • New method IOLoop.clear_instance makes it possible to uninstall the singleton instance.
  • Timeout scheduling is now more robust against slow callbacks.
  • IOLoop.add_timeout is now a bit more efficient.
  • When a function run by the IOLoop returns a Future and that Future has an exception, the
    IOLoop will log the exception.
  • New method IOLoop.spawn_callback simplifies the process of launching a fire-and-forget
    callback that is separated from the caller’s stack context.
  • New methods IOLoop.call_later and IOLoop.call_at simplify the specification of relative or
    absolute timeouts (as opposed to add_timeout, which used the type of its argument).

tornado.iostream¶

  • The callback argument to most IOStream methods is now optional. When called without a
    callback the method will return a Future for use with coroutines.
  • New method IOStream.start_tls converts an IOStream to an SSLIOStream.
  • No longer gets confused when an IOError or OSError without an errno attribute is raised.
  • BaseIOStream.read_bytes now accepts a partial keyword argument, which can be used to return
    before the full amount has been read. This is a more coroutine-friendly alternative to 
    streaming_callback.
  • BaseIOStream.read_until and read_until_regex now acept a max_bytes keyword argument which
    will cause the request to fail if it cannot be satisfied from the given number of bytes.
  • IOStream no longer reads from the socket into memory if it does not need data to satisfy a
    pending read. As a side effect, the close callback will not be run immediately if the other
    side closes the connection while there is unconsumed data in the buffer.
  • The default chunk_size has been increased to 64KB (from 4KB)
  • The IOStream constructor takes a new keyword argument max_write_buffer_size (defaults to
    unlimited). Calls to BaseIOStream.write will raise StreamBufferFullError if the amount of
    unsent buffered data exceeds this limit.
  • ETIMEDOUT errors are no longer logged. If you need to distinguish timeouts from other forms
    of closed connections, examine stream.error from a close callback.

tornado.netutil¶

  • When bind_sockets chooses a port automatically, it will now use the same port for IPv4 and
    IPv6.
  • TLS compression is now disabled by default on Python 3.3 and higher (it is not possible to
    change this option in older versions).

tornado.options¶

  • It is now possible to disable the default logging configuration by setting options.logging
    to None instead of the string "none".

tornado.platform.asyncio¶

  • Now works on Python 2.6.
  • Now works with Trollius version 0.3.

tornado.platform.twisted¶

  • TwistedIOLoop now works on Python 3.3+ (with Twisted 14.0.0+).

tornado.simple_httpclient¶

  • simple_httpclient has better support for IPv6, which is now enabled by default.
  • Improved default cipher suite selection (Python 2.7+).
  • HTTP implementation has been unified with tornado.httpserver in tornado.http1connection
  • Streaming request bodies are now supported via the body_producer keyword argument to
    tornado.httpclient.HTTPRequest.
  • The expect_100_continue keyword argument to tornado.httpclient.HTTPRequest allows the use of
    the HTTP Expect: 100-continue feature.
  • simple_httpclient now raises the original exception (e.g. an IOError) in more cases, instead
    of converting everything to HTTPError.

tornado.stack_context¶

  • The stack context system now has less performance overhead when no stack contexts are
    active.

tornado.tcpclient¶

  • New module which creates TCP connections and IOStreams, including name resolution,
    connecting, and SSL handshakes.

tornado.testing¶

  • AsyncTestCase now attempts to detect test methods that are generators but were not run with 
    @gen_test or any similar decorator (this would previously result in the test silently being
    skipped).
  • Better stack traces are now displayed when a test times out.
  • The @gen_test decorator now passes along *args, **kwargs so it can be used on functions with
    arguments.
  • Fixed the test suite when unittest2 is installed on Python 3.

tornado.web¶

  • It is now possible to support streaming request bodies with the stream_request_body
    decorator and the new RequestHandler.data_received method.
  • RequestHandler.flush now returns a Future if no callback is given.
  • New exception Finish may be raised to finish a request without triggering error handling.
  • When gzip support is enabled, all text/* mime types will be compressed, not just those on a
    whitelist.
  • Application now implements the HTTPMessageDelegate interface.
  • HEAD requests in StaticFileHandler no longer read the entire file.
  • StaticFileHandler now streams response bodies to the client.
  • New setting compress_response replaces the existing gzip setting; both names are accepted.
  • XSRF cookies that were not generated by this module (i.e. strings without any particular
    formatting) are once again accepted (as long as the cookie and body/header match). This
    pattern was common for testing and non-browser clients but was broken by the changes in
    Tornado 3.2.2.

tornado.websocket¶

  • WebSocket connections from other origin sites are now rejected by default. Browsers do not
    use the same-origin policy for WebSocket connections as they do for most other
    browser-initiated communications. This can be surprising and a security risk, so we disallow
    these connections on the server side by default. To accept cross-origin websocket
    connections, override the new method WebSocketHandler.check_origin.
  • WebSocketHandler.close and WebSocketClientConnection.close now support code and reason
    arguments to send a status code and message to the other side of the connection when
    closing. Both classes also have close_code and close_reason attributes to receive these
    values when the other side closes.
  • The C speedup module now builds correctly with MSVC, and can support messages larger than
    2GB on 64-bit systems.
  • The fallback mechanism for detecting a missing C compiler now works correctly on Mac OS X.
  • Arguments to WebSocketHandler.open are now decoded in the same way as arguments to
    RequestHandler.get and similar methods.
  • It is now allowed to override prepare in a WebSocketHandler, and this method may generate
    HTTP responses (error pages) in the usual way. The HTTP response methods are still not
    allowed once the WebSocket handshake has completed.

tornado.wsgi¶

  • New class WSGIAdapter supports running a Tornado Application on a WSGI server in a way that
    is more compatible with Tornado’s non-WSGI HTTPServer. WSGIApplication is deprecated in
    favor of using WSGIAdapter with a regular Application.
  • WSGIAdapter now supports gzipped output.

What’s new in Tornado 3.2.2¶

June 3, 2014¶

Security fixes¶

  • The XSRF token is now encoded with a random mask on each request. This makes it safe to
    include in compressed pages without being vulnerable to the BREACH attack. This applies to
    most applications that use both the xsrf_cookies and gzip options (or have gzip applied by a
    proxy).

Backwards-compatibility notes¶

  • If Tornado 3.2.2 is run at the same time as older versions on the same domain, there is some
    potential for issues with the differing cookie versions. The Application setting 
    xsrf_cookie_version=1 can be used for a transitional period to generate the older cookie
    format on newer servers.

Other changes¶

  • tornado.platform.asyncio is now compatible with trollius version 0.3.

What’s new in Tornado 3.2.1¶

May 5, 2014¶

Security fixes¶

  • The signed-value format used by RequestHandler.set_secure_cookie and
    RequestHandler.get_secure_cookie has changed to be more secure. This is a disruptive change.
    The secure_cookie functions take new version parameters to support transitions between
    cookie formats.
  • The new cookie format fixes a vulnerability that may be present in applications that use
    multiple cookies where the name of one cookie is a prefix of the name of another.
  • To minimize disruption, cookies in the older format will be accepted by default until they
    expire. Applications that may be vulnerable can reject all cookies in the older format by
    passing min_version=2 to RequestHandler.get_secure_cookie.
  • Thanks to Joost Pol of Certified Secure for reporting this issue.

Backwards-compatibility notes¶

  • Signed cookies issued by RequestHandler.set_secure_cookie in Tornado 3.2.1 cannot be read by
    older releases. If you need to run 3.2.1 in parallel with older releases, you can pass 
    version=1 to RequestHandler.set_secure_cookie to issue cookies that are backwards-compatible
    (but have a known weakness, so this option should only be used for a transitional period).

Other changes¶

  • The C extension used to speed up the websocket module now compiles correctly on Windows with
    MSVC and 64-bit mode. The fallback to the pure-Python alternative now works correctly on Mac
    OS X machines with no C compiler installed.

What’s new in Tornado 3.2¶

Jan 14, 2014¶

Installation¶

  • Tornado now depends on the backports.ssl_match_hostname when running on Python 2. This will
    be installed automatically when using pip or easy_install
  • Tornado now includes an optional C extension module, which greatly improves performance of
    websockets. This extension will be built automatically if a C compiler is found at install
    time.

New modules¶

  • The tornado.platform.asyncio module provides integration with the asyncio module introduced
    in Python 3.4 (also available for Python 3.3 with pip install asyncio).

tornado.auth¶

  • Added GoogleOAuth2Mixin support authentication to Google services with OAuth 2 instead of
    OpenID and OAuth 1.
  • FacebookGraphMixin has been updated to use the current Facebook login URL, which saves a
    redirect.

tornado.concurrent¶

  • TracebackFuture now accepts a timeout keyword argument (although it is still incorrect to
    use a non-zero timeout in non-blocking code).

tornado.curl_httpclient¶

  • tornado.curl_httpclient now works on Python 3 with the soon-to-be-released pycurl 7.19.3,
    which will officially support Python 3 for the first time. Note that there are some
    unofficial Python 3 ports of pycurl (Ubuntu has included one for its past several releases);
    these are not supported for use with Tornado.

tornado.escape¶

  • xhtml_escape now escapes apostrophes as well.
  • tornado.escape.utf8, to_unicode, and native_str now raise TypeError instead of
    AssertionError when given an invalid value.

tornado.gen¶

  • Coroutines may now yield dicts in addition to lists to wait for multiple tasks in parallel.
  • Improved performance of tornado.gen when yielding a Future that is already done.

tornado.httpclient¶

  • tornado.httpclient.HTTPRequest now uses property setters so that setting attributes after
    construction applies the same conversions as __init__ (e.g. converting the body attribute to
    bytes).

tornado.httpserver¶

  • Malformed x-www-form-urlencoded request bodies will now log a warning and continue instead
    of causing the request to fail (similar to the existing handling of malformed multipart/
    form-data bodies. This is done mainly because some libraries send this content type by
    default even when the data is not form-encoded.
  • Fix some error messages for unix sockets (and other non-IP sockets)

tornado.ioloop¶

  • IOLoop now uses handle_callback_exception consistently for error logging.
  • IOLoop now frees callback objects earlier, reducing memory usage while idle.
  • IOLoop will no longer call logging.basicConfig if there is a handler defined for the root
    logger or for the tornado or tornado.application loggers (previously it only looked at the
    root logger).

tornado.iostream¶

  • IOStream now recognizes ECONNABORTED error codes in more places (which was mainly an issue
    on Windows).
  • IOStream now frees memory earlier if a connection is closed while there is data in the write
    buffer.
  • PipeIOStream now handles EAGAIN error codes correctly.
  • SSLIOStream now initiates the SSL handshake automatically without waiting for the
    application to try and read or write to the connection.
  • Swallow a spurious exception from set_nodelay when a connection has been reset.

tornado.locale¶

  • Locale.format_date no longer forces the use of absolute dates in Russian.

tornado.log¶

  • Fix an error from tornado.log.enable_pretty_logging when sys.stderr does not have an isatty
    method.
  • tornado.log.LogFormatter now accepts keyword arguments fmt and datefmt.

tornado.netutil¶

  • is_valid_ip (and therefore HTTPRequest.remote_ip) now rejects empty strings.
  • Synchronously using ThreadedResolver at import time to resolve a unicode hostname no longer
    deadlocks.

tornado.platform.twisted¶

  • TwistedResolver now has better error handling.

tornado.process¶

  • Subprocess no longer leaks file descriptors if subprocess.Popen fails.

tornado.simple_httpclient¶

  • simple_httpclient now applies the connect_timeout to requests that are queued and have not
    yet started.
  • On Python 2.6, simple_httpclient now uses TLSv1 instead of SSLv3.
  • simple_httpclient now enforces the connect timeout during DNS resolution.
  • The embedded ca-certificates.crt file has been updated with the current Mozilla CA list.

tornado.web¶

  • StaticFileHandler no longer fails if the client requests a Range that is larger than the
    entire file (Facebook has a crawler that does this).
  • RequestHandler.on_connection_close now works correctly on subsequent requests of a
    keep-alive connection.
  • New application setting default_handler_class can be used to easily set up custom 404 pages.
  • New application settings autoreload, compiled_template_cache, static_hash_cache, and 
    serve_traceback can be used to control individual aspects of debug mode.
  • New methods RequestHandler.get_query_argument and RequestHandler.get_body_argument and new
    attributes HTTPRequest.query_arguments and HTTPRequest.body_arguments allow access to
    arguments without intermingling those from the query string with those from the request
    body.
  • RequestHandler.decode_argument and related methods now raise an HTTPError(400) instead of
    UnicodeDecodeError when the argument could not be decoded.
  • RequestHandler.clear_all_cookies now accepts domain and path arguments, just like
    clear_cookie.
  • It is now possible to specify handlers by name when using the URLSpec class.
  • Application now accepts 4-tuples to specify the name parameter (which previously required
    constructing a URLSpec object instead of a tuple).
  • Fixed an incorrect error message when handler methods return a value other than None or a
    Future.
  • Exceptions will no longer be logged twice when using both @asynchronous and @gen.coroutine

tornado.websocket¶

  • WebSocketHandler.write_message now raises WebSocketClosedError instead of AttributeError
    when the connection has been closed.
  • websocket_connect now accepts preconstructed HTTPRequest objects.
  • Fix a bug with WebSocketHandler when used with some proxies that unconditionally modify the 
    Connection header.
  • websocket_connect now returns an error immediately for refused connections instead of
    waiting for the timeout.
  • WebSocketClientConnection now has a close method.

tornado.wsgi¶

  • WSGIContainer now calls the iterable’s close() method even if an error is raised, in
    compliance with the spec.

What’s new in Tornado 3.1.1¶

Sep 1, 2013¶

  • StaticFileHandler no longer fails if the client requests a Range that is larger than the
    entire file (Facebook has a crawler that does this).
  • RequestHandler.on_connection_close now works correctly on subsequent requests of a
    keep-alive connection.

What’s new in Tornado 3.1¶

Jun 15, 2013¶

Multiple modules¶

  • Many reference cycles have been broken up throughout the package, allowing for more
    efficient garbage collection on CPython.
  • Silenced some log messages when connections are opened and immediately closed (i.e. port
    scans), or other situations related to closed connections.
  • Various small speedups: HTTPHeaders case normalization, UIModule proxy objects, precompile
    some regexes.

tornado.auth¶

  • OAuthMixin always sends oauth_version=1.0 in its request as required by the spec.
  • FacebookGraphMixin now uses self._FACEBOOK_BASE_URL in facebook_request to allow the base
    url to be overridden.
  • The authenticate_redirect and authorize_redirect methods in the tornado.auth mixin classes
    all now return Futures. These methods are asynchronous in OAuthMixin and derived classes,
    although they do not take a callback. The Future these methods return must be yielded if
    they are called from a function decorated with gen.coroutine (but not gen.engine).
  • TwitterMixin now uses /account/verify_credentials to get information about the logged-in
    user, which is more robust against changing screen names.
  • The demos directory (in the source distribution) has a new twitter demo using TwitterMixin.

tornado.escape¶

  • url_escape and url_unescape have a new plus argument (defaulting to True for consistency
    with the previous behavior) which specifies whether they work like urllib.parse.unquote or
    urllib.parse.unquote_plus.

tornado.gen¶

  • Fixed a potential memory leak with long chains of tornado.gen coroutines.

tornado.httpclient¶

  • tornado.httpclient.HTTPRequest takes a new argument auth_mode, which can be either basic or 
    digest. Digest authentication is only supported with tornado.curl_httpclient.
  • tornado.curl_httpclient no longer goes into an infinite loop when pycurl returns a negative
    timeout.
  • curl_httpclient now supports the PATCH and OPTIONS methods without the use of 
    allow_nonstandard_methods=True.
  • Worked around a class of bugs in libcurl that would result in errors from
    IOLoop.update_handler in various scenarios including digest authentication and socks
    proxies.
  • The TCP_NODELAY flag is now set when appropriate in simple_httpclient.
  • simple_httpclient no longer logs exceptions, since those exceptions are made available to
    the caller as HTTPResponse.error.

tornado.httpserver¶

  • tornado.httpserver.HTTPServer handles malformed HTTP headers more gracefully.
  • HTTPServer now supports lists of IPs in X-Forwarded-For (it chooses the last, i.e. nearest
    one).
  • Memory is now reclaimed promptly on CPython when an HTTP request fails because it exceeded
    the maximum upload size.
  • The TCP_NODELAY flag is now set when appropriate in HTTPServer.
  • The HTTPServer no_keep_alive option is now respected with HTTP 1.0 connections that
    explicitly pass Connection: keep-alive.
  • The Connection: keep-alive check for HTTP 1.0 connections is now case-insensitive.
  • The str and repr of tornado.httpserver.HTTPRequest no longer include the request body,
    reducing log spam on errors (and potential exposure/retention of private data).

tornado.httputil¶

  • The cache used in HTTPHeaders will no longer grow without bound.

tornado.ioloop¶

  • Some IOLoop implementations (such as pyzmq) accept objects other than integer file
    descriptors; these objects will now have their .close() method called when the IOLoop` is 
    closed with ``all_fds=True.
  • The stub handles left behind by IOLoop.remove_timeout will now get cleaned up instead of
    waiting to expire.

tornado.iostream¶

  • Fixed a bug in BaseIOStream.read_until_close that would sometimes cause data to be passed to
    the final callback instead of the streaming callback.
  • The IOStream close callback is now run more reliably if there is an exception in 
    _try_inline_read.
  • New method BaseIOStream.set_nodelay can be used to set the TCP_NODELAY flag.
  • Fixed a case where errors in SSLIOStream.connect (and SimpleAsyncHTTPClient) were not being
    reported correctly.

tornado.locale¶

  • Locale.format_date now works on Python 3.

tornado.netutil¶

  • The default Resolver implementation now works on Solaris.
  • Resolver now has a close method.
  • Fixed a potential CPU DoS when tornado.netutil.ssl_match_hostname is used on certificates
    with an abusive wildcard pattern.
  • All instances of ThreadedResolver now share a single thread pool, whose size is set by the
    first one to be created (or the static Resolver.configure method).
  • ExecutorResolver is now documented for public use.
  • bind_sockets now works in configurations with incomplete IPv6 support.

tornado.options¶

  • tornado.options.define with multiple=True now works on Python 3.
  • tornado.options.options and other OptionParser instances support some new dict-like methods:
    items(), iteration over keys, and (read-only) access to options with square braket syntax.
    OptionParser.group_dict returns all options with a given group name, and
    OptionParser.as_dict returns all options.

tornado.process¶

  • tornado.process.Subprocess no longer leaks file descriptors into the child process, which
    fixes a problem in which the child could not detect that the parent process had closed its
    stdin pipe.
  • Subprocess.set_exit_callback now works for subprocesses created without an explicit io_loop
    parameter.

tornado.stack_context¶

  • tornado.stack_context has been rewritten and is now much faster.
  • New function run_with_stack_context facilitates the use of stack contexts with coroutines.

tornado.tcpserver¶

  • The constructors of TCPServer and HTTPServer now take a max_buffer_size keyword argument.

tornado.template¶

  • Some internal names used by the template system have been changed; now all “reserved” names
    in templates start with _tt_.

tornado.testing¶

  • tornado.testing.AsyncTestCase.wait now raises the correct exception when it has been
    modified by tornado.stack_context.
  • tornado.testing.gen_test can now be called as @gen_test(timeout=60) to give some tests a
    longer timeout than others.
  • The environment variable ASYNC_TEST_TIMEOUT can now be set to override the default timeout
    for AsyncTestCase.wait and gen_test.
  • bind_unused_port now passes None instead of 0 as the port to getaddrinfo, which works better
    with some unusual network configurations.

tornado.util¶

  • tornado.util.import_object now works with top-level module names that do not contain a dot.
  • tornado.util.import_object now consistently raises ImportError instead of AttributeError
    when it fails.

tornado.web¶

  • The handlers list passed to the tornado.web.Application constructor and add_handlers methods
    can now contain lists in addition to tuples and URLSpec objects.
  • tornado.web.StaticFileHandler now works on Windows when the client passes an 
    If-Modified-Since timestamp before 1970.
  • New method RequestHandler.log_exception can be overridden to customize the logging behavior
    when an exception is uncaught. Most apps that currently override _handle_request_exception
    can now use a combination of RequestHandler.log_exception and write_error.
  • RequestHandler.get_argument now raises MissingArgumentError (a subclass of
    tornado.web.HTTPError, which is what it raised previously) if the argument cannot be found.
  • Application.reverse_url now uses url_escape with plus=False, i.e. spaces are encoded as %20
    instead of +.
  • Arguments extracted from the url path are now decoded with url_unescape with plus=False, so
    plus signs are left as-is instead of being turned into spaces.
  • RequestHandler.send_error will now only be called once per request, even if multiple
    exceptions are caught by the stack context.
  • The tornado.web.asynchronous decorator is no longer necessary for methods that return a
    Future (i.e. those that use the gen.coroutine or return_future decorators)
  • RequestHandler.prepare may now be asynchronous if it returns a Future. The asynchronous
    decorator is not used with prepare; one of the Future-related decorators should be used
    instead.
  • RequestHandler.current_user may now be assigned to normally.
  • RequestHandler.redirect no longer silently strips control characters and whitespace. It is
    now an error to pass control characters, newlines or tabs.
  • StaticFileHandler has been reorganized internally and now has additional extension points
    that can be overridden in subclasses.
  • StaticFileHandler now supports HTTP Range requests. StaticFileHandler is still not suitable
    for files too large to comfortably fit in memory, but Range support is necessary in some
    browsers to enable seeking of HTML5 audio and video.
  • StaticFileHandler now uses longer hashes by default, and uses the same hashes for Etag as it
    does for versioned urls.
  • StaticFileHandler.make_static_url and RequestHandler.static_url now have an additional
    keyword argument include_version to suppress the url versioning.
  • StaticFileHandler now reads its file in chunks, which will reduce memory fragmentation.
  • Fixed a problem with the Date header and cookie expiration dates when the system locale is
    set to a non-english configuration.

tornado.websocket¶

  • WebSocketHandler now catches StreamClosedError and runs on_close immediately instead of
    logging a stack trace.
  • New method WebSocketHandler.set_nodelay can be used to set the TCP_NODELAY flag.

tornado.wsgi¶

  • Fixed an exception in WSGIContainer when the connection is closed while output is being
    written.

What’s new in Tornado 3.0.2¶

Jun 2, 2013¶

  • tornado.auth.TwitterMixin now defaults to version 1.1 of the Twitter API, instead of version
    1.0 which is being discontinued on June 11. It also now uses HTTPS when talking to Twitter.
  • Fixed a potential memory leak with a long chain of gen.coroutine or gen.engine functions.

What’s new in Tornado 3.0.1¶

Apr 8, 2013¶

  • The interface of tornado.auth.FacebookGraphMixin is now consistent with its documentation
    and the rest of the module. The get_authenticated_user and facebook_request methods return a
    Future and the callback argument is optional.
  • The tornado.testing.gen_test decorator will no longer be recognized as a (broken) test by 
    nose.
  • Work around a bug in Ubuntu 13.04 betas involving an incomplete backport of the
    ssl.match_hostname function.
  • tornado.websocket.websocket_connect now fails cleanly when it attempts to connect to a
    non-websocket url.
  • tornado.testing.LogTrapTestCase once again works with byte strings on Python 2.
  • The request attribute of tornado.httpclient.HTTPResponse is now always an HTTPRequest, never
    a _RequestProxy.
  • Exceptions raised by the tornado.gen module now have better messages when tuples are used as
    callback keys.

What’s new in Tornado 3.0¶

Mar 29, 2013¶

Highlights¶

  • The callback argument to many asynchronous methods is now optional, and these methods return
    a Future. The tornado.gen module now understands Futures, and these methods can be used
    directly without a gen.Task wrapper.
  • New function IOLoop.current returns the IOLoop that is running on the current thread (as
    opposed to IOLoop.instance, which returns a specific thread’s (usually the main thread’s)
    IOLoop.
  • New class tornado.netutil.Resolver provides an asynchronous interface to DNS resolution. The
    default implementation is still blocking, but non-blocking implementations are available
    using one of three optional dependencies: ThreadedResolver using the concurrent.futures
    thread pool, tornado.platform.caresresolver.CaresResolver using the pycares library, or 
    tornado.platform.twisted.TwistedResolver using twisted
  • Tornado’s logging is now less noisy, and it no longer goes directly to the root logger,
    allowing for finer-grained configuration.
  • New class tornado.process.Subprocess wraps subprocess.Popen with PipeIOStream access to the
    child’s file descriptors.
  • IOLoop now has a static configure method like the one on AsyncHTTPClient, which can be used
    to select an IOLoop implementation other than the default.
  • IOLoop can now optionally use a monotonic clock if available (see below for more details).

Backwards-incompatible changes¶

  • Python 2.5 is no longer supported. Python 3 is now supported in a single codebase instead of
    using 2to3
  • The tornado.database module has been removed. It is now available as a separate package,
    torndb
  • Functions that take an io_loop parameter now default to IOLoop.current() instead of
    IOLoop.instance().
  • Empty HTTP request arguments are no longer ignored. This applies to HTTPRequest.arguments
    and RequestHandler.get_argument[s] in WSGI and non-WSGI modes.
  • On Python 3, tornado.escape.json_encode no longer accepts byte strings.
  • On Python 3, the get_authenticated_user methods in tornado.auth now return character strings
    instead of byte strings.
  • tornado.netutil.TCPServer has moved to its own module, tornado.tcpserver.
  • The Tornado test suite now requires unittest2 when run on Python 2.6.
  • tornado.options.options is no longer a subclass of dict; attribute-style access is now
    required.

Detailed changes by module¶

Multiple modules¶

  • Tornado no longer logs to the root logger. Details on the new logging scheme can be found
    under the tornado.log module. Note that in some cases this will require that you add an
    explicit logging configuration in order to see any output (perhaps just calling 
    logging.basicConfig()), although both IOLoop.start() and tornado.options.parse_command_line
    will do this for you.
  • On python 3.2+, methods that take an ssl_options argument (on SSLIOStream, TCPServer, and
    HTTPServer) now accept either a dictionary of options or an ssl.SSLContext object.
  • New optional dependency on concurrent.futures to provide better support for working with
    threads. concurrent.futures is in the standard library for Python 3.2+, and can be installed
    on older versions with pip install futures.

tornado.autoreload¶

  • tornado.autoreload is now more reliable when there are errors at import time.
  • Calling tornado.autoreload.start (or creating an Application with debug=True) twice on the
    same IOLoop now does nothing (instead of creating multiple periodic callbacks). Starting
    autoreload on more than one IOLoop in the same process now logs a warning.
  • Scripts run by autoreload no longer inherit __future__ imports used by Tornado.

tornado.auth¶

  • On Python 3, the get_authenticated_user method family now returns character strings instead
    of byte strings.
  • Asynchronous methods defined in tornado.auth now return a Future, and their callback
    argument is optional. The Future interface is preferred as it offers better error handling
    (the previous interface just logged a warning and returned None).
  • The tornado.auth mixin classes now define a method get_auth_http_client, which can be
    overridden to use a non-default AsyncHTTPClient instance (e.g. to use a different IOLoop)
  • Subclasses of OAuthMixin are encouraged to override OAuthMixin._oauth_get_user_future
    instead of _oauth_get_user, although both methods are still supported.

tornado.concurrent¶

  • New module tornado.concurrent contains code to support working with concurrent.futures, or
    to emulate future-based interface when that module is not available.

tornado.curl_httpclient¶

  • Preliminary support for tornado.curl_httpclient on Python 3. The latest official release of
    pycurl only supports Python 2, but Ubuntu has a port available in 12.10 (apt-get install 
    python3-pycurl). This port currently has bugs that prevent it from handling arbitrary binary
    data but it should work for textual (utf8) resources.
  • Fix a crash with libcurl 7.29.0 if a curl object is created and closed without being used.

tornado.escape¶

  • On Python 3, json_encode no longer accepts byte strings. This mirrors the behavior of the
    underlying json module. Python 2 behavior is unchanged but should be faster.

tornado.gen¶

  • New decorator @gen.coroutine is available as an alternative to @gen.engine. It automatically
    returns a Future, and within the function instead of calling a callback you return a value
    with raise gen.Return(value) (or simply return value in Python 3.3).
  • Generators may now yield Future objects.
  • Callbacks produced by gen.Callback and gen.Task are now automatically stack-context-wrapped,
    to minimize the risk of context leaks when used with asynchronous functions that don’t do
    their own wrapping.
  • Fixed a memory leak involving generators, RequestHandler.flush, and clients closing
    connections while output is being written.
  • Yielding a large list no longer has quadratic performance.

tornado.httpclient¶

  • AsyncHTTPClient.fetch now returns a Future and its callback argument is optional. When the
    future interface is used, any error will be raised automatically, as if HTTPResponse.rethrow
    was called.
  • AsyncHTTPClient.configure and all AsyncHTTPClient constructors now take a defaults keyword
    argument. This argument should be a dictionary, and its values will be used in place of
    corresponding attributes of HTTPRequest that are not set.
  • All unset attributes of tornado.httpclient.HTTPRequest are now None. The default values of
    some attributes (connect_timeout, request_timeout, follow_redirects, max_redirects, use_gzip
    , proxy_password, allow_nonstandard_methods, and validate_cert have been moved from
    HTTPRequest to the client implementations.
  • The max_clients argument to AsyncHTTPClient is now a keyword-only argument.
  • Keyword arguments to AsyncHTTPClient.configure are no longer used when instantiating an
    implementation subclass directly.
  • Secondary AsyncHTTPClient callbacks (streaming_callback, header_callback, and 
    prepare_curl_callback) now respect StackContext.

tornado.httpserver¶

  • HTTPServer no longer logs an error when it is unable to read a second request from an HTTP
    1.1 keep-alive connection.
  • HTTPServer now takes a protocol keyword argument which can be set to https if the server is
    behind an SSL-decoding proxy that does not set any supported X-headers.
  • tornado.httpserver.HTTPConnection now has a set_close_callback method that should be used
    instead of reaching into its stream attribute.
  • Empty HTTP request arguments are no longer ignored. This applies to HTTPRequest.arguments
    and RequestHandler.get_argument[s] in WSGI and non-WSGI modes.

tornado.ioloop¶

  • New function IOLoop.current returns the IOLoop that is running on the current thread (as
    opposed to IOLoop.instance, which returns a specific thread’s (usually the main thread’s)
    IOLoop).
  • New method IOLoop.add_future to run a callback on the IOLoop when an asynchronous Future
    finishes.
  • IOLoop now has a static configure method like the one on AsyncHTTPClient, which can be used
    to select an IOLoop implementation other than the default.
  • The IOLoop poller implementations (select, epoll, kqueue) are now available as distinct
    subclasses of IOLoop. Instantiating IOLoop will continue to automatically choose the best
    available implementation.
  • The IOLoop constructor has a new keyword argument time_func, which can be used to set the
    time function used when scheduling callbacks. This is most useful with the time.monotonic
    function, introduced in Python 3.3 and backported to older versions via the monotime module.
    Using a monotonic clock here avoids problems when the system clock is changed.
  • New function IOLoop.time returns the current time according to the IOLoop. To use the new
    monotonic clock functionality, all calls to IOLoop.add_timeout must be either pass a
    datetime.timedelta or a time relative to IOLoop.time, not time.time. (time.time will
    continue to work only as long as the IOLoop’s time_func argument is not used).
  • New convenience method IOLoop.run_sync can be used to start an IOLoop just long enough to
    run a single coroutine.
  • New method IOLoop.add_callback_from_signal is safe to use in a signal handler (the regular
    add_callback method may deadlock).
  • IOLoop now uses signal.set_wakeup_fd where available (Python 2.6+ on Unix) to avoid a race
    condition that could result in Python signal handlers being delayed.
  • Method IOLoop.running() has been removed.
  • IOLoop has been refactored to better support subclassing.
  • IOLoop.add_callback and add_callback_from_signal now take *args, **kwargs to pass along to
    the callback.

tornado.iostream¶

  • IOStream.connect now has an optional server_hostname argument which will be used for SSL
    certificate validation when applicable. Additionally, when supported (on Python 3.2+), this
    hostname will be sent via SNI (and this is supported by tornado.simple_httpclient)
  • Much of IOStream has been refactored into a separate class BaseIOStream.
  • New class tornado.iostream.PipeIOStream provides the IOStream interface on pipe file
    descriptors.
  • IOStream now raises a new exception tornado.iostream.StreamClosedError when you attempt to
    read or write after the stream has been closed (by either side).
  • IOStream now simply closes the connection when it gets an ECONNRESET error, rather than
    logging it as an error.
  • IOStream.error no longer picks up unrelated exceptions.
  • BaseIOStream.close now has an exc_info argument (similar to the one used in the logging
    module) that can be used to set the stream’s error attribute when closing it.
  • BaseIOStream.read_until_close now works correctly when it is called while there is buffered
    data.
  • Fixed a major performance regression when run on PyPy (introduced in Tornado 2.3).

tornado.log¶

  • New module containing enable_pretty_logging and LogFormatter, moved from the options module.
  • LogFormatter now handles non-ascii data in messages and tracebacks better.

tornado.netutil¶

  • New class tornado.netutil.Resolver provides an asynchronous interface to DNS resolution. The
    default implementation is still blocking, but non-blocking implementations are available
    using one of three optional dependencies: ThreadedResolver using the concurrent.futures
    thread pool, tornado.platform.caresresolver.CaresResolver using the pycares library, or
    tornado.platform.twisted.TwistedResolver using twisted
  • New function tornado.netutil.is_valid_ip returns true if a given string is a valid IP (v4 or
    v6) address.
  • tornado.netutil.bind_sockets has a new flags argument that can be used to pass additional
    flags to getaddrinfo.
  • tornado.netutil.bind_sockets no longer sets AI_ADDRCONFIG; this will cause it to bind to
    both ipv4 and ipv6 more often than before.
  • tornado.netutil.bind_sockets now works when Python was compiled with --disable-ipv6 but IPv6
    DNS resolution is available on the system.
  • tornado.netutil.TCPServer has moved to its own module, tornado.tcpserver.

tornado.options¶

  • The class underlying the functions in tornado.options is now public (
    tornado.options.OptionParser). This can be used to create multiple independent option sets,
    such as for subcommands.
  • tornado.options.parse_config_file now configures logging automatically by default, in the
    same way that parse_command_line does.
  • New function tornado.options.add_parse_callback schedules a callback to be run after the
    command line or config file has been parsed. The keyword argument final=False can be used on
    either parsing function to supress these callbacks.
  • tornado.options.define now takes a callback argument. This callback will be run with the new
    value whenever the option is changed. This is especially useful for options that set other
    options, such as by reading from a config file.
  • tornado.options.parse_command_line --help output now goes to stderr rather than stdout.
  • tornado.options.options is no longer a subclass of dict; attribute-style access is now
    required.
  • tornado.options.options (and OptionParser instances generally) now have a mockable() method
    that returns a wrapper object compatible with mock.patch.
  • Function tornado.options.enable_pretty_logging has been moved to the tornado.log module.

tornado.platform.caresresolver¶

  • New module containing an asynchronous implementation of the Resolver interface, using the 
    pycares library.

tornado.platform.twisted¶

  • New class tornado.platform.twisted.TwistedIOLoop allows Tornado code to be run on the
    Twisted reactor (as opposed to the existing TornadoReactor, which bridges the gap in the
    other direction).
  • New class tornado.platform.twisted.TwistedResolver is an asynchronous implementation of the
    Resolver interface.

tornado.process¶

  • New class tornado.process.Subprocess wraps subprocess.Popen with PipeIOStream access to the
    child’s file descriptors.

tornado.simple_httpclient¶

  • SimpleAsyncHTTPClient now takes a resolver keyword argument (which may be passed to either
    the constructor or configure), to allow it to use the new non-blocking
    tornado.netutil.Resolver.
  • When following redirects, SimpleAsyncHTTPClient now treats a 302 response code the same as a
    303. This is contrary to the HTTP spec but consistent with all browsers and other major HTTP
    clients (including CurlAsyncHTTPClient).
  • The behavior of header_callback with SimpleAsyncHTTPClient has changed and is now the same
    as that of CurlAsyncHTTPClient. The header callback now receives the first line of the
    response (e.g. HTTP/1.0 200 OK) and the final empty line.
  • tornado.simple_httpclient now accepts responses with a 304 status code that include a 
    Content-Length header.
  • Fixed a bug in which SimpleAsyncHTTPClient callbacks were being run in the client’s 
    stack_context.

tornado.stack_context¶

  • stack_context.wrap now runs the wrapped callback in a more consistent environment by
    recreating contexts even if they already exist on the stack.
  • Fixed a bug in which stack contexts could leak from one callback chain to another.
  • Yield statements inside a with statement can cause stack contexts to become inconsistent; an
    exception will now be raised when this case is detected.

tornado.template¶

  • Errors while rendering templates no longer log the generated code, since the enhanced stack
    traces (from version 2.1) should make this unnecessary.
  • The {% apply %} directive now works properly with functions that return both unicode strings
    and byte strings (previously only byte strings were supported).
  • Code in templates is no longer affected by Tornado’s __future__ imports (which previously
    included absolute_import and division).

tornado.testing¶

  • New function tornado.testing.bind_unused_port both chooses a port and binds a socket to it,
    so there is no risk of another process using the same port. get_unused_port is now
    deprecated.
  • New decorator tornado.testing.gen_test can be used to allow for yielding tornado.gen objects
    in tests, as an alternative to the stop and wait methods of AsyncTestCase.
  • tornado.testing.AsyncTestCase and friends now extend unittest2.TestCase when it is available
    (and continue to use the standard unittest module when unittest2 is not available)
  • tornado.testing.ExpectLog can be used as a finer-grained alternative to
    tornado.testing.LogTrapTestCase
  • The command-line interface to tornado.testing.main now supports additional arguments from
    the underlying unittest module: verbose, quiet, failfast, catch, buffer.
  • The deprecated --autoreload option of tornado.testing.main has been removed. Use python -m 
    tornado.autoreload as a prefix command instead.
  • The --httpclient option of tornado.testing.main has been moved to tornado.test.runtests so
    as not to pollute the application option namespace. The tornado.options module’s new
    callback support now makes it easy to add options from a wrapper script instead of putting
    all possible options in tornado.testing.main.
  • AsyncHTTPTestCase no longer calls AsyncHTTPClient.close for tests that use the singleton
    IOLoop.instance.
  • LogTrapTestCase no longer fails when run in unknown logging configurations. This allows
    tests to be run under nose, which does its own log buffering (LogTrapTestCase doesn’t do
    anything useful in this case, but at least it doesn’t break things any more).

tornado.util¶

  • tornado.util.b (which was only intended for internal use) is gone.

tornado.web¶

  • RequestHandler.set_header now overwrites previous header values case-insensitively.
  • tornado.web.RequestHandler has new attributes path_args and path_kwargs, which contain the
    positional and keyword arguments that are passed to the get/post/etc method. These
    attributes are set before those methods are called, so they are available during prepare()
  • tornado.web.ErrorHandler no longer requires XSRF tokens on POST requests, so posts to an
    unknown url will always return 404 instead of complaining about XSRF tokens.
  • Several methods related to HTTP status codes now take a reason keyword argument to specify
    an alternate “reason” string (i.e. the “Not Found” in “HTTP/1.1 404 Not Found”). It is now
    possible to set status codes other than those defined in the spec, as long as a reason
    string is given.
  • The Date HTTP header is now set by default on all responses.
  • Etag/If-None-Match requests now work with StaticFileHandler.
  • StaticFileHandler no longer sets Cache-Control: public unnecessarily.
  • When gzip is enabled in a tornado.web.Application, appropriate Vary: Accept-Encoding headers
    are now sent.
  • It is no longer necessary to pass all handlers for a host in a single
    Application.add_handlers call. Now the request will be matched against the handlers for any 
    host_pattern that includes the request’s Host header.

tornado.websocket¶

  • Client-side WebSocket support is now available: tornado.websocket.websocket_connect
  • WebSocketHandler has new methods ping and on_pong to send pings to the browser (not
    supported on the draft76 protocol)

What’s new in Tornado 2.4.1¶

Nov 24, 2012¶

Bug fixes¶

  • Fixed a memory leak in tornado.stack_context that was especially likely with long-running 
    @gen.engine functions.
  • tornado.auth.TwitterMixin now works on Python 3.
  • Fixed a bug in which IOStream.read_until_close with a streaming callback would sometimes
    pass the last chunk of data to the final callback instead of the streaming callback.

What’s new in Tornado 2.4¶

Sep 4, 2012¶

General¶

  • Fixed Python 3 bugs in tornado.auth, tornado.locale, and tornado.wsgi.

HTTP clients¶

  • Removed max_simultaneous_connections argument from tornado.httpclient (both
    implementations). This argument hasn’t been useful for some time (if you were using it you
    probably want max_clients instead)
  • tornado.simple_httpclient now accepts and ignores HTTP 1xx status responses.

tornado.ioloop and tornado.iostream¶

  • Fixed a bug introduced in 2.3 that would cause IOStream close callbacks to not run if there
    were pending reads.
  • Improved error handling in SSLIOStream and SSL-enabled TCPServer.
  • SSLIOStream.get_ssl_certificate now has a binary_form argument which is passed to 
    SSLSocket.getpeercert.
  • SSLIOStream.write can now be called while the connection is in progress, same as non-SSL
    IOStream (but be careful not to send sensitive data until the connection has completed and
    the certificate has been verified).
  • IOLoop.add_handler cannot be called more than once with the same file descriptor. This was
    always true for epoll, but now the other implementations enforce it too.
  • On Windows, TCPServer uses SO_EXCLUSIVEADDRUSER instead of SO_REUSEADDR.

tornado.template¶

  • {% break %} and {% continue %} can now be used looping constructs in templates.
  • It is no longer an error for an if/else/for/etc block in a template to have an empty body.

tornado.testing¶

  • New class tornado.testing.AsyncHTTPSTestCase is like AsyncHTTPTestCase. but enables SSL for
    the testing server (by default using a self-signed testing certificate).
  • tornado.testing.main now accepts additional keyword arguments and forwards them to
    unittest.main.

tornado.web¶

  • New method RequestHandler.get_template_namespace can be overridden to add additional
    variables without modifying keyword arguments to render_string.
  • RequestHandler.add_header now works with WSGIApplication.
  • RequestHandler.get_secure_cookie now handles a potential error case.
  • RequestHandler.__init__ now calls super().__init__ to ensure that all constructors are
    called when multiple inheritance is used.
  • Docs have been updated with a description of all available Application settings

Other modules¶

  • OAuthMixin now accepts "oob" as a callback_uri.
  • OpenIdMixin now also returns the claimed_id field for the user.
  • tornado.platform.twisted shutdown sequence is now more compatible.
  • The logging configuration used in tornado.options is now more tolerant of non-ascii byte
    strings.

What’s new in Tornado 2.3¶

May 31, 2012¶

HTTP clients¶

  • tornado.httpclient.HTTPClient now supports the same constructor keyword arguments as
    AsyncHTTPClient.
  • The max_clients keyword argument to AsyncHTTPClient.configure now works.
  • tornado.simple_httpclient now supports the OPTIONS and PATCH HTTP methods.
  • tornado.simple_httpclient is better about closing its sockets instead of leaving them for
    garbage collection.
  • tornado.simple_httpclient correctly verifies SSL certificates for URLs containing IPv6
    literals (This bug affected Python 2.5 and 2.6).
  • tornado.simple_httpclient no longer includes basic auth credentials in the Host header when
    those credentials are extracted from the URL.
  • tornado.simple_httpclient no longer modifies the caller-supplied header dictionary, which
    caused problems when following redirects.
  • tornado.curl_httpclient now supports client SSL certificates (using the same client_cert and
    client_key arguments as tornado.simple_httpclient)

HTTP Server¶

  • HTTPServer now works correctly with paths starting with //
  • HTTPHeaders.copy (inherited from dict.copy) now works correctly.
  • HTTPConnection.address is now always the socket address, even for non-IP sockets. 
    HTTPRequest.remote_ip is still always an IP-style address (fake data is used for non-IP
    sockets)
  • Extra data at the end of multipart form bodies is now ignored, which fixes a compatibility
    problem with an iOS HTTP client library.

IOLoop and IOStream¶

  • IOStream now has an error attribute that can be used to determine why a socket was closed.
  • tornado.iostream.IOStream.read_until and read_until_regex are much faster with large input.
  • IOStream.write performs better when given very large strings.
  • IOLoop.instance() is now thread-safe.

tornado.options¶

  • tornado.options options with multiple=True that are set more than once now overwrite rather
    than append. This makes it possible to override values set in parse_config_file with 
    parse_command_line.
  • tornado.options --help output is now prettier.
  • tornado.options.options now supports attribute assignment.

tornado.template¶

  • Template files containing non-ASCII (utf8) characters now work on Python 3 regardless of the
    locale environment variables.
  • Templates now support else clauses in try/except/finally/else blocks.

tornado.web¶

  • tornado.web.RequestHandler now supports the PATCH HTTP method. Note that this means any
    existing methods named patch in RequestHandler subclasses will need to be renamed.
  • tornado.web.addslash and removeslash decorators now send permanent redirects (301) instead
    of temporary (302).
  • RequestHandler.flush now invokes its callback whether there was any data to flush or not.
  • Repeated calls to RequestHandler.set_cookie with the same name now overwrite the previous
    cookie instead of producing additional copies.
  • tornado.web.OutputTransform.transform_first_chunk now takes and returns a status code in
    addition to the headers and chunk. This is a backwards-incompatible change to an interface
    that was never technically private, but was not included in the documentation and does not
    appear to have been used outside Tornado itself.
  • Fixed a bug on python versions before 2.6.5 when URLSpec regexes are constructed from
    unicode strings and keyword arguments are extracted.
  • The reverse_url function in the template namespace now comes from the RequestHandler rather
    than the Application. (Unless overridden, RequestHandler.reverse_url is just an alias for
    the Application method).
  • The Etag header is now returned on 304 responses to an If-None-Match request, improving
    compatibility with some caches.
  • tornado.web will no longer produce responses with status code 304 that also have entity
    headers such as Content-Length.

Other modules¶

  • tornado.auth.FacebookGraphMixin no longer sends post_args redundantly in the url.
  • The extra_params argument to tornado.escape.linkify may now be a callable, to allow
    parameters to be chosen separately for each link.
  • tornado.gen no longer leaks StackContexts when a @gen.engine wrapped function is called
    repeatedly.
  • tornado.locale.get_supported_locales no longer takes a meaningless cls argument.
  • StackContext instances now have a deactivation callback that can be used to prevent further
    propagation.
  • tornado.testing.AsyncTestCase.wait now resets its timeout on each call.
  • tornado.wsgi.WSGIApplication now parses arguments correctly on Python 3.
  • Exception handling on Python 3 has been improved; previously some exceptions such as
    UnicodeDecodeError would generate TypeErrors

What’s new in Tornado 2.2.1¶

Apr 23, 2012¶

Security fixes¶

  • tornado.web.RequestHandler.set_header now properly sanitizes input values to protect against
    header injection, response splitting, etc. (it has always attempted to do this, but the
    check was incorrect). Note that redirects, the most likely source of such bugs, are
    protected by a separate check in RequestHandler.redirect.

Bug fixes¶

  • Colored logging configuration in tornado.options is compatible with Python 3.2.3 (and 3.3).

What’s new in Tornado 2.2¶

Jan 30, 2012¶

Highlights¶

  • Updated and expanded WebSocket support.
  • Improved compatibility in the Twisted/Tornado bridge.
  • Template errors now generate better stack traces.
  • Better exception handling in tornado.gen.

Security fixes¶

  • tornado.simple_httpclient now disables SSLv2 in all cases. Previously SSLv2 would be allowed
    if the Python interpreter was linked against a pre-1.0 version of OpenSSL.

Backwards-incompatible changes¶

  • tornado.process.fork_processes now raises SystemExit if all child processes exit cleanly
    rather than returning None. The old behavior was surprising and inconsistent with most of
    the documented examples of this function (which did not check the return value).
  • On Python 2.6, tornado.simple_httpclient only supports SSLv3. This is because Python 2.6
    does not expose a way to support both SSLv3 and TLSv1 without also supporting the insecure
    SSLv2.
  • tornado.websocket no longer supports the older “draft 76” version of the websocket protocol
    by default, although this version can be enabled by overriding 
    tornado.websocket.WebSocketHandler.allow_draft76.

tornado.httpclient¶

  • SimpleAsyncHTTPClient no longer hangs on HEAD requests, responses with no content, or empty 
    POST/PUT response bodies.
  • SimpleAsyncHTTPClient now supports 303 and 307 redirect codes.
  • tornado.curl_httpclient now accepts non-integer timeouts.
  • tornado.curl_httpclient now supports basic authentication with an empty password.

tornado.httpserver¶

  • HTTPServer with xheaders=True will no longer accept X-Real-IP headers that don’t look like
    valid IP addresses.
  • HTTPServer now treats the Connection request header as case-insensitive.

tornado.ioloop and tornado.iostream¶

  • IOStream.write now works correctly when given an empty string.
  • IOStream.read_until (and read_until_regex) now perform better when there is a lot of
    buffered data, which improves peformance of SimpleAsyncHTTPClient when downloading files
    with lots of chunks.
  • SSLIOStream now works correctly when ssl_version is set to a value other than SSLv23.
  • Idle IOLoops no longer wake up several times a second.
  • tornado.ioloop.PeriodicCallback no longer triggers duplicate callbacks when stopped and
    started repeatedly.

tornado.template¶

  • Exceptions in template code will now show better stack traces that reference lines from the
    original template file.
  • {# and #} can now be used for comments (and unlike the old {% comment %} directive, these
    can wrap other template directives).
  • Template directives may now span multiple lines.

tornado.web¶

  • Now behaves better when given malformed Cookie headers
  • RequestHandler.redirect now has a status argument to send status codes other than 301 and
    302.
  • New method RequestHandler.on_finish may be overridden for post-request processing (as a
    counterpart to RequestHandler.prepare)
  • StaticFileHandler now outputs Content-Length and Etag headers on HEAD requests.
  • StaticFileHandler now has overridable get_version and parse_url_path methods for use in
    subclasses.
  • RequestHandler.static_url now takes an include_host parameter (in addition to the old
    support for the RequestHandler.include_host attribute).

tornado.websocket¶

  • Updated to support the latest version of the protocol, as finalized in RFC 6455.
  • Many bugs were fixed in all supported protocol versions.
  • tornado.websocket no longer supports the older “draft 76” version of the websocket protocol
    by default, although this version can be enabled by overriding 
    tornado.websocket.WebSocketHandler.allow_draft76.
  • WebSocketHandler.write_message now accepts a binary argument to send binary messages.
  • Subprotocols (i.e. the Sec-WebSocket-Protocol header) are now supported; see the
    WebSocketHandler.select_subprotocol method for details.
  • .WebSocketHandler.get_websocket_scheme can be used to select the appropriate url scheme (ws:
    // or wss://) in cases where HTTPRequest.protocol is not set correctly.

Other modules¶

  • tornado.auth.TwitterMixin.authenticate_redirect now takes a callback_uri parameter.
  • tornado.auth.TwitterMixin.twitter_request now accepts both URLs and partial paths (complete
    URLs are useful for the search API which follows different patterns).
  • Exception handling in tornado.gen has been improved. It is now possible to catch exceptions
    thrown by a Task.
  • tornado.netutil.bind_sockets now works when getaddrinfo returns duplicate addresses.
  • tornado.platform.twisted compatibility has been significantly improved. Twisted version
    11.1.0 is now supported in addition to 11.0.0.
  • tornado.process.fork_processes correctly reseeds the random module even when os.urandom is
    not implemented.
  • tornado.testing.main supports a new flag --exception_on_interrupt, which can be set to false
    to make Ctrl-C kill the process more reliably (at the expense of stack traces when it does
    so).
  • tornado.version_info is now a four-tuple so official releases can be distinguished from
    development branches.

What’s new in Tornado 2.1.1¶

Oct 4, 2011¶

Bug fixes¶

  • Fixed handling of closed connections with the epoll (i.e. Linux) IOLoop. Previously, closed
    connections could be shut down too early, which most often manifested as “Stream is closed”
    exceptions in SimpleAsyncHTTPClient.
  • Fixed a case in which chunked responses could be closed prematurely, leading to truncated
    output.
  • IOStream.connect now reports errors more consistently via logging and the close callback
    (this affects e.g. connections to localhost on FreeBSD).
  • IOStream.read_bytes again accepts both int and long arguments.
  • PeriodicCallback no longer runs repeatedly when IOLoop iterations complete faster than the
    resolution of time.time() (mainly a problem on Windows).

Backwards-compatibility note¶

  • Listening for IOLoop.ERROR alone is no longer sufficient for detecting closed connections on
    an otherwise unused socket. IOLoop.ERROR must always be used in combination with READ or 
    WRITE.

What’s new in Tornado 2.1¶

Sep 20, 2011¶

Backwards-incompatible changes¶

  • Support for secure cookies written by pre-1.0 releases of Tornado has been removed. The
    RequestHandler.get_secure_cookie method no longer takes an include_name parameter.
  • The debug application setting now causes stack traces to be displayed in the browser on
    uncaught exceptions. Since this may leak sensitive information, debug mode is not
    recommended for public-facing servers.

Security fixes¶

  • Diginotar has been removed from the default CA certificates file used by 
    SimpleAsyncHTTPClient.

New modules¶

  • tornado.gen: A generator-based interface to simplify writing asynchronous functions.
  • tornado.netutil: Parts of tornado.httpserver have been extracted into a new module for use
    with non-HTTP protocols.
  • tornado.platform.twisted: A bridge between the Tornado IOLoop and the Twisted Reactor,
    allowing code written for Twisted to be run on Tornado.
  • tornado.process: Multi-process mode has been improved, and can now restart crashed child
    processes. A new entry point has been added at tornado.process.fork_processes, although 
    tornado.httpserver.HTTPServer.start is still supported.

tornado.web¶

  • tornado.web.RequestHandler.write_error replaces get_error_html as the preferred way to
    generate custom error pages (get_error_html is still supported, but deprecated)
  • In tornado.web.Application, handlers may be specified by (fully-qualified) name instead of
    importing and passing the class object itself.
  • It is now possible to use a custom subclass of StaticFileHandler with the 
    static_handler_class application setting, and this subclass can override the behavior of the
    static_url method.
  • StaticFileHandler subclasses can now override get_cache_time to customize cache control
    behavior.
  • tornado.web.RequestHandler.get_secure_cookie now has a max_age_days parameter to allow
    applications to override the default one-month expiration.
  • set_cookie now accepts a max_age keyword argument to set the max-age cookie attribute (note
    underscore vs dash)
  • tornado.web.RequestHandler.set_default_headers may be overridden to set headers in a way
    that does not get reset during error handling.
  • RequestHandler.add_header can now be used to set a header that can appear multiple times in
    the response.
  • RequestHandler.flush can now take a callback for flow control.
  • The application/json content type can now be gzipped.
  • The cookie-signing functions are now accessible as static functions 
    tornado.web.create_signed_value and tornado.web.decode_signed_value.

tornado.httpserver¶

  • To facilitate some advanced multi-process scenarios, HTTPServer has a new method add_sockets
    , and socket-opening code is available separately as tornado.netutil.bind_sockets.
  • The cookies property is now available on tornado.httpserver.HTTPRequest (it is also
    available in its old location as a property of RequestHandler)
  • tornado.httpserver.HTTPServer.bind now takes a backlog argument with the same meaning as 
    socket.listen.
  • HTTPServer can now be run on a unix socket as well as TCP.
  • Fixed exception at startup when socket.AI_ADDRCONFIG is not available, as on Windows XP

IOLoop and IOStream¶

  • IOStream performance has been improved, especially for small synchronous requests.
  • New methods tornado.iostream.IOStream.read_until_close and 
    tornado.iostream.IOStream.read_until_regex.
  • IOStream.read_bytes and IOStream.read_until_close now take a streaming_callback argument to
    return data as it is received rather than all at once.
  • IOLoop.add_timeout now accepts datetime.timedelta objects in addition to absolute
    timestamps.
  • PeriodicCallback now sticks to the specified period instead of creeping later due to
    accumulated errors.
  • tornado.ioloop.IOLoop and tornado.httpclient.HTTPClient now have close() methods that should
    be used in applications that create and destroy many of these objects.
  • IOLoop.install can now be used to use a custom subclass of IOLoop as the singleton without
    monkey-patching.
  • IOStream should now always call the close callback instead of the connect callback on a
    connection error.
  • The IOStream close callback will no longer be called while there are pending read callbacks
    that can be satisfied with buffered data.

tornado.simple_httpclient¶

  • Now supports client SSL certificates with the client_key and client_cert parameters to
    tornado.httpclient.HTTPRequest
  • Now takes a maximum buffer size, to allow reading files larger than 100MB
  • Now works with HTTP 1.0 servers that don’t send a Content-Length header
  • The allow_nonstandard_methods flag on HTTP client requests now permits methods other than 
    POST and PUT to contain bodies.
  • Fixed file descriptor leaks and multiple callback invocations in SimpleAsyncHTTPClient
  • No longer consumes extra connection resources when following redirects.
  • Now works with buggy web servers that separate headers with \n instead of \r\n\r\n.
  • Now sets response.request_time correctly.
  • Connect timeouts now work correctly.

Other modules¶

  • tornado.auth.OpenIdMixin now uses the correct realm when the callback URI is on a different
    domain.
  • tornado.autoreload has a new command-line interface which can be used to wrap any script.
    This replaces the --autoreload argument to tornado.testing.main and is more robust against
    syntax errors.
  • tornado.autoreload.watch can be used to watch files other than the sources of imported
    modules.
  • tornado.database.Connection has new variants of execute and executemany that return the
    number of rows affected instead of the last inserted row id.
  • tornado.locale.load_translations now accepts any properly-formatted locale name, not just
    those in the predefined LOCALE_NAMES list.
  • tornado.options.define now takes a group parameter to group options in --help output.
  • Template loaders now take a namespace constructor argument to add entries to the template
    namespace.
  • tornado.websocket now supports the latest (“hybi-10”) version of the protocol (the old
    version, “hixie-76” is still supported; the correct version is detected automatically).
  • tornado.websocket now works on Python 3

Bug fixes¶

  • Windows support has been improved. Windows is still not an officially supported platform,
    but the test suite now passes and tornado.autoreload works.
  • Uploading files whose names contain special characters will now work.
  • Cookie values containing special characters are now properly quoted and unquoted.
  • Multi-line headers are now supported.
  • Repeated Content-Length headers (which may be added by certain proxies) are now supported in
    HTTPServer.
  • Unicode string literals now work in template expressions.
  • The template {% module %} directive now works even if applications use a template variable
    named modules.
  • Requests with “Expect: 100-continue” now work on python 3

What’s new in Tornado 2.0¶

Jun 21, 2011¶

Major changes:
* Template output is automatically escaped by default; see backwards
  compatibility note below.
* The default AsyncHTTPClient implementation is now simple_httpclient.
* Python 3.2 is now supported.

Backwards compatibility:
* Template autoescaping is enabled by default.  Applications upgrading from
  a previous release of Tornado must either disable autoescaping or adapt
  their templates to work with it.  For most applications, the simplest
  way to do this is to pass autoescape=None to the Application constructor.
  Note that this affects certain built-in methods, e.g. xsrf_form_html
  and linkify, which must now be called with {% raw %} instead of {}
* Applications that wish to continue using curl_httpclient instead of
  simple_httpclient may do so by calling
    AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
  at the beginning of the process.  Users of Python 2.5 will probably want
  to use curl_httpclient as simple_httpclient only supports ssl on Python 2.6+.
* Python 3 compatibility involved many changes throughout the codebase,
  so users are encouraged to test their applications more thoroughly than
  usual when upgrading to this release.

Other changes in this release:
* Templates support several new directives:
  - {% autoescape ...%} to control escaping behavior
  - {% raw ... %} for unescaped output
  - {% module ... %} for calling UIModules
* {% module Template(path, **kwargs) %} may now be used to call another
  template with an independent namespace
* All IOStream callbacks are now run directly on the IOLoop via add_callback.
* HTTPServer now supports IPv6 where available.  To disable, pass
  family=socket.AF_INET to HTTPServer.bind().
* HTTPClient now supports IPv6, configurable via allow_ipv6=bool on the
  HTTPRequest.  allow_ipv6 defaults to false on simple_httpclient and true
  on curl_httpclient.
* RequestHandlers can use an encoding other than utf-8 for query parameters
  by overriding decode_argument()
* Performance improvements, especially for applications that use a lot of
  IOLoop timeouts
* HTTP OPTIONS method no longer requires an XSRF token.
* JSON output (RequestHandler.write(dict)) now sets Content-Type to
  application/json
* Etag computation can now be customized or disabled by overriding
  RequestHandler.compute_etag
* USE_SIMPLE_HTTPCLIENT environment variable is no longer supported.
  Use AsyncHTTPClient.configure instead.

What’s new in Tornado 1.2.1¶

Mar 3, 2011¶

We are pleased to announce the release of Tornado 1.2.1, available from
https://github.com/downloads/facebook/tornado/tornado-1.2.1.tar.gz

This release contains only two small changes relative to version 1.2:
* FacebookGraphMixin has been updated to work with a recent change to the
  Facebook API.
* Running "setup.py install" will no longer attempt to automatically
  install pycurl.  This wasn't working well on platforms where the best way
  to install pycurl is via something like apt-get instead of easy_install.

This is an important upgrade if you are using FacebookGraphMixin, but
otherwise it can be safely ignored.

What’s new in Tornado 1.2¶

Feb 20, 2011¶

We are pleased to announce the release of Tornado 1.2, available from
https://github.com/downloads/facebook/tornado/tornado-1.2.tar.gz

Backwards compatibility notes:
* This release includes the backwards-incompatible security change from
  version 1.1.1.  Users upgrading from 1.1 or earlier should read the
  release notes from that release:
  http://groups.google.com/group/python-tornado/browse_thread/thread/b36191c781580cde
* StackContexts that do something other than catch exceptions may need to
  be modified to be reentrant.
  https://github.com/tornadoweb/tornado/commit/7a7e24143e77481d140fb5579bc67e4c45cbcfad
* When XSRF tokens are used, the token must also be present on PUT and
  DELETE requests (anything but GET and HEAD)

New features:
* A new HTTP client implementation is available in the module
  tornado.simple_httpclient.  This HTTP client does not depend on pycurl.
  It has not yet been tested extensively in production, but is intended
  to eventually replace the pycurl-based HTTP client in a future release of
  Tornado.  To transparently replace tornado.httpclient.AsyncHTTPClient with
  this new implementation, you can set the environment variable
  USE_SIMPLE_HTTPCLIENT=1 (note that the next release of Tornado will
  likely include a different way to select HTTP client implementations)
* Request logging is now done by the Application rather than the
  RequestHandler.  Logging behavior may be customized by either overriding
  Application.log_request in a subclass or by passing log_function
  as an Application setting
* Application.listen(port): Convenience method as an alternative to
  explicitly creating an HTTPServer
* tornado.escape.linkify(): Wrap urls in <a> tags
* RequestHandler.create_signed_value(): Create signatures like the
  secure_cookie methods without setting cookies.
* tornado.testing.get_unused_port(): Returns a port selected in the same
  way as inAsyncHTTPTestCase
* AsyncHTTPTestCase.fetch(): Convenience method for synchronous fetches
* IOLoop.set_blocking_signal_threshold(): Set a callback to be run when
  the IOLoop is blocked.
* IOStream.connect(): Asynchronously connect a client socket
* AsyncHTTPClient.handle_callback_exception(): May be overridden
  in subclass for custom error handling
* httpclient.HTTPRequest has two new keyword arguments, validate_cert and
  ca_certs. Setting validate_cert=False will disable all certificate checks
  when fetching https urls.  ca_certs may be set to a filename containing
  trusted certificate authorities (defaults will be used if this is
  unspecified)
* HTTPRequest.get_ssl_certificate(): Returns the client's SSL certificate
  (if client certificates were requested in the server's ssl_options
* StaticFileHandler can be configured to return a default file (e.g.
  index.html) when a directory is requested
* Template directives of the form "{% from x import y %}" are now
  supported (in addition to the existing support for "{% import x
  %}"
* FacebookGraphMixin.get_authenticated_user now accepts a new
  parameter 'extra_fields' which may be used to request additional
  information about the user

Bug fixes:
* auth: Fixed KeyError with Facebook offline_access
* auth: Uses request.uri instead of request.path as the default redirect
  so that parameters are preserved.
* escape: xhtml_escape() now returns a unicode string, not
  utf8-encoded bytes
* ioloop: Callbacks added with add_callback are now run in the order they
  were added
* ioloop: PeriodicCallback.stop can now be called from inside the callback.
* iostream: Fixed several bugs in SSLIOStream
* iostream: Detect when the other side has closed the connection even with
  the select()-based IOLoop
* iostream: read_bytes(0) now works as expected
* iostream: Fixed bug when writing large amounts of data on windows
* iostream: Fixed infinite loop that could occur with unhandled exceptions
* httpclient: Fix bugs when some requests use proxies and others don't
* httpserver: HTTPRequest.protocol is now set correctly when using the
  built-in SSL support
* httpserver: When using multiple processes, the standard library's
  random number generator is re-seeded in each child process
* httpserver: With xheaders enabled, X-Forwarded-Proto is supported as an
  alternative to X-Scheme
* httpserver: Fixed bugs in multipart/form-data parsing
* locale: format_date() now behaves sanely with dates in the future
* locale: Updates to the language list
* stack_context: Fixed bug with contexts leaking through reused IOStreams
* stack_context: Simplified semantics and improved performance
* web: The order of css_files from UIModules is now preserved
* web: Fixed error with default_host redirect
* web: StaticFileHandler works when os.path.sep != '/' (i.e. on Windows)
* web: Fixed a caching-related bug in StaticFileHandler when a file's
  timestamp has changed but its contents have not.
* web: Fixed bugs with HEAD requests and e.g. Etag headers
* web: Fix bugs when different handlers have different static_paths
* web: @removeslash will no longer cause a redirect loop when applied to the
  root path
* websocket: Now works over SSL
* websocket: Improved compatibility with proxies

Many thanks to everyone who contributed patches, bug reports, and feedback
that went into this release!

-Ben

What’s new in Tornado 1.1.1¶

Feb 8, 2011¶

Tornado 1.1.1 is a BACKWARDS-INCOMPATIBLE security update that fixes an
XSRF vulnerability.  It is available at
https://github.com/downloads/facebook/tornado/tornado-1.1.1.tar.gz

This is a backwards-incompatible change.  Applications that previously
relied on a blanket exception for XMLHTTPRequest may need to be modified
to explicitly include the XSRF token when making ajax requests.

The tornado chat demo application demonstrates one way of adding this
token (specifically the function postJSON in demos/chat/static/chat.js).

More information about this change and its justification can be found at
http://www.djangoproject.com/weblog/2011/feb/08/security/
http://weblog.rubyonrails.org/2011/2/8/csrf-protection-bypass-in-ruby-on-rails

What’s new in Tornado 1.1¶

Sep 7, 2010¶

We are pleased to announce the release of Tornado 1.1, available from
https://github.com/downloads/facebook/tornado/tornado-1.1.tar.gz

Changes in this release:
* RequestHandler.async_callback and related functions in other classes
  are no longer needed in most cases (although it's harmless to continue
  using them).  Uncaught exceptions will now cause the request to be closed
  even in a callback.  If you're curious how this works, see the new
  tornado.stack_context module.
* The new tornado.testing module contains support for unit testing
  asynchronous IOLoop-based code.
* AsyncHTTPClient has been rewritten (the new implementation was
  available as AsyncHTTPClient2 in Tornado 1.0; both names are
  supported for backwards compatibility).
* The tornado.auth module has had a number of updates, including support
  for OAuth 2.0 and the Facebook Graph API, and upgrading Twitter and
  Google support to OAuth 1.0a.
* The websocket module is back and supports the latest version (76) of the
  websocket protocol.  Note that this module's interface is different
  from the websocket module that appeared in pre-1.0 versions of Tornado.
* New method RequestHandler.initialize() can be overridden in subclasses
  to simplify handling arguments from URLSpecs.  The sequence of methods
  called during initialization is documented at
  http://tornadoweb.org/documentation#overriding-requesthandler-methods
* get_argument() and related methods now work on PUT requests in addition
  to POST.
* The httpclient module now supports HTTP proxies.
* When HTTPServer is run in SSL mode, the SSL handshake is now non-blocking.
* Many smaller bug fixes and documentation updates

Backwards-compatibility notes:
* While most users of Tornado should not have to deal with the stack_context
  module directly, users of worker thread pools and similar constructs may
  need to use stack_context.wrap and/or NullContext to avoid memory leaks.
* The new AsyncHTTPClient still works with libcurl version 7.16.x, but it
  performs better when both libcurl and pycurl are at least version 7.18.2.
* OAuth transactions started under previous versions of the auth module
  cannot be completed under the new module.  This applies only to the
  initial authorization process; once an authorized token is issued that
  token works with either version.

Many thanks to everyone who contributed patches, bug reports, and feedback
that went into this release!

-Ben

What’s new in Tornado 1.0.1¶

Aug 13, 2010¶

This release fixes a bug with RequestHandler.get_secure_cookie, which would
in some circumstances allow an attacker to tamper with data stored in the
cookie.

What’s new in Tornado 1.0¶

July 22, 2010¶

We are pleased to announce the release of Tornado 1.0, available
from
https://github.com/downloads/facebook/tornado/tornado-1.0.tar.gz.
There have been many changes since version 0.2; here are some of
the highlights:

New features:
* Improved support for running other WSGI applications in a
  Tornado server (tested with Django and CherryPy)
* Improved performance on Mac OS X and BSD (kqueue-based IOLoop),
  and experimental support for win32
* Rewritten AsyncHTTPClient available as
  tornado.httpclient.AsyncHTTPClient2 (this will become the
  default in a future release)
* Support for standard .mo files in addition to .csv in the locale
  module
* Pre-forking support for running multiple Tornado processes at
  once (see HTTPServer.start())
* SSL and gzip support in HTTPServer
* reverse_url() function refers to urls from the Application
  config by name from templates and RequestHandlers
* RequestHandler.on_connection_close() callback is called when the
  client has closed the connection (subject to limitations of the
  underlying network stack, any proxies, etc)
* Static files can now be served somewhere other than /static/ via
  the static_url_prefix application setting
* URL regexes can now use named groups ("(?P<name>)") to pass
  arguments to get()/post() via keyword instead of position
* HTTP header dictionary-like objects now support multiple values
  for the same header via the get_all() and add() methods.
* Several new options in the httpclient module, including
  prepare_curl_callback and header_callback
* Improved logging configuration in tornado.options.
* UIModule.html_body() can be used to return html to be inserted
  at the end of the document body.

Backwards-incompatible changes:
* RequestHandler.get_error_html() now receives the exception
  object as a keyword argument if the error was caused by an
  uncaught exception.
* Secure cookies are now more secure, but incompatible with
  cookies set by Tornado 0.2.  To read cookies set by older
  versions of Tornado, pass include_name=False to
  RequestHandler.get_secure_cookie()
* Parameters passed to RequestHandler.get/post() by extraction
  from the path now have %-escapes decoded, for consistency with
  the processing that was already done with other query
  parameters.

Many thanks to everyone who contributed patches, bug reports, and
feedback that went into this release!

-Ben

  • 索引
  • 模块索引
  • 搜索页面

讨论和支持¶

你可以讨论Tornado在 Tornado 开发者邮件列表, 报告bug在 GitHub issue tracker.

其他资源可以在 Tornado wiki 上找到. 新版本会宣布在 announcements mailing list.

Tornado is available under the Apache License, Version 2.0.

This web site and all documentation is licensed under Creative Commons 3.0.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

© Copyright 2009-2017, The Tornado Authors. Revision 14f4412a.

Built with Sphinx using a theme provided by Read the Docs.
Read the Docs v: latest

Versions
    latest

Downloads
    htmlzip
    epub

On Read the Docs
    Project Home
    Builds

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Free document hosting provided by Read the Docs.
