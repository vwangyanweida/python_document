
<!-- vim-markdown-toc GFM -->

	* [logging]
* [Logger 对象]
* [日志级别]
* [处理器对象]
* [Formatter Objects]
* [Filter Objects]
* [LogRecord Objects]
* [LogRecord 属性]
* [LoggerAdapter 对象]
* [线程安全]
* [模块级别函数]
* [模块级属性]
* [Integration with the warnings module]

<!-- vim-markdown-toc -->

## logging
> "logging" --- Python 的日志记录工具

1. 	- *源代码：** Lib/logging/__init__.py

2. 此页面仅包含 API 参考信息。教程信息和更多高级用法的讨论，请参阅

	- 基础教程

	- 进阶教程

	- 日志操作手册

3. 这个模块为**应用与库定义了实现灵活的事件日志系统的函数与类**.

4. **使用标准库提提供的 logging API 最主要的好处是，所有的 Python 模块都可
能参与日志输出，包括你的日志消息和第三方模块的日志消息**。

5. 这个模块提供许多强大而灵活的功能。如果你对 logging 不太熟悉的话， 掌握
它最好的方式就是查看它对应的教程（详见右侧的链接）。

6. 该模块定义的基础类和函数都列在下面。

	- 记录器暴露了应用程序代码直接使用的接口。

	- 处理程序将日志记录（由记录器创建）发送到适当的目标。

	- 过滤器提供了更精细的设施，用于确定要输出的日志记录。

	- 格式化程序指定最终输出中日志记录的样式。


Logger 对象
===========

Loggers 有以下的属性和方法。注意 	- 永远* 不要直接实例化 Loggers，应当通
过模块级别的函数 "logging.getLogger(name)" 。多次使用相同的名字调用
"getLogger()" 会一直返回相同的 Logger 对象的引用。

"name" 是潜在的周期分割层级值, 像``foo.bar.baz`` (例如, 抛出的可以只是
明文的``foo``)。Loggers是进一步在子层次列表的更高loggers列表。例如，有
个名叫``foo``的logger，名叫``foo.bar``，"foo.bar.baz"，和 "foo.bam" 都
是 "foo``的衍生logger。logger的名字分级类似Python 包的层级，并且相同的
如果你组织你的loggers在每模块级别基本上使用推荐的结构
``logging.getLogger(__name__)"。这是因为在模块里，在Python包的命名空间
的模块名为``__name__``。

class logging.Logger

   propagate

      如果这个属性为真，记录到这个记录器的事件将会传递给这个高级别处理
      器的记录器（原型），此外任何关联到这个记录器的处理器。消息会直接
      传递给原型记录器的处理器 - 既不是这个原型记录器的级别也不是过滤
      器是在考虑的问题。

      如果等于假，记录消息将不会传递给这个原型记录器的处理器。

      构造器将这个属性初始化为 "True"。

      注解: 如果你关联了一个处理器	- 并且*到它自己的一个或多个记录器，
        它可能 发出多次相同的记录。总体来说，你不需要关联处理器到一个
        或多个记 录器 - 如果你只是关联它到一个合适的记录器等级中的最高
        级别记录 器，它将会看到子记录器所有记录的事件，他们的传播剩下
        的设置为 ``True``。一个常见的场景是只关联处理器到根记录器，并
        且让传播照 顾剩下的。

   setLevel(level)

      给 logger 设置阈值为 	- level* 。日志等级小于 *level* 会被忽略。严
      重性为 	- level* 或更高的日志消息将由该 logger 的任何一个或多个
      handler 发出，除非将处理程序的级别设置为比 	- level* 更高的级别。

      创建一个 logger 时，设置级别为 "NOTSET"  （当 logger 是根 logger
      时，将处理所有消息；当 logger 是非根 logger 时，所有消息会委派给
      父级）。注意根 logger 创建时使用的是 "WARNING" 级别。

      委派给父级的意思是如果一个 logger 的级别设置为 NOTSET，遍历其祖
      先 logger，直到找到另一个不是 NOTSET 级别的 logger，或者到根
      logger 为止。

      If an ancestor is found with a level other than NOTSET, then
      that ancestor's level is treated as the effective level of the
      logger where the ancestor search began, and is used to determine
      how a logging event is handled.

      If the root is reached, and it has a level of NOTSET, then all
      messages will be processed. Otherwise, the root's level will be
      used as the effective level.

      参见 日志级别 级别列表。

      在 3.2 版更改: The 	- level* parameter now accepts a string
      representation of the level such as 'INFO' as an alternative to
      the integer constants such as "INFO". Note, however, that levels
      are internally stored as integers, and methods such as e.g.
      "getEffectiveLevel()" and "isEnabledFor()" will return/expect to
      be passed integers.

   isEnabledFor(level)

      Indicates if a message of severity 	- level* would be processed by
      this logger. This method checks first the module-level level set
      by "logging.disable(level)" and then the logger's effective
      level as determined by "getEffectiveLevel()".

   getEffectiveLevel()

      Indicates the effective level for this logger. If a value other
      than "NOTSET" has been set using "setLevel()", it is returned.
      Otherwise, the hierarchy is traversed towards the root until a
      value other than "NOTSET" is found, and that value is returned.
      The value returned is an integer, typically one of
      "logging.DEBUG", "logging.INFO" etc.

   getChild(suffix)

      Returns a logger which is a descendant to this logger, as
      determined by the suffix. Thus,
      "logging.getLogger('abc').getChild('def.ghi')" would return the
      same logger as would be returned by
      "logging.getLogger('abc.def.ghi')". This is a convenience
      method, useful when the parent logger is named using e.g.
      "__name__" rather than a literal string.

      3.2 新版功能.

   debug(msg, 	- args, **kwargs)

      Logs a message with level "DEBUG" on this logger. The 	- msg* is
      the message format string, and the 	- args* are the arguments
      which are merged into 	- msg* using the string formatting
      operator. (Note that this means that you can use keywords in the
      format string, together with a single dictionary argument.)

      There are four keyword arguments in 	- kwargs* which are
      inspected: 	- exc_info*, *stack_info*, *stacklevel* and *extra*.

      If 	- exc_info* does not evaluate as false, it causes exception
      information to be added to the logging message. If an exception
      tuple (in the format returned by "sys.exc_info()") or an
      exception instance is provided, it is used; otherwise,
      "sys.exc_info()" is called to get the exception information.

      The second optional keyword argument is 	- stack_info*, which
      defaults to "False". If true, stack information is added to the
      logging message, including the actual logging call. Note that
      this is not the same stack information as that displayed through
      specifying 	- exc_info*: The former is stack frames from the
      bottom of the stack up to the logging call in the current
      thread, whereas the latter is information about stack frames
      which have been unwound, following an exception, while searching
      for exception handlers.

      You can specify 	- stack_info* independently of *exc_info*, e.g.
      to just show how you got to a certain point in your code, even
      when no exceptions were raised. The stack frames are printed
      following a header line which says:

         Stack (most recent call last):

      This mimics the "Traceback (most recent call last):" which is
      used when displaying exception frames.

      The third optional keyword argument is 	- stacklevel*, which
      defaults to "1". If greater than 1, the corresponding number of
      stack frames are skipped when computing the line number and
      function name set in the "LogRecord" created for the logging
      event. This can be used in logging helpers so that the function
      name, filename and line number recorded are not the information
      for the helper function/method, but rather its caller. The name
      of this parameter mirrors the equivalent one in the "warnings"
      module.

      The fourth keyword argument is 	- extra* which can be used to pass
      a dictionary which is used to populate the __dict__ of the
      "LogRecord" created for the logging event with user-defined
      attributes. These custom attributes can then be used as you
      like. For example, they could be incorporated into logged
      messages. For example:

         FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
         logging.basicConfig(format=FORMAT)
         d = {'clientip': '192.168.0.1', 'user': 'fbloggs'}
         logger = logging.getLogger('tcpserver')
         logger.warning('Protocol problem: %s', 'connection reset', extra=d)

      would print something like

         2006-02-08 22:20:02,165 192.168.0.1 fbloggs  Protocol problem: connection reset

      The keys in the dictionary passed in 	- extra* should not clash
      with the keys used by the logging system. (See the "Formatter"
      documentation for more information on which keys are used by the
      logging system.)

      If you choose to use these attributes in logged messages, you
      need to exercise some care. In the above example, for instance,
      the "Formatter" has been set up with a format string which
      expects 'clientip' and 'user' in the attribute dictionary of the
      "LogRecord". If these are missing, the message will not be
      logged because a string formatting exception will occur. So in
      this case, you always need to pass the 	- extra* dictionary with
      these keys.

      While this might be annoying, this feature is intended for use
      in specialized circumstances, such as multi-threaded servers
      where the same code executes in many contexts, and interesting
      conditions which arise are dependent on this context (such as
      remote client IP address and authenticated user name, in the
      above example). In such circumstances, it is likely that
      specialized "Formatter"s would be used with particular
      "Handler"s.

      在 3.2 版更改: 增加了 	- stack_info* 参数。

      在 3.5 版更改: The 	- exc_info* parameter can now accept exception
      instances.

      在 3.8 版更改: 增加了 	- stacklevel* 参数。

   info(msg, 	- args, **kwargs)

      Logs a message with level "INFO" on this logger. The arguments
      are interpreted as for "debug()".

   warning(msg, 	- args, **kwargs)

      Logs a message with level "WARNING" on this logger. The
      arguments are interpreted as for "debug()".

      注解: There is an obsolete method "warn" which is functionally
        identical to "warning". As "warn" is deprecated, please do not
        use it - use "warning" instead.

   error(msg, 	- args, **kwargs)

      Logs a message with level "ERROR" on this logger. The arguments
      are interpreted as for "debug()".

   critical(msg, 	- args, **kwargs)

      Logs a message with level "CRITICAL" on this logger. The
      arguments are interpreted as for "debug()".

   log(level, msg, 	- args, **kwargs)

      Logs a message with integer level 	- level* on this logger. The
      other arguments are interpreted as for "debug()".

   exception(msg, 	- args, **kwargs)

      Logs a message with level "ERROR" on this logger. The arguments
      are interpreted as for "debug()". Exception info is added to the
      logging message. This method should only be called from an
      exception handler.

   addFilter(filter)

      Adds the specified filter 	- filter* to this logger.

   removeFilter(filter)

      Removes the specified filter 	- filter* from this logger.

   filter(record)

      Apply this logger's filters to the record and return "True" if
      the record is to be processed. The filters are consulted in
      turn, until one of them returns a false value. If none of them
      return a false value, the record will be processed (passed to
      handlers). If one returns a false value, no further processing
      of the record occurs.

   addHandler(hdlr)

      Adds the specified handler 	- hdlr* to this logger.

   removeHandler(hdlr)

      Removes the specified handler 	- hdlr* from this logger.

   findCaller(stack_info=False, stacklevel=1)

      Finds the caller's source filename and line number. Returns the
      filename, line number, function name and stack information as a
      4-element tuple. The stack information is returned as "None"
      unless 	- stack_info* is "True".

      The 	- stacklevel* parameter is passed from code calling the
      "debug()" and other APIs. If greater than 1, the excess is used
      to skip stack frames before determining the values to be
      returned. This will generally be useful when calling logging
      APIs from helper/wrapper code, so that the information in the
      event log refers not to the helper/wrapper code, but to the code
      that calls it.

   handle(record)

      Handles a record by passing it to all handlers associated with
      this logger and its ancestors (until a false value of
      	- propagate* is found). This method is used for unpickled records
      received from a socket, as well as those created locally.
      Logger-level filtering is applied using "filter()".

   makeRecord(name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None)

      This is a factory method which can be overridden in subclasses
      to create specialized "LogRecord" instances.

   hasHandlers()

      Checks to see if this logger has any handlers configured. This
      is done by looking for handlers in this logger and its parents
      in the logger hierarchy. Returns "True" if a handler was found,
      else "False". The method stops searching up the hierarchy
      whenever a logger with the 'propagate' attribute set to false is
      found - that will be the last logger which is checked for the
      existence of handlers.

      3.2 新版功能.

   在 3.7 版更改: Loggers can now be pickled and unpickled.


日志级别
========

日志记录级别的数值在下表中给出。如果你想要定义自己的级别，并且需要它们
具有相对于预定义级别的特定值，那么这些内容可能是你感兴趣的。如果你定义
具有相同数值的级别，它将覆盖预定义的值; 预定义的名称丢失。

+----------------+-----------------+
| 级别           | 数值            |
|================|=================|
| "CRITICAL"     | 50              |
+----------------+-----------------+
| "ERROR"        | 40              |
+----------------+-----------------+
| "WARNING"      | 30              |
+----------------+-----------------+
| "INFO"         | 20              |
+----------------+-----------------+
| "DEBUG"        | 10              |
+----------------+-----------------+
| "NOTSET"       | 0               |
+----------------+-----------------+


处理器对象
==========

Handler 有以下属性和方法。注意不要直接实例化 "Handler" ；这个类用来派
生其他更有用的子类。但是，子类的 "__init__()" 方法需要调用
"Handler.__init__()" 。

class logging.Handler

   __init__(level=NOTSET)

      初始化 "Handler" 实例时，需要设置它的级别，将过滤列表置为空，并
      且创建锁（通过 "createLock()" ）来序列化对 I/O 的访问。

   createLock()

      初始化一个线程锁，用来序列化对底层的 I/O 功能的访问，底层的 I/O
      功能可能不是线程安全的。

   acquire()

      使用 "createLock()" 获取线程锁。

   release()

      使用 "acquire()" 来释放线程锁。

   setLevel(level)

      给处理器设置阈值为 	- level* 。日志级别小于 *level* 将被忽略。创建
      处理器时，日志级别被设置为 "NOTSET" （所有的消息都会被处理）。

      参见 日志级别 级别列表。

      在 3.2 版更改: 	- level* 形参现在接受像 'INFO' 这样的字符串形式的
      级别表达方式，也可以使用像 "INFO" 这样的整数常量。

   setFormatter(fmt)

      Sets the "Formatter" for this handler to 	- fmt*.

   addFilter(filter)

      Adds the specified filter 	- filter* to this handler.

   removeFilter(filter)

      Removes the specified filter 	- filter* from this handler.

   filter(record)

      Apply this handler's filters to the record and return "True" if
      the record is to be processed. The filters are consulted in
      turn, until one of them returns a false value. If none of them
      return a false value, the record will be emitted. If one returns
      a false value, the handler will not emit the record.

   flush()

      Ensure all logging output has been flushed. This version does
      nothing and is intended to be implemented by subclasses.

   close()

      Tidy up any resources used by the handler. This version does no
      output but removes the handler from an internal list of handlers
      which is closed when "shutdown()" is called. Subclasses should
      ensure that this gets called from overridden "close()" methods.

   handle(record)

      Conditionally emits the specified logging record, depending on
      filters which may have been added to the handler. Wraps the
      actual emission of the record with acquisition/release of the
      I/O thread lock.

   handleError(record)

      This method should be called from handlers when an exception is
      encountered during an "emit()" call. If the module-level
      attribute "raiseExceptions" is "False", exceptions get silently
      ignored. This is what is mostly wanted for a logging system -
      most users will not care about errors in the logging system,
      they are more interested in application errors. You could,
      however, replace this with a custom handler if you wish. The
      specified record is the one which was being processed when the
      exception occurred. (The default value of "raiseExceptions" is
      "True", as that is more useful during development).

   format(record)

      Do formatting for a record - if a formatter is set, use it.
      Otherwise, use the default formatter for the module.

   emit(record)

      Do whatever it takes to actually log the specified logging
      record. This version is intended to be implemented by subclasses
      and so raises a "NotImplementedError".

For a list of handlers included as standard, see "logging.handlers".


Formatter Objects
=================

"Formatter" objects have the following attributes and methods. They
are responsible for converting a "LogRecord" to (usually) a string
which can be interpreted by either a human or an external system. The
base "Formatter" allows a formatting string to be specified. If none
is supplied, the default value of "'%(message)s'" is used, which just
includes the message in the logging call. To have additional items of
information in the formatted output (such as a timestamp), keep
reading.

A Formatter can be initialized with a format string which makes use of
knowledge of the "LogRecord" attributes - such as the default value
mentioned above making use of the fact that the user's message and
arguments are pre-formatted into a "LogRecord"'s 	- message* attribute.
This format string contains standard Python %-style mapping keys. See
section printf 风格的字符串格式化 for more information on string
formatting.

The useful mapping keys in a "LogRecord" are given in the section on
LogRecord 属性.

class logging.Formatter(fmt=None, datefmt=None, style='%')

   Returns a new instance of the "Formatter" class.  The instance is
   initialized with a format string for the message as a whole, as
   well as a format string for the date/time portion of a message.  If
   no 	- fmt* is specified, "'%(message)s'" is used.  If no *datefmt* is
   specified, a format is used which is described in the
   "formatTime()" documentation.

   The 	- style* parameter can be one of '%', '{' or '$' and determines
   how the format string will be merged with its data: using one of
   %-formatting, "str.format()" or "string.Template". See Using
   particular formatting styles throughout your application for more
   information on using {- and $-formatting for log messages.

   在 3.2 版更改: The 	- style* parameter was added.

   在 3.8 版更改: The 	- validate* parameter was added. Incorrect or
   mismatched style and fmt will raise a "ValueError". For example:
   "logging.Formatter('%(asctime)s - %(message)s', style='{')".

   format(record)

      The record's attribute dictionary is used as the operand to a
      string formatting operation. Returns the resulting string.
      Before formatting the dictionary, a couple of preparatory steps
      are carried out. The 	- message* attribute of the record is
      computed using 	- msg* % *args*. If the formatting string contains
      "'(asctime)'", "formatTime()" is called to format the event
      time. If there is exception information, it is formatted using
      "formatException()" and appended to the message. Note that the
      formatted exception information is cached in attribute
      	- exc_text*. This is useful because the exception information can
      be pickled and sent across the wire, but you should be careful
      if you have more than one "Formatter" subclass which customizes
      the formatting of exception information. In this case, you will
      have to clear the cached value after a formatter has done its
      formatting, so that the next formatter to handle the event
      doesn't use the cached value but recalculates it afresh.

      If stack information is available, it's appended after the
      exception information, using "formatStack()" to transform it if
      necessary.

   formatTime(record, datefmt=None)

      This method should be called from "format()" by a formatter
      which wants to make use of a formatted time. This method can be
      overridden in formatters to provide for any specific
      requirement, but the basic behavior is as follows: if 	- datefmt*
      (a string) is specified, it is used with "time.strftime()" to
      format the creation time of the record. Otherwise, the format
      '%Y-%m-%d %H:%M:%S,uuu' is used, where the uuu part is a
      millisecond value and the other letters are as per the
      "time.strftime()" documentation.  An example time in this format
      is "2003-01-23 00:29:50,411".  The resulting string is returned.

      This function uses a user-configurable function to convert the
      creation time to a tuple. By default, "time.localtime()" is
      used; to change this for a particular formatter instance, set
      the "converter" attribute to a function with the same signature
      as "time.localtime()" or "time.gmtime()". To change it for all
      formatters, for example if you want all logging times to be
      shown in GMT, set the "converter" attribute in the "Formatter"
      class.

      在 3.3 版更改: Previously, the default format was hard-coded as
      in this example: "2010-09-06 22:38:15,292" where the part before
      the comma is handled by a strptime format string ("'%Y-%m-%d
      %H:%M:%S'"), and the part after the comma is a millisecond
      value. Because strptime does not have a format placeholder for
      milliseconds, the millisecond value is appended using another
      format string, "'%s,%03d'" --- and both of these format strings
      have been hardcoded into this method. With the change, these
      strings are defined as class-level attributes which can be
      overridden at the instance level when desired. The names of the
      attributes are "default_time_format" (for the strptime format
      string) and "default_msec_format" (for appending the millisecond
      value).

   formatException(exc_info)

      Formats the specified exception information (a standard
      exception tuple as returned by "sys.exc_info()") as a string.
      This default implementation just uses
      "traceback.print_exception()". The resulting string is returned.

   formatStack(stack_info)

      Formats the specified stack information (a string as returned by
      "traceback.print_stack()", but with the last newline removed) as
      a string. This default implementation just returns the input
      value.


Filter Objects
==============

"Filters" can be used by "Handlers" and "Loggers" for more
sophisticated filtering than is provided by levels. The base filter
class only allows events which are below a certain point in the logger
hierarchy. For example, a filter initialized with 'A.B' will allow
events logged by loggers 'A.B', 'A.B.C', 'A.B.C.D', 'A.B.D' etc. but
not 'A.BB', 'B.A.B' etc. If initialized with the empty string, all
events are passed.

class logging.Filter(name='')

   Returns an instance of the "Filter" class. If 	- name* is specified,
   it names a logger which, together with its children, will have its
   events allowed through the filter. If 	- name* is the empty string,
   allows every event.

   filter(record)

      Is the specified record to be logged? Returns zero for no,
      nonzero for yes. If deemed appropriate, the record may be
      modified in-place by this method.

Note that filters attached to handlers are consulted before an event
is emitted by the handler, whereas filters attached to loggers are
consulted whenever an event is logged (using "debug()", "info()",
etc.), before sending an event to handlers. This means that events
which have been generated by descendant loggers will not be filtered
by a logger's filter setting, unless the filter has also been applied
to those descendant loggers.

You don't actually need to subclass "Filter": you can pass any
instance which has a "filter" method with the same semantics.

在 3.2 版更改: You don't need to create specialized "Filter" classes,
or use other classes with a "filter" method: you can use a function
(or other callable) as a filter. The filtering logic will check to see
if the filter object has a "filter" attribute: if it does, it's
assumed to be a "Filter" and its "filter()" method is called.
Otherwise, it's assumed to be a callable and called with the record as
the single parameter. The returned value should conform to that
returned by "filter()".

Although filters are used primarily to filter records based on more
sophisticated criteria than levels, they get to see every record which
is processed by the handler or logger they're attached to: this can be
useful if you want to do things like counting how many records were
processed by a particular logger or handler, or adding, changing or
removing attributes in the "LogRecord" being processed. Obviously
changing the LogRecord needs to be done with some care, but it does
allow the injection of contextual information into logs (see 使用过滤
器传递上下文信息).


LogRecord Objects
=================

"LogRecord" instances are created automatically by the "Logger" every
time something is logged, and can be created manually via
"makeLogRecord()" (for example, from a pickled event received over the
wire).

class logging.LogRecord(name, level, pathname, lineno, msg, args, exc_info, func=None, sinfo=None)

   Contains all the information pertinent to the event being logged.

   The primary information is passed in "msg" and "args", which are
   combined using "msg % args" to create the "message" field of the
   record.

   参数:
      	- **name** -- The name of the logger used to log the event
        represented by this LogRecord. Note that this name will always
        have this value, even though it may be emitted by a handler
        attached to a different (ancestor) logger.

      	- **level** -- The numeric level of the logging event (one of
        DEBUG, INFO etc.) Note that this is converted to 	- two*
        attributes of the LogRecord: "levelno" for the numeric value
        and "levelname" for the corresponding level name.

      	- **pathname** -- The full pathname of the source file where
        the logging call was made.

      	- **lineno** -- The line number in the source file where the
        logging call was made.

      	- **msg** -- The event description message, possibly a format
        string with placeholders for variable data.

      	- **args** -- Variable data to merge into the *msg* argument
        to obtain the event description.

      	- **exc_info** -- An exception tuple with the current
        exception information, or "None" if no exception information
        is available.

      	- **func** -- The name of the function or method from which
        the logging call was invoked.

      	- **sinfo** -- A text string representing stack information
        from the base of the stack in the current thread, up to the
        logging call.

   getMessage()

      Returns the message for this "LogRecord" instance after merging
      any user-supplied arguments with the message. If the user-
      supplied message argument to the logging call is not a string,
      "str()" is called on it to convert it to a string. This allows
      use of user-defined classes as messages, whose "__str__" method
      can return the actual format string to be used.

   在 3.2 版更改: The creation of a "LogRecord" has been made more
   configurable by providing a factory which is used to create the
   record. The factory can be set using "getLogRecordFactory()" and
   "setLogRecordFactory()" (see this for the factory's signature).

   This functionality can be used to inject your own values into a
   "LogRecord" at creation time. You can use the following pattern:

      old_factory = logging.getLogRecordFactory()

      def record_factory(	- args, **kwargs):
          record = old_factory(	- args, **kwargs)
          record.custom_attribute = 0xdecafbad
          return record

      logging.setLogRecordFactory(record_factory)

   With this pattern, multiple factories could be chained, and as long
   as they don't overwrite each other's attributes or unintentionally
   overwrite the standard attributes listed above, there should be no
   surprises.


LogRecord 属性
==============

The LogRecord has a number of attributes, most of which are derived
from the parameters to the constructor. (Note that the names do not
always correspond exactly between the LogRecord constructor parameters
and the LogRecord attributes.) These attributes can be used to merge
data from the record into the format string. The following table lists
(in alphabetical order) the attribute names, their meanings and the
corresponding placeholder in a %-style format string.

If you are using {}-formatting ("str.format()"), you can use
"{attrname}" as the placeholder in the format string. If you are using
$-formatting ("string.Template"), use the form "${attrname}". In both
cases, of course, replace "attrname" with the actual attribute name
you want to use.

In the case of {}-formatting, you can specify formatting flags by
placing them after the attribute name, separated from it with a colon.
For example: a placeholder of "{msecs:03d}" would format a millisecond
value of "4" as "004". Refer to the "str.format()" documentation for
full details on the options available to you.

+------------------+---------------------------+-------------------------------------------------+
| 属性名称         | 格式                      | 描述                                            |
|==================|===========================|=================================================|
| args             | 不需要格式化。            | The tuple of arguments merged into "msg" to     |
|                  |                           | produce "message", or a dict whose values are   |
|                  |                           | used for the merge (when there is only one      |
|                  |                           | argument, and it is a dictionary).              |
+------------------+---------------------------+-------------------------------------------------+
| asctime          | "%(asctime)s"             | Human-readable time when the "LogRecord" was    |
|                  |                           | created.  By default this is of the form        |
|                  |                           | '2003-07-08 16:49:45,896' (the numbers after    |
|                  |                           | the comma are millisecond portion of the time). |
+------------------+---------------------------+-------------------------------------------------+
| created          | "%(created)f"             | Time when the "LogRecord" was created (as       |
|                  |                           | returned by "time.time()").                     |
+------------------+---------------------------+-------------------------------------------------+
| exc_info         | 不需要格式化。            | Exception tuple (à la "sys.exc_info") or, if no |
|                  |                           | exception has occurred, "None".                 |
+------------------+---------------------------+-------------------------------------------------+
| filename         | "%(filename)s"            | Filename portion of "pathname".                 |
+------------------+---------------------------+-------------------------------------------------+
| funcName         | "%(funcName)s"            | Name of function containing the logging call.   |
+------------------+---------------------------+-------------------------------------------------+
| levelname        | "%(levelname)s"           | Text logging level for the message ("'DEBUG'",  |
|                  |                           | "'INFO'", "'WARNING'", "'ERROR'",               |
|                  |                           | "'CRITICAL'").                                  |
+------------------+---------------------------+-------------------------------------------------+
| levelno          | "%(levelno)s"             | Numeric logging level for the message ("DEBUG", |
|                  |                           | "INFO", "WARNING", "ERROR", "CRITICAL").        |
+------------------+---------------------------+-------------------------------------------------+
| lineno           | "%(lineno)d"              | Source line number where the logging call was   |
|                  |                           | issued (if available).                          |
+------------------+---------------------------+-------------------------------------------------+
| message          | "%(message)s"             | The logged message, computed as "msg % args".   |
|                  |                           | This is set when "Formatter.format()" is        |
|                  |                           | invoked.                                        |
+------------------+---------------------------+-------------------------------------------------+
| module           | "%(module)s"              | 模块 ("filename" 的名称部分)。                  |
+------------------+---------------------------+-------------------------------------------------+
| msecs            | "%(msecs)d"               | Millisecond portion of the time when the        |
|                  |                           | "LogRecord" was created.                        |
+------------------+---------------------------+-------------------------------------------------+
| msg              | 不需要格式化。            | The format string passed in the original        |
|                  |                           | logging call. Merged with "args" to produce     |
|                  |                           | "message", or an arbitrary object (see 使用任意 |
|                  |                           | 对象 作为消息).                                 |
+------------------+---------------------------+-------------------------------------------------+
| name             | "%(name)s"                | Name of the logger used to log the call.        |
+------------------+---------------------------+-------------------------------------------------+
| pathname         | "%(pathname)s"            | Full pathname of the source file where the      |
|                  |                           | logging call was issued (if available).         |
+------------------+---------------------------+-------------------------------------------------+
| process          | "%(process)d"             | 进程ID（如果可用）                              |
+------------------+---------------------------+-------------------------------------------------+
| processName      | "%(processName)s"         | 进程名（如果可用）                              |
+------------------+---------------------------+-------------------------------------------------+
| relativeCreated  | "%(relativeCreated)d"     | Time in milliseconds when the LogRecord was     |
|                  |                           | created, relative to the time the logging       |
|                  |                           | module was loaded.                              |
+------------------+---------------------------+-------------------------------------------------+
| stack_info       | 不需要格式化。            | Stack frame information (where available) from  |
|                  |                           | the bottom of the stack in the current thread,  |
|                  |                           | up to and including the stack frame of the      |
|                  |                           | logging call which resulted in the creation of  |
|                  |                           | this record.                                    |
+------------------+---------------------------+-------------------------------------------------+
| thread           | "%(thread)d"              | 线程ID（如果可用）                              |
+------------------+---------------------------+-------------------------------------------------+
| threadName       | "%(threadName)s"          | 线程名（如果可用）                              |
+------------------+---------------------------+-------------------------------------------------+

在 3.1 版更改: 添加了 	- processName*


LoggerAdapter 对象
==================

"LoggerAdapter" instances are used to conveniently pass contextual
information into logging calls. For a usage example, see the section
on adding contextual information to your logging output.

class logging.LoggerAdapter(logger, extra)

   Returns an instance of "LoggerAdapter" initialized with an
   underlying "Logger" instance and a dict-like object.

   process(msg, kwargs)

      Modifies the message and/or keyword arguments passed to a
      logging call in order to insert contextual information. This
      implementation takes the object passed as 	- extra* to the
      constructor and adds it to 	- kwargs* using key 'extra'. The
      return value is a (	- msg*, *kwargs*) tuple which has the
      (possibly modified) versions of the arguments passed in.

In addition to the above, "LoggerAdapter" supports the following
methods of "Logger": "debug()", "info()", "warning()", "error()",
"exception()", "critical()", "log()", "isEnabledFor()",
"getEffectiveLevel()", "setLevel()" and "hasHandlers()". These methods
have the same signatures as their counterparts in "Logger", so you can
use the two types of instances interchangeably.

在 3.2 版更改: The "isEnabledFor()", "getEffectiveLevel()",
"setLevel()" and "hasHandlers()" methods were added to
"LoggerAdapter".  These methods delegate to the underlying logger.


线程安全
========

The logging module is intended to be thread-safe without any special
work needing to be done by its clients. It achieves this though using
threading locks; there is one lock to serialize access to the module's
shared data, and each handler also creates a lock to serialize access
to its underlying I/O.

If you are implementing asynchronous signal handlers using the
"signal" module, you may not be able to use logging from within such
handlers. This is because lock implementations in the "threading"
module are not always re-entrant, and so cannot be invoked from such
signal handlers.


模块级别函数
============

In addition to the classes described above, there are a number of
module-level functions.

logging.getLogger(name=None)

   Return a logger with the specified name or, if name is "None",
   return a logger which is the root logger of the hierarchy. If
   specified, the name is typically a dot-separated hierarchical name
   like 	- 'a'*, *'a.b'* or *'a.b.c.d'*. Choice of these names is
   entirely up to the developer who is using logging.

   All calls to this function with a given name return the same logger
   instance. This means that logger instances never need to be passed
   between different parts of an application.

logging.getLoggerClass()

   Return either the standard "Logger" class, or the last class passed
   to "setLoggerClass()". This function may be called from within a
   new class definition, to ensure that installing a customized
   "Logger" class will not undo customizations already applied by
   other code. For example:

      class MyLogger(logging.getLoggerClass()):
          # ... override behaviour here

logging.getLogRecordFactory()

   Return a callable which is used to create a "LogRecord".

   3.2 新版功能: This function has been provided, along with
   "setLogRecordFactory()", to allow developers more control over how
   the "LogRecord" representing a logging event is constructed.

   See "setLogRecordFactory()" for more information about the how the
   factory is called.

logging.debug(msg, 	- args, **kwargs)

   Logs a message with level "DEBUG" on the root logger. The 	- msg* is
   the message format string, and the 	- args* are the arguments which
   are merged into 	- msg* using the string formatting operator. (Note
   that this means that you can use keywords in the format string,
   together with a single dictionary argument.)

   There are three keyword arguments in 	- kwargs* which are inspected:
   	- exc_info* which, if it does not evaluate as false, causes
   exception information to be added to the logging message. If an
   exception tuple (in the format returned by "sys.exc_info()") or an
   exception instance is provided, it is used; otherwise,
   "sys.exc_info()" is called to get the exception information.

   The second optional keyword argument is 	- stack_info*, which
   defaults to "False". If true, stack information is added to the
   logging message, including the actual logging call. Note that this
   is not the same stack information as that displayed through
   specifying 	- exc_info*: The former is stack frames from the bottom
   of the stack up to the logging call in the current thread, whereas
   the latter is information about stack frames which have been
   unwound, following an exception, while searching for exception
   handlers.

   You can specify 	- stack_info* independently of *exc_info*, e.g. to
   just show how you got to a certain point in your code, even when no
   exceptions were raised. The stack frames are printed following a
   header line which says:

      Stack (most recent call last):

   This mimics the "Traceback (most recent call last):" which is used
   when displaying exception frames.

   The third optional keyword argument is 	- extra* which can be used to
   pass a dictionary which is used to populate the __dict__ of the
   LogRecord created for the logging event with user-defined
   attributes. These custom attributes can then be used as you like.
   For example, they could be incorporated into logged messages. For
   example:

      FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
      logging.basicConfig(format=FORMAT)
      d = {'clientip': '192.168.0.1', 'user': 'fbloggs'}
      logging.warning('Protocol problem: %s', 'connection reset', extra=d)

   would print something like:

      2006-02-08 22:20:02,165 192.168.0.1 fbloggs  Protocol problem: connection reset

   The keys in the dictionary passed in 	- extra* should not clash with
   the keys used by the logging system. (See the "Formatter"
   documentation for more information on which keys are used by the
   logging system.)

   If you choose to use these attributes in logged messages, you need
   to exercise some care. In the above example, for instance, the
   "Formatter" has been set up with a format string which expects
   'clientip' and 'user' in the attribute dictionary of the LogRecord.
   If these are missing, the message will not be logged because a
   string formatting exception will occur. So in this case, you always
   need to pass the 	- extra* dictionary with these keys.

   While this might be annoying, this feature is intended for use in
   specialized circumstances, such as multi-threaded servers where the
   same code executes in many contexts, and interesting conditions
   which arise are dependent on this context (such as remote client IP
   address and authenticated user name, in the above example). In such
   circumstances, it is likely that specialized "Formatter"s would be
   used with particular "Handler"s.

   在 3.2 版更改: 增加了 	- stack_info* 参数。

logging.info(msg, 	- args, **kwargs)

   Logs a message with level "INFO" on the root logger. The arguments
   are interpreted as for "debug()".

logging.warning(msg, 	- args, **kwargs)

   Logs a message with level "WARNING" on the root logger. The
   arguments are interpreted as for "debug()".

   注解: There is an obsolete function "warn" which is functionally
     identical to "warning". As "warn" is deprecated, please do not
     use it - use "warning" instead.

logging.error(msg, 	- args, **kwargs)

   Logs a message with level "ERROR" on the root logger. The arguments
   are interpreted as for "debug()".

logging.critical(msg, 	- args, **kwargs)

   Logs a message with level "CRITICAL" on the root logger. The
   arguments are interpreted as for "debug()".

logging.exception(msg, 	- args, **kwargs)

   Logs a message with level "ERROR" on the root logger. The arguments
   are interpreted as for "debug()". Exception info is added to the
   logging message. This function should only be called from an
   exception handler.

logging.log(level, msg, 	- args, **kwargs)

   Logs a message with level 	- level* on the root logger. The other
   arguments are interpreted as for "debug()".

   注解: The above module-level convenience functions, which
     delegate to the root logger, call "basicConfig()" to ensure that
     at least one handler is available. Because of this, they should
     	- not* be used in threads, in versions of Python earlier than
     2.7.1 and 3.2, unless at least one handler has been added to the
     root logger 	- before* the threads are started. In earlier versions
     of Python, due to a thread safety shortcoming in "basicConfig()",
     this can (under rare circumstances) lead to handlers being added
     multiple times to the root logger, which can in turn lead to
     multiple messages for the same event.

logging.disable(level=CRITICAL)

   Provides an overriding level 	- level* for all loggers which takes
   precedence over the logger's own level. When the need arises to
   temporarily throttle logging output down across the whole
   application, this function can be useful. Its effect is to disable
   all logging calls of severity 	- level* and below, so that if you
   call it with a value of INFO, then all INFO and DEBUG events would
   be discarded, whereas those of severity WARNING and above would be
   processed according to the logger's effective level. If
   "logging.disable(logging.NOTSET)" is called, it effectively removes
   this overriding level, so that logging output again depends on the
   effective levels of individual loggers.

   Note that if you have defined any custom logging level higher than
   "CRITICAL" (this is not recommended), you won't be able to rely on
   the default value for the 	- level* parameter, but will have to
   explicitly supply a suitable value.

   在 3.7 版更改: The 	- level* parameter was defaulted to level
   "CRITICAL". See Issue #28524 for more information about this
   change.

logging.addLevelName(level, levelName)

   Associates level 	- level* with text *levelName* in an internal
   dictionary, which is used to map numeric levels to a textual
   representation, for example when a "Formatter" formats a message.
   This function can also be used to define your own levels. The only
   constraints are that all levels used must be registered using this
   function, levels should be positive integers and they should
   increase in increasing order of severity.

   注解: If you are thinking of defining your own levels, please see
     the section on 自定义级别.

logging.getLevelName(level)

   Returns the textual representation of logging level 	- level*. If the
   level is one of the predefined levels "CRITICAL", "ERROR",
   "WARNING", "INFO" or "DEBUG" then you get the corresponding string.
   If you have associated levels with names using "addLevelName()"
   then the name you have associated with 	- level* is returned. If a
   numeric value corresponding to one of the defined levels is passed
   in, the corresponding string representation is returned. Otherwise,
   the string 'Level %s' % level is returned.

   注解: Levels are internally integers (as they need to be compared
     in the logging logic). This function is used to convert between
     an integer level and the level name displayed in the formatted
     log output by means of the "%(levelname)s" format specifier (see
     LogRecord 属性).

   在 3.4 版更改: In Python versions earlier than 3.4, this function
   could also be passed a text level, and would return the
   corresponding numeric value of the level. This undocumented
   behaviour was considered a mistake, and was removed in Python 3.4,
   but reinstated in 3.4.2 due to retain backward compatibility.

logging.makeLogRecord(attrdict)

   Creates and returns a new "LogRecord" instance whose attributes are
   defined by 	- attrdict*. This function is useful for taking a pickled
   "LogRecord" attribute dictionary, sent over a socket, and
   reconstituting it as a "LogRecord" instance at the receiving end.

logging.basicConfig(	- *kwargs)

   Does basic configuration for the logging system by creating a
   "StreamHandler" with a default "Formatter" and adding it to the
   root logger. The functions "debug()", "info()", "warning()",
   "error()" and "critical()" will call "basicConfig()" automatically
   if no handlers are defined for the root logger.

   This function does nothing if the root logger already has handlers
   configured, unless the keyword argument 	- force* is set to "True".

   注解: This function should be called from the main thread before
     other threads are started. In versions of Python prior to 2.7.1
     and 3.2, if this function is called from multiple threads, it is
     possible (in rare circumstances) that a handler will be added to
     the root logger more than once, leading to unexpected results
     such as messages being duplicated in the log.

   支持以下关键字参数。

   +----------------+-----------------------------------------------+
   | 格式           | 描述                                          |
   |================|===============================================|
   | 	- filename*     | Specifies that a FileHandler be created,      |
   |                | using the specified filename, rather than a   |
   |                | StreamHandler.                                |
   +----------------+-----------------------------------------------+
   | 	- filemode*     | If *filename* is specified, open the file in  |
   |                | this mode. Defaults to "'a'".                 |
   +----------------+-----------------------------------------------+
   | 	- format*       | Use the specified format string for the       |
   |                | handler.                                      |
   +----------------+-----------------------------------------------+
   | 	- datefmt*      | Use the specified date/time format, as        |
   |                | accepted by "time.strftime()".                |
   +----------------+-----------------------------------------------+
   | 	- style*        | If *format* is specified, use this style for  |
   |                | the format string. One of "'%'", "'{'" or     |
   |                | "'$'" for printf-style, "str.format()" or     |
   |                | "string.Template" respectively. Defaults to   |
   |                | "'%'".                                        |
   +----------------+-----------------------------------------------+
   | 	- level*        | Set the root logger level to the specified    |
   |                | level.                                        |
   +----------------+-----------------------------------------------+
   | 	- stream*       | Use the specified stream to initialize the    |
   |                | StreamHandler. Note that this argument is     |
   |                | incompatible with 	- filename* - if both are    |
   |                | present, a "ValueError" is raised.            |
   +----------------+-----------------------------------------------+
   | 	- handlers*     | If specified, this should be an iterable of   |
   |                | already created handlers to add to the root   |
   |                | logger. Any handlers which don't already have |
   |                | a formatter set will be assigned the default  |
   |                | formatter created in this function. Note that |
   |                | this argument is incompatible with 	- filename* |
   |                | or 	- stream* - if both are present, a          |
   |                | "ValueError" is raised.                       |
   +----------------+-----------------------------------------------+
   | 	- force*        | If this keyword argument is specified as      |
   |                | true, any existing handlers attached to the   |
   |                | root logger are removed and closed, before    |
   |                | carrying out the configuration as specified   |
   |                | by the other arguments.                       |
   +----------------+-----------------------------------------------+

   在 3.2 版更改: 增加了 	- style* 参数。

   在 3.3 版更改: The 	- handlers* argument was added. Additional checks
   were added to catch situations where incompatible arguments are
   specified (e.g. 	- handlers* together with *stream* or *filename*, or
   	- stream* together with *filename*).

   在 3.8 版更改: 增加了 	- force* 参数。

logging.shutdown()

   Informs the logging system to perform an orderly shutdown by
   flushing and closing all handlers. This should be called at
   application exit and no further use of the logging system should be
   made after this call.

   When the logging module is imported, it registers this function as
   an exit handler (see "atexit"), so normally there's no need to do
   that manually.

logging.setLoggerClass(klass)

   Tells the logging system to use the class 	- klass* when
   instantiating a logger. The class should define "__init__()" such
   that only a name argument is required, and the "__init__()" should
   call "Logger.__init__()". This function is typically called before
   any loggers are instantiated by applications which need to use
   custom logger behavior. After this call, as at any other time, do
   not instantiate loggers directly using the subclass: continue to
   use the "logging.getLogger()" API to get your loggers.

logging.setLogRecordFactory(factory)

   Set a callable which is used to create a "LogRecord".

   参数:
      	- *factory** -- The factory callable to be used to instantiate a
      log record.

   3.2 新版功能: This function has been provided, along with
   "getLogRecordFactory()", to allow developers more control over how
   the "LogRecord" representing a logging event is constructed.

   The factory has the following signature:

   "factory(name, level, fn, lno, msg, args, exc_info, func=None,
   sinfo=None, 	- *kwargs)"

      name:
         日志记录器名称

      level:
         日志记录级别（数字）。

      fn:
         进行日志记录调用的文件的完整路径名。

      lno:
         记录调用所在文件中的行号。

      msg:
         日志消息。

      args:
         日志记录消息的参数。

      exc_info:
         异常元组，或 "None" 。

      func:
         调用日志记录调用的函数或方法的名称。

      sinfo:
         A stack traceback such as is provided by
         "traceback.print_stack()", showing the call hierarchy.

      kwargs:
         其他关键字参数。


模块级属性
==========

logging.lastResort

   A "handler of last resort" is available through this attribute.
   This is a "StreamHandler" writing to "sys.stderr" with a level of
   "WARNING", and is used to handle logging events in the absence of
   any logging configuration. The end result is to just print the
   message to "sys.stderr". This replaces the earlier error message
   saying that "no handlers could be found for logger XYZ". If you
   need the earlier behaviour for some reason, "lastResort" can be set
   to "None".

   3.2 新版功能.


Integration with the warnings module
====================================

The "captureWarnings()" function can be used to integrate "logging"
with the "warnings" module.

logging.captureWarnings(capture)

   This function is used to turn the capture of warnings by logging on
   and off.

   If 	- capture* is "True", warnings issued by the "warnings" module
   will be redirected to the logging system. Specifically, a warning
   will be formatted using "warnings.formatwarning()" and the
   resulting string logged to a logger named "'py.warnings'" with a
   severity of "WARNING".

   If 	- capture* is "False", the redirection of warnings to the logging
   system will stop, and warnings will be redirected to their original
   destinations (i.e. those in effect before "captureWarnings(True)"
   was called).

参见:

  模块 "logging.config"
     日志记录模块的配置 API 。

  模块 "logging.handlers"
     日志记录模块附带的有用处理程序。

  	- *PEP 282** - A Logging System
     该提案描述了Python标准库中包含的这个特性。

  Original Python logging package
     This is the original source for the "logging" package.  The
     version of the package available from this site is suitable for
     use with Python 1.5.2, 2.1.x and 2.2.x, which do not include the
     "logging" package in the standard library.