# Measure weight with with HX711

UNDER CONSTRUCTION

See the __[HX711 class documentation in robert-hh repository](https://github.com/robert-hh/hx711)__.

## Library credit

This section is based on the wonderful work of robert-hh implementation (see https://github.com/robert-hh/hx711) released under MIT license.

The robert-hh library implement support of hx711 with gpio, rp2040 pio, spi bus. This section and examples only focus on the GPIO implementation.

The full library source, examples and documentation are available available in the lib/ folder, see [robert-hh_hx711_full-source.zip](lib/robert-hh_hx711_full-source.zip) .

# Calibrate the sensor

xxxxx

# Library 
xxx

# Wiring 

## HX711 with Raspberry-Pi Pico

The wiring is quite simple. 

Enlarge the picture to read labels on the HX711 breakout.

Load-cell wires color are: red, black, green, white

![Wiring HX711 to Raspberry-Pico](docs/pico-to-hx711.jpg)

# Testing

## Reading values 

xxx

## About the tare

xxx

## Reading with units

xxx

__Results__

```
get_units: -4.357268 gr  # Tare done. Nothing on the gauge sensor
get_units: -3.604047 gr
get_units: -4.682615 gr
get_units: -4.604581 gr
get_units: -8.71075 gr
get_units: 18.30691 gr
get_units: 58.58892 gr # Placing 984 gr weight
get_units: 80.48586 gr
get_units: 78.27495 gr
get_units: 263.9093 gr
get_units: 475.1167 gr
get_units: 615.8622 gr
get_units: 708.4283 gr
get_units: 777.3264 gr
get_units: 829.2479 gr
get_units: 867.9638 gr
get_units: 896.8296 gr
get_units: 918.7194 gr
get_units: 934.871 gr
get_units: 947.2517 gr
get_units: 956.6745 gr
get_units: 963.5883 gr
get_units: 968.6321 gr
get_units: 971.5428 gr
get_units: 974.6895 gr
get_units: 977.1093 gr
get_units: 978.8817 gr
get_units: 980.0651 gr
get_units: 981.0663 gr
get_units: 981.842 gr
get_units: 982.331 gr
get_units: 982.8474 gr
get_units: 983.2507 gr
get_units: 983.2565 gr
get_units: 983.3103 gr
get_units: 983.4044 gr
get_units: 983.4819 gr
get_units: 983.48 gr
get_units: 983.6163 gr
get_units: 983.6889 gr
get_units: 983.7946 gr
get_units: 983.8339 gr
get_units: 983.917 gr
get_units: 983.9597 gr
get_units: 983.8796 gr
get_units: 983.8314 gr
get_units: 983.98 gr
get_units: 983.9612 gr
get_units: 983.96 gr
get_units: 984.0054 gr
get_units: 983.9194 gr
get_units: 983.8694 gr
get_units: 983.9677 gr
get_units: 983.9352 gr
get_units: 984.0208 gr
get_units: 983.8057 gr
get_units: 983.9856 gr
get_units: 984.0765 gr
get_units: 983.9964 gr
get_units: 984.0296 gr
get_units: 984.1484 gr
get_units: 984.0583 gr
get_units: 983.8487 gr
get_units: 984.019 gr
get_units: 984.0038 gr
```

# Shopping list
* [HX711 - 24 bits ADC for Load Cells / Strain Gauges](https://shop.mchobby.be/product.php?id_product=2710) @ MCHobby
* [5 Kg Load cell, 4 wires](https://shop.mchobby.be/product.php?id_product=2712) @ MCHobby
* [10 Kg Load cell, 4 wires](https://shop.mchobby.be/product.php?id_product=2711) @ MCHobby
