import functools

def load_data(fun=None):
    res = []
    with open('input') as input:
        res = input.read().splitlines()
    if fun is not None:
        res = [fun(line) for line in res]
    return res

def load_list_of_ints():
    res = []
    with open('input') as input:
        res = [int(i) for line in
               input.read().splitlines() for i in line.split(',')]
    return res

def load_lists_of_strings():
    data = [line.rstrip('\r\n').split(',') for line in open('input')]
    return data

def trace_fn(fn):
    @functools.wraps(fn)
    def wrapper_debug(*args, **kargs):
        args_repr = [repr(a) for a in args]
        kargs_repr = [f'{k}={v!r}' for k,v in kargs.items()]
        sig = ', '.join(args_repr + kargs_repr)
        print(f'Calling {fn.__name__}({sig})')
        res = fn(*args, **kargs)
        print(f'{fn.__name__!r} returned {res!r}')
        return res
    return wrapper_debug
