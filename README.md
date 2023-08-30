# Oriel Cornerstone 260
A library allowing easy control over an Oriel Cornerstone 260 monochromator with an GPIB port.
> Install with `python -m pip install oriel-cornerstone-260`

> **_NOTE:_** For newer models with a USB connection, see the [USB Connection](#usb_connection) section at the bottom of this page.

## Monochromator
Represents a monochromator.

+ **Monochromator( addr = None, timeout = 5, read_delay = 0.1 ):** Creates a new monochromator for the device at the specificed address, with the provided communication timeout and the delay of the read operation.

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

### <a name="usb_connection"></a>USB Connection
The USB Newport/Oriel Cornerstone 260 works differently, and **can not utilize this package**.
It is Windows only and requires two proprietary .NET .DLLs from Newport.
The Python interface is through the package [pythonnet](https://github.com/pythonnet/pythonnet).
As of late 2020, these are 32 bit DLL's that require a 32-bit (not AMD64) version of python.

```python
import clr
clr.AddReference( 'Cornerstone' )
import CornerstoneDll

mono = CornerstoneDll.Cornerstone( True )
if not mono.connect():
  raise IOError( 'Monochromator not found' )
```
The `mono` object will control the monochromator using methods documented in the Cornerstone 260 manual.
