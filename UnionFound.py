
class UF (object):

    def __init__(self, N):
        self.id = [x for x in range(N)]
        self.sz = [1] * N
    '''
    return int
    '''
    def root(self, i):
        while i != self.id[i]:
            i = self.id[i]
        return i

    '''
    return void
    '''
    def union (self, p, q):
        i = self.root(p)
        j = self.root(q)
        if i == j:
            return
        # self.id[i] = j
        if self.sz[i] < self.sz[j]:
            self.id[i] = j
            self.sz[j] += self.sz[i]
        else:
            self.id[j] = i
            self.sz[i] += self.sz[j]

    '''
    return boolean
    '''
    def connected (self, p, q):
        return self.root(p) == self.root(q)

    '''
    calulate number of classes
    return int
    '''
    def count(self):
        s = 0
        for i in range(len(self.id)):
            if self.id[i] == i:
                s += 1
        return s

    '''
    output classification details
    '''
    def details(self):
        ret = []
        for i in range(len(self.id)):
            if self.id[i] == i:
                ret.append([i])

        # print len(ret)
        for i in range(len(self.id)):
            if not self.id[i] == i:
                for c in ret:
                    if c[0] == self.root(i):
                        c.append(i)
                        break

        return ret