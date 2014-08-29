#!/usr/bin/python
# vim: set fileencoding=utf8 :

__author__ = 'cping.ju'

import abc


class AbstractBackend(object):
    """
    cache system
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def increase(self, key, step=1, timeout=0):
        """
        increase the value of key with step,
        step must be positive
        """
        pass

    @abc.abstractmethod
    def decrease(self, key, step=1, timeout=0):
        """
        decrease the value of key with step,
        step must be positive
        """
        pass

    @abc.abstractmethod
    def get(self, key):
        pass

    @abc.abstractmethod
    def set(self, key, value, timeout):
        pass

    @abc.abstractmethod
    def remove(self, key):
        pass


class BackendAdaptor(AbstractBackend):
    """
    adaptor of cache system, all subclasses should inherit this class,
    and subclass can override one or more method
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(BackendAdaptor, cls).__new__(cls)

        return cls.instance


    def increase(self, key, step=1, timeout=0):
        pass

    def decrease(self, key, step=1, timeout=0):
        pass

    def get(self, key):
        pass

    def set(self, key, value, timeout):
        pass

    def remove(self, key):
        pass


class RedisBackend(BackendAdaptor):
    """
    redis backend
    """

    def __init__(self, real_backend=None):

        if not hasattr(self, 'real_backend'):
            if not real_backend:
                # default
                import redis

                pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
                real_backend = redis.Redis(connection_pool=pool)

            self.real_backend = real_backend

    def increase(self, key, step=1, timeout=0):

        self.real_backend.incr(key, step)
        self.real_backend.expire(key, timeout)

    def decrease(self, key, step=1, timeout=0):

        self.real_backend.decr(key, step)
        self.real_backend.expire(key, timeout)

    def get(self, key):
        return self.real_backend.get(key)

    def set(self, key, value, timeout):
        self.real_backend.setex(key, value, timeout)

    def remove(self, key):
        self.real_backend.delete(key)