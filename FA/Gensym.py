# This class is used to greatly reduce the time it takes to generate a unique statename, by simply incrementing a
# counter everytime a new statename is requested. In order for it to work well however, state names should always be
# generated using this. If they are not, no error will result, since checks are done to ensure that any two
# nfas can be combined using the same state symbols, although this does result in a loss of efficiency, and could be
# removed if desired. This does put a limit to the number of states in the NFA - the maximum integer value in the
# system. However, on a 64bit machine, this is 9223372036854775807, and probably shouldn't pose an issue.


class Gensym:
    def __init__(self):
        self.symcount = int(0)

    def __call__(self, *args, **kwargs):
        self.symcount += 1
        return self.symcount
