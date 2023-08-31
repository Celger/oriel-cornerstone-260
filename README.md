# Oriel Cornerstone 260 ![pyVISA](https://img.shields.io/badge/pyVISA-1.3.0-brightgreen) ![Python](https://img.shields.io/badge/Python-3.10.0-brightgreen)
A library allowing easy control over an Oriel Cornerstone 260 monochromator using pyVISA (independent of interface and adapters such as GPIB, serial, USB...).
This code is based on the [@bicarlsen](https://github.com/bicarlsen) repository [oriel-cornersttone-260](https://github.com/bicarlsen/oriel-cornerstone-260).
> Install with `python -m pip install oriel-cornerstone-260`

## Monochromator
Represents a monochromator.

+ **Monochromator( addr = None, timeout = 5, read_delay = 0.1 ):** Creates a new monochromator for the device at the specificed address, with the provided communication timeout and the delay of the read operation ina a query.

### Methods

#### Low Level
Low level methods allows reading and writing to the device.

+ **connect():** Connects to the device.

+ **disconnect():** Disconnects from the device.

+ **write( msg ):** Writes a message to the device.

+ **read():** Reads a single response from the device.

+ **command( cmd, \*args ):** Sends a command to the device with the given arguments. Returns the command.

+ **query( msg ):** Queries the device. Returns a Response object.

### High Level
High level methods are convenience methods used for commonly needed functions.

+ **goto( wavelength ):** Goes to the given wavelength.

+ **abort():** Starts the given channel.

+ **set_grating( grating ):** Sets the grating to the given number.

+ **set_filter( filter ):** Sets the filter to the given position.

+ **filter_label(filter, label = None ):** Gets or sets a filter's label.

+ **shutter( close = True ):** Open or close the shutter.

+ **set_outport( port ):** Sets the output port.

+ **slit_width( slit, width = None ):** Gets or sets the slit width.


### Properties
+ **_instr:** GPIB instrument resource from `pyvisa`.
+ **addr:** Device address.
+ **term_chars:** Termination characters used for reading and writing. [Default: '\r\n']
+ **info:** Device info.
+ **position:** Wavelength position.
+ **grating:** Current grating and its properties. Returns a dictionary with `number`, `lines`, and `label`.
+ **filter:** Current filter position.
+ **shuttered:** Whether the shutter is closed or open.
+ **outport:** The output port.

## Example

A basic example for using a Monochromator.
```python
from oriel_cornerstone_260 import Monochromator

# create device
mono = Monochromator()

# print monochromator info
print( mono.info )

# go to 600 nm
mono.goto( 600 )
```

#### Note
A Monochromator is a ultimately a `GPIB` resource from `pyvisa`, so you can call any functions on a Monochromator that you would on a pyvisa resource.

---
