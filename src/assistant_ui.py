import wx
import wx.lib.newevent

from src.personal_assistant import EventHandler


class ChatRecorderFrame(wx.Frame):
    def __init__(self, event_handler):
        super().__init__(None, title="Personal Assistant", size=(400, 300))
        self.record_button = None
        self.text_box = None
        self.recording = False
        self.initUI()
        self.event_handler = event_handler

    def initUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.text_box = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.text_box, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        self.record_button = wx.Button(panel, label="Start Recording")
        vbox.Add(self.record_button, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(vbox)

        self.record_button.Bind(wx.EVT_BUTTON, self.onToggleRecording)

    def onToggleRecording(self, event):
        self.recording = not self.recording
        if self.recording:
            self.record_button.SetLabel("Stop Recording")
            self.record_button.SetBackgroundColour(wx.RED)
            self.event_handler.handle_event(EventHandler.RECORDING_STARTED)

        else:
            self.record_button.SetLabel("Start Recording")
            self.record_button.SetBackgroundColour(wx.GREEN)
            self.event_handler.handle_event(EventHandler.RECORDING_STOPPED)

    def appendMessage(self, message, person):
        current_text = self.text_box.GetValue()
        formatted_message = f"\n{person}: {message}\n"
        if current_text:
            new_text = current_text + formatted_message
        else:
            new_text = formatted_message
        self.text_box.SetValue(new_text)
