import Tkinter as tk

WRONG_BALANCE = "ERROR - Unsafe Proportions! Advise not continuing!"
WRONG_TIME = ("ERROR - you must only adjust the balances at a certain time. "
              "Attempts remaining: %d")
ADJUSTING = "Please wait - adjusting chemical balances"
FINAL = "Balance complete. Please remove blurple wire."


def FormatAsTime(time):
  return "%02d:%02d" % (int(time/60), time % 60)


class BombApp(object):

  def __init__(self, percentages, time, safe_tens, attempts):
    self.root = tk.Tk()
    self.root.minsize(width=500, height=400)
    self.root.maxsize(width=500, height=400)

    self.percentages = percentages
    self.time = time
    self.safe_tens = safe_tens
    self.attempts = attempts
    self.correct = False

    self.countdown_text = tk.StringVar()
    self.countdown_label = tk.Label(self.root, textvariable=self.countdown_text)
    self.countdown_label.pack(pady=20)

    self.sliders = [
        tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, length=200)
        for _ in percentages]
    for slider in self.sliders: slider.pack()

    self.status_text = tk.StringVar()
    self.SetStatusText("Enter correct percentages.")
    self.status_label = tk.Label(self.root, textvariable=self.status_text,
                                 wraplength=350, height=2)
    self.status_label.pack()

    self.button = tk.Button(self.root, text="Ok", command=self.ButtonPress)
    self.button.pack(pady=5)

  def Run(self):
    self.Countdown()
    self.root.mainloop()

  def Fail(self):
    self.SetStatusText("BOOM")

  def ButtonPress(self):
    if self.correct:
      return
    if [slider.get() for slider in self.sliders] == self.percentages:
      tens_in_time = (self.time % 60)/10
      if tens_in_time == self.safe_tens:
        # This stops the countdown.
        self.correct = True
        self.AdjustingNode()
        return
      else:
        self.attempts -= 1
        if self.attempts == 0:
          self.Fail()
          return
        self.SetStatusText(WRONG_TIME % self.attempts)
    else:
      self.SetStatusText(WRONG_BALANCE)


  def SetStatusText(self, text):
    self.status_text.set(text)

  def Countdown(self):
    if self.time == 0:
      self.Fail()
      return

    if self.correct:
      return

    self.time-=1
    self.countdown_text.set(FormatAsTime(self.time))
    self.root.after(1000, self.Countdown)

  def AdjustingNode(self, dots=0):
    self.SetStatusText(ADJUSTING + "." * dots)

    if dots == 3:
      self.root.after(1000, self.SetFinalText)
    else:
      self.root.after(1000, self.AdjustingNode, dots+1)

  def SetFinalText(self):
    self.SetStatusText(FINAL)


bomb_app = BombApp([10,20,30], 121, 3, 3)
bomb_app.Run()
