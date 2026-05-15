# Summary of major changes to [`TPBot.py`](https://github.com/lionyhw/EF_Produce_MicroPython/blob/master/TPBot.py)

The module in this repository includes a number of changes to [`tpbot.py`](https://github.com/lionyhw/EF_Produce_MicroPython/blob/master/TPBot.py).

## 1. Added a new class

A new class was added:

- `TPBotEduPIDController`

This class was added to create a PID (Proportional-Integral-Derivative) controller.  This controller was not available in [`TPBot.py`](https://github.com/lionyhw/EF_Produce_MicroPython/blob/master/TPBot.py).

## 2. Public methods added

The following public methods were added:

- `set_motor_stop(...)`
- `track_side(...)`
- `track_line(...)`
- `set_positional_servo(...)`
- `set_continuous_servo(...)`

The following changes were made in order to resolve a problem with continuous servos not stopping when the stop angle of set_continuous_servo(...) is set to 0:

- added per-port continuous-servo configuration storage in `TPBotEdu.__init__`
- added a private helper `_validate_servo_port()` to avoid repeating the same port validation logic
- added a new public method `configure_continuous_servo(port, stop_angle=90, min_angle=0, max_angle=180)`, which allows the user to tune the stop point for continuous servos.
- added a new public method `get_continuous_servo_config(port)`
- revised `set_continuous_servo()` so it no longer assumes stop is always exactly angle `90`
  preserved backward compatibility:
  - if you do nothing, behavior remains effectively the same as before
  - users can now tune stop position per servo port
- added `sweep_continuous_servo_stop(port, start_angle=88, end_angle=92, step=1, settle_ms=2000, stop_ms=1000)`
  What it does:
    - steps through a small range of candidate neutral angles
    - commands each angle directly through the same servo path used by continuous servos
    - waits at each angle so you can observe whether the servo creeps
    - finishes by commanding the configured `stop_angle` for that port


## 3. Public method implementation changes

The following public methods have the same name and function as methods used in [`TPBot.py`](https://github.com/lionyhw/EF_Produce_MicroPython/blob/master/TPBot.py), but the code for constraining input values is different:

- `set_motors_speed()`
- `get_distance()`
- `get_tracking()`

Similarly, `set_headlight(...)` in this repository and `set_car_light(...)` in [`TPBot.py`](https://github.com/lionyhw/EF_Produce_MicroPython/blob/master/TPBot.py) both operate the robot's headlight, but the code for constraining input values is different.

## 4. Module Level and Class Level Constants

Related constants have been grouped into classes.  These classes are being used as **namespaces**, not as “real objects” with behavior.  The constants represent public options passed into methods.  This method of organization was chosen in order make the API more readable.

The module-level constants are used for things that are more like **internal protocol details**.

# Summary of major changes to ELECFREAKS [V2.ts](https://github.com/elecfreaks/pxt-TPBot/blob/master/V2.ts)

The module in this repository is a MicroPython implementation of TPBot Edu functionality.

ELECFREAKS [V2.ts](https://github.com/elecfreaks/pxt-TPBot/blob/master/V2.ts) is a TypeScript implementation of TPBot Edu functionality, designed for block-coding with [Microsoft MakeCode](https://makecode.microbit.org/). 