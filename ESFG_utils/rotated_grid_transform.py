def rotated_grid_transform(grid_in, option, SP_coor):
    """Permite tranformar coordenadas rotadas al sistema de corrdenadas WGS84 o viceversa.
    
    Parámetros:
    ---------------------
    grid_in : array. Coordendas que se desean tranformar
    option  : int. 1: # WGS84 -> Rotadas  2: # Rotadas -> WGS84 
    SP_coor : list. grid_north_pole #SP_lon = NP_lon - 180, SP_lat = -NP_lat. Los parámetros NP_ se obtienen del netcdf o fichero de datos.
    
    Salidas:
    ----------------------
    lon_new , lat_new : Coordendas tansformadas

    """
    
    lon = grid_in[0]
    lat = grid_in[1];

    lon = (lon*pi)/180; # Convert degrees to radians
    lat = (lat*pi)/180;

    SP_lon = SP_coor[0];
    SP_lat = SP_coor[1];
    
    #SP_lon = NP_lon - 180, SP_lat = -NP_lat.

    theta = 90+SP_lat; # Rotation around y-axis
    phi = SP_lon; # Rotation around z-axis

    theta = (theta*pi)/180;
    phi = (phi*pi)/180; # Convert degrees to radians

    x = cos(lon)*cos(lat); # Convert from spherical to cartesian coordinates
    y = sin(lon)*cos(lat);
    z = sin(lat);

    if option == 1: # Regular -> Rotated

        x_new = cos(theta)*cos(phi)*x + cos(theta)*sin(phi)*y + sin(theta)*z;
        y_new = -sin(phi)*x + cos(phi)*y;
        z_new = -sin(theta)*cos(phi)*x - sin(theta)*sin(phi)*y + cos(theta)*z;

    else:  # Rotated -> Regular

        phi = -phi;
        theta = -theta;

        x_new = cos(theta)*cos(phi)*x + sin(phi)*y + sin(theta)*cos(phi)*z;
        y_new = -cos(theta)*sin(phi)*x + cos(phi)*y - sin(theta)*sin(phi)*z;
        z_new = -sin(theta)*x + cos(theta)*z;



    lon_new = atan2(y_new,x_new); # Convert cartesian back to spherical coordinates
    lat_new = asin(z_new);

    lon_new = (lon_new*180)/pi; # Convert radians back to degrees
    lat_new = (lat_new*180)/pi;

    return lon_new , lat_new