#!/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'cping.ju'

import abc


class AbstractCondition(object):
    """
    defense condition
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, key, threshold, timeout):
        self.key = key
        self.threshold = threshold
        self.timeout = timeout

    def increase_value(self):
        """
        increase the condition

        """
        try:
            self.get_backend().increase(self.key, 1, self.timeout)
        except:
            pass

    def decrease_value(self):
        """
        decrease the condition
        """
        try:
            self.get_backend().decrease(self.key, 1, self.timeout)
        except:
            pass

    def reach(self):
        try:
            value = self.get_backend().get(self.key)
            if value:
                return value >= self.threshold
            else:
                return False
        except:
            pass

    def destroy(self):
        try:
            self.get_backend().remove(self.key)
        except:
            pass

    @abc.abstractmethod
    def get_backend(self):
        """
        cache server or persistence
        """
        pass


class SimpleCondition(AbstractCondition):
    def __init__(self, key, threshold, timeout, backend):
        super(SimpleCondition, self).__init__(key, threshold, timeout)
        self.backend = backend

    def get_backend(self):
        return self.backend


class AbstractAction(object):
    """
    do something when reach the condition
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def process(self, condition):
        pass

    @abc.abstractmethod
    def accept(self, condition):
        pass


class ResponseAction(AbstractAction):
    def __init__(self, response):
        self.response = response

    def process(self, condition):
        return self.response

    def accept(self, condition):
        return True


class Defense:
    """
    single defense
    """

    def __init__(self, condition, action):
        self.action = action
        self.condition = condition

    def is_condition_reached(self):
        if self.condition.reach():
            return self.action.process(self.condition)

        return None

    def destroy(self):
        self.condition.destroy()


class CompositeDefense(Defense):
    """
    composite defense
    """

    def __init__(self):
        super(CompositeDefense, self).__init__(None, None)
        self.defenses = []

    def put_defense(self, defense):
        self.defenses.append(defense)

    def is_condition_reached(self):

        for defense in self.defenses:
            res = defense.is_condition_reached()
            if res:
                return res
        return None

    def destroy(self):
        for defense in self.defenses:
            defense.destroy()

        del self.defenses[:]
