Dynamic Module Replacing
========================

This example shows the possibility of dynamically replacing the
working Python modules. We use this ability to change the source code
of threaded tasks.


    thread Task A started
    thread Task B started
    Task A tick
    Task B tick
    Task B tick
    Task A tick
    Task B tick
    Task A tick
    Task B tick
    thread Task B finished
    thread Task Bzz started
    Task Bzz tick
    Task A tick
    Task Bzz tick
    Task A tick
    Task Bzz tick
    Task Bzz tick
    thread Task B started
    thread Task Bzz finished
    Task B tick
    Task A tick
    ^C
    thread Task B finished
    thread Task A finished
