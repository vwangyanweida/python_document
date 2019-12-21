并发执行
********

本章中描述的模块支持并发执行代码。 适当的工具选择取决于要执行的任务（
CPU密集型或IO密集型）和偏好的开发风格（事件驱动的协作式多任务或抢占式
多任务处理）。 这是一个概述：

* "threading" --- 基于线程的并行

  * 线程本地数据

  * 线程对象

  * 锁对象

  * 递归锁对象

  * 条件对象

  * 信号量对象

    * "Semaphore" 例子

  * 事件对象

  * 定时器对象

  * 栅栏对象

  * 在 "with" 语句中使用锁、条件和信号量

* "multiprocessing" --- 基于进程的并行

  * 概述

    * "Process" 类

    * 上下文和启动方法

    * 在进程之间交换对象

    * 进程间同步

    * 进程间共享状态

    * 使用工作进程

  * 参考

    * "Process" 和异常

    * 管道和队列

    * 杂项

    * 连接（Connection）对象

    * 同步原语

    * 共享 "ctypes" 对象

      * "multiprocessing.sharedctypes" 模块

    * 管理器

      * 自定义管理器

      * 使用远程管理器

    * 代理对象

      * 清理

    * 进程池

    * 监听者及客户端

      * 地址格式

    * 认证密码

    * 日志

    * "multiprocessing.dummy" 模块

  * 编程指导

    * 所有start方法

    * *spawn* 和 *forkserver* 启动方式

  * 示例

* "multiprocessing.shared_memory" --- 可从进程直接访问的共享内存

* "concurrent" 包

* "concurrent.futures" --- 启动并行任务

  * 执行器对象

  * ThreadPoolExecutor

    * ThreadPoolExecutor 例子

  * ProcessPoolExecutor

    * ProcessPoolExecutor 例子

  * 期程对象

  * 模块函数

  * Exception类

* "subprocess" --- 子进程管理

  * 使用 "subprocess" 模块

    * 常用参数

    * Popen 构造函数

    * 异常

  * 安全考量

  * Popen 对象

  * Windows Popen 助手

    * Windows 常数

  * Older high-level API

  * Replacing Older Functions with the "subprocess" Module

    * Replacing **/bin/sh** shell command substitution

    * Replacing shell pipeline

    * Replacing "os.system()"

    * Replacing the "os.spawn" family

    * Replacing "os.popen()", "os.popen2()", "os.popen3()"

    * Replacing functions from the "popen2" module

  * Legacy Shell Invocation Functions

  * 注释

    * Converting an argument sequence to a string on Windows

* "sched" --- 事件调度器

  * 调度器对象

* "queue" --- 一个同步的队列类

  * Queue对象

  * SimpleQueue 对象

以下是上述某些服务的支持模块：

* "_thread" --- 底层多线程 API

* "_dummy_thread" --- "_thread" 的替代模块

* "dummy_threading" ---  可直接替代 "threading" 模块。
