"grp" --- The group database
****************************

======================================================================

This module provides access to the Unix group database. It is
available on all Unix versions.

Group database entries are reported as a tuple-like object, whose
attributes correspond to the members of the "group" structure
(Attribute field below, see "<pwd.h>"):

+---------+-------------+-----------------------------------+
| 索引    | 属性        | 意义                              |
|=========|=============|===================================|
| 0       | gr_name     | the name of the group             |
+---------+-------------+-----------------------------------+
| 1       | gr_passwd   | the (encrypted) group password;   |
|         |             | often empty                       |
+---------+-------------+-----------------------------------+
| 2       | gr_gid      | the numerical group ID            |
+---------+-------------+-----------------------------------+
| 3       | gr_mem      | all the group member's  user      |
|         |             | names                             |
+---------+-------------+-----------------------------------+

The gid is an integer, name and password are strings, and the member
list is a list of strings. (Note that most users are not explicitly
listed as members of the group they are in according to the password
database.  Check both databases to get complete membership
information.  Also note that a "gr_name" that starts with a "+" or "-"
is likely to be a YP/NIS reference and may not be accessible via
"getgrnam()" or "getgrgid()".)

本模块定义如下内容：

grp.getgrgid(gid)

   Return the group database entry for the given numeric group ID.
   "KeyError" is raised if the entry asked for cannot be found.

   3.6 版后已移除: Since Python 3.6 the support of non-integer
   arguments like floats or strings in "getgrgid()" is deprecated.

grp.getgrnam(name)

   Return the group database entry for the given group name.
   "KeyError" is raised if the entry asked for cannot be found.

grp.getgrall()

   Return a list of all available group entries, in arbitrary order.

参见:

  Module "pwd"
     An interface to the user database, similar to this.

  模块 "spwd"
     针对影子密码数据库的接口，与本模块类似。
