#!/usr/bin/env python
# coding: utf-8

# # Newport Monochromator
# 
# For use with a Oriel Cornerstone 260 monochromator.
# 
# For documentation see the [Oriel Cornerstone Manual](https://www.newport.com/medias/sys_master/images/images/hae/h47/8797226926110/Oriel-Cornerstone-260-User-Manual-RevA.pdf).

# In[97]:


import serial
from collections import namedtuple


# In[98]:


Response = namedtuple( 'Response', [ 'statement', 'response' ] )


# In[103]:


class Monochromator:
    """
    Represents an Oriel Cornerstone 260 monochromator.
    """
    
    def __init__( self, port, timeout = 5 ):
        """
        Creates a new Monochromator.
        
        :param port: Device port.
        :param timeout: Communication timeout.
        """
        self.port = port
        self.com = serial.Serial( port, timeout = timeout )
        self.term_chars = '\r\n'
        
        
    def __del__( self ):
        """
        Closes serial port connection.
        """
        self.com.close()
        
        
    def __getattr__( self, attr ):
        """
        Pass unknown attributes to serial.
        
        :param attr: Attribute.
        """
        return getattr( self.com, attr )
    
    #--- low level methods ---
    
    def connect( self ):
        """
        Connects to the device.
        """
        self.com.open()
        
        
    def disconnect( self ):
        """
        disconnects from the device.
        """
        self.com.close()
    
    def write( self, msg ):
        """
        Writes a message to the monochromator.
        
        :param msg: Message to send.
        :returns: Number of bytes written.
        """
        msg += self.term_chars
        msg = msg.upper()
        msg = msg.encode( 'utf-8' )
        return self.com.write( msg )
       
    
    def read( self ):
        """
        Reads the buffer of the monochromator.
        
        :returns: The response.
        """
        resp = self.com.read_until( self.term_chars ).decode( 'utf-8' )
        return resp
    
    
    def command( self, cmd, *args ):
        """
        Sends a command to the monochromator.
        
        :param msg: Message to send.
        :returns: Command sent.
        """
        args = map( str, args )
        msg = cmd + ' ' +  ' '.join( args )
        
        self.write( msg )
        return self.read().rstrip()
    
    
    def query( self, msg ):
        """
        Queries the monochromator.
        Equivalent to doing a write( msg ) then a read().
        
        :param msg: Query message. '?' added if needed.
        :returns: A dictionary object containing the statement and response.
        """
        if msg[ -1 ] != '?':
            msg += '?'
        
        self.write( msg )
        
        resp = self.read()
        resp = resp.split( self.term_chars )
        return Response( statement = resp[ 0 ], response = resp[ 1 ] )
    
    
    #--- high level methods ---
    
    @property
    def info( self ):
        """
        :returns: Device info.
        """
        resp = self.query( 'info' )
        return resp.response
    
    
    @property
    def position( self ):
        """
        :returns: Current wavelength position in nanometers.
        """
        resp = self.query( 'wave' )
        return resp.response
    
    
    def goto( self, wavelength ):
        """
        Moves monochromator to given wavelength.
        
        :param wavelength: Desired wavelength in nanometers.
        :returns: Set wavelength.
        """
        wavelength = '{:.3f}'.format( wavelength )
        self.command( 'gowave', wavelength )
        
        return self.position
    
    
    def abort( self ):
        """
        Haults the monochromator.
        """
        self.command( 'abort' )
        
        
    @property
    def grating( self ):
        """
        :returns: Current grating and its properties.
        """
        resp = self.query( 'grat' ).split( ',' )
        return {
            'number': resp[ 0 ],
            'lines':  resp[ 1 ],
            'label':  resp[ 2 ]
        }
        
        
    def set_grating( self, grating ):
        """
        Sets the grating.
        
        :param grating: Number of the grating.
        """
        self.command( 'grat', str( grating ) )
        
        
    @property    
    def shuttered( self ):
        """
        :returns: True if shutter is close , False if open
        """
        resp = self.query( 'shutter' )
        return ( resp.response == 'C' )
        
        
    def shutter( self, close = True ):
        """
        Opens or closes the shutter.
        
        :param close: True to close the shutter, False to open.
            [Default: True]
        """
        cmd = 'C' if close else 'O'
        self.command( 'shutter', cmd )
        
    @property
    def outport( self ):
        """
        :returns: The output port number.
        """
        resp = self.query( 'outport' )
        return int( resp.response )
    
    def set_outport( self, port ):
        """
        Sets the ouput port.
        
        :param port: Output port to set.
        """
        self.command( 'outport', str( port ) )
        
    
    def slit_width( self, slit, width = None ):
        """
        Gets or sets the slit with.
        
        :param slit: Slit number.
        :param width: If None, returns current slit width.
            If a number, sets the slit width.
            [Default: None]
        :returns: Slit width.
        """
        cmd = 'slit{}microns'.format( slit )
        if width is not None:
            self.command( cmd, str( width ) )
        
        resp = self.query( cmd )
        return int( resp.response )


# # Work

# In[105]:


# mono = Monochromator( 'COM9', timeout = 10 )


# In[106]:


# mono.position


# In[104]:


# mono.close()

