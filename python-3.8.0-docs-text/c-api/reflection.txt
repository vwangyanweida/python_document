反射
****

PyObject* PyEval_GetBuiltins()
    *Return value: Borrowed reference.*

   返回当前执行帧中内置函数的字典，如果当前没有帧正在执行，则返回线程
   状态的解释器。

PyObject* PyEval_GetLocals()
    *Return value: Borrowed reference.*

   返回当前执行帧中局部变量的字典，如果没有当前执行的帧则返回 "NULL"。

PyObject* PyEval_GetGlobals()
    *Return value: Borrowed reference.*

   返回当前执行帧中全局变量的字典，如果没有当前执行的帧则返回 "NULL"。

PyFrameObject* PyEval_GetFrame()
    *Return value: Borrowed reference.*

   返回当前线程状态的帧，如果没有当前执行的帧则返回 "NULL"。

int PyFrame_GetLineNumber(PyFrameObject *frame)

   返回 *frame* 当前正在执行的行号。

const char* PyEval_GetFuncName(PyObject *func)

   如果 *func* 是函数、类或实例对象，则返回它的名称，否则返回 *func*
   的类型的名称。

const char* PyEval_GetFuncDesc(PyObject *func)

   根据 *func* 的类型返回描述字符串。 返回值包括函数和方法的 "()", "
   constructor", " instance" 和 " object"。 与 "PyEval_GetFuncName()"
   的结果连接，结果将是 *func* 的描述。
