    """ action_prototype.py:
            A prototype for the new Extend-A-Class Action definition system. """

    """ So, we have a list of actions. It's easy to find them since we just
        regex out the first word and check it against the list of actions.

        The arguments are similarly easy to get: just split the rest of the string.

        It's a different problem to change those arguments to objects instead of
        just the names of the objects but let's assume that an Action
        is passed either nothing, a single element, or an ordered pair.


        I've made some example Actions. I think they're pretty good - I especially
        like being able to just use Python logic.

        The ability to call on Engine methods is SUPREMELY important. As in,
        it's how anything gets done around here. Having aliases to simplify
        calls is a good thing, I like it.

        I just need to test these babies out...
    """

    action_list = [x for x in dir() if "__" not in x] 

    class Take(Action):
    id_ = "take"

    def zero(act):
        E.puts("What are you picking up?")

    def one(act, arg):
        if arg.isProp():
            E.puts("That's not the sort of thing you can take.")
        else:
            E.move(arg, E.loc, '_') 

class Cry(Action):
    id_ = "cry"

    def zero(act):
        E.puts("You cry for a while but don't feel any better.")

    def one(act, arg):
        E.err("Input > Max")

    def two(act, a, b):
        E.err("Input > Max")

class Throw(Action):
    prep = "at"
    id_ = "throw"
    aliases = ["toss", "chuck"]

    def zero(act):
        E.err("0 < Min")

    def one(act, arg):
        if not arg.is_("fragile"):
            E.move(arg, E.inventory, E.loc)
            if arg.is_("wooden"):
                E.puts("Thud!")
            elif arg.is_("metal"):
                E.puts("Clang!")
            elif arg.is_("stone"):
                E.puts("It makes a hard rocky noise against the ground.")
            else:
                E,puts("Thud.")
            E.puts("The %s has been thrown onto the ground." % arg.nickname)
        else:
            E,remove(arg, '_')
            E.puts("You smash the %s to pieces. The poor thing." % arg.name)

    def two(act, ammo, target):
        act.one(ammo)
