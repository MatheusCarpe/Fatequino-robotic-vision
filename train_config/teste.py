import sys
import gc

import string
import random

def get_obj_size(obj):
    marked = {id(obj)}
    obj_q = [obj]
    sz = 0

    while obj_q:
        sz += sum(map(sys.getsizeof, obj_q))

        # Lookup all the object referred to by the object in obj_q.
        # See: https://docs.python.org/3.7/library/gc.html#gc.get_referents
        all_refr = ((id(o), o) for o in gc.get_referents(*obj_q))

        # Filter object that are already marked.
        # Using dict notation will prevent repeated objects.
        new_refr = {o_id: o for o_id, o in all_refr if o_id not in marked and not isinstance(o, type)}

        # The new obj_q will be the ones that were not marked,
        # and we will update marked with their ids so we will
        # not traverse them again.
        obj_q = new_refr.values()
        marked.update(new_refr.keys())

    return sz

if __name__ == "__main__":

    arr = []

    for i in range(1, 1000001):
        arr.append({
            "id": i,
            "name": ''.join(random.choices(string.ascii_uppercase + string.digits, k=255)),
            "type": "Funcionário",
            "status": "UPDATED"
        })

    print(get_obj_size(arr))

#5807708