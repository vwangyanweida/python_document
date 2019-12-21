NumPy NumPy 中文网
概述
文章
深度学习
用户指南
参考手册
精选资源
其他文档

  • 防脱发指南
  • NumPy 基准测试
  • NumPy 开发者指南
  • F2Py 指南
  • 构建和扩展文档

了解更多

  • 社区
  • 报告错误
  • 发布日志
  • NumPy 许可证
  • Numpy 开发计划

选择语言

  • 简体中文
  • English

GitHub
概述
文章
深度学习
用户指南
参考手册
精选资源
其他文档

  • 防脱发指南
  • NumPy 基准测试
  • NumPy 开发者指南
  • F2Py 指南
  • 构建和扩展文档

了解更多

  • 社区
  • 报告错误
  • 发布日志
  • NumPy 许可证
  • Numpy 开发计划

选择语言

  • 简体中文
  • English

GitHub

  • NumPy 介绍

  • 快速入门教程

  • NumPy 基础知识

  • 其他杂项

  • 与 Matlab 比较

      □ 与 Matlab 比较
          ☆ 介绍
          ☆ 一些关键的差异
          ☆ 'array'或'matrix'？我应该使用哪个？
              ○ 简答
              ○ 长答案
          ☆ MATLAB 和 NumPy粗略的功能对应表
              ○ 一般功能的对应表
              ○ 线性代数功能对应表
          ☆ 备注
          ☆ 自定义您的环境
          ☆ 链接
  • 从源代码构建

  • 使用NumPy的C-API

# 与 Matlab 比较

# 介绍

MATLAB®和NumPy / SciPy有很多共同之处。但是有很多不同之处。创建NumPy和SciPy是为了用Python最自然的方式进行数值和科学计算，而不是MATLAB®克隆。本页面旨在收集有关
差异的智慧，主要是为了帮助熟练的MATLAB®用户成为熟练的NumPy和SciPy用户。

# 一些关键的差异

                                MATLAB                                                                          NumPy
在MATLAB®中，基本数据类型是双精度浮点数的多维数组。大多数表达式采用这样 在NumPy中，基本类型是多维的array。包括2D在内的所有维度中对这些数组的操作是逐元素操作
的数组并返回这样的数对这些数组的2-D实例的操作被设计成或多或少地像线性代 。人们需要使用线性代数的特定函数（尽管对于矩阵乘法，可以@在python 3.5及更高版本中使用
数中的矩阵运算。                                                        运算符）。
MATLAB®使用基于1（一）的索引。使用（1）找到序列的初始元素。请参阅备注   Python使用基于0（零）的索引。使用[0]找到序列的初始元素。
MATLAB®的脚本语言是为执行线性代数而创建的。基本矩阵操作的语法很好而且干 NumPy基于Python，它从一开始就被设计成一种优秀的通用编程语言。虽然Matlab的一些数组操作
净，但是用于添加GUI和制作完整应用程序的API或多或少都是事后的想法。      的语法比NumPy更紧凑，但NumPy（由于是Python的附加组件）可以做许多Matlab不能做的事情，
                                                                        例如正确处理矩阵堆栈。
在MATLAB®中，数组具有按值传递的语义，并具有惰性写入时复制方案，以防止在 在NumPy数组中有传递引用语义。切片操作是对数组的视图。
实际需要之前实际创建副本。切片操作复制数组的一部分。

# 'array'或'matrix'？我应该使用哪个？

从历史上看，NumPy提供了一种特殊的矩阵类型 np.matrix ，它是ndarray的子​​类，它使二进制运算成为线性代数运算。您可能会在某些现有代码中看到它而不是 np.array 。那
么，使用哪一个？

# 简答

使用数组。

  • 它们是numpy的标准矢量/矩阵/张量类型。许多numpy函数返回数组，而不是矩阵。
  • 元素操作和线性代数操作之间有明显的区别。
  • 如果您愿意，可以使用标准向量或行/列向量。

在Python 3.5之前，使用数组类型的唯一缺点是你必须使用dot而不是*乘法（减少）两个张量（标量乘积，矩阵向量乘法等）。从Python 3.5开始，您可以使用矩阵乘法@运算符。

鉴于上述情况，我们打算matrix最终弃用。

# 长答案

NumPy包含array类和matrix类。所述 array类旨在是对许多种数值计算的通用n维数组中，而matrix意在具体促进线性代数计算。在实践中，两者之间只有少数关键差异。

  • 运算符*和@函数dot()，以及multiply()：
      □ 对于数组，*表示逐元素乘法，而 @ 表示矩阵乘法; 它们具有相关的函数 multiply() 和 dot() 。（在python 3.5之前，@ 不存在，并且必须使用dot() 进行矩阵乘法）
        。
      □ 对于矩阵，* 表示矩阵乘法，对于逐元素乘法，必须使用 multiply() 函数。
  • 矢量处理（一维数组）
      □ 对于数组，向量形状1xN，Nx1和N都是不同的东西。像 A[:, 1] 这样的操作返回形状N的一维数组，而不是形状Nx1的二维数组。在一维数组上转置什么都不做。
      □ 对于矩阵，一维数组总是被上变频为1xN或Nx1矩阵（行或列向量）。A[:, 1] 返回形状为Nx1的二维矩阵。
  • 处理更高维数组（ndim> 2）
      □ 数组对象的维数可以 > 2 ;
      □ 矩阵对象总是有两个维度。
  • 便利属性
      □ array 有一个.T属性，它返回数据的转置。
      □ matrix 还有.H，.I和.A属性，分别返回共轭转置，反转和asarray()矩阵。
  • 便利构造函数
      □ 该array构造采用（嵌套）的Python序列初始化。如：array([[1,2,3],[4,5,6]])。
      □ 该matrix构造还需要一个方便的字符串初始化。如：matrix("[1 2 3; 4 5 6]")。

使用两者有利有弊：

  • array
      □ :) 元素乘法很容易：A*B。
      □ :( 你必须记住，矩阵乘法有自己的运算符@。
      □ :) 可以将一维数组视为行向量或列向量。 A @ v 将 v 视为列向量，而 v @ A 将 v 视为行向量。这可以节省您键入许多转置。
      □ :) array 是“默认”NumPy类型，因此它获得的测试最多，并且是使用NumPy的第三方代码最有可能返回的类型。
      □ :) 非常擅长处理任何维度的数据。
      □ :) 如果你熟悉那么语义学更接近张量代数。
      □ :) 所有操作（*，/，+，-等）逐元素。
      □ :( 稀疏矩阵scipy.sparse不与数组交互。
  • matrix
      □ :\\ 行为更像MATLAB®矩阵。
      □ <:( 最大二维。要保存您需要的三维数据，array或者可能是Python列表matrix。
      □ <:( 最小二维。你不能有载体。它们必须作为单列或单行矩阵进行转换。
      □ <:( 由于array是NumPy中的默认值，因此array即使您将它们matrix作为参数给出，某些函数也可能返回。这不应该发生在NumPy函数中（如果它确实是一个错误），但基
        于NumPy的第三方代码可能不像NumPy那样遵守类型保存。
      □ :) A*B是矩阵乘法，所以它看起来就像你在线性代数中写的那样（对于Python> = 3.5普通数组与@运算符具有相同的便利性）。
      □ <:( 元素乘法需要调用函数， multiply(A,B)。
      □ <:( 运算符重载的使用有点不合逻辑：* 不能按元素操作，但 / 确实如此。
      □ 与之互动scipy.sparse有点清洁。

因此，使用数组（array）要明智得多。事实上，我们打算最终废除矩阵（matrix）。

# MATLAB 和 NumPy粗略的功能对应表

下表给出了一些常见MATLAB®表达式的粗略等价物。这些不是确切的等价物，而应该作为提示让你朝着正确的方向前进。有关更多详细信息，请阅读NumPy函数的内置文档。

在下表中，假设您已在Python中执行以下命令：

from numpy import *
import scipy.linalg

另外如果下表中的注释这一列的内容是和 “matrix” 有关的话，那么参数一定是二维的形式。

# 一般功能的对应表

     MATLAB                           NumPy                                             注释
help func         info(func)或者help(func)或func?（在IPython的） 获得函数func的帮助
which func        请参阅备注                                     找出func定义的位置
type func         source(func)或者func??（在Ipython中）          func的打印源（如果不是本机函数）
a && b            a and b                                        短路逻辑AND运算符（Python本机运算符）; 只有标量参数
a                                                                b
1*i，1*j， 1i，1j 1j                                             复数
eps               np.spacing(1)                                  1与最近的浮点数之间的距离。
ode45             scipy.integrate.solve_ivp(f)                   将ODE与Runge-Kutta 4,5集成
ode15s            scipy.integrate.solve_ivp(f, method='BDF')     将ODE与BDF方法集成

# 线性代数功能对应表

             MATLAB                                    NumPy                                                          注释
ndims(a)                         ndim(a) 要么 a.ndim                                获取数组的维数
numel(a)                         size(a) 要么 a.size                                获取数组的元素数
size(a)                          shape(a) 要么 a.shape                              得到矩阵的“大小”
size(a,n)                        a.shape[n-1]                                       获取数组第n维元素的数量a。（请注意，MATLAB®使用基于1的索引，而Python使用
                                                                                    基于0的索引，请参阅备注）
[ 1 2 3; 4 5 6 ]                 array([[1.,2.,3.], [4.,5.,6.]])                    2x3矩阵文字
[ a b; c d ]                     block([[a,b], [c,d]])                              从块构造一个矩阵a，b，c，和d
a(end)                           a[-1]                                              访问1xn矩阵中的最后一个元素 a
a(2,5)                           a[1,4]                                             第二行，第五列中的访问元素
a(2,:)                           a[1] 要么 a[1,:]                                   整个第二排 a
a(1:5,:)                         a[0:5]或a[:5]或a[0:5,:]                            前五行 a
a(end-4:end,:)                   a[-5:]                                             最后五行 a
a(1:3,5:9)                       a[0:3][:,4:9]                                      第一至第三行以及第五至第九列a。这提供了只读访问权限。
a([2,4,5],[1,3])                 a[ix_([1,3,4],[0,2])]                              行2,4和5以及第1列和第3列。这允许修改矩阵，并且不需要常规切片。
a(3:2:21,:)                      a[ 2:21:2,:]                                       每隔一行a，从第三行开始到第二十一行
a(1:2:end,:)                     a[ ::2,:]                                          每一行a，从第一行开始
a(end: -1:1,:) 要么 flipud(a)    a[ ::-1,:]                                         a 行以相反的顺序排列
a([1:end 1],: )                  a[r_[:len(a),0]]                                   a 附加到末尾的第一行的副本
a.'                              a.transpose() 要么 a.T                             转置 a
a'                               a.conj().transpose() 要么 a.conj().T               共轭转置 a
a * b                            a @ b                                              矩阵乘法
a .* b                           a * b                                              元素乘法
a./b                             a/b                                                元素划分
a.^3                             a**3                                               元素取幂
(a>0.5)                          (a>0.5)                                            其i，jth元素为（a_ij> 0.5）的矩阵。Matlab结果是一个0和1的数组。NumPy结果
                                                                                    是布尔值的数组False和True。
find(a>0.5)                      nonzero(a>0.5)                                     找到指数在哪里（a> 0.5）
a(:,find(v>0.5))                 a[:,nonzero(v>0.5)[0]]                             提取a向量v> 0.5 的columms
a(:,find(v>0.5))                 a[:,v.T>0.5]                                       提取a列向量v> 0.5的列的列
a(a<0.5)=0                       a[a<0.5]=0                                         a 小于0.5的元素归零
a .* (a>0.5)                     a * (a>0.5)                                        a 小于0.5的元素归零
a(: ) = 3                        a[:] = 3                                           将所有值设置为相同的标量值
y=x                              y = x.copy()                                       numpy通过引用分配
y=x(2,:)                         y = x[1,:].copy()                                  numpy切片是参考
y=x(: )                          y = x.flatten()                                    将数组转换为向量（请注意，这会强制复制）
1:10                             arange(1.,11.)或r_[1.:11.]或 r_[1:10:10j]          创建一个增加的向量（参见备注）
0:9                              arange(10.)或 r_[:10.]或 r_[:9:10j]                创建一个增加的向量（参见注释范围）
[1:10]'                          arange(1.,11.)[:, newaxis]                         创建列向量
zeros(3,4)                       zeros((3,4))                                       3x4二维数组，充满64位浮点零
zeros(3,4,5)                     zeros((3,4,5))                                     3x4x5三维数组，全部为64位浮点零
ones(3,4)                        ones((3,4))                                        3x4二维数组，充满64位浮点数
eye(3)                           eye(3)                                             3x3单位矩阵
diag(a)                          diag(a)                                            矢量对角元素 a
diag(a,0)                        diag(a,0)                                          方形对角矩阵，其非零值是元素 a
rand(3,4)                        random.rand(3,4) 要么 random.random_sample((3, 4)) 随机3x4矩阵
linspace(1,3,4)                  linspace(1,3,4)                                    4个等间距的样本，介于1和3之间
[x,y]=meshgrid(0:8,0:5)          mgrid[0:9.,0:6.] 要么 meshgrid(r_[0:9.],r_[0:6.]   两个2D数组：一个是x值，另一个是y值
ogrid[0:9.,0:6.] 要么 ix_(r_     在网格上评估函数的最佳方法
[0:9.],r_[0:6.]
[x,y]=meshgrid([1,2,4],[2,4,5])  meshgrid([1,2,4],[2,4,5])
ix_([1,2,4],[2,4,5])             在网格上评估函数的最佳方法
repmat(a, m, n)                  tile(a, (m, n))                                    用n份副本创建m a
[a b]                            concatenate((a,b),1)或者hstack((a,b))或            连接a和的列b
                                 column_stack((a,b))或c_[a,b]
[a; b]                           concatenate((a,b))或vstack((a,b))或r_[a,b]         连接a和的行b
max(max(a))                      a.max()                                            最大元素a（对于matlab，ndims（a）<= 2）
max(a)                           a.max(0)                                           每列矩阵的最大元素 a
max(a,[],2)                      a.max(1)                                           每行矩阵的最大元素 a
max(a,b)                         maximum(a, b)                                      比较a和b逐个元素，并返回每对中的最大值
norm(v)                          sqrt(v @ v) 要么 np.linalg.norm(v)                 L2矢量的规范 v
a & b                            logical_and(a,b)                                   逐个元素AND运算符（NumPy ufunc）请参阅备注LOGICOPS
a                                b                                                  logical_or(a,b)
bitand(a,b)                      a & b                                              按位AND运算符（Python native和NumPy ufunc）
bitor(a,b)                       a                                                  b
inv(a)                           linalg.inv(a)                                      方阵的逆 a
pinv(a)                          linalg.pinv(a)                                     矩阵的伪逆 a
rank(a)                          linalg.matrix_rank(a)                              二维数组/矩阵的矩阵秩 a
a\b                              linalg.solve(a,b)如果a是正方形; linalg.lstsq(a,b)  ax = b的解为x
                                 除此以外
b/a                              解决aT xT = bT                                     xa = b的解为x
[U,S,V]=svd(a)                   U, S, Vh = linalg.svd(a), V = Vh.T                 奇异值分解 a
chol(a)                          linalg.cholesky(a).T                               矩阵的cholesky分解（chol(a)在matlab中返回一个上三角矩阵，但
                                                                                    linalg.cholesky(a)返回一个下三角矩阵）
[V,D]=eig(a)                     D,V = linalg.eig(a)                                特征值和特征向量 a
[V,D]=eig(a,b)                   D,V = scipy.linalg.eig(a,b)                        特征值和特征向量a，b
[V,D]=eigs(a,k)                                                                     找到k最大的特征值和特征向量a
[Q,R,P]=qr(a,0)                  Q,R = scipy.linalg.qr(a)                           QR分解
[L,U,P]=lu(a)                    L,U = scipy.linalg.lu(a) 要么 LU,P=                LU分解（注：P（Matlab）==转置（P（numpy）））
                                 scipy.linalg.lu_factor(a)
conjgrad                         scipy.sparse.linalg.cg                             共轭渐变求解器
fft(a)                           fft(a)                                             傅立叶变换 a
ifft(a)                          ifft(a)                                            逆傅立叶变换 a
sort(a)                          sort(a) 要么 a.sort()                              对矩阵进行排序
[b,I] = sortrows(a,i)            I = argsort(a[:,i]), b=a[I,:]                      对矩阵的行进行排序
regress(y,X)                     linalg.lstsq(X,y)                                  多线性回归
decimate(x, q)                   scipy.signal.resample(x, len(x)/q)                 采用低通滤波的下采样
unique(a)                        unique(a)
squeeze(a)                       a.squeeze()

# 备注

子矩阵：使用该ix_命令可以使用索引列表完成对子矩阵的分配。例如，对于2D数组a，可能会做：ind=[1,3]; a[np.ix_(ind,ind)]+=100。

帮助：有MATLAB的没有直接等价which的命令，但命令help和source通常会列出其中函数所在的文件名。Python还有一个inspect模块（do import inspect），它提供了一个
getfile经常工作的模块。

索引：MATLAB®使用一个基于索引，因此序列的初始元素具有索引1.Python使用基于零的索引，因此序列的初始元素具有索引0.出现混淆和火焰，因为每个元素都有优点和缺点。一
种基于索引的方法与常见的人类语言使用一致，其中序列的“第一”元素具有索引1.基于零的索引简化了索引。另见prof.dr的文本。Edsger W. Dijkstra 。

范围：在MATLAB®中，0:5可以用作范围文字和“切片”索引（括号内）; 然而，在Python，构建体等0:5可以仅被用作切片指数（方括号内）。因此，r_创建了一些有点古怪的对象，
以使numpy具有类似的简洁范围构造机制。请注意，r_它不像函数或构造函数那样被调用，而是使用方括号进行索引，这允许在参数中使用Python的切片语法。

逻辑运算：＆或| 在NumPy中是按位AND / OR，而在Matlab＆和|中是逻辑AND / OR。任何具有重要编程经验的人都应该清楚这种差异。这两者似乎工作原理相同，但存在重要差异
。如果您使用过Matlab的＆或| 运算符，您应该使用NumPy ufuncs logical_and / logical_or。Matlab和NumPy的＆和|之间的显着差异运营商是：

  • 非逻辑{0,1}输入：NumPy的输出是输入的按位AND。Matlab将任何非零值视为1并返回逻辑AND。例如，NumPy中的（3和4）是0，而在Matlab中，3和4都被认为是逻辑真，而（3
    和4）返回1。
  • 优先级：NumPy的＆运算符优先于<和>之类的逻辑运算符; Matlab是相反的。

如果你知道你有布尔参数，你可以使用NumPy的按位运算符，但要注意括号，如：z =（x> 1）＆（x <2）。缺少NumPy运算符形式的logical_and和logical_or是Python设计的一个
不幸结果。

重塑与线性索引：Matlab总是允许使用标量或线性索引访问多维数组，而NumPy则不然。线性索引在Matlab程序中很常见，例如矩阵上的find()返回它们，而NumPy的查找行为则不
同。在转换Matlab代码时，可能需要首先将矩阵重新整形为线性序列，执行一些索引操作然后重新整形。由于重塑（通常）会在同一存储上生成视图，因此应该可以相当有效地执
行此操作。请注意，在NumPy中重新整形使用的扫描顺序默认为'C'顺序，而Matlab使用Fortran顺序。如果您只是简单地转换为线性序列，那么这无关紧要。但是如果要从依赖于扫
描顺序的Matlab代码转换重构，那么这个Matlab代码：z = reshape(x，3,4) 应该变成 z = x.reshape(3,4,order=’F’).copy() 。

# 自定义您的环境

在MATLAB®中，可用于自定义环境的主要工具是使用您喜欢的功能的位置修改搜索路径。您可以将此类自定义项放入MATLAB将在启动时运行的启动脚本中。

NumPy，或者更确切地说是Python，具有类似的功能。

  • 要修改Python搜索路径以包含您自己的模块的位置，请定义PYTHONPATH环境变量。
  • 要在启动交互式Python解释器时执行特定的脚本文件，请定义PYTHONSTARTUP环境变量以包含启动脚本的名称。

与MATLAB®不同，可以立即调用路径上的任何内容，使用Python，您需要先执行“import”语句，以使特定文件中的函数可访问。

例如，您可能会创建一个如下所示的启动脚本（注意：这只是一个示例，而不是“最佳实践”的声明）：

# Make all numpy available via shorter 'np' prefix
import numpy as np
# Make all matlib functions accessible at the top level via M.func()
import numpy.matlib as M
# Make some matlib functions accessible directly at the top level via, e.g. rand(3,3)
from numpy.matlib import rand,zeros,ones,empty,eye
# Define a Hermitian function
def hermitian(A, **kwargs):
    return np.transpose(A,**kwargs).conj()
# Make some shortcuts for transpose,hermitian:
#    np.transpose(A) --> T(A)
#    hermitian(A) --> H(A)
T = np.transpose
H = hermitian

# 链接

有关另一个MATLAB®/ NumPy交叉引用，请参见http://mathesaurus.sf.net/ 。

可以在主题软件页面中找到用于python科学工作的广泛工具列表。

MATLAB®和SimuLink®是The MathWorks的注册商标。

在 GitHub 上编辑此页
上次更新: 2019-9-23 19:23:30

← 其他杂项从源代码构建→

