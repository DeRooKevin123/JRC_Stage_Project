# I. General Information

- **Created:** 29/6/2018
- **Author:** Kevin de Roo (Aged 16)
- **Subject:** Python 2.7 (Graphs)
- **Software used:** Spyder, Jupyter Notebook, Anaconda Navigator, Anaconda Prompt, ArcMap
- **Libraries used:** Pandas, Numpy, Seaborn, Matplotlib, netCDF4

# II. Execution Of The File

## 1. **Parameters**
Before executing the file, you need to know what the parameters are:

- **Filename** (The path to the file (in this case the discharge file) and the name of the file without dataformat) 
- **Dataformat** (The dataformat of the file. The user can choose between '**nc**' and '**tss**')
- **Mask** (The mask for the graph. Either the coordinates for **a single point**, which will plot a line graph, or the coordinates for **two points**, which will give you a piece of a map)
- **Start Date** (The first date on the graph. Usage is day/month/year.)
- **End Date** (The last date on the graph. Usage is day/month/year.)
- **Yearly Aggregation** (View all graphs per year in one single graph. Choose '**yes**' or '**no**')
- **Outfile** (The name of the outfile. The user can choose any name)

## 2. **Execution of the file**
To **execute** the file, you can use **Anaconda Prompt**, for example. Just write the following in the prompt:

- `cd [Folder Name]` 'Folder Name' is the folder where the python file is located
- `python [Python File] -f [Filename] -d [Dataformat] -m [Mask] -s [Start Date] -e [End Date] -a [Yearly Aggregation] -o [Outfile]` 'Python File' is the name of the python file you want to execute, the others are the parameters.
- **Example1 (1 point):**
`python PythonFile1.py -f dis -d nc -m 1111111 2222222 -s 1/1/1990 -e 1/1/2000 -a yes -o OutFile1` Mask: x1=1111111, y1=2222222. This will create graphs for the values at those coordinates.
- **Example2 (2 points):**
`python PythonFile1.py -f dis -d nc -m 1111111 3333333 2222222 1111111 -s 1/1/1990 -e 1/1/2000 -a yes -o OutFile1` Mask: x1=1111111, y1=3333333, x2=2222222, y2=1111111. This will create a piece of the world map with TopLeft corner (x1,y1) and BottomRight corner (x2,y2).

# III. Quick Introduction

Python is a powerful programming language, being able to do anything the user wishes. This is why I chose to spend my working experience on python, hoping to learn a lot more than I already knew. **Valerio Lorini** and **Peter Salamon**, from unit "**Copernicus E.1**" at the **JRC (Joint Research Centre)** in **Ispra (Italy)** made this possible for me and I am really grateful to them for their support. With that being said, here is a summary of the projects that I was assigned:

## **Project 1:**
The first thing I did was experiment with new Python **libraries** and commands using **Jupyter Notebook** and **Spyder**, two python editors. Following some tutorials, I couldn't wait to learn more. My first project was to extract information from a text file that I was given. This file contained **discharge values** for many different stations across Europe. Extracting the information and putting them in a **dataframe** was my first problem, since I actually didn't know much about python. Luckily we have modern technology, namely the Internet. During my coding I had to look up many things and it started to give me a clear picture of what python can do. After figuring out how to create the dataframe, I had to make a **timestamp** (timeline), so I could plot a graph. Again, I had to look up a few things, since new commands created new problems or bugs. Finally, after two or three days of coding, I completed my first project. A thing that I could have added are parameters to let the user choose a station and a start/end date. I wasn't confident of my coding skills yet, so I decided not to do it.

## **Project 2:**
My second project was way more complex. It was basically the same thing, but with a **NetCDF** file and parameters included (which is the project you downloaded). Reading the file and making a dataframe was just one line of code, which really saved a lot of time. Many of the problems I encountered were based on the **complexity of the code**, something that I simply didn't understand, because I hadn't spent much time on understanding python. Nevertheless, with the help of the Internet and my tutor **Valerio Lorini**, I managed to get the code and parameters to work. About **seven days** were spent on the making of this project. I did not have the time to finish the .tss part (I also included a parameter for when you have a .tss file), but the code for a NetCDF file is (pretty much) done.

# IV. To-Do List
I haven't finished everything yet, so here is a quick to-do list:

- **Remove hardcoded values:** Unfortunately I have no idea how to remove the last hardcoded values, for example the 'dis' variable. This variable will not work for any other file that does not contain discharge values. Another example is the "timestamp" variable. Some files contain values per month, while mine contains values per day.
- **Finish .tss part:** So far I only had time to extract all information and put it in a dataframe. I still need to plot the graphs according to the parameters and to write some code for the outfile.
- **Decrease memory usage:** Some lines of code can be done much quicker, reducing the memory used during the execution of the file.
- **Aggregation = 'no':** I haven't added this part for any of the file types. Basically, when the user chooses 'no' for the Yearly Aggregation, the graphs just have to pop up one after another. If you choose 'no' right now, the execution will finish without doing anything.
- **Projection:** The projection of the map piece currently doesn't work for **ArcMap**, but it should work for **QGIS**.

# V. Copyright

This script is released under terms of **EUPL License**. The python file is for general use (anyone can feel free to use it), but do not claim it as your own. I have spent many hours on the file, trying to make it as bug-free as possible. You may change the code or anything else, but that does not make you the owner. Thank you in advance.






