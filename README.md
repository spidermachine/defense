defense
=======

A simple defense module for python, which can be used with web or non-web framework.

construction
============

The defense module is composed of four parts:

- Condition: stored as (key, value, threshold, timeout). By increasing/decreasing value, threshold can be reached.
- Backend: cache/persistence of condition.
- Action: triggered when condition reached.
- Defense: composite of condition and action.

The following diagram indicates the whole construction.

.. image:: ./diagram.png

How to use it
=============
Now this module use redis as cache backend, but you can redefine your backend.

**use redis as cache backend.**

    from backend import RedisBackend
    from defense import SimpleCondition, ResponseAction, Defense
    
    import redis
    #initial redis
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
    real_backend = redis.Redis(connection_pool=pool)
    #cache backend
    redis_backend = RedisBackend(real_backend)
    #condition
    condition = SimpleCondition(key, limited, timeout, redis_backend)   
    #action
    action = ResponseAction(HttpResponse('ok'))
    
    defense = Defense(condition, action)
    
    #increase the value
    condition.increase_value()
    
    #decrease the value
    condition.decrease_value()
    
    #execute the action when condition reached, the result indicate whether condition reached,
    #None means not reached, otherwise reached
    result = defense.is_condition_reached()
        
        
**redefine your backend**

your backend should inherit BackendAdaptor, override one or more method. as following code,
    
    class MemBackend(BackendAdaptor):
    
        def __init__(self, memcached):
            self.memcached = memcached
            
        def increase(self, key, step, timeout):
            ......
            
        def decrease(self, key, step, timeout):
            ......
            
        #override other method
        ......


**use composite defense**

    from defense import CompositeDefense
    ......
    ip_defense = Defense(ip_condition, ip_action)
    login_defense = Defense(login_condition, login_action)
    
    defense = CompositeDefense()
    defense.push(ip_defense)
    defense.push(login_defense)
    
    result = defense.is_condition_reached()
    

License
=======
The MIT License (MIT)

Copyright (c) 2014 spidermachine

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
