root.geometry ("480x580")
title = customtkinter.CTkLabel(
        root,
        text="UIB MART",
        font=customtkinter.CTkFont(family="Montserrat", size=36, weight="bold"),
        text_color="#00d4ff",
        width=480
    )
    title.place(x=0, y=80)
    title.configure(anchor="center")