import sys
import dbus
import dbus.service
import gobject
from dbus.mainloop.glib import DBusGMainLoop

import server_role

class DomainControllerRoleObject(server_role.ServerRoleObject):
    
    def __init__(self, conn=None, object_path=None, bus_name=None):
        super(DomainControllerRoleObject, self).__init__(conn, object_path, bus_name)
        self.Set(server_role.ROLE_IFACE, 'firewall_ports',
                 [(389, 'tcp'), (389, 'udp')])
    
    @dbus.service.method(server_role.ROLE_IFACE,
                         in_signature='', out_signature='as')
    def PreloadRole(self, pkgs=None):
        '''
        Installs a set of packages on the system
        :Parameters:
            `pkgs` : list
                A list of packages to be installed using the system's native
                package management utility.
        '''
        role_packages = ('freeipa-server',
                         'bind-dyndb-ldap')
        return super(DomainControllerRoleObject, self).PreloadRole(pkgs=role_packages)

    @dbus.service.method(server_role.ROLE_IFACE,
                         in_signature='', out_signature='')
    def DeployRole(self, settings=None):
        # Validate the settings and call out to ipa-server-install
        pass


def main(argv):
    DBusGMainLoop(set_as_default=True)
    bus = dbus.SessionBus()

    name = dbus.service.BusName("org.fedoraproject.server.RoleService", bus)
    DC_obj = DomainControllerRoleObject(
                object_path="/DomainControllerRoleObject", conn=bus)

    loop = gobject.MainLoop()
    loop.run()

if __name__ == '__main__':
    main(sys.argv)
