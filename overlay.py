import tkinter as tk
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.chat import Chat, ChatMessage
from twitchAPI.oauth import AuthScope
import asyncio

TWITCH_CLIENT_ID="9agv3m9pjbnxf2blf6q4ar4blencbu"
TWITCH_CLIENT_SECRET="i75yjecg7xo5rmxvngtfdcwhn6hbf7"
CHANNEL_NAME="ekl1f"

# Создаём окно чата
root=tk.Tk()
root.title("Twitch Chat Overlay")
root.attributes("-topmost", True) #атрибут поверх окон
root.attributes("-transparentcolor", "black")
root.configure(bg="black")
root.geometry("400x600+100+100")

# Текстовое поле для сообщений
chat_text=tk.Text(
    root,
    bg="black",
    fg="White",
    front=("Arial",12),
    wrap=tk.WORD,
    borderwidth=0,
    highlightthickness=0
)
chat_text.pack(fill=tk.BOTH, expand=True)

# Функция для добавления сообщений в чат
async def on_message(msg:ChatMessage):
    chat_text.insert(tk.END, f"{msg.user.name}: {msg.text}\n")
    chat_text.see(tk.END)
    # Автопрокрутка вниз
    # Ограничиваем количество строк (чтобы не перегружать память)
    if chat_text.index(tk.END).split('.')[0] > 100:
        chat_text.delete(1.0, 2.0)

async def run_chat():
    #Авторизация в твич
    twitch = await Twitch(TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET)
    auth=UserAuthenticator(twitch, [AuthScope.CHAT_READ])
    await auth.authenticate()
    chat = await Chat(twitch).connect()
    await chat.join_channel(CHANNEL_NAME)
    chat.register_callback(ChatMessage, on_message)

    # Бесконечное ожидание новых сообщений
    await asyncio.Event().wait()

# Запуск чата в фоне
def start_chat():
    asyncio.run(run_chat())

root.after(100, start_chat)
root.mainloop()
