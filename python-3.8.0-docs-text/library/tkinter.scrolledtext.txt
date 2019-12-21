"tkinter.scrolledtext" --- 滚动文字控件
***************************************

**源代码：** Lib/tkinter/scrolledtext.py

======================================================================

"tkinter.scrolledtext" 模块提供一个同名的类，实现了一个带有垂直滚动条
的文字控件。使用 "ScrolledText"  类会比直接配置一个文本控件和滚动条简
单。它的构造函数与 "tkinter.Text" 类相同。

文本控件与滚动条打包在一个 "Frame" 中， "Grid" 方法和 "Pack" 方法的布
局管理器从 "Frame" 对象中获得。这允许 "ScrolledText" 控件可以直接用于
实现大多数正常的布局管理行为。

如果需要更具体的控制，可以使用以下属性：

ScrolledText.frame

   围绕文本和滚动条控件的框架。

ScrolledText.vbar

   滚动条控件。
