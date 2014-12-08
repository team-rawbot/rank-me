def memoize(function):
    """
    Copied from http://stackoverflow.com/questions/815110/is-there-a-decorator-to-simply-cache-function-return-values
    """
    memo = {}

    def wrapper(*args):
        if args in memo:
            return memo[args]
        else:
            rv = function(*args)
        memo[args] = rv
        return rv
    return wrapper
