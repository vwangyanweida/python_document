编解码器注册与支持功能
**********************

int PyCodec_Register(PyObject *search_function)

   注册一个新的编解码器搜索函数。

   作为副作用，其尝试加载 "encodings" 包，如果尚未完成，请确保它始终位
   于搜索函数列表的第一位。

int PyCodec_KnownEncoding(const char *encoding)

   根据注册的给定 *encoding* 的编解码器是否已存在而返回 "1" 或 "0"。此
   函数总能成功。

PyObject* PyCodec_Encode(PyObject *object, const char *encoding, const char *errors)
    *Return value: New reference.*

   泛型编解码器基本编码 API。

   *object* is passed through the encoder function found for the given
   *encoding* using the error handling method defined by *errors*.
   *errors* may be "NULL" to use the default method defined for the
   codec.  Raises a "LookupError" if no encoder can be found.

PyObject* PyCodec_Decode(PyObject *object, const char *encoding, const char *errors)
    *Return value: New reference.*

   泛型编解码器基本解码 API。

   *object* is passed through the decoder function found for the given
   *encoding* using the error handling method defined by *errors*.
   *errors* may be "NULL" to use the default method defined for the
   codec.  Raises a "LookupError" if no encoder can be found.


Codec 查找API
=============

In the following functions, the *encoding* string is looked up
converted to all lower-case characters, which makes encodings looked
up through this mechanism effectively case-insensitive.  If no codec
is found, a "KeyError" is set and "NULL" returned.

PyObject* PyCodec_Encoder(const char *encoding)
    *Return value: New reference.*

   Get an encoder function for the given *encoding*.

PyObject* PyCodec_Decoder(const char *encoding)
    *Return value: New reference.*

   Get a decoder function for the given *encoding*.

PyObject* PyCodec_IncrementalEncoder(const char *encoding, const char *errors)
    *Return value: New reference.*

   Get an "IncrementalEncoder" object for the given *encoding*.

PyObject* PyCodec_IncrementalDecoder(const char *encoding, const char *errors)
    *Return value: New reference.*

   Get an "IncrementalDecoder" object for the given *encoding*.

PyObject* PyCodec_StreamReader(const char *encoding, PyObject *stream, const char *errors)
    *Return value: New reference.*

   Get a "StreamReader" factory function for the given *encoding*.

PyObject* PyCodec_StreamWriter(const char *encoding, PyObject *stream, const char *errors)
    *Return value: New reference.*

   为给定的 *encoding* 获取一个 "StreamWriter" 工厂函数。


用于Unicode编码错误处理程序的注册表API
======================================

int PyCodec_RegisterError(const char *name, PyObject *error)

   Register the error handling callback function *error* under the
   given *name*. This callback function will be called by a codec when
   it encounters unencodable characters/undecodable bytes and *name*
   is specified as the error parameter in the call to the
   encode/decode function.

   The callback gets a single argument, an instance of
   "UnicodeEncodeError", "UnicodeDecodeError" or
   "UnicodeTranslateError" that holds information about the
   problematic sequence of characters or bytes and their offset in the
   original string (see Unicode Exception Objects for functions to
   extract this information).  The callback must either raise the
   given exception, or return a two-item tuple containing the
   replacement for the problematic sequence, and an integer giving the
   offset in the original string at which encoding/decoding should be
   resumed.

   成功则返回``0`` ，失败则返回``-1``

PyObject* PyCodec_LookupError(const char *name)
    *Return value: New reference.*

   Lookup the error handling callback function registered under
   *name*.  As a special case "NULL" can be passed, in which case the
   error handling callback for "strict" will be returned.

PyObject* PyCodec_StrictErrors(PyObject *exc)
    *Return value: Always NULL.*

   Raise *exc* as an exception.

PyObject* PyCodec_IgnoreErrors(PyObject *exc)
    *Return value: New reference.*

   Ignore the unicode error, skipping the faulty input.

PyObject* PyCodec_ReplaceErrors(PyObject *exc)
    *Return value: New reference.*

   Replace the unicode encode error with "?" or "U+FFFD".

PyObject* PyCodec_XMLCharRefReplaceErrors(PyObject *exc)
    *Return value: New reference.*

   Replace the unicode encode error with XML character references.

PyObject* PyCodec_BackslashReplaceErrors(PyObject *exc)
    *Return value: New reference.*

   Replace the unicode encode error with backslash escapes ("\x", "\u"
   and "\U").

PyObject* PyCodec_NameReplaceErrors(PyObject *exc)
    *Return value: New reference.*

   Replace the unicode encode error with "\N{...}" escapes.

   3.5 新版功能.
