#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class Bug184_Frame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: Bug184_Frame.__init__
        kwds["style"] = kwds.get("style", 0)
        wx.Frame.__init__(self, *args, **kwds)
        self.SetTitle(_("frame_1"))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BACKGROUND))

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        self.label_1 = wx.StaticText(self, wx.ID_ANY, _("Just a label"))
        sizer_1.Add(self.label_1, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(sizer_1)
        sizer_1.Fit(self)

        self.Layout()
        # end wxGlade

# end of class Bug184_Frame

class MyApp(wx.App):
    def OnInit(self):
        self.Frame184 = Bug184_Frame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.Frame184)
        self.Frame184.Show()
        return True

# end of class MyApp

if __name__ == "__main__":
    gettext.install("app") # replace with the appropriate catalog name

    app = MyApp(0)
    app.MainLoop()
