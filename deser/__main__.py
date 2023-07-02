from deser import core, types

@core.serializable
class A:
    a: types.U8
    b: types.I16

@core.serializable
class B:
    i: types.U16
    a: A
    arr: types.Array[types.U32, types.Literal[3]]

a = B(32, A(0, 2), [1, 2, 3])
print(a.serialize())
raw = a.serialize()
print(B.deserialize(raw))
