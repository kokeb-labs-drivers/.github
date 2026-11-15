# Figures

<!-- Written by kokeb-docs figures from docs/diagrams/figures/*.py. Do not edit by hand. -->

Every figure on this site is drawn by a Python module from facts extracted from the code, so it is rebuilt,
not redrawn, when the code changes. CI runs `kokeb-docs figures --check` and fails when a
committed figure no longer matches the code. Each figure below lists the files it is drawn from.

## A driver sits between your code and the chip

<!-- figure: driver-layers -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="driver-layers.dark.svg">
  <img src="driver-layers.svg"
    alt="Pipeline in which your application calls a chip driver, the driver talks to a port that moves bytes
    on your SPI, I2C, UART or ADC bus, and the port drives the chip.">
</picture>
<!-- /figure -->

Hardware description: [`docs/model/driver-layers.pipeline.yml`](../model/driver-layers.pipeline.yml)

Drawn from:

- [`docs/model/driver-layers.pipeline.yml`](../model/driver-layers.pipeline.yml)

## How a driver is built

<!-- figure: driver-pipeline -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="driver-pipeline.dark.svg">
  <img src="driver-pipeline.svg"
    alt="Pipeline from a driver request through triage, design, build, independent review, a private CI
    rehearsal, a clean public copy, a release candidate and hardware validation to a release.">
</picture>
<!-- /figure -->

Hardware description: [`docs/model/driver-pipeline.pipeline.yml`](../model/driver-pipeline.pipeline.yml)

Drawn from:

- [`docs/model/driver-pipeline.pipeline.yml`](../model/driver-pipeline.pipeline.yml)

## What each hardware level means

<!-- figure: hardware-levels -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="hardware-levels.dark.svg">
  <img src="hardware-levels.svg"
    alt="Matrix of the three hardware validation levels H0, H1 and H2 against the evidence each one needs -
    host tests against a model, a bench rig run with kept logs, and a hardware engineer sign-off.">
</picture>
<!-- /figure -->

Hardware description: [`docs/model/hardware-levels.matrix.yml`](../model/hardware-levels.matrix.yml)

Drawn from:

- [`docs/model/hardware-levels.matrix.yml`](../model/hardware-levels.matrix.yml)
