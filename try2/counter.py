from pymtl3 import *
class RegIncr( Component ):
 # Constructor
  def construct( s ):
    # Port-based interface
    s.in_ = InPort ( Bits8 )
    s.out = OutPort ( Bits8 )
    
    # update_ff block modeling register
    s.reg_out = Wire( 8 ) # 8 is the same as Bits8 for Wire/InPort/OutPort
    
    @update_ff
    def block1():
      if s.reset:
        s.reg_out <<= 0
      else:
        s.reg_out <<= s.reg_out + 1
    # update block modeling incrementer
    
    @update
    def block2():
      s.out @= s.reg_out + 1

  def line_trace( s ):
    return "{} {} {}".format(
      s.in_,
      s.reg_out,
      s.out
    )