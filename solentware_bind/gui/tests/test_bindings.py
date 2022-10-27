# test_bindings.py
# Copyright 2022 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""bindings tests.

tkinter.SEL is a 'ready-made' tag which can be used for the tag_bind tests.
"""

import unittest
import tkinter
import tkinter.ttk

from .. import bindings
from .. import exceptionhandler


def callback_a(event):
    pass


def callback_b(event):
    pass


def callback_c(event):
    pass


class Bindings(unittest.TestCase):
    def setUp(self):
        self.bindings = bindings.Bindings()
        # One each of tkinter, tkinter.ttk, with and without 'tag_bind',
        # but Text and Canvas 'tag_bind' are significantly different.
        # No ttk class has 'tag_bind'.
        self.text = tkinter.Text()
        self.canvas = tkinter.Canvas()
        self.entry = tkinter.Entry()
        self.ttk_entry = tkinter.ttk.Entry()
        self.menu = tkinter.Menu()  # Not Listbox to avoid 'l = self.listbox'.

    def tearDown(self):
        pass

    def test_001___init___001(self):
        self.assertIsInstance(self.bindings, bindings.Bindings)
        self.assertIsInstance(self.bindings, exceptionhandler.ExceptionHandler)
        self.assertTrue(
            issubclass(bindings.Bindings, exceptionhandler.ExceptionHandler)
        )
        self.assertEqual(self.bindings._binding, dict())
        self.assertEqual(self.bindings._tag_binding, dict())
        self.assertEqual(self.bindings._current_binding, None)
        self.assertEqual(self.bindings._frozen_binding, set())
        self.assertEqual(len(self.bindings.__dict__), 4)

    def test_001___init___002(self):
        t = self.text
        self.assertEqual(repr(t.bind()), "()")
        # tkinter.Text.tag_bind does not support query form of Tk's 'tag bind'
        # command but calling 'tk.call' directly seems ok: in particular not
        # passing the default tag_bind arguments to 'tk.call'.
        self.assertEqual(
            repr(t.tk.call(t._w, "tag", "bind", tkinter.SEL)), "''"
        )

    def test_001___init___003(self):
        e = self.entry
        self.assertEqual(repr(e.bind()), "()")
        self.assertFalse(hasattr(e, "tag_bind"))

    def test_001___init___004(self):
        e = self.ttk_entry
        self.assertEqual(repr(e.bind()), "()")
        self.assertFalse(hasattr(e, "tag_bind"))

    def test_001___init___005(self):
        c = self.canvas
        self.assertEqual(repr(c.bind()), "()")
        # tkinter.Canvas.tag_bind does not support query form of Tk's
        # 'tag bind' command but calling 'tk.call' directly seems ok: in
        # particular not passing the default tag_bind arguments to 'tk.call'.
        self.assertEqual(repr(c.tk.call((c._w, "bind", tkinter.SEL))), "''")

    def test_001___init___006(self):
        m = self.menu
        self.assertEqual(repr(m.bind()), "()")
        self.assertFalse(hasattr(m, "tag_bind"))

    def test_002_bind_001(self):
        for w in (
            self.text,
            self.entry,
            self.ttk_entry,
            self.canvas,
            self.menu,
        ):
            self.assertRaisesRegex(
                bindings.BindSequenceIsNone,
                "sequence must be an event sequence",
                self.bindings.bind,
                *(w, None),
            )

    def test_002_bind_002(self):
        for w in (
            self.text,
            self.entry,
            self.ttk_entry,
            self.canvas,
            self.menu,
        ):
            self.bindings.bind(w, "a")
            self.assertEqual(repr(w.bind()), "()")
        self.assertEqual(self.bindings._binding, dict())

    def test_002_bind_003(self):
        for w in (
            self.text,
            self.entry,
            self.ttk_entry,
            self.canvas,
            self.menu,
        ):
            self.bindings.bind(w, "a", function=callback_a)
            self.assertEqual(repr(w.bind()), "('a',)")
            f = w.bind(sequence="a")
            self.assertEqual(f.startswith('if {"['), True)
            self.assertEqual(
                f.endswith(
                    "".join(
                        (
                            "wrapped_event_method %# %b %f %h %k %s ",
                            "%t %w %x %y %A %E %K %N %W %T %X %Y %D]",
                            '" == "break"} break\n',
                        )
                    )
                ),
                True,
            )
        self.assertEqual(len(self.bindings._binding), 5)
        for b in self.bindings._binding.values():
            self.assertIsInstance(b, set)
            self.assertEqual(len(b), 1)

    def test_002_bind_004(self):
        for w in (
            self.text,
            self.entry,
            self.ttk_entry,
            self.canvas,
            self.menu,
        ):
            self.bindings.bind(w, "a", function=callback_a)
            self.bindings.bind(w, "a", function=callback_b)
            self.assertEqual(repr(w.bind()), "('a',)")
            flist = w.bind(sequence="a").split("\n")
            self.assertEqual(len(flist), 2)
            for f in flist:
                if not f:
                    continue
                self.assertEqual(f.startswith('if {"['), True)
                self.assertEqual(
                    f.endswith(
                        "".join(
                            (
                                "wrapped_event_method %# %b %f %h %k %s ",
                                "%t %w %x %y %A %E %K %N %W %T %X %Y %D]",
                                '" == "break"} break',
                            )
                        )
                    ),
                    True,
                )
        self.assertEqual(len(self.bindings._binding), 5)
        for b in self.bindings._binding.values():
            self.assertIsInstance(b, set)
            self.assertEqual(len(b), 1)

    def test_002_bind_005(self):
        for w in (
            self.text,
            self.entry,
            self.ttk_entry,
            self.canvas,
            self.menu,
        ):
            self.bindings.bind(w, "a", function=callback_a)
            self.bindings.bind(w, "a", function=callback_b, add=True)
            self.assertEqual(repr(w.bind()), "('a',)")
            flist = w.bind(sequence="a").split("\n")
            self.assertEqual(len(flist), 4)
            for f in flist:
                if not f:
                    continue
                self.assertEqual(f.startswith('if {"['), True)
                self.assertEqual(
                    f.endswith(
                        "".join(
                            (
                                "wrapped_event_method %# %b %f %h %k %s ",
                                "%t %w %x %y %A %E %K %N %W %T %X %Y %D]",
                                '" == "break"} break',
                            )
                        )
                    ),
                    True,
                )
        self.assertEqual(len(self.bindings._binding), 5)
        for b in self.bindings._binding.values():
            self.assertIsInstance(b, set)
            self.assertEqual(len(b), 2)

    def test_002_bind_006(self):
        for w in (
            self.text,
            self.entry,
            self.ttk_entry,
            self.canvas,
            self.menu,
        ):
            self.bindings.bind(w, "a", function=callback_a)
            self.bindings.bind(w, "b", function=callback_b)
            bset = set(w.bind())
            self.assertEqual(bset, {"a", "b"})
            for s in bset:
                flist = w.bind(sequence=s).split("\n")
                self.assertEqual(len(flist), 2)
                for f in flist:
                    if not f:
                        continue
                    self.assertEqual(f.startswith('if {"['), True)
                    self.assertEqual(
                        f.endswith(
                            "".join(
                                (
                                    "wrapped_event_method %# %b %f %h %k %s ",
                                    "%t %w %x %y %A %E %K %N %W %T %X %Y %D]",
                                    '" == "break"} break',
                                )
                            )
                        ),
                        True,
                    )
        self.assertEqual(len(self.bindings._binding), 10)
        for b in self.bindings._binding.values():
            self.assertIsInstance(b, set)
            self.assertEqual(len(b), 1)

    def test_003_tag_bind_not_text_nor_canvas_001(self):
        self.assertRaisesRegex(
            bindings.WidgetIsNotTextOrCanvas,
            "widget must be a tkinter Text or Canvas instance",
            self.bindings.tag_bind,
            *(self.menu, None, None),
        )

    def test_004_tag_bind_text_001(self):
        self.assertRaisesRegex(
            bindings.TextTagBindSequenceIsNone,
            "sequence must be an event sequence",
            self.bindings.tag_bind,
            *(self.text, None, None),
        )

    def test_004_tag_bind_text_002(self):
        t = self.text
        self.bindings.tag_bind(t, tkinter.SEL, "a", function=callback_a)
        # tkinter.Text.tag_bind does not support query form of Tk's
        # 'tag bind' command but calling 'tk.call' directly seems ok: in
        # particular not passing the default tag_bind arguments to 'tk.call'.
        self.assertEqual(
            repr(t.tk.call((t._w, "tag", "bind", tkinter.SEL))), "('a',)"
        )
        flist = t.tk.call((t._w, "tag", "bind", tkinter.SEL, "a")).split("\n")
        self.assertEqual(len(flist), 2)
        for f in flist:
            if not f:
                continue
            self.assertEqual(f.startswith('if {"['), True)
            self.assertEqual(
                f.endswith(
                    "".join(
                        (
                            "wrapped_event_method %# %b %f %h %k %s ",
                            "%t %w %x %y %A %E %K %N %W %T %X %Y %D]",
                            '" == "break"} break',
                        )
                    )
                ),
                True,
            )
        self.assertEqual(len(self.bindings._tag_binding), 1)
        for b in self.bindings._tag_binding.values():
            self.assertIsInstance(b, set)
            self.assertEqual(len(b), 1)

    def test_004_tag_bind_text_003(self):
        t = self.text
        self.bindings.tag_bind(t, tkinter.SEL, "a", function=callback_a)
        self.bindings.tag_bind(t, tkinter.SEL, "a", function=callback_b)
        # tkinter.Text.tag_bind does not support query form of Tk's
        # 'tag bind' command but calling 'tk.call' directly seems ok: in
        # particular not passing the default tag_bind arguments to 'tk.call'.
        self.assertEqual(
            repr(t.tk.call((t._w, "tag", "bind", tkinter.SEL))), "('a',)"
        )
        flist = t.tk.call((t._w, "tag", "bind", tkinter.SEL, "a")).split("\n")
        self.assertEqual(len(flist), 2)
        for f in flist:
            if not f:
                continue
            self.assertEqual(f.startswith('if {"['), True)
            self.assertEqual(
                f.endswith(
                    "".join(
                        (
                            "wrapped_event_method %# %b %f %h %k %s ",
                            "%t %w %x %y %A %E %K %N %W %T %X %Y %D]",
                            '" == "break"} break',
                        )
                    )
                ),
                True,
            )
        self.assertEqual(len(self.bindings._tag_binding), 1)
        for b in self.bindings._tag_binding.values():
            self.assertIsInstance(b, set)
            self.assertEqual(len(b), 1)

    def test_004_tag_bind_text_004(self):
        t = self.text
        self.bindings.tag_bind(t, tkinter.SEL, "a", function=callback_a)
        self.bindings.tag_bind(
            t, tkinter.SEL, "a", function=callback_b, add=True
        )
        # tkinter.Text.tag_bind does not support query form of Tk's
        # 'tag bind' command but calling 'tk.call' directly seems ok: in
        # particular not passing the default tag_bind arguments to 'tk.call'.
        self.assertEqual(
            repr(t.tk.call((t._w, "tag", "bind", tkinter.SEL))), "('a',)"
        )
        flist = t.tk.call((t._w, "tag", "bind", tkinter.SEL, "a")).split("\n")
        self.assertEqual(len(flist), 4)
        for f in flist:
            if not f:
                continue
            self.assertEqual(f.startswith('if {"['), True)
            self.assertEqual(
                f.endswith(
                    "".join(
                        (
                            "wrapped_event_method %# %b %f %h %k %s ",
                            "%t %w %x %y %A %E %K %N %W %T %X %Y %D]",
                            '" == "break"} break',
                        )
                    )
                ),
                True,
            )
        self.assertEqual(len(self.bindings._tag_binding), 1)
        for b in self.bindings._tag_binding.values():
            self.assertIsInstance(b, set)
            self.assertEqual(len(b), 2)

    def test_004_tag_bind_text_005(self):
        t = self.text
        self.bindings.tag_bind(t, tkinter.SEL, "a", function=callback_a)
        self.bindings.tag_bind(t, tkinter.SEL, "b", function=callback_b)
        # tkinter.Text.tag_bind does not support query form of Tk's
        # 'tag bind' command but calling 'tk.call' directly seems ok: in
        # particular not passing the default tag_bind arguments to 'tk.call'.
        self.assertEqual(
            set(t.tk.call((t._w, "tag", "bind", tkinter.SEL))), set(("a", "b"))
        )
        flist = t.tk.call((t._w, "tag", "bind", tkinter.SEL, "a")).split("\n")
        self.assertEqual(len(flist), 2)
        for f in flist:
            if not f:
                continue
            self.assertEqual(f.startswith('if {"['), True)
            self.assertEqual(
                f.endswith(
                    "".join(
                        (
                            "wrapped_event_method %# %b %f %h %k %s ",
                            "%t %w %x %y %A %E %K %N %W %T %X %Y %D]",
                            '" == "break"} break',
                        )
                    )
                ),
                True,
            )
        self.assertEqual(len(self.bindings._tag_binding), 2)
        for b in self.bindings._tag_binding.values():
            self.assertIsInstance(b, set)
            self.assertEqual(len(b), 1)

    def test_005_tag_bind_canvas_001(self):
        self.assertRaisesRegex(
            bindings.CanvasTagBindSequenceIsNone,
            "sequence must be an event sequence",
            self.bindings.tag_bind,
            *(self.canvas, None, None),
        )

    def test_005_tag_bind_canvas_002(self):
        c = self.canvas
        self.bindings.tag_bind(c, tkinter.SEL, "a", function=callback_a)
        # tkinter.Canvas.tag_bind does not support query form of Tk's
        # 'tag bind' command but calling 'tk.call' directly seems ok: in
        # particular not passing the default tag_bind arguments to 'tk.call'.
        self.assertEqual(
            repr(c.tk.call((c._w, "bind", tkinter.SEL))), "('a',)"
        )
        flist = c.tk.call((c._w, "bind", tkinter.SEL, "a")).split("\n")
        self.assertEqual(len(flist), 2)
        for f in flist:
            if not f:
                continue
            self.assertEqual(f.startswith('if {"['), True)
            self.assertEqual(
                f.endswith(
                    "".join(
                        (
                            "wrapped_event_method %# %b %f %h %k %s ",
                            "%t %w %x %y %A %E %K %N %W %T %X %Y %D]",
                            '" == "break"} break',
                        )
                    )
                ),
                True,
            )
        self.assertEqual(len(self.bindings._tag_binding), 1)
        for b in self.bindings._tag_binding.values():
            self.assertIsInstance(b, set)
            self.assertEqual(len(b), 1)

    def test_005_tag_bind_canvas_003(self):
        c = self.canvas
        self.bindings.tag_bind(c, tkinter.SEL, "a", function=callback_a)
        self.bindings.tag_bind(c, tkinter.SEL, "a", function=callback_b)
        # tkinter.Canvas.tag_bind does not support query form of Tk's
        # 'tag bind' command but calling 'tk.call' directly seems ok: in
        # particular not passing the default tag_bind arguments to 'tk.call'.
        self.assertEqual(
            repr(c.tk.call((c._w, "bind", tkinter.SEL))), "('a',)"
        )
        flist = c.tk.call((c._w, "bind", tkinter.SEL, "a")).split("\n")
        self.assertEqual(len(flist), 2)
        for f in flist:
            if not f:
                continue
            self.assertEqual(f.startswith('if {"['), True)
            self.assertEqual(
                f.endswith(
                    "".join(
                        (
                            "wrapped_event_method %# %b %f %h %k %s ",
                            "%t %w %x %y %A %E %K %N %W %T %X %Y %D]",
                            '" == "break"} break',
                        )
                    )
                ),
                True,
            )
        self.assertEqual(len(self.bindings._tag_binding), 1)
        for b in self.bindings._tag_binding.values():
            self.assertIsInstance(b, set)
            self.assertEqual(len(b), 1)

    def test_005_tag_bind_canvas_004(self):
        c = self.canvas
        self.bindings.tag_bind(c, tkinter.SEL, "a", function=callback_a)
        self.bindings.tag_bind(
            c, tkinter.SEL, "a", function=callback_b, add=True
        )
        # tkinter.Canvas.tag_bind does not support query form of Tk's
        # 'tag bind' command but calling 'tk.call' directly seems ok: in
        # particular not passing the default tag_bind arguments to 'tk.call'.
        self.assertEqual(
            repr(c.tk.call((c._w, "bind", tkinter.SEL))), "('a',)"
        )
        flist = c.tk.call((c._w, "bind", tkinter.SEL, "a")).split("\n")
        self.assertEqual(len(flist), 4)
        for f in flist:
            if not f:
                continue
            self.assertEqual(f.startswith('if {"['), True)
            self.assertEqual(
                f.endswith(
                    "".join(
                        (
                            "wrapped_event_method %# %b %f %h %k %s ",
                            "%t %w %x %y %A %E %K %N %W %T %X %Y %D]",
                            '" == "break"} break',
                        )
                    )
                ),
                True,
            )
        self.assertEqual(len(self.bindings._tag_binding), 1)
        for b in self.bindings._tag_binding.values():
            self.assertIsInstance(b, set)
            self.assertEqual(len(b), 2)

    def test_005_tag_bind_canvas_005(self):
        c = self.canvas
        self.bindings.tag_bind(c, tkinter.SEL, "a", function=callback_a)
        self.bindings.tag_bind(c, tkinter.SEL, "b", function=callback_b)
        # tkinter.Canvas.tag_bind does not support query form of Tk's
        # 'tag bind' command but calling 'tk.call' directly seems ok: in
        # particular not passing the default tag_bind arguments to 'tk.call'.
        self.assertEqual(
            set(c.tk.call((c._w, "bind", tkinter.SEL))), set(("a", "b"))
        )
        flist = c.tk.call((c._w, "bind", tkinter.SEL, "a")).split("\n")
        self.assertEqual(len(flist), 2)
        for f in flist:
            if not f:
                continue
            self.assertEqual(f.startswith('if {"['), True)
            self.assertEqual(
                f.endswith(
                    "".join(
                        (
                            "wrapped_event_method %# %b %f %h %k %s ",
                            "%t %w %x %y %A %E %K %N %W %T %X %Y %D]",
                            '" == "break"} break',
                        )
                    )
                ),
                True,
            )
        self.assertEqual(len(self.bindings._tag_binding), 2)
        for b in self.bindings._tag_binding.values():
            self.assertIsInstance(b, set)
            self.assertEqual(len(b), 1)

    def test_006_unbind_all_001(self):
        for w in (
            self.text,
            self.entry,
            self.ttk_entry,
            self.canvas,
            self.menu,
        ):
            self.bindings.bind(w, "a", function=callback_a)
            self.bindings.bind(w, "a", function=callback_b, add=True)
            self.bindings.bind(w, "b", function=callback_b)
            self.bindings.bind(w, "c", function=callback_c)
            self.bindings.bind(w, "c", function=callback_b, add=True)
            self.bindings.bind(w, "c", function=callback_a, add=True)
        self.assertEqual(len(self.bindings._binding), 15)
        for b in self.bindings._binding.values():
            self.assertIsInstance(b, set)
            self.assertEqual(len(b) in {1, 2, 3}, True)
        for w in (self.text, self.canvas):
            self.bindings.tag_bind(w, tkinter.SEL, "a", function=callback_a)
            self.bindings.tag_bind(
                w, tkinter.SEL, "a", function=callback_b, add=True
            )
            self.bindings.tag_bind(w, tkinter.SEL, "b", function=callback_b)
            self.bindings.tag_bind(w, tkinter.SEL, "c", function=callback_c)
            self.bindings.tag_bind(
                w, tkinter.SEL, "c", function=callback_b, add=True
            )
            self.bindings.tag_bind(
                w, tkinter.SEL, "c", function=callback_a, add=True
            )
        self.assertEqual(len(self.bindings._tag_binding), 6)
        for b in self.bindings._tag_binding.values():
            self.assertIsInstance(b, set)
            self.assertEqual(len(b) in {1, 2, 3}, True)
        self.bindings.unbind_all_handlers()
        self.assertEqual(len(self.bindings._binding), 0)
        self.assertEqual(len(self.bindings._tag_binding), 0)

    def test_007_unbind_all_except_frozen_001(self):
        for w in (
            self.text,
            self.entry,
            self.ttk_entry,
            self.canvas,
            self.menu,
        ):
            self.bindings.bind(w, "a", function=callback_a)
            self.bindings.bind(w, "a", function=callback_b, add=True)
            self.bindings.bind(w, "b", function=callback_b)
            self.bindings.bind(w, "c", function=callback_c)
            self.bindings.bind(w, "c", function=callback_b, add=True)
            self.bindings.bind(w, "c", function=callback_a, add=True)
        self.assertEqual(len(self.bindings._binding), 15)
        for b in self.bindings._binding.values():
            self.assertIsInstance(b, set)
            self.assertEqual(len(b) in {1, 2, 3}, True)
        for w in (self.text, self.canvas):
            self.bindings.tag_bind(w, tkinter.SEL, "a", function=callback_a)
            self.bindings.tag_bind(
                w, tkinter.SEL, "a", function=callback_b, add=True
            )
            self.bindings.tag_bind(w, tkinter.SEL, "b", function=callback_b)
            self.bindings.tag_bind(w, tkinter.SEL, "c", function=callback_c)
            self.bindings.tag_bind(
                w, tkinter.SEL, "c", function=callback_b, add=True
            )
            self.bindings.tag_bind(
                w, tkinter.SEL, "c", function=callback_a, add=True
            )
        self.assertEqual(len(self.bindings._tag_binding), 6)
        for b in self.bindings._tag_binding.values():
            self.assertIsInstance(b, set)
            self.assertEqual(len(b) in {1, 2, 3}, True)
        self.bindings.unbind_all_handlers_except_frozen()
        self.assertEqual(len(self.bindings._binding), 0)
        self.assertEqual(len(self.bindings._tag_binding), 0)

    def test_007_unbind_all_except_frozen_002(self):
        for w in (
            self.text,
            self.entry,
            self.ttk_entry,
            self.canvas,
            self.menu,
        ):
            self.bindings.bind(w, "a", function=callback_a)
            self.bindings.bind(w, "a", function=callback_b, add=True)
            self.bindings.bind(w, "a", function=callback_c, add=True)
            self.bindings.bind(w, "b", function=callback_b)
            self.bindings.bind(w, "b", function=callback_a, add=True)
            self.bindings.bind(w, "b", function=callback_c, add=True)
            self.bindings.bind(w, "c", function=callback_c)
            self.bindings.bind(w, "c", function=callback_b, add=True)
            self.bindings.bind(w, "c", function=callback_a, add=True)
        self.assertEqual(len(self.bindings._binding), 15)
        for b in self.bindings._binding.values():
            self.assertIsInstance(b, set)
            self.assertEqual(len(b), 3)
        for w in (self.text, self.canvas):
            self.bindings.tag_bind(w, tkinter.SEL, "a", function=callback_a)
            self.bindings.tag_bind(
                w, tkinter.SEL, "a", function=callback_b, add=True
            )
            self.bindings.tag_bind(
                w, tkinter.SEL, "a", function=callback_c, add=True
            )
            self.bindings.tag_bind(w, tkinter.SEL, "b", function=callback_b)
            self.bindings.tag_bind(
                w, tkinter.SEL, "b", function=callback_a, add=True
            )
            self.bindings.tag_bind(
                w, tkinter.SEL, "b", function=callback_c, add=True
            )
            self.bindings.tag_bind(w, tkinter.SEL, "c", function=callback_c)
            self.bindings.tag_bind(
                w, tkinter.SEL, "c", function=callback_b, add=True
            )
            self.bindings.tag_bind(
                w, tkinter.SEL, "c", function=callback_a, add=True
            )
        self.assertEqual(len(self.bindings._tag_binding), 6)
        for b in self.bindings._tag_binding.values():
            self.assertIsInstance(b, set)
            self.assertEqual(len(b), 3)
        self.bindings.set_frozen_bindings()
        self.bindings.unbind_all_handlers_except_frozen()
        self.assertEqual(len(self.bindings._binding), 15)
        self.assertEqual(len(self.bindings._tag_binding), 6)
        for w in (
            self.text,
            self.entry,
            self.ttk_entry,
            self.canvas,
            self.menu,
        ):
            self.bindings.bind(w, "d", function=callback_a)
            self.bindings.bind(w, "d", function=callback_b, add=True)
            self.bindings.bind(w, "d", function=callback_c, add=True)
            self.bindings.bind(w, "e", function=callback_b)
            self.bindings.bind(w, "e", function=callback_a, add=True)
            self.bindings.bind(w, "e", function=callback_c, add=True)
            self.bindings.bind(w, "f", function=callback_c)
            self.bindings.bind(w, "f", function=callback_b, add=True)
            self.bindings.bind(w, "f", function=callback_a, add=True)
        for b in self.bindings._binding.values():
            self.assertIsInstance(b, set)
            self.assertEqual(len(b), 3)
        for w in (self.text, self.canvas):
            self.bindings.tag_bind(w, tkinter.SEL, "d", function=callback_a)
            self.bindings.tag_bind(
                w, tkinter.SEL, "d", function=callback_b, add=True
            )
            self.bindings.tag_bind(
                w, tkinter.SEL, "d", function=callback_c, add=True
            )
            self.bindings.tag_bind(w, tkinter.SEL, "e", function=callback_a)
            self.bindings.tag_bind(
                w, tkinter.SEL, "e", function=callback_b, add=True
            )
            self.bindings.tag_bind(
                w, tkinter.SEL, "e", function=callback_c, add=True
            )
            self.bindings.tag_bind(w, tkinter.SEL, "f", function=callback_c)
            self.bindings.tag_bind(
                w, tkinter.SEL, "f", function=callback_b, add=True
            )
            self.bindings.tag_bind(
                w, tkinter.SEL, "f", function=callback_a, add=True
            )
        for b in self.bindings._tag_binding.values():
            self.assertIsInstance(b, set)
            self.assertEqual(len(b), 3)
        self.assertEqual(len(self.bindings._binding), 30)
        self.assertEqual(len(self.bindings._tag_binding), 12)
        self.bindings.unbind_all_handlers_except_frozen()
        for b in self.bindings._binding.values():
            self.assertIsInstance(b, set)
            self.assertEqual(len(b), 3)
        for b in self.bindings._tag_binding.values():
            self.assertIsInstance(b, set)
            self.assertEqual(len(b), 3)
        self.assertEqual(len(self.bindings._binding), 15)
        self.assertEqual(len(self.bindings._tag_binding), 6)
        self.bindings.unset_frozen_bindings()
        self.bindings.unbind_all_handlers_except_frozen()
        self.assertEqual(len(self.bindings._binding), 0)
        self.assertEqual(len(self.bindings._tag_binding), 0)

    def test_008_unset_frozen_bindings_001(self):
        self.bindings.unset_frozen_bindings()

    def test_009_set_frozen_bindings_001(self):
        self.bindings.set_frozen_bindings()


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(Bindings))
