# Compartment ODE Solver

Compartment ODE solver is a tool focused in solving molecule transfer between compartments problems that are part of the University of Utah BME 4001 - bioTransport class. In using this tool known data can be entered to create a concentration vs time plot. This program is designed to solve compartment ODE's in the form:

$$ \frac{d\vec{C}}{dt} + \overline{m}\,\vec{C} = \vec{F} $$

and will output a concentration vs time plot. The m matrix ($\,\overline{m}\,$) is a ratio of the concentration coefficents ($\,k_{ij}\,$) and compartment volumes ($\,V\,$) in the form $n \times n$ matrix in the form:

$$
\overline{m} =
\begin{bmatrix}
m_{11} & m_{12} & m_{13} & m_{14}\\
m_{21} & m_{22} & m_{23} & m_{24}\\
m_{31} & m_{32} & m_{33} & m_{34}\\
m_{41} & m_{42} & m_{43} & m_{44}\\
\end{bmatrix}
$$

Required Modules:
<br/>

[![numpy](https://img.shields.io/badge/numpy-1.26.0-blue)](https://numpy.org/)
[![scipy](https://img.shields.io/badge/scipy-1.11.4-blue)](https://scipy.org/)
[![matplotlib](https://img.shields.io/badge/matplotlib-3.8-blue)](https://matplotlib.org/)
[![tkinter](https://img.shields.io/badge/tkinter-3.12.1-blue)](https://docs.python.org/3/library/tkinter.html)

## Usage

### Terminal

Launch python program from ther terminal with:

```
python comp_ODE_solver.py
```

Terminal must be active in the same directory as the python program to launch.

### Windows

For windows users a compiled app is availible [here](comp_ODE_TK.exe). The program may also be launched using ther terminal command above.

### MacOS/Linux

For macOS and linux users a compiled app is not avalible and muse be lunched using there terminal outlined above.

## Documentation

After the program has been launced a window will open (this may take a few seconds to apear). The window consists of three primary sections: Compartments, m Matrix, and Initial Conditions. This is then followed by the button Run Simulation.

### Compartments

This section of the program has a single box to enter the number of compartments the problem consists of. The number of compartments this program is able to hande ranges from 2 compartments to 4 compartments.

### m Matrix

This section of the program consists of a $4 \times 4$ grid of boxes to enter numarical values. The number of rows and columns to be used is determined by the number of compartments entered in the prevous section. Values entered into the box must be numarical and can consist of desimal values as well as positive and negative numbers. Values entered bust start at the upper left entry box and will be assosiated with the $m_{11}$ value of the m matrix. If the number of compartments is less than 4 you do not need to enter values into the extra boxes.

### Initial Conditions

This section of the program consists of 4 boxes to enter the values of the known initial conditions of each of the compartments. These values must be numarical and may contain desimal values. The order of the initial condition boxes are with the top being the first compartment and assinding in order as you move down. If the number of compartments is less than 4 you do not need to enter values into the extra boxes.

### Time Settings
This secion of the program consists of 3 boxes to enter the start time, end time, and time between input (skip) of molecules into compartments. The start time or initial is the time value where the plot time will begin. The end time or final is where the plot time will end. If multiple inputs of molecules is not occuring leave the skip box blank.

### Run Simulation

This button is to be pressed after all values in the previous sections are filled out. By pressing this putton the ODE will be solved for time values from 0-20 and a plot will be created in a new window. This plot may then be saved by pressing the save icon in the plot window.

## Examples

|               <h3>Main Program</h3>                |              <h3>Plot</h3>              |
| :------------------------------------------------: | :-------------------------------------: |
| ![Main Program Example Image](program_example.png) | ![Plot Example Image](plot_example.png) |
