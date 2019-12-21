import types

A = types.new_class('A', bases=(object), 'a'='wang', 'name'="yanwei")

b = A()
print(type(b), b)
