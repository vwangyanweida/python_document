数字协议
********

int PyNumber_Check(PyObject *o)

   如果对象 *o* 提供数字的协议，返回真 "1"，否则返回假。这个函数不会调
   用失败。

   在 3.8 版更改: 如果 *o* 是一个索引整数则返回 "1"。

PyObject* PyNumber_Add(PyObject *o1, PyObject *o2)
    *Return value: New reference.*

   Returns the result of adding *o1* and *o2*, or "NULL" on failure.
   This is the equivalent of the Python expression "o1 + o2".

PyObject* PyNumber_Subtract(PyObject *o1, PyObject *o2)
    *Return value: New reference.*

   Returns the result of subtracting *o2* from *o1*, or "NULL" on
   failure.  This is the equivalent of the Python expression "o1 -
   o2".

PyObject* PyNumber_Multiply(PyObject *o1, PyObject *o2)
    *Return value: New reference.*

   Returns the result of multiplying *o1* and *o2*, or "NULL" on
   failure.  This is the equivalent of the Python expression "o1 *
   o2".

PyObject* PyNumber_MatrixMultiply(PyObject *o1, PyObject *o2)
    *Return value: New reference.*

   Returns the result of matrix multiplication on *o1* and *o2*, or
   "NULL" on failure.  This is the equivalent of the Python expression
   "o1 @ o2".

   3.5 新版功能.

PyObject* PyNumber_FloorDivide(PyObject *o1, PyObject *o2)
    *Return value: New reference.*

   Return the floor of *o1* divided by *o2*, or "NULL" on failure.
   This is equivalent to the "classic" division of integers.

PyObject* PyNumber_TrueDivide(PyObject *o1, PyObject *o2)
    *Return value: New reference.*

   Return a reasonable approximation for the mathematical value of
   *o1* divided by *o2*, or "NULL" on failure.  The return value is
   "approximate" because binary floating point numbers are
   approximate; it is not possible to represent all real numbers in
   base two.  This function can return a floating point value when
   passed two integers.

PyObject* PyNumber_Remainder(PyObject *o1, PyObject *o2)
    *Return value: New reference.*

   Returns the remainder of dividing *o1* by *o2*, or "NULL" on
   failure.  This is the equivalent of the Python expression "o1 %
   o2".

PyObject* PyNumber_Divmod(PyObject *o1, PyObject *o2)
    *Return value: New reference.*

   See the built-in function "divmod()". Returns "NULL" on failure.
   This is the equivalent of the Python expression "divmod(o1, o2)".

PyObject* PyNumber_Power(PyObject *o1, PyObject *o2, PyObject *o3)
    *Return value: New reference.*

   See the built-in function "pow()". Returns "NULL" on failure.  This
   is the equivalent of the Python expression "pow(o1, o2, o3)", where
   *o3* is optional. If *o3* is to be ignored, pass "Py_None" in its
   place (passing "NULL" for *o3* would cause an illegal memory
   access).

PyObject* PyNumber_Negative(PyObject *o)
    *Return value: New reference.*

   Returns the negation of *o* on success, or "NULL" on failure. This
   is the equivalent of the Python expression "-o".

PyObject* PyNumber_Positive(PyObject *o)
    *Return value: New reference.*

   Returns *o* on success, or "NULL" on failure.  This is the
   equivalent of the Python expression "+o".

PyObject* PyNumber_Absolute(PyObject *o)
    *Return value: New reference.*

   Returns the absolute value of *o*, or "NULL" on failure.  This is
   the equivalent of the Python expression "abs(o)".

PyObject* PyNumber_Invert(PyObject *o)
    *Return value: New reference.*

   Returns the bitwise negation of *o* on success, or "NULL" on
   failure.  This is the equivalent of the Python expression "~o".

PyObject* PyNumber_Lshift(PyObject *o1, PyObject *o2)
    *Return value: New reference.*

   Returns the result of left shifting *o1* by *o2* on success, or
   "NULL" on failure.  This is the equivalent of the Python expression
   "o1 << o2".

PyObject* PyNumber_Rshift(PyObject *o1, PyObject *o2)
    *Return value: New reference.*

   Returns the result of right shifting *o1* by *o2* on success, or
   "NULL" on failure.  This is the equivalent of the Python expression
   "o1 >> o2".

PyObject* PyNumber_And(PyObject *o1, PyObject *o2)
    *Return value: New reference.*

   Returns the "bitwise and" of *o1* and *o2* on success and "NULL" on
   failure. This is the equivalent of the Python expression "o1 & o2".

PyObject* PyNumber_Xor(PyObject *o1, PyObject *o2)
    *Return value: New reference.*

   Returns the "bitwise exclusive or" of *o1* by *o2* on success, or
   "NULL" on failure.  This is the equivalent of the Python expression
   "o1 ^ o2".

PyObject* PyNumber_Or(PyObject *o1, PyObject *o2)
    *Return value: New reference.*

   Returns the "bitwise or" of *o1* and *o2* on success, or "NULL" on
   failure. This is the equivalent of the Python expression "o1 | o2".

PyObject* PyNumber_InPlaceAdd(PyObject *o1, PyObject *o2)
    *Return value: New reference.*

   Returns the result of adding *o1* and *o2*, or "NULL" on failure.
   The operation is done *in-place* when *o1* supports it.  This is
   the equivalent of the Python statement "o1 += o2".

PyObject* PyNumber_InPlaceSubtract(PyObject *o1, PyObject *o2)
    *Return value: New reference.*

   Returns the result of subtracting *o2* from *o1*, or "NULL" on
   failure.  The operation is done *in-place* when *o1* supports it.
   This is the equivalent of the Python statement "o1 -= o2".

PyObject* PyNumber_InPlaceMultiply(PyObject *o1, PyObject *o2)
    *Return value: New reference.*

   Returns the result of multiplying *o1* and *o2*, or "NULL" on
   failure.  The operation is done *in-place* when *o1* supports it.
   This is the equivalent of the Python statement "o1 *= o2".

PyObject* PyNumber_InPlaceMatrixMultiply(PyObject *o1, PyObject *o2)
    *Return value: New reference.*

   Returns the result of matrix multiplication on *o1* and *o2*, or
   "NULL" on failure.  The operation is done *in-place* when *o1*
   supports it.  This is the equivalent of the Python statement "o1 @=
   o2".

   3.5 新版功能.

PyObject* PyNumber_InPlaceFloorDivide(PyObject *o1, PyObject *o2)
    *Return value: New reference.*

   Returns the mathematical floor of dividing *o1* by *o2*, or "NULL"
   on failure. The operation is done *in-place* when *o1* supports it.
   This is the equivalent of the Python statement "o1 //= o2".

PyObject* PyNumber_InPlaceTrueDivide(PyObject *o1, PyObject *o2)
    *Return value: New reference.*

   Return a reasonable approximation for the mathematical value of
   *o1* divided by *o2*, or "NULL" on failure.  The return value is
   "approximate" because binary floating point numbers are
   approximate; it is not possible to represent all real numbers in
   base two.  This function can return a floating point value when
   passed two integers.  The operation is done *in-place* when *o1*
   supports it.

PyObject* PyNumber_InPlaceRemainder(PyObject *o1, PyObject *o2)
    *Return value: New reference.*

   Returns the remainder of dividing *o1* by *o2*, or "NULL" on
   failure.  The operation is done *in-place* when *o1* supports it.
   This is the equivalent of the Python statement "o1 %= o2".

PyObject* PyNumber_InPlacePower(PyObject *o1, PyObject *o2, PyObject *o3)
    *Return value: New reference.*

   See the built-in function "pow()". Returns "NULL" on failure.  The
   operation is done *in-place* when *o1* supports it.  This is the
   equivalent of the Python statement "o1 **= o2" when o3 is
   "Py_None", or an in-place variant of "pow(o1, o2, o3)" otherwise.
   If *o3* is to be ignored, pass "Py_None" in its place (passing
   "NULL" for *o3* would cause an illegal memory access).

PyObject* PyNumber_InPlaceLshift(PyObject *o1, PyObject *o2)
    *Return value: New reference.*

   Returns the result of left shifting *o1* by *o2* on success, or
   "NULL" on failure.  The operation is done *in-place* when *o1*
   supports it.  This is the equivalent of the Python statement "o1
   <<= o2".

PyObject* PyNumber_InPlaceRshift(PyObject *o1, PyObject *o2)
    *Return value: New reference.*

   Returns the result of right shifting *o1* by *o2* on success, or
   "NULL" on failure.  The operation is done *in-place* when *o1*
   supports it.  This is the equivalent of the Python statement "o1
   >>= o2".

PyObject* PyNumber_InPlaceAnd(PyObject *o1, PyObject *o2)
    *Return value: New reference.*

   Returns the "bitwise and" of *o1* and *o2* on success and "NULL" on
   failure. The operation is done *in-place* when *o1* supports it.
   This is the equivalent of the Python statement "o1 &= o2".

PyObject* PyNumber_InPlaceXor(PyObject *o1, PyObject *o2)
    *Return value: New reference.*

   Returns the "bitwise exclusive or" of *o1* by *o2* on success, or
   "NULL" on failure.  The operation is done *in-place* when *o1*
   supports it.  This is the equivalent of the Python statement "o1 ^=
   o2".

PyObject* PyNumber_InPlaceOr(PyObject *o1, PyObject *o2)
    *Return value: New reference.*

   Returns the "bitwise or" of *o1* and *o2* on success, or "NULL" on
   failure.  The operation is done *in-place* when *o1* supports it.
   This is the equivalent of the Python statement "o1 |= o2".

PyObject* PyNumber_Long(PyObject *o)
    *Return value: New reference.*

   Returns the *o* converted to an integer object on success, or
   "NULL" on failure.  This is the equivalent of the Python expression
   "int(o)".

PyObject* PyNumber_Float(PyObject *o)
    *Return value: New reference.*

   Returns the *o* converted to a float object on success, or "NULL"
   on failure. This is the equivalent of the Python expression
   "float(o)".

PyObject* PyNumber_Index(PyObject *o)
    *Return value: New reference.*

   Returns the *o* converted to a Python int on success or "NULL" with
   a "TypeError" exception raised on failure.

PyObject* PyNumber_ToBase(PyObject *n, int base)
    *Return value: New reference.*

   返回整数 *n* 转换成以 *base* 为基数的字符串后的结果。这个 *base* 参
   数必须是 2，8，10 或者 16 。对于基数 2，8，或 16 ，返回的字符串将分
   别加上基数标识 "'0b'", "'0o'", or "'0x'"。如果 *n* 不是 Python 中的
   整数 *int* 类型，就先通过 "PyNumber_Index()" 将它转换成整数类型。

Py_ssize_t PyNumber_AsSsize_t(PyObject *o, PyObject *exc)

   如果 *o* 是一个整数类型的解释型，返回 *o* 转换成一个 Py_ssize_t 值
   项后的结果。如果调用失败，返回 "-1" 并引发异常。

   If *o* can be converted to a Python int but the attempt to convert
   to a Py_ssize_t value would raise an "OverflowError", then the
   *exc* argument is the type of exception that will be raised
   (usually "IndexError" or "OverflowError").  If *exc* is "NULL",
   then the exception is cleared and the value is clipped to
   "PY_SSIZE_T_MIN" for a negative integer or "PY_SSIZE_T_MAX" for a
   positive integer.

int PyIndex_Check(PyObject *o)

   如果 *o* 是一个索引整数（存有 nb_index 位置并有 tp_as_number 填入其
   中）则返回 "1"，否则返回 "0" 。这个函数不会调用失败。
