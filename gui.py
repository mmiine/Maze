from guizero import App, Text


# Action you would like to perform
def counter():
    text.value = cnt

app = App("Hello world")
text = Text(app, text="1")
text.repeat(1000, counter)  # Schedule call to counter() every 1000ms
app.display()

