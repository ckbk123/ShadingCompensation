from numpy import pi, sin, cos, array

# this function calculate the homogeneous coordinates of the sun in the camera's frame of reference
# phi = azimuth
# theta = zenith
# omega = inclination
# psi = orientation
# PLEASE provide them in DEGREES
# astropy_coords = [phi, theta]
def astropy_to_camera_extrinsic (astropy_coords, psi, omega):
    # convert to radians
    phi = astropy_coords[0]*pi/180
    theta = astropy_coords[1]*pi/180
    psi = psi*pi/180
    omega = omega*pi/180

    # first convert to ground basis
    theta_ground = 3*pi/2 - theta
    phi_ground = phi

    # spherical in ground basis to rectangular in ground basis
    x = sin(phi_ground)*cos(theta_ground)/cos(phi_ground)
    y = sin(phi_ground)*sin(theta_ground)/cos(phi_ground)

    # ground basis to (x',y',z')
    x_prime = cos(psi)*x + sin(psi)*y
    y_prime = -sin(psi)*x + cos(psi)*y

    # (x',y',z') basis to camera basis, but we add 1 to the mix
    x_c = x_prime/(sin(omega)*y_prime + cos(omega))
    y_c = (cos(omega)*y_prime - sin(omega))/(sin(omega)*y_prime + cos(omega))

    return array([x_c,y_c]).T.tolist()