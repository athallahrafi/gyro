import smbus
import time

# Alamat I2C MPU-6050
MPU_ADDRESS = 0x68

# Register MPU-6050
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

# Inisialisasi SMBus (I2C bus 1 pada Jetson Nano)
bus = smbus.SMBus(1)

# Fungsi untuk membaca data 16-bit dari register
def read_word_2c(addr):
    high = bus.read_byte_data(MPU_ADDRESS, addr)
    low = bus.read_byte_data(MPU_ADDRESS, addr + 1)
    val = (high << 8) + low
    if val >= 0x8000:
        return -((65535 - val) + 1)
    else:
        return val

# Fungsi untuk membaca data akselerometer
def read_accel_data():
    accel_x = read_word_2c(ACCEL_XOUT_H) / 16384.0
    accel_y = read_word_2c(ACCEL_XOUT_H + 2) / 16384.0
    accel_z = read_word_2c(ACCEL_XOUT_H + 4) / 16384.0
    return {"x": accel_x, "y": accel_y, "z": accel_z}

# Fungsi untuk membaca data gyroscope
def read_gyro_data():
    gyro_x = read_word_2c(GYRO_XOUT_H) / 131.0
    gyro_y = read_word_2c(GYRO_XOUT_H + 2) / 131.0
    gyro_z = read_word_2c(GYRO_XOUT_H + 4) / 131.0
    return {"x": gyro_x, "y": gyro_y, "z": gyro_z}

# Inisialisasi MPU-6050
def initialize_mpu():
    bus.write_byte_data(MPU_ADDRESS, PWR_MGMT_1, 0)  # Bangunkan MPU-6050 dari mode sleep

# Program utama
if __name__ == "__main__":
    try:
        print("Inisialisasi MPU-6050...")
        initialize_mpu()
        time.sleep(1)

        while True:
            accel = read_accel_data()
            gyro = read_gyro_data()

            print(f"Akselerometer: X={accel['x']:.2f}, Y={accel['y']:.2f}, Z={accel['z']:.2f}")
            print(f"Gyroscope: X={gyro['x']:.2f}, Y={gyro['y']:.2f}, Z={gyro['z']:.2f}")
            print("-" * 40)

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nProgram dihentikan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
