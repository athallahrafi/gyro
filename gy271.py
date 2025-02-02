import smbus2
     import time

     # Alamat I2C untuk HMC5883L
     HMC5883L_ADDRESS = 0x1E

     # Inisialisasi I2C bus
     bus = smbus2.SMBus(1)

     # Konfigurasi sensor
     bus.write_byte_data(HMC5883L_ADDRESS, 0x02, 0x00)  # Mode continuous measurement

     def read_magnetometer():
         # Baca data dari register sensor
         data = bus.read_i2c_block_data(HMC5883L_ADDRESS, 0x03, 6)
         x = (data[0] << 8) | data[1]
         z = (data[2] << 8) | data[3]
         y = (data[4] << 8) | data[5]
         return x, y, z

     try:
         while True:
             x, y, z = read_magnetometer()
             print(f"X: {x}, Y: {y}, Z: {z}")
             time.sleep(1)
     except KeyboardInterrupt:
         print("Program dihentikan")
