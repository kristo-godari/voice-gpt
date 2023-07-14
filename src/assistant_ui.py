import wx
import wx.lib.newevent

from src.ui_event_handler import UiEventHandler


class ChatUi(wx.Frame):
    def __init__(self, event_handler):
        super().__init__(None, title="Personal Assistant", size=(400, 300))
        self.text_label = None
        self.record_button = None
        self.text_box = None
        self.recording = False
        self.initUI()
        self.event_handler = event_handler

    def initUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.text_box = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.text_box, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        # Create a vertical box sizer for the label and add a spacer to the left
        label_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.text_label = wx.StaticText(panel, label="Press reply button to start replying...")
        label_sizer.Add(self.text_label, proportion=0, flag=wx.EXPAND | wx.LEFT, border=5)

        vbox.Add(label_sizer, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        self.record_button = wx.Button(panel, label="Reply")
        vbox.Add(self.record_button, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(vbox)

        self.record_button.Bind(wx.EVT_BUTTON, self.onToggleRecording)

    def onToggleRecording(self, event):
        self.recording = not self.recording
        if self.recording:
            self.record_button.SetLabel("Stop recording and send reply")
            self.text_label.SetLabel("Recording audio ....")
            self.event_handler.handle_event(UiEventHandler.RECORDING_STARTED)

        else:
            self.record_button.SetLabel("Reply")
            self.text_label.SetLabel("Recording audio stopped. Press reply to start replying.")
            self.event_handler.handle_event(UiEventHandler.RECORDING_STOPPED)

    def appendMessage(self, message, person):
        current_text = self.text_box.GetValue()
        formatted_message = f"\n{person}: {message}\n"
        if current_text:
            new_text = current_text + formatted_message
        else:
            new_text = formatted_message
        self.text_box.SetValue(new_text)

        # Scroll to the bottom of the text box
        self.text_box.SetInsertionPointEnd()
        self.text_box.ShowPosition(self.text_box.GetLastPosition())
