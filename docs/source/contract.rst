How to create a smart contract
==============================

A smart contract in pyledger is a function that returns an instance of
:py:class:`pyledger.contract.Builder`. This object is a helper to manage the
attributes of the smart contract and the methods that may or may not modify
those attributes. The simplest smart contract you may think of is one that
just returns the string "Hello". 

.. code-block:: python

    from pyledger.handlers import make_tornado
    from pyledger.contract import Builder
    from pyledger.config import args
    import tornado.ioloop


    def hello():
        def say_hello(attrs):
            return attrs, 'Hello'

        contract = Builder('Hello')
        contract.add_method(say_hello)

        return contract


    if __name__ == '__main__':
        application = make_tornado(hello)
        application.listen(args.port)
        tornado.ioloop.IOLoop.instance().start()

If you run this snippet as script without options, you will be able to
connect to this server with the command line client provided by pyledger,
called ``pyledger-shell``::

    (env) $> pyledger-shell
    PyLedger simple client
    (http://localhost:8888)> contracts
         Hello
    (http://localhost:8888)> api Hello
       say_hello (  )

    (http://localhost:8888)> call Hello say_hello
    Hello
    (http://localhost:8888)>


This almost trival example is useful to understand the very basics about how
the contracts are created. The contract is called *Hello* which is the argument
of the Builder instance. The method *say_hello* gets no arguments and it
modifies no attributes, but it must get the attributes as an argument and
return them anyways.  If an additional argument, like the ``Hello`` string,
is returned by the method, it is given as a second return argument.

Attributes
----------

Let's change the previous example a little by adding an attribute to the
contract. For instance, we will make a counter of the amount of times the
contract has greeted us.

.. code-block:: python

    def hello():
        def say_hello(attrs):
            attrs.counter += 1
            return attrs, 'Hello {}'.format(attrs.counter)

        contract = Builder('Hello')
        contract.add_attribute('counter', 0)
        contract.add_method(say_hello)

        return contract

A session with this new smart contract would be as follows::

    (http://localhost:8888)> call Hello say_hello
    Hello 1
    (http://localhost:8888)> call Hello say_hello
    Hello 2
    (http://localhost:8888)> status Hello
    {'counter': 2}


Note that the contract function pretty much looks like an object, it has
attributes and methods that change those attributes. It is also quite similar
as how Solidity defines the smart contracts, with attributes and
methods that modify them. Pyledger is a little more explicit.

We can also define methods with arguments, and here's one of the important
particularities of pyledger: *all the arguments but the first one (attrs)
must be type annotated*. For instance, this is a contract that greets with a
name, that is passed as a parameter.

.. code-block:: python

    def hello():
        def say_hello(attrs, name: str):
            attrs.counter += 1
            return attrs, 'Hello {} for time #{}'.format(name, attrs.counter)

        contract = Builder('Hello')
        contract.add_attribute('counter', 0)
        contract.add_method(say_hello)

        return contract


A smart contract must expose an API, and type annotation is needed to let the
client and any user of the contract to know which type the arguments must be::

    (env) $> pyledger-shell
    PyLedger simple client
    (http://localhost:8888)> api Hello
       say_hello ( name [str] )

    (http://localhost:8888)> call Hello say_hello Guillem
    Hello Guillem for time #1
    (http://localhost:8888)> call Hello say_hello Guillem
    Hello Guillem for time #2
    (http://localhost:8888)> status Hello
    {'counter': 2}
    (http://localhost:8888)>


With these features, the smart contracts can be as complex as needed. One can
store information of any kind within the arguments, that are the ones that
define the status of the contract.

.. important::

    If you want the contract to be fast and you want to avoid obscure bugs
    too, keep your attributes as primitive python types.


Exceptions
----------

Contracts can raise only a generic exception of type :py:class:`Exception`.
The goal is only to inform the user that the operation has not been
successful. Note that the methods that return no additional value send back
to the client the string *SUCCESS*. This means that the client is always
waiting for a message to come.

We will introduce some very simple exception that checks the most common
mispelling of my name

.. code-block:: python

    def hello():
        def say_hello(attrs, name: str):
            if name == 'Guillen':
                raise Exception('You probably mispelled Guillem')

            attrs.counter += 1
            return attrs, 'Hello {} for time #{}'.format(name, attrs.counter)

        contract = Builder('Hello')
        contract.add_attribute('counter', 0)
        contract.add_method(say_hello)

        return contract

And how the exception is handled at the client side::

    (env) $> pyledger-shell
    PyLedger simple client
    (http://localhost:8888)> call Hello say_hello Guillem
    Hello Guillem for time #1
    (http://localhost:8888)> call Hello say_hello Guillen
    You probably mispelled Guillem
    (http://localhost:8888)> call Hello say_hello Guillem
    Hello Guillem for time #2


Docstrings of the classes cited in this section
-----------------------------------------------

.. autoclass:: pyledger.contract.Builder
   :members: add_method, add_attribute
