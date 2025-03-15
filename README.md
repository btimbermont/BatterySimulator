# Home Battery Simulator

This is a simple home battery simulator I wrote for myself.
Given [.mbc files](https://forum.beeclear.nl/showthread.php?tid=91)
containing your current household, it will simulate how much power your household would consume and produce during the
same period if it had had a home battery.

Home batteries can be configured with a capacity, maximum charge and discharge rate, and a
[round trip efficiency](https://bolk.energy/kennisbank/round-trip-efficiency/).
Because I am considering a [HomeWizard plugin battery](https://www.homewizard.com/nl/plug-in-battery/), this battery
has been added in the code, but you can add your own if you have the specs of the battery you want to simulate.

To add your own battery, add your battery specs into the code at the start of in `main.py`, in `BATTERIES_TO_SIMULATE`.
For example, to add a battery with a capacity of 5kWh, maximum charge rate of 1000 Watt, maximum discharge rate of 750
Watt, and an efficiency of 75%, add the following line as the end of `BATTERIES_TO_SIMULATE`:

```python
    'my battery', Battery(5, 1000, 750, 0.75)
```

# Running the simulation

Put all .mbc files you want to take into account into an `input` directory next to main.py. Then run main.py:

```bash
python3 main.py
```

As a result, the program will print how much power consumption and production would have without the batteries, and with
the batteries listed in the current simulation:
```
Simulation done!
without battery: consumed 4209.90 kWh, produced 2274.07kWh
With batteries:
Saldering: consumed 1935.83 kWh, produced 0.00kWh
HomeWizard x 1: consumed 3546.21 kWh, produced 1444.46kWh
HomeWizard x 2: consumed 3261.87 kWh, produced 1089.03kWh
HomeWizard x 2 (eigen groep): consumed 3217.32 kWh, produced 1033.34kWh
HomeWizard x 3: consumed 3195.20 kWh, produced 1005.70kWh
HomeWizard x 3 (eigen groep): consumed 3098.61 kWh, produced 884.96kWh
```
(These are the current batteries in `main.py`. You can change that if you want)

A simulation with 1 battery over an entire year of mbc data takes about 4 seconds on my machine. The same simulation
with 6 batteries takes about 9 seconds. So even if you have a slower machine it shouldn't take too long.

# How many .mbc files do I need?

I have noticed that year-over-year consumption and solar production is quite constant, so data from an entire year
should be sufficient to make a decent simulation.

# I don't have .mbc files, what do I do?

I know, .mbc isn't an industry standard or anything, it just happens to be the file format of the smart meter I have at
home, and this one was made by a small Dutch company that has since stopped selling their product.

If you want to use another format (you probably have CSVs?) you're free to open a PR, or create an issue and if I find
the time and if you provide example files I'll look into adding support.