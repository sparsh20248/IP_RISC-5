from pymtl3 import *
from pymtl3.stdlib.test_utils import config_model_with_cmdline_opts

from  counter import RegIncr

# In pytest, unit tests are simply functions that begin with a "test_"
# prefix. PyMTL3 is setup to collect command line options. Simply specify
# "cmdline_opts" as an argument to your unit test source code,
# and then you can dump VCD by adding --dump-vcd option to pytest
# invocation from the command line.

def test_basic( cmdline_opts ):

  # Create the model

  model = RegIncr()

  # Configure the model

  model = config_model_with_cmdline_opts( model, cmdline_opts, duts=[] )

  # Create and reset simulator

  model.apply( DefaultPassGroup ( textwave = True ) )
  model.sim_reset()

  # Helper function

  def t( in_, out ):

    # Write input value to input port

    model.in_ @= in_

    # Ensure that all combinational concurrent blocks are called

    model.sim_eval_combinational()

    # If reference output is not '?', verify value read from output port
    if out != '?':
      assert model.out == out

    # Tick simulator one cycle

    model.sim_tick()

  t( 0, '?' )
  t( 13, 2 )
  t( 27, 3 )
  t( 00, 4 )
  t( 0, 5 )
  t( 0, 6 )
