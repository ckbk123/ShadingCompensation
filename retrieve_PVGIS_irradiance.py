
import pvlib.iotools.pvgis as PVGIS



def retrieve_PVGIS_irradiance(lat, long, start_year, end_year, inclination, orientation):
    data, meta, inputs = PVGIS.get_pvgis_hourly(latitude=lat, longitude=long, start=start_year, end=end_year,
                                                outputformat='json', components=True, usehorizon=False,
                                                surface_tilt=inclination, surface_azimuth=180+orientation)

    # return the direct irradiance, diffuse irradiance, and time (it is probably in datetime format, ambiguous documentation)
    return data['poa_direct'], data['poa_sky_diffuse'], data.index.tz_localize(None)