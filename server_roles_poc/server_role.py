'''
Created on Mar 17, 2014

@author: sgallagh
'''
import dbus

ROLE_IFACE = "org.fedoraproject.server.RoleInterface"

class UnknownInterfaceException(dbus.DBusException):
    _dbus_error_name = 'org.fedoraproject.server.UnknownInterface'

class MethodNotImplementedException(dbus.DBusException):
    _dbus_error_name = 'org.fedoraproject.server.MethodNotImplemented'

class ServerRoleObject(dbus.service.Object):
    '''
    Base class for Server Role D-BUS objects
    '''

    @dbus.service.method(ROLE_IFACE,
                         in_signature='', out_signature='as')
    def PreloadRole(self, pkgs=None):
        '''
        Installs a set of packages on the system
        :Parameters:
            `pkgs` : list
                A list of packages to be installed using the system's native
                package management utility.
        :Returns:
            `pkgs` : a list of packages that were installed on the system
                     (including dependencies)
        '''

        # TODO: call out to PackageKit
        print pkgs
        return pkgs

    @dbus.service.method(ROLE_IFACE,
                         in_signature='', out_signature='a(qs)')
    def GetFirewallPorts(self):
        '''
        Returns an array of port/protocol pairs
        This represents the list of ports that the Role currently indicates
        that it requires to be open to the public for proper operation.
        NOTE: This method does not indicate whether these ports are available
        or not on the system. For that functionality, the Firewall object
        should be consulted.
        '''
        return self.Get(ROLE_IFACE, 'firewall_ports')
    
    @dbus.service.method(ROLE_IFACE,
                         in_signature='', out_signature='')
    def DeployRole(self, settings=None):
        '''
        Abstract interface. This *must* be overridden by the child class
        '''
        raise MethodNotImplementedException(
                'This Server Role is missing the DeployRole method')

    # Common routines for property handling
    dbus_properties = {}

    @dbus.service.method(dbus_interface=dbus.PROPERTIES_IFACE,
                         in_signature='ss', out_signature='v')
    def Get(self, interface_name, property_name):
        return self.GetAll(interface_name)[property_name]

    @dbus.service.method(dbus_interface=dbus.PROPERTIES_IFACE,
                         in_signature='s', out_signature='a{sv}')
    def GetAll(self, interface_name):
        try:
            return self.dbus_properties[interface_name]
        except:
            raise dbus.exceptions.DBusException(
                'Object does not implement the %s interface'
                    % interface_name)

    @dbus.service.method(dbus_interface=dbus.PROPERTIES_IFACE,
                         in_signature='ssv')
    def Set(self, interface_name, property_name, new_value):
        if not self.dbus_properties.has_key(interface_name):
            self.dbus_properties[interface_name] = {}
        self.dbus_properties[interface_name][property_name] = new_value

        if new_value is None:
            if self.dbus_properties[interface_name].has_key(property_name):
                # Invalidate the property
                del self.dbus_properties[interface_name][property_name]

                # Notify listeners of the invalidation
                self.PropertiesChanged(interface_name, [],
                                       [property_name])
                return

        # Otherwise, notify of the change.
        self.PropertiesChanged(interface_name,
            { property_name: new_value }, [])

    @dbus.service.signal(dbus_interface=dbus.PROPERTIES_IFACE,
                         signature='sa{sv}as')
    def PropertiesChanged(self, interface_name, changed_properties,
                          invalidated_properties):
        # Don't need to take any action here, just send the signal
        print ("Changing properties: %s" % changed_properties)
        pass
