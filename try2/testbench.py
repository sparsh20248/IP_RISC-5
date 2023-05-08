from pymtl3 import *
from sys import argv
from counter import RegIncr

# Get list of input values from command line
# input_values = [ int(x,0) for x in argv[1:] ]

# Add three zero values to end of list of input values

input_values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# Instantiate and elaborate the model


model = RegIncr()
model.elaborate()

# Applying the default pass group to add simulation facilities
model.apply( DefaultPassGroup( textwave=True ) )

# # Reset simulator
model.sim_reset()


# # Apply input values and display output values
for input_value in input_values:
    
    # Write input value to input port
    model.in_ @= input_value
    model.sim_eval_combinational()
    
    # Display input and output ports
    print( f" cycle = {model.sim_cycle_count()}: in = {model.in_}, out = {model.out}" )
    
    # Tick simulator one cycle
    model.sim_tick()
    if(input_value == 4):
        model.reset @= True
    
    if(input_value == 6):
        model.reset @= False

model.print_textwave()