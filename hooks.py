# -*- coding:utf-8 -*-
from tkinter import *
from tkinter import ttk

class Hooks(Tk):
    def __init__(self, type="", global_stats=False):
        super().__init__()
        self.type = type
        self.global_stats = global_stats
        if global_stats:
            with open('hookstats.txt') as f:
                at_total, at_hits = f.read().split()
                self.at_total = int(at_total)
                self.at_hits = int(at_total)
        self.total = 0
        self.count = 0
        self.title('Hit counter')
        self._gui()

    def _gui(self):
        frHeader = ttk.Frame(self)
        frButtons = ttk.Frame(self)
        self.status = StringVar(self, "Awaiting command...")
        labStatus = ttk.Label(self, textvariable=self.status)
        labType = ttk.Label(frHeader, text="Type:")
        entType = ttk.Entry(frHeader, width=30)
        butCommit = ttk.Button(frHeader, text="Commit", command=lambda: self._type(entType.get()))
        butHit = ttk.Button(frButtons, text="Hit", command=lambda: self.hit())
        butMiss = ttk.Button(frButtons, text="Miss", command=lambda: self.miss())
        butFin = ttk.Button(frButtons, text="Finished", command=lambda: self.fin())

        labType.grid(column=0, row=0, padx=5)
        entType.grid(column=1, row=0, padx=5)
        butCommit.grid(column=2, row=0, padx=5)

        butHit.grid(column=0, row=0, padx=5)
        butMiss.grid(column=1, row=0, padx=5)
        butFin.grid(column=0, row=1, columnspan=2, padx=5)

        frHeader.grid(row=0)
        frButtons.grid(row=1)
        labStatus.grid(row=2)

    def _perc(self, count=0, state=""):
        self.count += count
        self.total += 0 if state else 1
        p = self.count / self.total if self.total else 0
        sn = "---> {} {}/{} {} ({:.1%} rate) <---".format(state, self.count, self.total, self.type, p)
        self.status.set(sn)
        self.clipboard_clear()
        self.clipboard_append("/me " + sn)
        print('" /me ', sn, '" copied to clipboard')

    def _type(self, value):
        self.total, self.count = 0, 0
        self.status.set("Skillshot type set to: " + value)
        self.type = value

    def hit(self):
        self._perc(1)

    def miss(self):
        self._perc()

    def fin(self):
        self._perc(state="Game finished!")
        if self.type and self.global_stats:
            self.at_total += self.total
            self.at_hits += self.count
            with open('hookstats.txt', 'w') as f:
                f.write("{} {}".format(self.at_total, self.at_hits))
        self.total, self.count = 0, 0

    def glob(self):
        self._perc("Global stats:")

if __name__ == '__main__':
    c = Hooks()
    c.mainloop()
