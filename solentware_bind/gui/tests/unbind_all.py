# unbind_all.py
# Copyright 2022 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Demonstrate sequences not being unbound by unbind_all."""

import tkinter


if __name__ == "__main__":

    def callback(event):
        """Avoid defining a lambda in each bind call."""

    widget = tkinter.Text()

    widget.bind(sequence="a", func=callback)
    widget.tag_bind(tkinter.SEL, "b", callback)
    print("After establish bindings")
    print(widget.bind())
    # tkinter.Text.tag_bind does not support Tk's 'tag bind' query format,
    # but the appropriate invokation of tk.call() does answer the query.
    # print(widget.tag_bind(tkinter.SEL))
    print(widget.tk.call(widget._w, "tag", "bind", tkinter.SEL))
    print(repr(widget.bind("a")))
    print(repr(widget.tk.call(widget._w, "tag", "bind", tkinter.SEL, "b")))
    widget.unbind_all("a")
    widget.unbind_all("b")
    print("After unbind_all")
    print(widget.bind())
    print(widget.tk.call(widget._w, "tag", "bind", tkinter.SEL))
    print(repr(widget.bind("a")))
    print(repr(widget.tk.call(widget._w, "tag", "bind", tkinter.SEL, "b")))
    print("Huh: does above mean unbind_all has not done anything?")
    print("Above expects 'a' bindings to disappear; maybe not 'b' bindings.")
    print(repr(widget.bind("a", "")))
    print(repr(widget.bind("a")))
    print(repr(widget.tk.call(widget._w, "tag", "bind", tkinter.SEL, "b", "")))
    print(repr(widget.tk.call(widget._w, "tag", "bind", tkinter.SEL, "b")))
