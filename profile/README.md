<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/kokeb-labs/.github/main/brand/mark/mark-dark.svg">
  <img src="https://raw.githubusercontent.com/kokeb-labs/.github/main/brand/mark/mark.svg" alt="" width="96" height="96">
</picture>

# Kokeb Labs Drivers

C++20 drivers for the chips on embedded boards: ADCs, encoders, EEPROMs, GPIO expanders, PWM controllers, solenoid
drivers and sensors. Each one is a small, header-only library that runs on any MCU. You give it a few functions
that move bytes on your SPI or I2C bus, and it handles the chip.

The drivers are part of [Kokeb Labs](https://github.com/kokeb-labs). They are built from the same template, checked
by the same CI and held to the same engineering standard.

## The standard every driver meets

| | |
| --- | --- |
| **C++20, no surprises** | Header-only; no heap, exceptions, RTTI or virtual calls. Every call returns a result you must check |
| **Hardware-agnostic** | No MCU headers. The bus is a port class you write once; examples for ESP32 (ESP-IDF) and the host |
| **MISRA C++:2023 checked** | Every pull request runs the MISRA checks; each deviation is recorded with its reason |
| **Independent safety review** | Reviewed apart from the author's own checks: datasheet conformance, fault handling, safe outputs |
| **Tested and fuzzed** | Host tests against a protocol model of the chip; a fuzzer corrupts the chip's replies |
| **Documented** | Datasheet-backed docs with chip pinout, block and wiring diagrams, an API reference and stated limits |
| **MIT licensed** | Use it in open or closed products. Names, namespaces and macros follow the chip, never a brand |

## Drivers

| Repository | Chip | Bus |
| --- | --- | --- |
| [`driver-ads7952`](https://github.com/kokeb-labs-drivers/driver-ads7952) | TI ADS7950/51/52/53 12-bit 4/8/12/16-channel ADCs | SPI |
| [`driver-as5047u`](https://github.com/kokeb-labs-drivers/driver-as5047u) | ams OSRAM AS5047U 14-bit magnetic rotary position sensor | SPI |
| [`driver-at25040b`](https://github.com/kokeb-labs-drivers/driver-at25040b) | Microchip AT25010B/020B/040B serial EEPROMs | SPI |
| [`driver-bmp581`](https://github.com/kokeb-labs-drivers/driver-bmp581) | Bosch BMP581 barometric pressure and temperature sensor | I2C, SPI |
| [`driver-max22200`](https://github.com/kokeb-labs-drivers/driver-max22200) | Analog Devices MAX22200 octal solenoid and motor driver | SPI |
| [`driver-pca9685`](https://github.com/kokeb-labs-drivers/driver-pca9685) | NXP PCA9685 16-channel 12-bit PWM controller | I2C |
| [`driver-pcal9555`](https://github.com/kokeb-labs-drivers/driver-pcal9555) | NXP PCA9555 and PCAL9555A 16-bit GPIO expanders | I2C |
| [`driver-tle92466ed`](https://github.com/kokeb-labs-drivers/driver-tle92466ed) | Infineon TLE92466ED six-channel low-side solenoid driver | SPI |

Need a chip that isn't here? Open a **Driver request** in any repository, or start one yourself from the template.

## Where things live

| | |
| --- | --- |
| [`driver-template`](https://github.com/kokeb-labs/driver-template) | Start a new driver: one command gives code, host tests, an ESP32 example, docs and CI |
| [`ci-tools`](https://github.com/kokeb-labs/ci-tools) | The reusable workflows every driver's CI calls |
| [Handbook](https://kokeb-labs.github.io/handbook/) | Every rule for C++, CMake, docs, CI and reviews, with the check that verifies it |
| [Kokeb Labs portal](https://kokeb-labs.github.io/) | Projects, how we build, roadmap and contributing |

Questions and ideas go to [Discussions](https://github.com/kokeb-labs-drivers/.github/discussions). Report
vulnerabilities privately as the [security policy](https://github.com/kokeb-labs-drivers/.github/blob/main/SECURITY.md)
describes, never in a public issue.
