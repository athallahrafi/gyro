import smbus
import time
import math

# Alamat I2C dari QMC5883L
QMC5883L_ADDRESS = 0x0D

# Register untuk konfigurasi
MODE_REGISTER = 0x09
DATA_X_MSB = 0x00
DATA_X_LSB = 0x01
DATA_Y_MSB = 0x02
DATA_Y_LSB = 0x03
DATA_Z_MSB = 0x04
DATA_Z_LSB = 0x05

# Inisialisasi bus I2C
bus = smbus.SMBus(1)

def init_sensor():
    # Mengatur mode sensor ke mode normal
    bus.write_byte_data(QMC5883L_ADDRESS, MODE_REGISTER, 0x01)

def read_magnetometer():
    # Membaca data dari sensor
    data = bus.read_i2c_block_data(QMC5883L_ADDRESS, DATA_X_MSB, 6)

    # Mengonversi data ke nilai 16-bit
    x = (data[0] << 8) | data[1]
    y = (data[2] << 8) | data[3]
    z = (data[4] << 8) | data[5]

    # Mengatasi nilai negatif
    if x >= 0x8000:
        x -= 0x10000
    if y >= 0x8000:
        y -= 0x10000
    if z >= 0x8000:
        z -= 0x10000

    return x, y, z

def calculate_heading(x, y):
    # Menghitung sudut dalam radian
    heading_rad = math.atan2(y, x)

    # Mengonversi radian ke derajat
    heading_deg = math.degrees(heading_rad)

    # Normalisasi sudut ke rentang 0-360 derajat
    if heading_deg < 0:
        heading_deg += 360

    return heading_deg

if __name__ == "__main__":
    init_sensor()
    try:
        while True:
            x, y, z = read_magnetometer()
            heading = calculate_heading(x, y)
            print(f"X: {x}, Y: {y}, Z: {z}, Heading: {heading:.2f}°")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program dihentikan.")
