
from cement import namespaces, hooks

def define_hook(namespace):
    """
    Define a hook namespace that plugins can register hooks in.
    """
    if hooks.has_key(namespace):
        raise CementRuntimeError, "Hook name '%s' already defined!" % namespace
    hooks[namespace] = []
    
    
def register_hook(**kwargs):
    """
    Decorator function for plugins to register hooks.  Used as:
    
    @register_hook()
    def my_hook():
        ...
    """
    def decorate(func):
        if not hooks.has_key(func.__name__):
            #raise CementRuntimeError, "Hook name '%s' is not define!" % func.__name__
            log.warn("Hook name '%s' is not define!" % func.__name__)
            return func
        # (1) is the list of registered hooks in the namespace
        hooks[func.__name__].append(
            (int(kwargs.get('weight', 0)), func.__name__, func)
        )
        return func
    return decorate


def run_hooks(namespace, *args, **kwargs):
    """
    Run all defined hooks in the namespace.  Returns a list of return data.
    """
    if not hooks.has_key(namespace):
        CementRuntimeError, "Hook name '%s' is not defined!" % namespace
    hooks[namespace].sort() # will order based on weight
    for hook in hooks[namespace]:
        res = hook[2](*args, **kwargs)
        
        # FIXME: Need to validate the return data somehow
        yield res