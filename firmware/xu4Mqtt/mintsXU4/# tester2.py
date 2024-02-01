# tester2

     def get_formatted_spectrum(self) -> list[float]:
         """!
         Return a formatted spectrum.
         @return The formatted spectrum.
         """
  
         spd_c = (c_double * self.pixel_count_formattedpixel_count_formatted)()
         err_cp = (c_long * 1)(0)
         self.oceandirectoceandirect.odapi_get_formatted_spectrum(self.device_iddevice_id, err_cp, spd_c, self.pixel_count_formattedpixel_count_formatted)
         if err_cp[0] != 0:
             error_msg = self.decode_errordecode_error(err_cp[0],"get_formatted_spectrum")
             raise OceanDirectError(err_cp[0], error_msg)
         return list(spd_c)

    def get_stored_dark_spectrum(self) -> list[float]:
         """!
         Retrieve a previously stored dark spectrum for use in subsequent corrections i.e. dark correction and nonlinearity correction.
         @see setStoredDarkSpectrum.
         @return The dark spectrum.
         """
  
         double_array = (c_double * self.pixel_count_formattedpixel_count_formatted)()
         err_cp       = (c_long * 1)(0)
         self.oceandirectoceandirect.odapi_get_stored_dark_spectrum(self.device_iddevice_id, err_cp, double_array, self.pixel_count_formattedpixel_count_formatted)
         if err_cp[0] != 0:
             error_msg = self.decode_errordecode_error(err_cp[0],"get_stored_dark_spectrum")
             raise OceanDirectError(err_cp[0], error_msg)
         return list(double_array)

 def get_dark_corrected_spectrum1(self, darkSpectrum: list[float]) -> list[float]:
         """!
         Acquire a spectrum and use the supplied dark spectrum to perform a dark correction then return the dark corrected spectrum.
         @param darkSpectrum[in] the buffer that contains the dark spectrum to be used for the dark correction.
         @return The dark corrected spectrum.
         """
  
         if len(darkSpectrum) == 0:
             #code 10 means missing value
             error_msg = self.decode_errordecode_error(10,"get_dark_corrected_spectrum1")
             raise OceanDirectError(10, error_msg)
  
         corrected_spectrum_array  = (c_double * self.pixel_count_formattedpixel_count_formatted)()
         dark_spectrum_array_count = len(darkSpectrum)
         dark_spectrum_array       = (c_double * dark_spectrum_array_count)()
         err_cp                    = (c_long * 1)(0)
         for x in range(dark_spectrum_array_count):
             dark_spectrum_array[x] = darkSpectrum[x]
  
         self.oceandirectoceandirect.odapi_get_dark_corrected_spectrum1(self.device_iddevice_id, err_cp, dark_spectrum_array, dark_spectrum_array_count,
                                                             corrected_spectrum_array, self.pixel_count_formattedpixel_count_formatted)
         if err_cp[0] != 0:
             error_msg = self.decode_errordecode_error(err_cp[0],"get_dark_corrected_spectrum1")
             raise OceanDirectError(err_cp[0], error_msg)
         return list(corrected_spectrum_array)

     def get_dark_corrected_spectrum2(self) -> list[float]:
         """!
         Acquire a spectrum and use the previously stored dark spectrum to perform a dark correction then return the dark corrected spectrum.
         @see setStoredDarkSpectrum.
         @return The dark corrected spectrum.
         """
  
         corrected_spectrum_array = (c_double * self.pixel_count_formattedpixel_count_formatted)()
         err_cp                   = (c_long * 1)(0)
         self.oceandirectoceandirect.odapi_get_dark_corrected_spectrum2(self.device_iddevice_id, err_cp, corrected_spectrum_array, self.pixel_count_formattedpixel_count_formatted)
         if err_cp[0] != 0:
             error_msg = self.decode_errordecode_error(err_cp[0],"get_dark_corrected_spectrum2")
             raise OceanDirectError(err_cp[0], error_msg)
         return list(corrected_spectrum_array)
  

       def dark_correct_spectrum1(self, illuminatedSpectrum: list[float]) -> list[float]:
         """!
         Dark correct a previously acquired illuminated spectrum and using a stored dark spectrum.
         @see setStoredDarkSpectrum
         @param illuminatedSpectrum[in] the buffer that contains the illuminated spectrum to be corrected.
         @return The dark corrected spectrum.
         """
  
         if len(illuminatedSpectrum) == 0:
             #code 10 means missing value
             error_msg = self.decode_errordecode_error(10,"dark_correct_spectrum1")
             raise OceanDirectError(10, error_msg)
  
         corrected_spectrum_array         = (c_double * self.pixel_count_formattedpixel_count_formatted)()
         illuminated_spectrum_array_count = len(illuminatedSpectrum)
         illuminated_spectrum_array       = (c_double * illuminated_spectrum_array_count)()
         err_cp                           = (c_long * 1)(0)
         for x in range(illuminated_spectrum_array_count):
             illuminated_spectrum_array[x] = illuminatedSpectrum[x]
  
         self.oceandirectoceandirect.odapi_dark_correct_spectrum1(self.device_iddevice_id, err_cp, illuminated_spectrum_array, illuminated_spectrum_array_count,
                                                       corrected_spectrum_array, self.pixel_count_formattedpixel_count_formatted)
         if err_cp[0] != 0:
             error_msg = self.decode_errordecode_error(err_cp[0],"dark_correct_spectrum1")
             raise OceanDirectError(err_cp[0], error_msg)
         return list(corrected_spectrum_array)



 def dark_correct_spectrum2(self, darkSpectrum: list[float], illuminatedSpectrum: list[float]) -> list[float]:
         """!
         Dark correct a previously acquired illuminated spectrum and using a previously acquired dark spectrum.
         @param darkSpectrum[in] the buffer that contains the dark spectrum to be used for the dark correction.
         @param illuminatedSpectrum[in] the buffer that contains the illuminated spectrum to be corrected.
         @return The dark corrected spectrum.
         """
  
         if len(darkSpectrum) == 0 or len(illuminatedSpectrum) == 0:
             #code 10 means missing value
             error_msg = self.decode_errordecode_error(10,"dark_correct_spectrum2")
             raise OceanDirectError(10, error_msg)
  
         corrected_spectrum_array         = (c_double * self.pixel_count_formattedpixel_count_formatted)()
         dark_spectrum_array_count        = len(darkSpectrum)
         dark_spectrum_array              = (c_double * dark_spectrum_array_count)()
         illuminated_spectrum_array_count = len(illuminatedSpectrum)
         illuminated_spectrum_array       = (c_double * illuminated_spectrum_array_count)()
         err_cp                           = (c_long * 1)(0)
         for x in range(dark_spectrum_array_count):
             dark_spectrum_array[x] = darkSpectrum[x]
  
         for x in range(illuminated_spectrum_array_count):
             illuminated_spectrum_array[x] = illuminatedSpectrum[x]
  
         self.oceandirectoceandirect.odapi_dark_correct_spectrum2(self.device_iddevice_id, err_cp, dark_spectrum_array, dark_spectrum_array_count,
                                                       illuminated_spectrum_array, illuminated_spectrum_array_count,
                                                       corrected_spectrum_array, self.pixel_count_formattedpixel_count_formatted)
         if err_cp[0] != 0:
             error_msg = self.decode_errordecode_error(err_cp[0],"dark_correct_spectrum2")
             raise OceanDirectError(err_cp[0], error_msg)
         return list(corrected_spectrum_array) 

 def get_nonlinearity_corrected_spectrum1(self, darkSpectrum: list[float]) -> list[float]:
         """!
         Acquire a spectrum and use the supplied dark spectrum to perform a dark correction
         followed by the nonlinearity correction then return the nonlinearity corrected spectrum.
         @param darkSpectrum[in] the buffer that contains the dark spectrum to be used for the dark correction.
         @return The nonlinearity corrected spectrum.
         """
  
         if len(darkSpectrum) == 0:
             #code 10 means missing value
             error_msg = self.decode_errordecode_error(10,"get_nonlinearity_corrected_spectrum1")
             raise OceanDirectError(10, error_msg)
     
         corrected_spectrum_array  = (c_double * self.pixel_count_formattedpixel_count_formatted)()
         dark_spectrum_array_count = len(darkSpectrum)
         dark_spectrum_array       = (c_double * dark_spectrum_array_count)()
         err_cp                    = (c_long * 1)(0)
         for x in range(dark_spectrum_array_count):
             dark_spectrum_array[x] = darkSpectrum[x]
  
         self.oceandirectoceandirect.odapi_get_nonlinearity_corrected_spectrum1(self.device_iddevice_id, err_cp, dark_spectrum_array, dark_spectrum_array_count,
                                                                     corrected_spectrum_array, self.pixel_count_formattedpixel_count_formatted)
         if err_cp[0] != 0:
             error_msg = self.decode_errordecode_error(err_cp[0],"get_nonlinearity_corrected_spectrum1")
             raise OceanDirectError(err_cp[0], error_msg)
         return list(corrected_spectrum_array)



     def get_nonlinearity_corrected_spectrum2(self) -> list[float]:
         """!
         Acquire a spectrum and use the previously stored dark spectrum to perform a dark correction
         followed by a nonlinearity correction then return the nonlinearity corrected spectrum.
         @see setStoredDarkSpectrum.
         @return The nonlinearity corrected spectrum.
         """
  
         corrected_spectrum_array = (c_double * self.pixel_count_formattedpixel_count_formatted)()
         err_cp                   = (c_long * 1)(0)
  
         self.oceandirectoceandirect.odapi_get_nonlinearity_corrected_spectrum2(self.device_iddevice_id, err_cp, corrected_spectrum_array, self.pixel_count_formattedpixel_count_formatted)
         if err_cp[0] != 0:
             error_msg = self.decode_errordecode_error(err_cp[0],"get_nonlinearity_corrected_spectrum2")
             raise OceanDirectError(err_cp[0], error_msg)
         return list(corrected_spectrum_array)

