import tkinter as tk

def send_message():
    message = input_text.get()
    print("User sent message:", message)
    input_text.delete(0, tk.END)

root = tk.Tk()
root.title("Chat GUI")

# Tạo khung hiển thị tin nhắn
message_frame = tk.Frame(root)
message_frame.pack(pady=10)

message_label = tk.Label(message_frame, text="Enter message:")
message_label.pack(side=tk.LEFT)

input_text = tk.Entry(message_frame, width=50)
input_text.pack(side=tk.LEFT)

send_button = tk.Button(message_frame, text="Send", command=send_message)
send_button.pack(side=tk.LEFT)

root.mainloop()
