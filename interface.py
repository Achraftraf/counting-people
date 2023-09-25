import tkinter.messagebox
import customtkinter
import tkinter as tk
from tkinter.filedialog import askopenfilename
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
import counting_number_of_persons
import counting_number_of_person_video
import counter_number_of_persons_camera
from PIL import Image
confid=0.4
x=300
y=300
state = 1
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.change_appearance_mode_event("Dark")

        self.selected_Methode = ""
        selectedPath = ""
        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=150, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="People Counting", font=customtkinter.CTkFont(size=25, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
       
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 20))

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.sidebar_frame,anchor="w",
                                                        values=["Low", "Medium", "high"] , command=self.on_select)
        self.optionmenu_1.grid(row=3, column=0, padx=20, pady=(10, 10))
        self.optionmenu_2 = customtkinter.CTkOptionMenu(self.sidebar_frame,anchor="w",
                                                        values=["300,300", "340,280", "320,280","290,300"] , command=self.on_select_1)
        self.optionmenu_2.grid(row=4, column=0, padx=20, pady=(10, 10))
       
     

        # create radiobutton fram



        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.mainImage = customtkinter.CTkImage(light_image=Image.open(r"C:\Users\Administrator\Desktop\2.png"),size=(500,400),
                                                dark_image=Image.open(r"C:\Users\Administrator\Desktop\1.png"))
        self.image=customtkinter.CTkLabel(self.radiobutton_frame,text="",image=self.mainImage)
        self.image.grid(row=0,column=0,padx=12,pady=0,sticky="NSEW")
        self.radiobutton_frame.columnconfigure(0, weight=1)
        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, columnspan=2, padx=(40, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.seg_button_1 = customtkinter.CTkSegmentedButton(self.slider_progressbar_frame)
        self.seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        
        self.main_button_1 = customtkinter.CTkButton(self.slider_progressbar_frame, fg_color="transparent", border_width=3,height=45, text_color=("gray10", "#DCE4EE") , text="upload" , command=self.uploadOnclick)
        self.main_button_1.grid(row=3, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")


        # set default values
       
        
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.optionmenu_1.set("confidence")
        self.optionmenu_2.set("size")
        self.progressbar_1.configure(mode="indeterminnate")
        self.progressbar_1.start()
        self.seg_button_1.configure(values=["image", "video", "camera"] , command=self.sigm_OnChange)
        self.seg_button_1.set("Value 2")



    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def sigm_OnChange(self,value):
        self.selected_Methode = value

    def uploadOnclick(self):
            global state
            global selectedPath
            global confid
            if(self.selected_Methode ==""):
                return 
            if(self.selected_Methode=="camera"):
                cam = counter_number_of_persons_camera
                cam.init(confid,x,y)
                return
            self.openSelector_click()
            if (selectedPath == ""):
                    return
            if(self.selected_Methode=="image"):
                img = counting_number_of_persons
                img.init(selectedPath,confid,x,y)
                return
            if(self.selected_Methode=="video"):
                vid = counting_number_of_person_video
                vid.init(selectedPath,confid,x,y)
                return
           
    

    def openSelector_click(self):
        global selectedPath
        selectedPath=""
        window = tk.Tk()
        window.withdraw()  # we don't want a full GUI, so keep the root window from appearing
        selectedPath = askopenfilename()  # show an "Open" dialog box and return the path to the selected file

    # create the butons
    def on_select(self,value):
        global confid
        if(value=="high"):
            confid = 0.6
            return
        if(value=="Medium"):
            confid = 0.3
            return
        if(value == "Low"):
            confid = 0.1
            return
        confid = 0.4






    def on_select_1(self,value):
        global x,y
        if(value=="300,300"):
            x = 300
            y = 300
        if(value=="340,280"):
            x = 340
            y = 280
            return
        if(value=="320,280"):
             x = 320
             y = 280
             return
        if(value == "290,300"):
             x = 290
             y = 300
             return
        x = 300
        y = 300

if __name__ == "__main__":
    app = App()
    app.mainloop()
