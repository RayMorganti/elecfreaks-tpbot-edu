from microbit import i2c
from microbit import pin13
from microbit import pin14
from microbit import pin15
from microbit import pin16
from microbit import running_time
from microbit import sleep
import utime

I2C_ADDRESS = 0x10

CMD_MOTOR = 0x10
CMD_SERVO = 0x20
CMD_HEADLIGHT = 0x30
CMD_PID_WHEEL_SPEED = 0x40
CMD_PID_DISTANCE = 0x41
CMD_PID_STEERING = 0x42
CMD_PID_SPEED = 0x4F
CMD_PID_STOP_FLAG = 0xA0
CMD_ADJUST_MOTOR = 0xF0
CMD_RESET_MOTOR_ADJUST = 0xF1

DEFAULT_PID_SPEED = 250
MIN_PID_SPEED = 200
MAX_PID_SPEED = 500


class Direction:
    FORWARD = 0
    BACKWARD = 1


class ServoPort:
    S1 = 1
    S2 = 2
    S3 = 3
    S4 = 4


class TrackColor:
    BLACK = 0
    WHITE = 1


class Side:
    LEFT = 0
    RIGHT = 1


class SteeringMode:
    LEFT = 0
    RIGHT = 1
    STAY_LEFT = 2
    STAY_RIGHT = 3


class ServoType:
    SERVO_180 = 1
    SERVO_270 = 2
    SERVO_360 = 3
    DEG_180 = SERVO_180
    DEG_360 = SERVO_360


class MotorSelector:
    LEFT = 0
    RIGHT = 1
    ALL = 2


class SpeedUnit:
    CM_PER_SEC = 0
    IN_PER_SEC = 1


class DistanceUnit:
    UNIT_CM = 0
    UNIT_INCH = 1


class TPBotEdu:
    def __init__(self):
        self.left_speed = 0
        self.right_speed = 0
        self._continuous_servo_config = {
            ServoPort.S1: {"stop_angle": 90, "min_angle": 0, "max_angle": 180},
            ServoPort.S2: {"stop_angle": 90, "min_angle": 0, "max_angle": 180},
            ServoPort.S3: {"stop_angle": 90, "min_angle": 0, "max_angle": 180},
            ServoPort.S4: {"stop_angle": 90, "min_angle": 0, "max_angle": 180},
        }

    def _clamp(self, v, lo, hi):
        if v < lo:
            return lo
        if v > hi:
            return hi
        return v

    def _map_int(self, value, in_min, in_max, out_min, out_max):
        if in_max == in_min:
            raise ValueError("map range")
        return int(round((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min))

    def _validate_servo_port(self, port):
        if port not in (ServoPort.S1, ServoPort.S2, ServoPort.S3, ServoPort.S4):
            raise ValueError("port")

    def _i2c_send(self, cmd, params=None):
        if not isinstance(cmd, int):
            raise TypeError("cmd")
        if cmd < 0 or cmd > 255:
            raise ValueError("cmd")

        if params is None:
            params = []

        try:
            n = len(params)
        except Exception:
            raise TypeError("params")

        buf = bytearray(n + 4)
        buf[0] = 0xFF
        buf[1] = 0xF9
        buf[2] = cmd & 0xFF
        buf[3] = n

        for i in range(n):
            try:
                value = int(params[i])
            except Exception:
                raise TypeError("params")
            if value < 0 or value > 255:
                raise ValueError("params")
            buf[i + 4] = value

        i2c.write(I2C_ADDRESS, buf)

    def set_motors_speed(self, left_speed=50, right_speed=50):
        try:
            l = int(left_speed)
            r = int(right_speed)
        except Exception:
            raise TypeError("left_speed/right_speed")

        d = 0
        if l < 0:
            d |= 1
        if r < 0:
            d |= 2

        l = self._clamp(abs(l), 0, 100)
        r = self._clamp(abs(r), 0, 100)

        self.left_speed = -l if l != 0 and int(left_speed) < 0 else l
        self.right_speed = -r if r != 0 and int(right_speed) < 0 else r

        self._i2c_send(CMD_MOTOR, [l, r, d])

    def set_motor_stop(self, motor):
        if motor not in (MotorSelector.LEFT, MotorSelector.RIGHT, MotorSelector.ALL):
            raise ValueError("motor")
        if motor == MotorSelector.LEFT:
            self.set_motors_speed(0, self.right_speed)
            return
        if motor == MotorSelector.RIGHT:
            self.set_motors_speed(self.left_speed, 0)
            return
        self.set_motors_speed(0, 0)

    def track_side(self, side, state):
        if side not in (Side.LEFT, Side.RIGHT):
            raise ValueError("side")
        if state not in (TrackColor.BLACK, TrackColor.WHITE):
            raise ValueError("state")

        v = pin13.read_digital() if side == Side.LEFT else pin14.read_digital()
        if state == TrackColor.WHITE:
            return v == 1
        return v == 0

    def get_tracking(self):
        left = pin13.read_digital()
        right = pin14.read_digital()
        return str(left) + str(right)

    def get_distance(self, unit=DistanceUnit.UNIT_CM, max_cm_distance=500):
        try:
            unit = int(unit)
        except Exception:
            raise TypeError("unit")

        if unit not in (DistanceUnit.UNIT_CM, DistanceUnit.UNIT_INCH):
            raise ValueError("unit")

        try:
            max_cm_distance = float(max_cm_distance)
        except Exception:
            raise TypeError("max_cm_distance")

        if max_cm_distance <= 0:
            raise ValueError("max_cm_distance")

        pin16.write_digital(0)
        utime.sleep_us(2)
        pin16.write_digital(1)
        utime.sleep_us(10)
        pin16.write_digital(0)

        timeout_us = 30000
        t0 = utime.ticks_us()

        while pin15.read_digital() == 0:
            if utime.ticks_diff(utime.ticks_us(), t0) > timeout_us:
                raise OSError("sonar timeout waiting for echo start")

        t_rise = utime.ticks_us()
        t1 = t_rise

        while pin15.read_digital() == 1:
            if utime.ticks_diff(utime.ticks_us(), t1) > timeout_us:
                raise OSError("sonar timeout waiting for echo end")

        t_fall = utime.ticks_us()
        pulse = utime.ticks_diff(t_fall, t_rise)

        if pulse <= 0:
            raise OSError("invalid sonar pulse")

        if unit == DistanceUnit.UNIT_CM:
            distance = pulse // 58
            return min(distance, int(max_cm_distance))

        distance = pulse // 148
        max_inch_distance = int(max_cm_distance / 2.54)
        return min(distance, max_inch_distance)

    def set_headlight(self, red, green, blue):
        try:
            r = self._clamp(int(red), 0, 255)
            g = self._clamp(int(green), 0, 255)
            b = self._clamp(int(blue), 0, 255)
        except Exception:
            raise TypeError("red/green/blue")

        self._i2c_send(CMD_HEADLIGHT, [r, g, b])

    def set_positional_servo(self, servo_type, port, angle):
        if servo_type not in (ServoType.SERVO_180, ServoType.SERVO_270, ServoType.SERVO_360):
            raise ValueError("servo_type")
        self._validate_servo_port(port)
        if not isinstance(angle, (int, float)):
            raise TypeError("angle")

        if servo_type == ServoType.SERVO_180:
            angle_map = self._map_int(angle, 0, 180, 0, 180)
        elif servo_type == ServoType.SERVO_270:
            angle_map = self._map_int(angle, 0, 270, 0, 180)
        else:
            angle_map = self._map_int(angle, 0, 360, 0, 180)

        if angle_map < 0:
            angle_map = 0
        elif angle_map > 180:
            angle_map = 180

        self._i2c_send(CMD_SERVO, [int(port), int(angle_map)])

    def configure_continuous_servo(self, port, stop_angle=90, min_angle=0, max_angle=180):
        self._validate_servo_port(port)

        if not isinstance(stop_angle, (int, float)):
            raise TypeError("stop_angle")
        if not isinstance(min_angle, (int, float)):
            raise TypeError("min_angle")
        if not isinstance(max_angle, (int, float)):
            raise TypeError("max_angle")

        stop_angle = int(round(stop_angle))
        min_angle = int(round(min_angle))
        max_angle = int(round(max_angle))

        if min_angle < 0 or min_angle > 180:
            raise ValueError("min_angle")
        if max_angle < 0 or max_angle > 180:
            raise ValueError("max_angle")
        if stop_angle < 0 or stop_angle > 180:
            raise ValueError("stop_angle")
        if min_angle > stop_angle:
            raise ValueError("min_angle")
        if stop_angle > max_angle:
            raise ValueError("max_angle")

        self._continuous_servo_config[port] = {
            "stop_angle": stop_angle,
            "min_angle": min_angle,
            "max_angle": max_angle,
        }

    def get_continuous_servo_config(self, port):
        self._validate_servo_port(port)
        cfg = self._continuous_servo_config[port]
        return {
            "stop_angle": cfg["stop_angle"],
            "min_angle": cfg["min_angle"],
            "max_angle": cfg["max_angle"],
        }
    
    def sweep_continuous_servo_stop(self, port, start_angle=88, end_angle=92, step=1, settle_ms=2000, stop_ms=1000):
        self._validate_servo_port(port)

        try:
            start_angle = int(start_angle)
        except Exception:
            raise TypeError("start_angle")

        try:
            end_angle = int(end_angle)
        except Exception:
            raise TypeError("end_angle")

        try:
            step = int(step)
        except Exception:
            raise TypeError("step")

        try:
            settle_ms = int(settle_ms)
        except Exception:
            raise TypeError("settle_ms")

        try:
            stop_ms = int(stop_ms)
        except Exception:
            raise TypeError("stop_ms")

        if start_angle < 0 or start_angle > 180:
            raise ValueError("start_angle")
        if end_angle < 0 or end_angle > 180:
            raise ValueError("end_angle")
        if step <= 0:
            raise ValueError("step")
        if settle_ms < 0:
            raise ValueError("settle_ms")
        if stop_ms < 0:
            raise ValueError("stop_ms")

        if start_angle <= end_angle:
            angle = start_angle
            while angle <= end_angle:
                self.set_positional_servo(ServoType.SERVO_180, port, angle)
                sleep(settle_ms)
                angle += step
        else:
            angle = start_angle
            while angle >= end_angle:
                self.set_positional_servo(ServoType.SERVO_180, port, angle)
                sleep(settle_ms)
                angle -= step

        self.set_continuous_servo(port, 0)
        sleep(stop_ms)

    def set_continuous_servo(self, port, speed):
        self._validate_servo_port(port)
        if not isinstance(speed, (int, float)):
            raise TypeError("speed")

        speed = self._clamp(float(speed), -100, 100)
        cfg = self._continuous_servo_config[port]

        if speed == 0:
            angle_equivalent = cfg["stop_angle"]
        elif speed < 0:
            angle_equivalent = self._map_int(speed, -100, 0, cfg["min_angle"], cfg["stop_angle"])
        else:
            angle_equivalent = self._map_int(speed, 0, 100, cfg["stop_angle"], cfg["max_angle"])

        self.set_positional_servo(ServoType.SERVO_180, port, angle_equivalent)


class TPBotEduPIDController:
    def __init__(self, robot):
        self.robot = robot
        self.pid_speed = DEFAULT_PID_SPEED
        self.block_length = 0
        self.block_unit = DistanceUnit.UNIT_CM

    def _pid_finish_delay(self, delay_ms):
        if not isinstance(delay_ms, int):
            try:
                delay_ms = int(delay_ms)
            except Exception:
                raise TypeError("delay_ms")

        if delay_ms < 0:
            raise ValueError("delay_ms")

        if self.pid_speed > 0:
            delay_ms = int((500 * delay_ms) / self.pid_speed)

        end_time = running_time() + delay_ms

        while running_time() <= end_time:
            if self.get_pid_stop_flag() == 1:
                sleep(400)
                return
            sleep(1)

    def get_pid_stop_flag(self):
        self.robot._i2c_send(CMD_PID_STOP_FLAG, [0])
        data = i2c.read(I2C_ADDRESS, 1)
        if len(data) != 1:
            raise OSError("invalid pid stop flag response")
        return data[0]

    def pid_set_speed(self, speed, unit):
        try:
            speed = float(speed)
        except Exception:
            raise TypeError("speed")

        try:
            unit = int(unit)
        except Exception:
            raise TypeError("unit")

        if unit not in (SpeedUnit.CM_PER_SEC, SpeedUnit.IN_PER_SEC):
            raise ValueError("unit")

        v = int(speed * (10 if unit == SpeedUnit.CM_PER_SEC else 25.4))
        self.pid_speed = self.robot._clamp(v, MIN_PID_SPEED, MAX_PID_SPEED)
        self.robot._i2c_send(CMD_PID_SPEED, [self.pid_speed >> 8, self.pid_speed & 255])

    def pid_speed_control(self, left_speed, right_speed, unit):
        try:
            l = float(left_speed)
        except Exception:
            raise TypeError("left_speed")

        try:
            r = float(right_speed)
        except Exception:
            raise TypeError("right_speed")

        try:
            unit = int(unit)
        except Exception:
            raise TypeError("unit")

        if unit not in (SpeedUnit.CM_PER_SEC, SpeedUnit.IN_PER_SEC):
            raise ValueError("unit")

        d = 0
        if l < 0:
            d |= 1
        if r < 0:
            d |= 2

        scale = 10 if unit == SpeedUnit.CM_PER_SEC else 25.4
        lv = int(abs(l * scale))
        rv = int(abs(r * scale))

        if lv:
            lv = self.robot._clamp(lv, MIN_PID_SPEED, MAX_PID_SPEED)
        if rv:
            rv = self.robot._clamp(rv, MIN_PID_SPEED, MAX_PID_SPEED)

        self.robot._i2c_send(CMD_PID_WHEEL_SPEED, [lv >> 8, lv & 255, rv >> 8, rv & 255, d])

    def pid_run_distance(self, direction, distance, unit):
        try:
            direction = int(direction)
        except Exception:
            raise TypeError("direction")

        try:
            distance = float(distance)
        except Exception:
            raise TypeError("distance")

        try:
            unit = int(unit)
        except Exception:
            raise TypeError("unit")

        if direction not in (Direction.FORWARD, Direction.BACKWARD):
            raise ValueError("direction")

        if unit not in (DistanceUnit.UNIT_CM, DistanceUnit.UNIT_INCH):
            raise ValueError("unit")

        v = int(distance * (10 if unit == DistanceUnit.UNIT_CM else 25.4))

        if v == 0:
            return

        if v < 0:
            raise ValueError("distance")

        flag = 0 if direction == Direction.FORWARD else 3
        self.robot._i2c_send(CMD_PID_DISTANCE, [v >> 8, v & 255, flag])
        self._pid_finish_delay(v * 7 + 400)

    def pid_block_set(self, length, distance_unit):
        try:
            length = float(length)
        except Exception:
            raise TypeError("length")

        try:
            distance_unit = int(distance_unit)
        except Exception:
            raise TypeError("distance_unit")

        if distance_unit not in (DistanceUnit.UNIT_CM, DistanceUnit.UNIT_INCH):
            raise ValueError("distance_unit")

        self.block_length = length
        self.block_unit = distance_unit

    def pid_run_block(self, block_count):
        try:
            block_count = float(block_count)
        except Exception:
            raise TypeError("block_count")

        self.pid_run_distance(Direction.FORWARD, self.block_length * block_count, self.block_unit)

    def pid_run_steering(self, turn, angle):
        try:
            turn = int(turn)
        except Exception:
            raise TypeError("turn")

        try:
            angle = int(angle)
        except Exception:
            raise TypeError("angle")

        if turn not in (
            SteeringMode.LEFT,
            SteeringMode.RIGHT,
            SteeringMode.STAY_LEFT,
            SteeringMode.STAY_RIGHT,
        ):
            raise ValueError("turn")

        if angle < 0:
            raise ValueError("angle")

        lh = 0
        ll = 0
        rh = 0
        rl = 0
        mode = 0

        if turn == SteeringMode.LEFT:
            v = angle * 2
            rh = v >> 8
            rl = v & 255
        elif turn == SteeringMode.RIGHT:
            v = angle * 2
            lh = v >> 8
            ll = v & 255
        elif turn == SteeringMode.STAY_LEFT:
            v = angle
            lh = v >> 8
            rh = v >> 8
            ll = v & 255
            rl = v & 255
            mode = 1
        else:
            v = angle
            lh = v >> 8
            rh = v >> 8
            ll = v & 255
            rl = v & 255
            mode = 2

        self.robot._i2c_send(CMD_PID_STEERING, [lh, ll, rh, rl, mode])
        self._pid_finish_delay(angle * 8 + 500)

    def adjust_motor_speed(self):
        self.robot._i2c_send(CMD_ADJUST_MOTOR, [0])

    def reset_motor_adjust(self):
        self.robot._i2c_send(CMD_RESET_MOTOR_ADJUST, [0])
        