#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from tkinter import *
from tkinter import ttk

#Graphical User Interface
def on_click():
    print("hello")
    
button = ttk.Button()
button.pack()
button['text']='click me!'
button['command']=on_click

mainloop()


# In[ ]:


for i in range(10):
    ttk.Button(text=1).pack(fill=BOTH，expand=True)
    
mainloop()


# In[ ]:


for i in range(10):
    ttk.Button(text=1).pack(side=LEFT,fill= BOTH,expand=True)
    
mainloop()


# In[ ]:


def on click():
    label['text']='click'

label=ttk.label(text='hello')

button=ttk.Button()
button.pack()
button['text']='click me!'
button['command']=on_click

mainloop()


# In[ ]:


for i in range(4):
    for j in range(5):
        text=


# In[2]:


class calculator(TK):
    def_init_(self.*args,**kwargs):
        super().init_(*args,**kwargs)
        self.title('simple ')
        
        #row 1
        row = Frame(self)
        row.pack(side=TOP,expand=True,fill=BOTH)
        for i in range(4):
            ttk.button(row.text=i).pack(side=LEFT,expand=True,fill=BOTH)


# In[ ]:




