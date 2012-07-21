# rediscoll: pythonic data structure translated to redis.
# (C) 2012 Francesco Romani <fromani . gmail . com>
# based on the redisco.collections module of the redisco package.
# LICENSE: same as the original (follows) 
#
# Copyright (c) 2010 Tim Medina
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

"""
This module contains the container classes to create objects
that persist directly in a Redis server.
"""

import collections

class ConnectionError(Exception):
    pass


class Container(object):
    """Create a container object saved in Redis.

    Arguments:
        key -- the Redis key this container is stored at
        db  -- the Redis client object. Default: None

    When ``db`` is not set, the gets the default connection from
    ``redisco.connection`` module.
    """

    def __init__(self, key, db=None):
        self.key = key
        if callable(db):
            self._db = db(key)
        else:
            self._db = db

    def clear(self):
        """Remove container from Redis database."""
        del self.db[self.key]

    @property
    def db(self):
        if self._db:
            return self._db
        else:
            raise ConnectionError()

class Set(Container):
    """A set stored in Redis."""

    def sadd(self, value):
        """Add the specified member to the Set."""
        return self.db.sadd(self.key, value)

    def srem(self, value):
        return self.db.srem(self.key, value)

    def spop(self):
        """Remove and return (pop) a random element from the Set."""
        return self.db.spop(self.key)

    def discard(self, value):
        """Remove element elem from the set if it is present."""
        self.srem(value)

    def __repr__(self):
        return "<%s '%s' %s>" % (self.__class__.__name__, self.key,
                self.members)

    def isdisjoint(self, other):
        """Return True if the set has no elements in common with other."""
        return not bool(self.db.sinter([self.key, other.key]))

    def issubset(self, other):
        """Test whether every element in the set is in other."""
        return self <= other

    def __le__(self, other):
        return self.db.sinter([self.key, other.key]) == self.all()

    def __lt__(self, other):
        """Test whether the set is a true subset of other."""
        return self <= other and self != other

    def __eq__(self, other):
        if other.key == self.key:
            return True
        slen, olen = len(self), len(other)
        if olen == slen:
            return self.members == other.members
        else:
            return False

    def issuperset(self, other):
        """Test whether every element in other is in the set."""
        return self >= other

    def __ge__(self, other):
        """Test whether every element in other is in the set."""
        return self.db.sinter([self.key, other.key]) == other.all()

    def __gt__(self, other):
        """Test whether the set is a true superset of other."""
        return self >= other and self != other

    # SET Operations
    def union(self, key, *others):
        if not isinstance(key, str) and not isinstance(key, unicode):
            raise ValueError("Expect a (unicode) string as key")
        key = unicode(key)
        """Return a new set with elements from the set and all others."""
        self.db.sunionstore(key, [self.key] + [o.key for o in others])
        return Set(key)

    def intersection(self, key, *others):
        if not isinstance(key, str) and not isinstance(key, unicode):
            raise ValueError("Expect a (unicode) string as key")
        key = unicode(key)
        """Return a new set with elements common to the set and all others."""
        self.db.sinterstore(key, [self.key] + [o.key for o in others])
        return Set(key)

    def difference(self, key, *others):
        if not isinstance(key, str) and not isinstance(key, unicode):
            raise ValueError("Expect a (unicode) string as key")
        key = unicode(key)
        """Return a new set with elements in the set that are not in the others."""
        self.db.sdiffstore(key, [self.key] + [o.key for o in others])
        return Set(key)

    def update(self, *others):
        """Update the set, adding elements from all others."""
        self.db.sunionstore(self.key, [self.key] + [o.key for o in others])

    def __ior__(self, other):
        self.db.sunionstore(self.key, [self.key, other.key])
        return self

    def intersection_update(self, *others):
        """Update the set, keeping only elements found in it and all others."""
        self.db.sinterstore(self.key, [o.key for o in [self.key] + others])

    def __iand__(self, other):
        self.db.sinterstore(self.key, [self.key, other.key])
        return self

    def difference_update(self, *others):
        """Update the set, removing elements found in others."""
        self.db.sdiffstore(self.key, [o.key for o in [self.key] + others])

    def __isub__(self, other):
        self.db.sdiffstore(self.key, [self.key, other.key])
        return self

    def all(self):
        return self.db.smembers(self.key)
    members = property(all)

    def copy(self, key):
        """Copy the set to another key and return the new Set.

        WARNING: If the key exists, it overwrites it.
        """
        copy = Set(key=key, db=self.db)
        copy.clear()
        copy |= self
        return copy

    def __iter__(self):
        return self.members.__iter__()

    def sinter(self, *other_sets):
        """Performs an intersection between Sets.

        Returns a set of common members. Uses Redis.sinter.
        """
        return self.db.sinter([self.key] + [s.key for s in other_sets])

    def sunion(self, *other_sets):
        """Union between Sets.

        Returns a set of common members. Uses Redis.sunion.
        """
        return self.db.sunion([self.key] + [s.key for s in other_sets])

    def sdiff(self, *other_sets):
        """Union between Sets.

        Returns a set of common members. Uses Redis.sdiff.
        """
        return self.db.sdiff([self.key] + [s.key for s in other_sets])

    def scard(self):
        return self.db.scard(self.key)

    def sismember(self, value):
        return self.db.sismember(self.key, value)

    def smembers(self):
        return self.db.smembers(self.key)

    def srandmember(self):
        return self.db.srandmember(self.key)

    add = sadd
    pop = spop
    remove = srem
    __contains__ = sismember
    __len__ = scard


class List(Container):

    def all(self):
        """Returns all items in the list."""
        return self.lrange(0, -1)
    members = property(all)

    def llen(self):
        return self.db.llen(self.key)

    __len__ = llen

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.lindex(index)
        elif isinstance(index, slice):
            indices = index.indices(len(self))
            return self.lrange(indices[0], indices[1] - 1)
        else:
            raise TypeError

    def __setitem__(self, index, value):
        self.lset(index, value)

    def lrange(self, start, stop):
        return self.db.lrange(self.key, start, stop)

    def lpush(self, value):
        return self.db.lpush(self.key, value)

    def rpush(self, value):
        return self.db.rpush(self.key, value)

    def extend(self, iterable):
        """Extend list by appending elements from the iterable."""
        map(lambda i: self.rpush(i), iterable)

    def count(self, value):
        """Return number of occurrences of value."""
        return self.members.count(value)

    def lpop(self):
        return self.db.lpop(self.key)

    def rpop(self):
        return self.db.rpop(self.key)

    def rpoplpush(self, key):
        """
        Remove an element from the list,
        atomically add it to the head of the list indicated by key
        """
        return self.db.rpoplpush(self.key, key)

    def lrem(self, value, num=1):
        """Remove first occurrence of value."""
        return self.db.lrem(self.key, value, num)

    def reverse(self):
        """Reverse in place."""
        r = self[:]
        r.reverse()
        self.clear()
        self.extend(r)

    def copy(self, key):
        """Copy the list to a new list.

        WARNING: If key exists, it clears it before copying.
        """
        copy = List(key, self.db)
        copy.clear()
        copy.extend(self)
        return copy

    def ltrim(self, start, end):
        """Trim the list from start to end."""
        return self.db.ltrim(self.key, start, end)

    def lindex(self, value):
        return self.db.lindex(self.key, value)

    def lset(self, index, value=0):
        return self.db.lset(self.key, index, value)

    def __iter__(self):
        return self.members.__iter__()

    def __repr__(self):
        return "<%s '%s' %s>" % (self.__class__.__name__, self.key,
                self.members)

    __len__ = llen
    remove = lrem
    trim = ltrim
    shift = lpop
    unshift = lpush
    pop = rpop
    pop_onto = rpoplpush
    push = rpush
    append = rpush




class TypedList(object):
    """Create a container to store a list of objects in Redis.

    Arguments:
        key -- the Redis key this container is stored at
        target_type -- can be a Python object or a redisco model class.

    Optional Arguments:
        type_args -- additional args to pass to type constructor (tuple)
        type_kwargs -- additional kwargs to pass to type constructor (dict)

    If target_type is not a redisco model class, the target_type should
    also a callable that casts the (string) value of a list element into
    target_type. E.g. str, unicode, int, float -- using this format:

        target_type(string_val_of_list_elem, *type_args, **type_kwargs)

    target_type also accepts a string that refers to a redisco model.
    """

    def __init__(self, key, target_type, type_args=[], type_kwargs={}, **kwargs):
        self.list = List(key, **kwargs)
        self.klass = self.value_type(target_type)
        self._klass_args = type_args
        self._klass_kwargs = type_kwargs
        from models.base import Model
        self._redisco_model = issubclass(self.klass, Model)

    def value_type(self, target_type):
        if isinstance(target_type, basestring):
            t = target_type
            from models.base import get_model_from_key
            target_type = get_model_from_key(target_type)
            if target_type is None:
                raise ValueError("Unknown Redisco class %s" % t)
        return target_type

    def typecast_item(self, value):
        if self._redisco_model:
            return self.klass.objects.get_by_id(value)
        else:
            return self.klass(value, *self._klass_args, **self._klass_kwargs)

    def typecast_iter(self, values):
        if self._redisco_model:
            return filter(lambda o: o is not None, [self.klass.objects.get_by_id(v) for v in values])
        else:
            return [self.klass(v, *self._klass_args, **self._klass_kwargs) for v in values]

    def all(self):
        """Returns all items in the list."""
        return self.typecast_iter(self.list.all())

    def __len__(self):
        return len(self.list)

    def __getitem__(self, index):
        val = self.list[index]
        if isinstance(index, slice):
            return self.typecast_iter(val)
        else:
            return self.typecast_item(val)

    def typecast_stor(self, value):
        if self._redisco_model:
            return value.id
        else:
            return value

    def append(self, value):
        self.list.append(self.typecast_stor(value))

    def extend(self, iter):
        self.list.extend(map(lambda i: self.typecast_stor(i), iter))

    def __setitem__(self, index, value):
        self.list[index] = self.typecast_stor(value)

    def __iter__(self):
        for i in xrange(len(self.list)):
            yield self[i]

    def __repr__(self):
        return repr(self.typecast_iter(self.list))

class SortedSet(Container):

    def __getitem__(self, index):
        if isinstance(index, slice):
            return self.zrange(index.start, index.stop)
        else:
            return self.zrange(index, index)[0]

    def score(self, member):
        """Returns the score of member."""
        return self.zscore(member)

    def __contains__(self, val):
        return self.zscore(val) is not None

    @property
    def members(self):
        """Returns the members of the set."""
        return self.zrange(0, -1)

    @property
    def revmembers(self):
        """Returns the members of the set in reverse."""
        return self.zrevrange(0, -1)

    def __iter__(self):
        return self.members.__iter__()

    def __reversed__(self):
        return self.revmembers.__iter__()

    def __repr__(self):
        return "<%s '%s' %s>" % (self.__class__.__name__, self.key,
                self.members)

    @property
    def _min_score(self):
        return self.zscore(self.__getitem__(0))

    @property
    def _max_score(self):
        return self.zscore(self.__getitem__(-1))

    def lt(self, v, limit=None, offset=None):
        """Returns the list of the members of the set that have scores
        less than v.
        """
        if limit is not None and offset is None:
            offset = 0
        return self.zrangebyscore(self._min_score, "(%f" % v,
                start=offset, num=limit)

    def le(self, v, limit=None, offset=None):
        """Returns the list of the members of the set that have scores
        less than or equal to v.
        """
        if limit is not None and offset is None:
            offset = 0
        return self.zrangebyscore(self._min_score, v,
                start=offset, num=limit)

    def gt(self, v, limit=None, offset=None):
        """Returns the list of the members of the set that have scores
        greater than v.
        """
        if limit is not None and offset is None:
            offset = 0
        return self.zrangebyscore("(%f" % v, self._max_score,
                start=offset, num=limit)

    def ge(self, v, limit=None, offset=None):
        """Returns the list of the members of the set that have scores
        greater than or equal to v.
        """
        if limit is not None and offset is None:
            offset = 0
        return self.zrangebyscore("(%f" % v, self._max_score,
                start=offset, num=limit)

    def between(self, min, max, limit=None, offset=None):
        """Returns the list of the members of the set that have scores
        between min and max.
        """
        if limit is not None and offset is None:
            offset = 0
        return self.zrangebyscore(min, max,
                start=offset, num=limit)

    def zadd(self, member, value=1):
        return self.db.zadd(self.key, member, value)

    def zrem(self, value):
        return self.db.zrem(self.key, value)

    def zincrby(self, att, value=1):
        return self.db.zincrby(self.key, value, att)

    def zrevrank(self, member):
        return self.db.zrevrank(self.key, member)

    def zrange(self, start, stop, withscores=False):
        return self.db.zrange(self.key, start, stop, withscores=withscores)

    def zrevrange(self, start, end, **kwargs):
        return self.db.zrevrange(self.key, start, end, **kwargs)

    def zrangebyscore(self, min, max, **kwargs):
        return self.db.zrangebyscore(self.key, min, max, **kwargs)

    def zcard(self):
        return self.db.zcard(self.key)

    def zscore(self, value):
        return self.db.zscore(self.key, value)

    def zremrangebyrank(self, start, stop):
        return self.db.zremrangebyrank(self.key, start, stop)

    def zremrangebyscore(self, min_value, max_value):
        return self.db.zremrangebyscore(self.key, min_value, max_value)

    def zrank(self, value):
        return self.db.zrank(self.key, value)

    def eq(self, value):
        return self.zrangebyscore(value, value)

    __len__ = zcard
    revrank = zrevrank
    score = zscore
    rank = zrank
    incr_by = zincrby
    add = zadd
    remove = zrem


class NonPersistentList(object):
    def __init__(self, l):
        self._list = l

    @property
    def members(self):
        return self._list

    def __iter__(self):
        return iter(self.members)

    def __len__(self):
        return len(self._list)


class Hash(Container, collections.MutableMapping):

    def __iter__(self):
        return self.hgetall().__iter__()

    def __repr__(self):
        return "<%s '%s' %s>" % (self.__class__.__name__, self.key, self.hgetall())

    def _set_dict(self, new_dict):
        self.clear()
        self.update(new_dict)

    def hlen(self):
        return self.db.hlen(self.key)

    def hset(self, member, value):
        return self.db.hset(self.key, member, value)

    def hdel(self, member):
        return self.db.hdel(self.key, member)

    def hkeys(self):
        return self.db.hkeys(self.key)

    def hgetall(self):
        return self.db.hgetall(self.key)

    def hvals(self):
        return self.db.hvals(self.key)

    def hget(self, field):
        return self.db.hget(self.key, field)

    def hexists(self, field):
        return self.db.hexists(self.key, field)

    def hincrby(self, field, increment=1):
        return self.db.hincrby(self.key, field, increment)

    def hmget(self, fields):
        return self.db.hmget(self.key, fields)

    def hmset(self, mapping):
        """
        """
        return self.db.hmset(self.key, mapping)

    keys = hkeys
    values = hvals
    _get_dict = hgetall
    __getitem__ = hget
    __setitem__ = hset
    __delitem__ = hdel
    __len__ = hlen
    __contains__ = hexists
    dict = property(_get_dict, _set_dict)

# EOF

